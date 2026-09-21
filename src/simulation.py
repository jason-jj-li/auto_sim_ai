"""Simulation engine for running surveys and interventions."""
from typing import List, Dict, Any, Optional, Callable, TYPE_CHECKING
from datetime import datetime
import json
import time
from .persona import Persona
from .llm_client import LMStudioClient

if TYPE_CHECKING:
    from .survey_config import SurveyConfig
    from .cache import ResponseCache


class SimulationResult:
    """Container for simulation results."""
    
    def __init__(self, simulation_type: str, timestamp: str):
        """
        Initialize simulation result.
        
        Args:
            simulation_type: 'survey' or 'intervention'
            timestamp: ISO format timestamp
        """
        self.simulation_type = simulation_type
        self.timestamp = timestamp
        self.persona_responses: List[Dict[str, Any]] = []
        self.questions: List[str] = []
        self.intervention_text: Optional[str] = None
        self.survey_config: Optional[Dict[str, Any]] = None
        self.instrument_name: Optional[str] = None
        self.metadata: Dict[str, Any] = {}
        
    def add_response(
        self,
        persona: Persona,
        question: str,
        response: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        validation_status: str = "not_requested",
        validation_error: Optional[str] = None,
    ):
        """Add a response from a persona."""
        self.persona_responses.append({
            **self.persona_fields(persona),
            'question': question,
            'response': response,
            'conversation_history': conversation_history or [],
            'validation_status': validation_status,
            'validation_error': validation_error,
        })

    @staticmethod
    def persona_fields(persona: Persona) -> Dict[str, Any]:
        """Return every population variable as collision-safe result columns.

        The five historical core columns retain their existing names. All
        remaining standard and custom attributes use ``persona_<field>`` so a
        population variable can never overwrite response/study metadata.
        Values stay native in JSON; the CSV storage layer serializes nested
        lists and dictionaries losslessly as JSON text.
        """
        data = persona.to_dict()
        core_names = {
            'persona_id': 'persona_id',
            'name': 'persona_name',
            'age': 'persona_age',
            'gender': 'persona_gender',
            'occupation': 'persona_occupation',
        }
        fields: Dict[str, Any] = {}
        for key, value in data.items():
            column = core_names.get(key, f'persona_{key}')
            fields[column] = value
        return fields
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = {
            'simulation_type': self.simulation_type,
            'timestamp': self.timestamp,
            'intervention_text': self.intervention_text,
            'questions': self.questions,
            'responses': self.persona_responses,
            'survey_config': self.survey_config,
            'instrument_name': self.instrument_name,
            'metadata': self.metadata
        }
        if self.simulation_type == 'ab_testing':
            data['ab_test_assignments'] = self.metadata.get('assignments', {})
            data['ab_test_conditions'] = self.metadata.get('conditions', [])
        return data


