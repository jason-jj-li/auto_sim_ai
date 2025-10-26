"""Simulation engine for running surveys and interventions."""
from typing import List, Dict, Any, Optional, Callable, TYPE_CHECKING
from datetime import datetime
import json
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .persona import Persona
from .llm_client import LMStudioClient
from .tools import ToolRegistry, get_default_tool_registry

if TYPE_CHECKING:
    from .survey_config import SurveyConfig
    from .cache import ResponseCache
    from .checkpoint import CheckpointManager


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
        
    def add_response(self, persona: Persona, question: str, response: str, 
                     conversation_history: Optional[List[Dict[str, str]]] = None):
        """Add a response from a persona."""
        self.persona_responses.append({
            'persona_name': persona.name,
            'persona_age': persona.age,
            'persona_gender': persona.gender,
            'persona_occupation': persona.occupation,
            'question': question,
            'response': response,
            'conversation_history': conversation_history or []
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'simulation_type': self.simulation_type,
            'timestamp': self.timestamp,
            'intervention_text': self.intervention_text,
            'questions': self.questions,
            'responses': self.persona_responses,
            'survey_config': self.survey_config,
            'instrument_name': self.instrument_name
        }


class SimulationEngine:
    """Engine for running simulations with personas."""
    
    def __init__(
        self, 
        llm_client: LMStudioClient, 
        enable_tools: bool = False,
        cache: Optional['ResponseCache'] = None,
        checkpoint_manager: Optional['CheckpointManager'] = None
    ):
        """
        Initialize simulation engine.
        
        Args:
            llm_client: LM Studio client instance
            enable_tools: Whether to enable tool use for personas
            cache: Optional ResponseCache for caching LLM responses
            checkpoint_manager: Optional CheckpointManager for saving progress
        """
        self.llm_client = llm_client
        self.enable_tools = enable_tools
        self.tool_registry = get_default_tool_registry() if enable_tools else None
        self.cache = cache
        self.checkpoint_manager = checkpoint_manager
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
        stop_callback: Optional[Callable[[], bool]] = None
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
            
        Returns:
            SimulationResult object
        """
        timestamp = datetime.now().isoformat()
        result = SimulationResult('survey', timestamp)
        result.questions = questions
        
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
                        progress_callback("⏹️ Simulation stopped by user")
                    result.metadata = result.metadata or {}
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
                    system_prompt += f"\n\n⚠️ IMPORTANT RESPONSE FORMAT:\n{current_validation['instruction']}"
                
                # Format the question with response guidance
                question_with_guidance = question
                if not question.strip().endswith('?'):
                    question_with_guidance += "?"
                
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
                    persona_json = json.dumps({
                        'name': persona.name,
                        'age': persona.age,
                        'gender': persona.gender,
                        'occupation': persona.occupation,
                        'background': persona.background
                    }, sort_keys=True)
                    cached_response = self.cache.get(
                        persona_json, question, temperature, survey_context
                    )
                
                if cached_response:
                    response = cached_response
                else:
                    # Get response from LLM
                    start_time = time.time()
                    response = self.llm_client.chat_completion(
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    elapsed = time.time() - start_time
                    self.response_times.append(elapsed)
                    
                    # Store in cache if available
                    if response and self.cache:
                        self.cache.put(
                            persona_json, question, temperature, response, survey_context
                        )
                
                # Validate and clean response if validation rules provided
                if response and response_validation:
                    response = self._validate_and_clean_response(response, response_validation)
                
                if response:
                    result.add_response(persona, question, response, messages)
                else:
                    result.add_response(persona, question, "[Error: No response received]", messages)
                
                # Save checkpoint if manager is available and it's time
                if self.checkpoint_manager and self.checkpoint_manager.should_save_checkpoint(current_query):
                    completed_indices = {
                        i: list(range(len(questions))) 
                        for i in range(personas.index(persona))
                    }
                    # Add partial completion for current persona
                    current_idx = personas.index(persona)
                    question_idx = questions.index(question)
                    if current_idx not in completed_indices:
                        completed_indices[current_idx] = []
                    completed_indices[current_idx].append(question_idx)
                    
                    checkpoint = self.checkpoint_manager.create_checkpoint(
                        simulation_type='survey',
                        personas=personas,
                        questions=questions,
                        completed_responses=result.persona_responses,
                        completed_persona_indices=list(range(personas.index(persona))),
                        completed_question_indices=completed_indices,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        survey_context=survey_context,
                        response_validation=response_validation,
                        survey_config=survey_config.to_dict() if survey_config else None
                    )
                    self.checkpoint_manager.save_checkpoint(checkpoint)
                    if progress_callback:
                        progress_callback(f"💾 Checkpoint saved ({current_query}/{total_queries})")
        
        return result
    
    def _validate_and_clean_response(self, response: str, validation: Dict[str, Any]) -> str:
        """
        Validate and clean the LLM response based on validation rules.
        
        Args:
            response: The raw LLM response
            validation: Validation rules dictionary
            
        Returns:
            Cleaned and validated response, or original if validation fails
        """
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
                    return str(int(num))  # Return as integer string
                else:
                    # Out of range, try to clamp
                    clamped = max(min_val, min(max_val, num))
                    return str(int(clamped))
            return response  # Return original if no number found
        
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
                            return allowed_word
                    # Not in list, return closest match or first allowed
                    return allowed[0]
                return first_word
            return response
        
        elif validation_type == 'json':
            # Extract and validate JSON
            try:
                # Try to find JSON in response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    parsed = json_module.loads(json_str)
                    return json_module.dumps(parsed)  # Return valid JSON
            except:
                pass
            return response
        
        elif validation_type == 'regex':
            # Validate against regex pattern
            pattern = validation.get('pattern', '')
            if pattern:
                match = re.search(pattern, response)
                if match:
                    return match.group(0)
            return response
        
        return response
    
    def run_intervention(
        self,
        personas: List[Persona],
        intervention_text: str,
        followup_questions: List[str],
        temperature: float = 0.7,
        max_tokens: int = 500,
        progress_callback: Optional[Callable[[str], None]] = None,
        stop_callback: Optional[Callable[[], bool]] = None
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
        
        total_queries = len(personas) * (1 + len(followup_questions))
        current_query = 0
        
        for persona in personas:
            # Check if we should stop
            if stop_callback and stop_callback():
                if progress_callback:
                    progress_callback("⏹️ Simulation stopped by user")
                return result
            
            # Build conversation with intervention
            conversation = [
                {"role": "system", "content": persona.to_prompt_context()},
                {"role": "user", "content": f"Please read and consider the following:\n\n{intervention_text}\n\nPlease acknowledge that you've read this."}
            ]
            
            current_query += 1
            if progress_callback:
                progress_callback(
                    f"Presenting intervention to {persona.name} ({current_query}/{total_queries})..."
                )
            
            # Get acknowledgment
            acknowledgment = self.llm_client.chat_completion(
                messages=conversation,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if acknowledgment:
                conversation.append({"role": "assistant", "content": acknowledgment})
            
            # Ask follow-up questions
            for question in followup_questions:
                # Check if we should stop
                if stop_callback and stop_callback():
                    if progress_callback:
                        progress_callback("⏹️ Simulation stopped by user")
                    return result
                
                current_query += 1
                if progress_callback:
                    progress_callback(
                        f"Asking {persona.name} ({current_query}/{total_queries}): {question[:50]}..."
                    )
                
                # Format the question with response guidance
                question_with_guidance = question
                if not question.strip().endswith('?'):
                    question_with_guidance += "?"
                # For intervention follow-ups, encourage detailed responses
                question_with_guidance += "\n\n[Please provide a thoughtful, detailed response (2-4 sentences) based on the information you just read and your personal perspective. Answer naturally as yourself.]"
                
                conversation.append({"role": "user", "content": question_with_guidance})
                
                response = self.llm_client.chat_completion(
                    messages=conversation,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                if response:
                    conversation.append({"role": "assistant", "content": response})
                    result.add_response(persona, question, response, conversation.copy())
                else:
                    result.add_response(
                        persona, question, "[Error: No response received]", conversation.copy()
                    )
        
        return result
    
    def run_survey_parallel(
        self,
        personas: List[Persona],
        questions: List[str],
        temperature: float = 0.7,
        max_tokens: int = 500,
        max_workers: int = 5,
        progress_callback: Optional[Callable[[str], None]] = None,
        survey_context: Optional[str] = None,
        response_validation: Optional[Dict[str, Any]] = None,
        survey_config: Optional['SurveyConfig'] = None,
        per_question_validation: Optional[Dict[int, Dict[str, Any]]] = None
    ) -> SimulationResult:
        """
        Run a survey simulation with batched processing (optimized for Streamlit).
        
        NOTE: True parallel processing doesn't work with Streamlit due to ScriptRunContext issues.
        This method processes in batches to provide better progress updates and checkpointing
        opportunities, which improves the user experience for large simulations.
        
        Args:
            personas: List of personas to survey
            questions: List of questions to ask
            temperature: LLM temperature parameter
            max_tokens: Maximum tokens per response
            max_workers: Batch size for processing (default: 5)
            progress_callback: Optional callback for progress updates
            survey_context: Optional context/instructions for the survey
            response_validation: Optional validation rules for response format (applies to all questions)
            survey_config: Optional SurveyConfig object with full survey metadata
            per_question_validation: Optional dict mapping question index to validation rules
            
        Returns:
            SimulationResult object
        """
        if progress_callback:
            progress_callback(f"⚡ Sequential processing with batched progress updates (every {max_workers} responses)")
        
        timestamp = datetime.now().isoformat()
        result = SimulationResult('survey', timestamp)
        result.questions = questions
        
        # Store survey configuration metadata if provided
        if survey_config:
            result.survey_config = survey_config.to_dict()
            result.instrument_name = survey_config.template_name
        
        total_queries = len(personas) * len(questions)
        completed_queries = 0
        
        # Process all persona-question pairs with batched progress updates
        for persona in personas:
            for question_idx, question in enumerate(questions):
                # Build messages
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
                    system_prompt += f"\n\n⚠️ IMPORTANT RESPONSE FORMAT:\n{current_validation['instruction']}"
                
                # Format the question with response guidance  
                question_with_guidance = question
                if not question.strip().endswith('?'):
                    question_with_guidance += "?"
                
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
                
                # Check cache first
                cached_response = None
                if self.cache:
                    persona_json = json.dumps({
                        'name': persona.name,
                        'age': persona.age,
                        'gender': persona.gender,
                        'occupation': persona.occupation,
                        'background': persona.background
                    }, sort_keys=True)
                    cached_response = self.cache.get(
                        persona_json, question, temperature, survey_context
                    )
                
                if cached_response:
                    response = cached_response
                else:
                    # Get response from LLM
                    start_time = time.time()
                    response = self.llm_client.chat_completion(
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    elapsed = time.time() - start_time
                    self.response_times.append(elapsed)
                    
                    # Store in cache if available
                    if response and self.cache:
                        self.cache.put(
                            persona_json, question, temperature, response, survey_context
                        )
                
                # Validate and clean response if validation rules provided
                if response and response_validation:
                    response = self._validate_and_clean_response(response, response_validation)
                
                # Add to result
                result.add_response(
                    persona,
                    question,
                    response if response else "[Error: No response received]",
                    messages
                )
                
                # Update progress
                completed_queries += 1
                
                # Save checkpoint periodically
                if self.checkpoint_manager and self.checkpoint_manager.should_save_checkpoint(completed_queries):
                    if progress_callback:
                        progress_callback(f"💾 Saving checkpoint... ({completed_queries}/{total_queries})")
                    
                    # Create checkpoint for parallel execution
                    checkpoint = self.checkpoint_manager.create_checkpoint(
                        simulation_type='survey_parallel',
                        personas=personas,
                        questions=questions,
                        completed_responses=result.persona_responses,
                        completed_persona_indices=list(range(completed_queries // len(questions))),
                        completed_question_indices={},
                        temperature=temperature,
                        max_tokens=max_tokens,
                        survey_context=survey_context,
                        response_validation=response_validation,
                        survey_config=survey_config.to_dict() if survey_config else None
                    )
                    self.checkpoint_manager.save_checkpoint(checkpoint)
                
                # Update progress callback (every batch_size queries for better UX)
                if progress_callback and (completed_queries % max_workers == 0 or completed_queries == total_queries):
                    cache_info = ""
                    if self.cache:
                        stats = self.cache.get_stats()
                        cache_info = f" | Cache: {stats['hit_rate']:.0%} hits"
                    progress_callback(
                        f"⚡ Processing: {completed_queries}/{total_queries}{cache_info}"
                    )
        
        return result
    
    def run_longitudinal_intervention(
        self,
        personas: List[Persona],
        study_config: 'InterventionStudyConfig',
        temperature: float = 0.7,
        max_tokens: int = 500,
        progress_callback: Optional[Callable[[str], None]] = None,
        response_validation: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run a longitudinal intervention study with repeated waves.
        
        Args:
            personas: List of personas to simulate
            study_config: InterventionStudyConfig object defining the study
            temperature: LLM temperature
            max_tokens: Max tokens for responses
            progress_callback: Callback for progress updates
            response_validation: Response validation rules
        
        Returns:
            Dictionary with results for each wave
        """
        from .intervention_study import InterventionStudyConfig
        
        if progress_callback:
            progress_callback(f"📊 Starting longitudinal study: {study_config.study_name}")
            progress_callback(f"📋 {study_config.total_waves} waves, {len(personas)} personas")
        
        # Dictionary to store results for each wave
        wave_results = {}
        
        # Track total progress
        total_queries = sum(len(wave.questions) for wave in study_config.waves) * len(personas)
        completed_queries = 0
        
        # Process each wave
        for wave in study_config.waves:
            if progress_callback:
                progress_callback(f"\n🌊 Wave {wave.wave_number}/{study_config.total_waves}: {wave.wave_label}")
                progress_callback(f"📅 Day {wave.days_from_baseline} from baseline")
            
            # Create result for this wave
            wave_result = SimulationResult(
                simulation_type='longitudinal_intervention',
                timestamp=datetime.now().isoformat()
            )
            wave_result.questions = wave.questions
            wave_result.intervention_text = wave.intervention_text if wave.is_intervention_wave else None
            
            # Process each persona for this wave
            for persona in personas:
                # Build context for this wave
                wave_context = f"{wave.context_update}\n\n"
                
                # If this is the intervention wave, present the intervention first
                if wave.is_intervention_wave and wave.intervention_text:
                    if progress_callback:
                        progress_callback(f"💉 Presenting intervention to {persona.name}")
                    
                    # Present intervention
                    intervention_messages = [
                        {"role": "system", "content": f"You are simulating the perspective of this person:\n\n{persona.to_prompt_context(use_json_format=True)}"},
                        {"role": "system", "content": wave_context},
                        {"role": "user", "content": f"Please read the following information carefully:\n\n{wave.intervention_text}\n\nSimply acknowledge that you have read and understood this information."}
                    ]
                    
                    try:
                        _ = self.client.chat_completion(
                            messages=intervention_messages,
                            temperature=temperature,
                            max_tokens=max_tokens
                        )
                    except Exception as e:
                        if progress_callback:
                            progress_callback(f"⚠️ Intervention presentation error for {persona.name}: {str(e)}")
                
                # Ask questions for this wave
                for question in wave.questions:
                    completed_queries += 1
                    
                    # Build messages
                    messages = [
                        {"role": "system", "content": f"You are simulating the perspective of this person:\n\n{persona.to_prompt_context(use_json_format=True)}"},
                        {"role": "system", "content": wave_context}
                    ]
                    
                    # Add response format instruction if provided
                    if response_validation and 'instruction' in response_validation:
                        messages.append({"role": "system", "content": response_validation['instruction']})
                    
                    messages.append({"role": "user", "content": question})
                    
                    # Get response
                    try:
                        response = self.client.chat_completion(
                            messages=messages,
                            temperature=temperature,
                            max_tokens=max_tokens
                        )
                        
                        # Validate if needed
                        if response and response_validation:
                            response = self._validate_and_clean_response(response, response_validation)
                        
                        # Add to wave result
                        wave_result.add_response(
                            persona,
                            question,
                            response if response else "[Error: No response received]",
                            messages
                        )
                        
                    except Exception as e:
                        wave_result.add_response(
                            persona,
                            question,
                            f"[Error: {str(e)}]",
                            messages
                        )
                    
                    # Update progress
                    if progress_callback and completed_queries % 5 == 0:
                        progress_pct = (completed_queries / total_queries) * 100
                        progress_callback(f"⚡ Overall progress: {completed_queries}/{total_queries} ({progress_pct:.1f}%)")
            
            # Store wave result
            wave_results[f"wave_{wave.wave_number}"] = wave_result
            
            if progress_callback:
                progress_callback(f"✅ Wave {wave.wave_number} complete!")
        
        if progress_callback:
            progress_callback(f"\n🎉 Longitudinal study complete! {study_config.total_waves} waves processed.")
        
        return {
            "study_name": study_config.study_name,
            "total_waves": study_config.total_waves,
            "intervention_wave": study_config.intervention_wave_number,
            "wave_results": wave_results,
            "timestamp": datetime.now().isoformat()
        }
    
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
        """Validate and clean response based on validation rules.
        
        Args:
            response: Raw response from LLM
            validation: Validation rules
            
        Returns:
            Cleaned response
        """
        import re
        import json
        
        response_type = validation.get('type', '')
        
        if response_type == 'number':
            # Extract number from response
            # Try to find a number in the response
            numbers = re.findall(r'-?\d+\.?\d*', response)
            if numbers:
                try:
                    num = float(numbers[0])
                    # Validate range
                    min_val = validation.get('min', float('-inf'))
                    max_val = validation.get('max', float('inf'))
                    if min_val <= num <= max_val:
                        return str(int(num)) if num.is_integer() else str(num)
                except ValueError:
                    pass
            return response  # Return as-is if can't extract number
        
        elif response_type == 'word':
            # Extract single word from allowed list
            allowed = validation.get('allowed', [])
            response_lower = response.lower().strip()
            for word in allowed:
                if word.lower() in response_lower:
                    return word
            return response  # Return as-is if no match
        
        elif response_type == 'json':
            # Try to extract JSON object
            try:
                # First try parsing the whole response
                json_obj = json.loads(response)
                return json.dumps(json_obj)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
                if json_match:
                    try:
                        json_obj = json.loads(json_match.group(1))
                        return json.dumps(json_obj)
                    except json.JSONDecodeError:
                        pass
                
                # Try to find JSON object in the response
                json_match = re.search(r'\{.*?\}', response, re.DOTALL)
                if json_match:
                    try:
                        json_obj = json.loads(json_match.group(0))
                        return json.dumps(json_obj)
                    except json.JSONDecodeError:
                        pass
            
            return response  # Return as-is if can't extract JSON
        
        return response
        
    async def run_survey_parallel(
        self,
        personas: List[Persona],
        questions: List[str],
        temperature: float = 0.7,
        max_tokens: int = 500,
        progress_callback: Optional[Callable[[str], None]] = None,
        survey_context: Optional[str] = None,
        model: Optional[str] = None,
        response_validation: Optional[Dict[str, Any]] = None
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
            response_validation: Optional validation rules for response format
            
        Returns:
            SimulationResult
        """
        import asyncio
        from asyncio import Semaphore
        
        timestamp = datetime.now().isoformat()
        result = SimulationResult('survey', timestamp)
        result.questions = questions
        
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
                        progress_callback("⏹️ Simulation stopped by user")
                    raise asyncio.CancelledError("Simulation stopped by user")
                
                # Build prompt
                system_prompt = persona.to_prompt_context()
                if survey_context:
                    system_prompt += f"\n\n{survey_context}"
                
                # Add response format enforcement if provided
                if response_validation and 'instruction' in response_validation:
                    system_prompt += f"\n\n⚠️ CRITICAL RESPONSE FORMAT:\n{response_validation['instruction']}"
                    system_prompt += f"\n\nYou MUST follow this format exactly. Any deviation will cause the response to be rejected."
                
                full_prompt = f"{question}\n\nPlease provide a thoughtful and authentic response based on your background and perspective."
                
                # For structured responses, emphasize format in the question
                if response_validation and response_validation.get('type') == 'number':
                    full_prompt = f"{question}\n\n[Respond with ONLY a number between {response_validation.get('min', 0)} and {response_validation.get('max', 5)}. No text, no explanation, just the number.]"
                elif response_validation and response_validation.get('type') == 'word':
                    allowed = response_validation.get('allowed', [])
                    full_prompt = f"{question}\n\n[Respond with ONLY one word from this list: {', '.join(allowed)}. Nothing else.]"
                elif response_validation and response_validation.get('type') == 'json':
                    full_prompt = f"{question}\n\n[Respond with ONLY a valid JSON object. No markdown, no explanations, just pure JSON.]"
                
                # Make async request
                response = await self.async_client.generate_response_async(
                    prompt=full_prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=model
                )
                
                # Check again after request
                if self.should_stop:
                    raise asyncio.CancelledError("Simulation stopped by user")
                
                # Validate and clean response if validation rules provided
                if response and response_validation:
                    response = self._validate_and_clean_response_async(response, response_validation)
                
                # Update progress
                completed['count'] += 1
                if progress_callback:
                    progress = (completed['count'] / total_queries) * 100
                    progress_callback(f"⚡ Progress: {completed['count']}/{total_queries} ({progress:.1f}%)")
                
                return {
                    'persona': persona,
                    'question': question,
                    'question_idx': q_idx,
                    'response': response or "[Error: No response]"
                }
        
        # Create all tasks
        tasks = [
            process_single_query(persona, question, q_idx)
            for persona in personas
            for q_idx, question in enumerate(questions)
        ]
        
        if progress_callback:
            progress_callback(f"🚀 Starting {total_queries} parallel requests with {self.max_workers} workers...")
        
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
        print(f"[PARALLEL] Average time per request: {elapsed_time/len(results_list):.2f}s")
        if self.max_workers > 1:
            theoretical_sequential_time = elapsed_time * self.max_workers
            print(f"[PARALLEL] Estimated speedup: ~{theoretical_sequential_time/elapsed_time:.1f}x")
        error_count = sum(1 for item in results_list if isinstance(item, Exception))
        print(f"[PARALLEL] Errors: {error_count}")
        print(f"{'='*80}\n")
        
        # Process results
        for idx, item in enumerate(results_list):
            if isinstance(item, Exception):
                error_msg = f"Task {idx} failed: {type(item).__name__}: {str(item)}"
                print(f"[DEBUG] {error_msg}")
                if progress_callback:
                    progress_callback(f"⚠️ Error in task {idx}: {str(item)}")
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
                response=item['response']
            )
        
        if progress_callback:
            progress_callback(f"✅ Survey complete! Processed {total_queries} responses.")
        
        return result
    
    async def run_intervention_parallel(
        self,
        personas: List[Persona],
        intervention_text: str,
        questions: List[str],
        temperature: float = 0.7,
        max_tokens: int = 500,
        progress_callback: Optional[Callable[[str], None]] = None,
        model: Optional[str] = None
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
        
        total_queries = len(personas) * len(questions)
        completed = {'count': 0}
        
        semaphore = Semaphore(self.max_workers)
        
        async def process_intervention(persona: Persona, question: str, q_idx: int):
            """Process intervention for one persona-question pair."""
            async with semaphore:
                # Check if we should stop
                if self.should_stop:
                    if progress_callback:
                        progress_callback("⏹️ Simulation stopped by user")
                    raise asyncio.CancelledError("Simulation stopped by user")
                
                system_prompt = persona.to_prompt_context()
                
                full_prompt = f"""
Please read the following message carefully:

---
{intervention_text}
---

After reading this message, please answer the following question:

{question}

Provide your authentic response based on your background and perspective.
"""
                
                response = await self.async_client.generate_response_async(
                    prompt=full_prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=model
                )
                
                # Check again after request
                if self.should_stop:
                    raise asyncio.CancelledError("Simulation stopped by user")
                
                completed['count'] += 1
                if progress_callback:
                    progress = (completed['count'] / total_queries) * 100
                    progress_callback(f"⚡ Progress: {completed['count']}/{total_queries} ({progress:.1f}%)")
                
                return {
                    'persona': persona,
                    'question': question,
                    'response': response or "[Error: No response]"
                }
        
        tasks = [
            process_intervention(persona, question, q_idx)
            for persona in personas
            for q_idx, question in enumerate(questions)
        ]
        
        if progress_callback:
            progress_callback(f"🚀 Starting {total_queries} parallel intervention requests...")
        
        results_list = await asyncio.gather(*tasks, return_exceptions=True)
        
        for item in results_list:
            if isinstance(item, Exception):
                if progress_callback:
                    progress_callback(f"⚠️ Error: {str(item)}")
                continue
            
            result.add_response(
                persona=item['persona'],
                question=item['question'],
                response=item['response']
            )
        
        if progress_callback:
            progress_callback(f"✅ Intervention complete! Processed {total_queries} responses.")
        
        return result