class SimulationEngine:
    """Engine for running simulations with personas."""
    
    def __init__(
        self,
        llm_client: LMStudioClient,
        cache: Optional['ResponseCache'] = None
    ):
        """
        Initialize simulation engine.

        Args:
            llm_client: LM Studio client instance
            cache: Optional ResponseCache for caching LLM responses
        """
        self.llm_client = llm_client
        self.cache = cache
        self.response_times: List[float] = []  # Track for estimation
    
    def run_survey(
        self,
        personas: List[Persona],
        questions: List[str],
        temperature: float = 0.7,
        max_tokens: int = 500,
        progress_callback: Optional[Callable[[str], None]] = None,
        survey_context: Optional[str] = None,
        response_validation: Optional[Dict[str, Any]] = None,
        survey_config: Optional['SurveyConfig'] = None,
        per_question_validation: Optional[Dict[int, Dict[str, Any]]] = None,
        stop_callback: Optional[Callable[[], bool]] = None,
        model: Optional[str] = None,
        seed: Optional[int] = None
    ) -> SimulationResult:
        """
        Run a survey simulation.

        Args:
            personas: List of personas to survey
            questions: List of questions to ask
            temperature: LLM temperature parameter
            max_tokens: Maximum tokens per response
            progress_callback: Optional callback for progress updates
            survey_context: Optional context/instructions for the survey
            response_validation: Optional validation rules for response format (applies to all questions)
            survey_config: Optional SurveyConfig object with full survey metadata
            per_question_validation: Optional dict mapping question index to validation rules
            stop_callback: Optional callback that returns True if simulation should stop
            model: Model name (resolved via client if None)
            seed: Fixed LLM seed for reproducible runs (provider-dependent)

        Returns:
            SimulationResult object
        """
        timestamp = datetime.now().isoformat()
        result = SimulationResult('survey', timestamp)
        result.questions = questions
        model = self.llm_client.resolve_model(model)
        result.metadata['model'] = model
        result.metadata['seed'] = seed
        result.metadata['execution'] = 'sequential'
        
        # Store survey configuration metadata if provided
        if survey_config:
            result.survey_config = survey_config.to_dict()
            result.instrument_name = survey_config.template_name
        
        total_queries = len(personas) * len(questions)
        current_query = 0
        
        for persona in personas:
            for question_idx, question in enumerate(questions):
                # Check if we should stop
                if stop_callback and stop_callback():
                    if progress_callback:
                        progress_callback("Simulation stopped by user")
                    result.metadata['stopped_early'] = True
                    result.metadata['completed_queries'] = current_query
                    result.metadata['total_queries'] = total_queries
                    return result
                
                current_query += 1
                if progress_callback:
                    progress_callback(
                        f"Querying {persona.name} ({current_query}/{total_queries}): {question[:50]}..."
                    )
                
                # Build messages for this query
                system_prompt = persona.to_prompt_context()
                
                # Add survey context if provided
                if survey_context:
                    system_prompt += f"\n\n{survey_context}"
                
                # Determine validation for this specific question
                current_validation = None
                if per_question_validation and question_idx in per_question_validation:
                    # Use per-question validation if available
                    current_validation = per_question_validation[question_idx]
                elif response_validation:
                    # Fall back to global validation
                    current_validation = response_validation
                
                # Add response format enforcement if provided
                if current_validation and 'instruction' in current_validation:
                    system_prompt += f"\n\nIMPORTANT RESPONSE FORMAT:\n{current_validation['instruction']}"
                
                # Format the question with response guidance
                question_with_guidance = question
                
                # Add appropriate guidance based on whether there's strict format validation
                if current_validation and 'instruction' in current_validation:
                    # For scale/structured questions: just answer the format
                    question_with_guidance += "\n\n[Provide your answer in the specified format based on your personal perspective.]"
                else:
                    # For open-ended questions: encourage detailed response
                    question_with_guidance += "\n\n[Please provide a thoughtful, detailed response (2-4 sentences) based on your personal background and values. Answer naturally as yourself, not as an AI.]"
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question_with_guidance}
                ]
                
                # Check cache first if available
                cached_response = None
                if self.cache:
                    persona_json = json.dumps(
                        persona.to_dict(), ensure_ascii=False, sort_keys=True
                    )
                    request_fingerprint = json.dumps({
                        'max_tokens': max_tokens,
                        'validation': current_validation,
                    }, sort_keys=True)
                    cached_response = self.cache.get(
                        persona_json, question, temperature, survey_context,
                        model=model, seed=seed,
                        request_fingerprint=request_fingerprint,
                    )

                if cached_response:
                    response = cached_response
                else:
                    # Structured output channel for JSON-validated questions
                    response_format = (
                        {"type": "json_object"}
                        if current_validation and current_validation.get('type') == 'json'
                        else None
                    )
                    # Get response from LLM
                    start_time = time.time()
                    response = self.llm_client.chat_completion(
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        model=model,
                        seed=seed,
                        response_format=response_format
                    )
                    elapsed = time.time() - start_time
                    self.response_times.append(elapsed)

                    # Store in cache if available
                    if response and self.cache:
                        self.cache.put(
                            persona_json, question, temperature, response, survey_context,
                            model=model, seed=seed,
                            request_fingerprint=request_fingerprint,
                        )

                # Validate and clean response if validation rules provided
                # (per-question rules from the AI parser must drive cleaning too, not just prompting)
                validation_status = "not_requested"
                validation_error = None
                if response and current_validation:
                    response, is_valid, validation_error = self._validate_response(
                        response, current_validation
                    )
                    validation_status = "valid" if is_valid else "invalid"

                if response:
                    result.add_response(
                        persona, question, response, messages,
                        validation_status=validation_status,
                        validation_error=validation_error,
                    )
                else:
                    reason = getattr(self.llm_client, 'last_error', None) or 'no response'
                    result.add_response(persona, question, f"[Error: {reason}]", messages)

        return result
    
    @staticmethod
    def _validate_and_clean_response(response: str, validation: Dict[str, Any]) -> str:
        """
        Validate and clean the LLM response based on validation rules.
        
        Args:
            response: The raw LLM response
            validation: Validation rules dictionary
            
        Returns:
            Cleaned and validated response, or original if validation fails
        """
        cleaned, _, _ = SimulationEngine._validate_response(response, validation)
        return cleaned

    @staticmethod
    def _validate_response(
        response: str, validation: Dict[str, Any]
    ) -> tuple[str, bool, Optional[str]]:
        """Validate without inventing data; invalid values remain visible."""
        import re
        import json as json_module

        response = response.strip()
        validation_type = validation.get('type')
        
        if validation_type == 'number':
            # Extract single number
            match = re.search(r'-?\d+\.?\d*', response)
            if match:
                num = float(match.group()) if '.' in match.group() else int(match.group())
                # Check if within range
                min_val = validation.get('min', float('-inf'))
                max_val = validation.get('max', float('inf'))
                if min_val <= num <= max_val:
                    cleaned = str(int(num)) if float(num).is_integer() else str(num)
                    return cleaned, True, None
                return response, False, f"number {num} outside [{min_val}, {max_val}]"
            return response, False, "no numeric answer found"
        
        elif validation_type == 'word':
            # Extract single word
            words = response.split()
            if words:
                first_word = words[0].strip('.,!?;:"\'')
                allowed = validation.get('allowed')
                if allowed:
                    # Check if it's in the allowed list (case-insensitive)
                    for allowed_word in allowed:
                        if first_word.lower() == allowed_word.lower():
                            return allowed_word, True, None
                    return response, False, f"answer not in allowed values: {allowed}"
                return first_word, True, None
            return response, False, "empty answer"
        
        elif validation_type == 'json':
            # Extract and validate JSON
            try:
                # Try to find JSON in response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    parsed = json_module.loads(json_str)
                    return json_module.dumps(parsed, ensure_ascii=False), True, None
            except (ValueError, TypeError, json_module.JSONDecodeError):
                pass
            return response, False, "invalid JSON object"
        
        elif validation_type == 'regex':
            # Validate against regex pattern
            pattern = validation.get('pattern', '')
            if pattern:
                match = re.search(pattern, response)
                if match:
                    return match.group(0), True, None
            return response, False, "response does not match required pattern"
        
        # Instruction-only validation cannot be mechanically verified.
        return response, True, None
    
    def run_intervention(
        self,
        personas: List[Persona],
        intervention_text: str,
        followup_questions: List[str],
        temperature: float = 0.7,
        max_tokens: int = 500,
        progress_callback: Optional[Callable[[str], None]] = None,
        stop_callback: Optional[Callable[[], bool]] = None,
        seed: Optional[int] = None,
        model: Optional[str] = None,
        survey_context: Optional[str] = None,
        per_question_validation: Optional[Dict[int, Dict[str, Any]]] = None,
    ) -> SimulationResult:
        """
        Run an intervention simulation.
        
        Args:
            personas: List of personas to test intervention on
            intervention_text: The intervention message/treatment
            followup_questions: Questions to ask after presenting intervention
            temperature: LLM temperature parameter
            max_tokens: Maximum tokens per response
            progress_callback: Optional callback for progress updates
            stop_callback: Optional callback that returns True if simulation should stop
            
        Returns:
            SimulationResult object
        """
        timestamp = datetime.now().isoformat()
        result = SimulationResult('intervention', timestamp)
        result.intervention_text = intervention_text
        result.questions = followup_questions
        model = self.llm_client.resolve_model(model)
        result.metadata.update({'model': model, 'seed': seed, 'execution': 'sequential'})

        total_queries = len(personas) * len(followup_questions)
        current_query = 0

        for persona in personas:
            for q_idx, question in enumerate(followup_questions):
                # Check if we should stop
                if stop_callback and stop_callback():
                    if progress_callback:
                        progress_callback("Simulation stopped by user")
                    result.metadata.update({
                        'stopped_early': True,
                        'completed_queries': current_query,
                        'total_queries': total_queries,
                    })
                    return result

                current_query += 1
                if progress_callback:
                    progress_callback(
                        f"Asking {persona.name} ({current_query}/{total_queries}): {question[:50]}..."
                    )

                current_validation = (
                    per_question_validation.get(q_idx)
                    if per_question_validation else None
                )
                system_prompt = persona.to_prompt_context()
                if survey_context:
                    system_prompt += f"\n\n{survey_context}"
                if current_validation and current_validation.get('instruction'):
                    system_prompt += (
                        "\n\nIMPORTANT RESPONSE FORMAT:\n"
                        + current_validation['instruction']
                    )
                prompt = self._build_intervention_prompt(intervention_text, question)
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ]
                cache_context = json.dumps({
                    'intervention': intervention_text,
                    'survey_context': survey_context,
                }, ensure_ascii=False, sort_keys=True)
                request_fingerprint = json.dumps({
                    'max_tokens': max_tokens,
                    'validation': current_validation,
                    'mode': 'message_testing',
                }, sort_keys=True)
                persona_json = json.dumps(
                    persona.to_dict(), ensure_ascii=False, sort_keys=True
                )
                response = self.cache.get(
                    persona_json, question, temperature, cache_context,
                    model=model, seed=seed,
                    request_fingerprint=request_fingerprint,
                ) if self.cache else None
                if response is None:
                    start_time = time.time()
                    response = self.llm_client.chat_completion(
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        model=model,
                        seed=seed,
                        response_format=(
                            {"type": "json_object"}
                            if current_validation and current_validation.get('type') == 'json'
                            else None
                        ),
                    )
                    self.response_times.append(time.time() - start_time)
                    if response and self.cache:
                        self.cache.put(
                            persona_json, question, temperature, response, cache_context,
                            model=model, seed=seed,
                            request_fingerprint=request_fingerprint,
                        )

                if response:
                    validation_status = "not_requested"
                    validation_error = None
                    if current_validation:
                        response, is_valid, validation_error = self._validate_response(
                            response, current_validation
                        )
                        validation_status = "valid" if is_valid else "invalid"
                    result.add_response(
                        persona, question, response, messages,
                        validation_status=validation_status,
                        validation_error=validation_error,
                    )
                else:
                    reason = getattr(self.llm_client, 'last_error', None) or 'no response'
                    result.add_response(persona, question, f"[Error: {reason}]", messages)

        return result

    @staticmethod
    def _build_intervention_prompt(intervention_text: str, question: str) -> str:
        """Canonical message-testing prompt shared by sequential and parallel paths."""
        return (
            "Please read the following message carefully:\n\n"
            f"---\n{intervention_text}\n---\n\n"
            "After reading this message, answer the following question:\n\n"
            f"{question}\n\n"
            "Provide your authentic response based on your background and perspective."
        )
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics.
        
        Returns:
            Dictionary with cache stats and timing info
        """
        stats = {
            'response_times': {
                'count': len(self.response_times),
                'mean': sum(self.response_times) / len(self.response_times) if self.response_times else 0,
                'min': min(self.response_times) if self.response_times else 0,
                'max': max(self.response_times) if self.response_times else 0
            }
        }
        
        if self.cache:
            stats['cache'] = self.cache.get_stats()
        
        return stats


class ParallelSimulationEngine:
    """Async version of SimulationEngine for parallel execution (cloud APIs only)."""
    
    def __init__(self, llm_client: LMStudioClient, max_workers: int = 5):
        """Initialize parallel simulation engine.
        
        Args:
            llm_client: LLM client (must support cloud API)
            max_workers: Maximum number of parallel workers
        """
        self.llm_client = llm_client
        self.max_workers = max_workers
        self.should_stop = False  # Stop flag
        from .llm_client import AsyncLLMClient
        self.async_client = AsyncLLMClient(
            base_url=llm_client.base_url,
            api_key=llm_client.api_key
        )
    
    def _validate_and_clean_response_async(self, response: str, validation: Dict[str, Any]) -> str:
        """Delegates to the shared cleaner so parallel and sequential paths produce identical data."""
        return SimulationEngine._validate_and_clean_response(response, validation)
        
    async def run_survey_parallel(
        self,
        personas: List[Persona],
        questions: List[str],
        temperature: float = 0.7,
        max_tokens: int = 500,
        progress_callback: Optional[Callable[[str], None]] = None,
        survey_context: Optional[str] = None,
        model: Optional[str] = None,
        response_validation: Optional[Dict[str, Any]] = None,
        per_question_validation: Optional[Dict[int, Dict[str, Any]]] = None,
        seed: Optional[int] = None
    ) -> SimulationResult:
        """Run survey simulation with parallel requests.
        
        Args:
            personas: List of personas to survey
            questions: List of questions to ask
            temperature: LLM temperature
            max_tokens: Maximum tokens per response
            progress_callback: Progress callback
            survey_context: Optional survey context
            model: Model name
            response_validation: Optional validation rules for response format (applies to all)
            per_question_validation: Optional dict mapping question index to validation rules
            
        Returns:
            SimulationResult
        """
        import asyncio
        from asyncio import Semaphore
        
        timestamp = datetime.now().isoformat()
        result = SimulationResult('survey', timestamp)
        result.questions = questions
        model = self.llm_client.resolve_model(model)
        result.metadata.update({'model': model, 'seed': seed, 'execution': 'parallel'})
        
        total_queries = len(personas) * len(questions)
        completed = {'count': 0}
        
        # Semaphore to limit concurrent requests
        semaphore = Semaphore(self.max_workers)
        
        async def process_single_query(persona: Persona, question: str, q_idx: int):
            """Process a single persona-question pair."""
            async with semaphore:
                # Check if we should stop
                if self.should_stop:
                    if progress_callback:
                        progress_callback("Simulation stopped by user")
                    raise asyncio.CancelledError("Simulation stopped by user")
                
                # Build prompt
                system_prompt = persona.to_prompt_context()
                if survey_context:
                    system_prompt += f"\n\n{survey_context}"
                
                # Determine validation for this specific question
                current_validation = None
                if per_question_validation and q_idx in per_question_validation:
                    # Use per-question validation if available
                    current_validation = per_question_validation[q_idx]
                elif response_validation:
                    # Fall back to global validation
                    current_validation = response_validation
                
                # Add response format enforcement if provided
                if current_validation and 'instruction' in current_validation:
                    system_prompt += f"\n\nCRITICAL RESPONSE FORMAT:\n{current_validation['instruction']}"
                    system_prompt += f"\n\nYou MUST follow this format exactly. Any deviation will cause the response to be rejected."
                
                full_prompt = f"{question}\n\nPlease provide a thoughtful and authentic response based on your background and perspective."
                
                # For structured responses, emphasize format in the question
                if current_validation and current_validation.get('type') == 'number':
                    full_prompt = f"{question}\n\n[Respond with ONLY a number between {current_validation.get('min', 0)} and {current_validation.get('max', 5)}. No text, no explanation, just the number.]"
                elif current_validation and current_validation.get('type') == 'word':
                    allowed = current_validation.get('allowed', [])
                    full_prompt = f"{question}\n\n[Respond with ONLY one word from this list: {', '.join(allowed)}. Nothing else.]"
                elif current_validation and current_validation.get('type') == 'json':
                    full_prompt = f"{question}\n\n[Respond with ONLY a valid JSON object. No markdown, no explanations, just pure JSON.]"
                
                # Structured output channel for JSON-validated questions
                response_format = (
                    {"type": "json_object"}
                    if current_validation and current_validation.get('type') == 'json'
                    else None
                )
                # Make async request — (text, None) or (None, reason)
                response, req_error = await self.async_client.generate_response_async(
                    prompt=full_prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=model,
                    seed=seed,
                    response_format=response_format
                )
                
                # Check again after request
                if self.should_stop:
                    raise asyncio.CancelledError("Simulation stopped by user")
                
                # Validate and clean response if validation rules provided
                # (per-question rules from the AI parser must drive cleaning too, not just prompting)
                validation_status = "not_requested"
                validation_error = None
                if response and current_validation:
                    response, is_valid, validation_error = SimulationEngine._validate_response(
                        response, current_validation
                    )
                    validation_status = "valid" if is_valid else "invalid"
                
                # Update progress
                completed['count'] += 1
                if progress_callback:
                    progress = (completed['count'] / total_queries) * 100
                    progress_callback(f"Progress: {completed['count']}/{total_queries} ({progress:.1f}%)")
                
                return {
                    'persona': persona,
                    'question': question,
                    'question_idx': q_idx,
                    'response': response or f"[Error: {req_error or 'no response'}]",
                    'validation_status': validation_status,
                    'validation_error': validation_error,
                }
        
        # Create all tasks
        tasks = [
            process_single_query(persona, question, q_idx)
            for persona in personas
            for q_idx, question in enumerate(questions)
        ]
        
        if progress_callback:
            progress_callback(f"Starting {total_queries} parallel requests with {self.max_workers} workers...")
        
        # Debug: Print task count
        print(f"\n{'='*80}")
        print(f"[PARALLEL] Starting parallel execution")
        print(f"[PARALLEL] Created {len(tasks)} tasks for parallel execution")
        print(f"[PARALLEL] Max concurrent workers: {self.max_workers}")
        print(f"[PARALLEL] Using model: {model}")
        print(f"[PARALLEL] API URL: {self.async_client.base_url}")
        print(f"[PARALLEL] Tasks will execute concurrently (not sequentially)")
        print(f"{'='*80}\n")
        
        import time
        start_time = time.time()
        
        # Execute all tasks in parallel
        results_list = await asyncio.gather(*tasks, return_exceptions=True)
        
        elapsed_time = time.time() - start_time
        
        # Debug: Print results summary
        print(f"\n{'='*80}")
        print(f"[PARALLEL] Parallel execution completed")
        print(f"[PARALLEL] Total time: {elapsed_time:.2f} seconds")
        print(f"[PARALLEL] Received {len(results_list)} results")
        average_time = elapsed_time / len(results_list) if results_list else 0.0
        print(f"[PARALLEL] Average time per request: {average_time:.2f}s")
        if self.max_workers > 1:
            theoretical_sequential_time = elapsed_time * self.max_workers
            print(f"[PARALLEL] Estimated speedup: ~{theoretical_sequential_time/elapsed_time:.1f}x")
        error_count = sum(1 for item in results_list if isinstance(item, Exception))
        print(f"[PARALLEL] Errors: {error_count}")
        print(f"{'='*80}\n")
        
        # Process results (gather preserves task order: persona-major, then question index)
        for idx, item in enumerate(results_list):
            if isinstance(item, Exception):
                error_msg = f"Task {idx} failed: {type(item).__name__}: {str(item)}"
                print(f"[DEBUG] {error_msg}")
                if progress_callback:
                    progress_callback(f"Error in task {idx}: {str(item)}")
                if isinstance(item, asyncio.CancelledError):
                    continue  # user-initiated stop leaves no fake error rows
                # Keep a visible row instead of a silently missing persona-question pair
                result.add_response(
                    persona=personas[idx // len(questions)],
                    question=questions[idx % len(questions)],
                    response=f"[Error: {type(item).__name__}: {str(item)[:120]}]"
                )
                continue
            
            if item is None:
                print(f"[DEBUG] Task {idx} returned None")
                continue
            
            # Check if item is a dict with expected keys
            if not isinstance(item, dict):
                print(f"[DEBUG] Task {idx} returned unexpected type: {type(item)}")
                continue
            
            if 'persona' not in item or 'question' not in item or 'response' not in item:
                print(f"[DEBUG] Task {idx} missing required keys. Keys: {item.keys() if isinstance(item, dict) else 'N/A'}")
                continue
            
            result.add_response(
                persona=item['persona'],
                question=item['question'],
                response=item['response'],
                validation_status=item.get('validation_status', 'not_requested'),
                validation_error=item.get('validation_error'),
            )
        
        if progress_callback:
            failed = sum(1 for r in result.persona_responses if str(r.get('response', '')).startswith('[Error:'))
            progress_callback(f"Survey complete! {len(result.persona_responses) - failed}/{total_queries} succeeded, {failed} failed.")
        
        return result
    
    async def run_intervention_parallel(
        self,
        personas: List[Persona],
        intervention_text: str,
        questions: List[str],
        temperature: float = 0.7,
        max_tokens: int = 500,
        progress_callback: Optional[Callable[[str], None]] = None,
        model: Optional[str] = None,
        seed: Optional[int] = None,
        survey_context: Optional[str] = None,
        per_question_validation: Optional[Dict[int, Dict[str, Any]]] = None,
    ) -> SimulationResult:
        """Run intervention simulation with parallel requests.
        
        Args:
            personas: List of personas
            intervention_text: Intervention message to show
            questions: Follow-up questions
            temperature: LLM temperature
            max_tokens: Maximum tokens
            progress_callback: Progress callback
            model: Model name
            
        Returns:
            SimulationResult
        """
        import asyncio
        from asyncio import Semaphore
        
        timestamp = datetime.now().isoformat()
        result = SimulationResult('intervention', timestamp)
        result.intervention_text = intervention_text
        result.questions = questions
        model = self.llm_client.resolve_model(model)
        result.metadata.update({'model': model, 'seed': seed, 'execution': 'parallel'})
        
        total_queries = len(personas) * len(questions)
        completed = {'count': 0}
        
        semaphore = Semaphore(self.max_workers)
        
        async def process_intervention(persona: Persona, question: str, q_idx: int):
            """Process intervention for one persona-question pair."""
            async with semaphore:
                # Check if we should stop
                if self.should_stop:
                    if progress_callback:
                        progress_callback("Simulation stopped by user")
                    raise asyncio.CancelledError("Simulation stopped by user")
                
                system_prompt = persona.to_prompt_context()
                if survey_context:
                    system_prompt += f"\n\n{survey_context}"
                current_validation = (
                    per_question_validation.get(q_idx)
                    if per_question_validation else None
                )
                if current_validation and current_validation.get('instruction'):
                    system_prompt += (
                        "\n\nIMPORTANT RESPONSE FORMAT:\n"
                        + current_validation['instruction']
                    )

                full_prompt = SimulationEngine._build_intervention_prompt(
                    intervention_text, question
                )
                
                response, req_error = await self.async_client.generate_response_async(
                    prompt=full_prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=model,
                    seed=seed,
                    response_format=(
                        {"type": "json_object"}
                        if current_validation and current_validation.get('type') == 'json'
                        else None
                    ),
                )
                
                # Check again after request
                if self.should_stop:
                    raise asyncio.CancelledError("Simulation stopped by user")
                
                completed['count'] += 1
                if progress_callback:
                    progress = (completed['count'] / total_queries) * 100
                    progress_callback(f"Progress: {completed['count']}/{total_queries} ({progress:.1f}%)")
                
                validation_status = "not_requested"
                validation_error = None
                if response and current_validation:
                    response, is_valid, validation_error = SimulationEngine._validate_response(
                        response, current_validation
                    )
                    validation_status = "valid" if is_valid else "invalid"

                return {
                    'persona': persona,
                    'question': question,
                    'response': response or f"[Error: {req_error or 'no response'}]",
                    'validation_status': validation_status,
                    'validation_error': validation_error,
                }
        
        tasks = [
            process_intervention(persona, question, q_idx)
            for persona in personas
            for q_idx, question in enumerate(questions)
        ]
        
        if progress_callback:
            progress_callback(f"Starting {total_queries} parallel intervention requests...")
        
        results_list = await asyncio.gather(*tasks, return_exceptions=True)
        
        # gather preserves task order: persona-major, then question index
        for idx, item in enumerate(results_list):
            if isinstance(item, Exception):
                if isinstance(item, asyncio.CancelledError):
                    continue  # user-initiated stop leaves no fake error rows
                if progress_callback:
                    progress_callback(f"Error: {str(item)}")
                # Keep a visible row instead of a silently missing persona-question pair
                result.add_response(
                    persona=personas[idx // len(questions)],
                    question=questions[idx % len(questions)],
                    response=f"[Error: {type(item).__name__}: {str(item)[:120]}]"
                )
                continue

            result.add_response(
                persona=item['persona'],
                question=item['question'],
                response=item['response'],
                validation_status=item.get('validation_status', 'not_requested'),
                validation_error=item.get('validation_error'),
            )

        if progress_callback:
            failed = sum(1 for r in result.persona_responses if str(r.get('response', '')).startswith('[Error:'))
            progress_callback(f"Intervention complete! {len(result.persona_responses) - failed}/{total_queries} succeeded, {failed} failed.")
        
        return result
