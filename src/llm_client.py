"""OpenAI-Compatible API Client for LM Studio, DeepSeek, OpenAI, and other providers."""
import os
from typing import List, Dict, Optional, Any, Tuple
from openai import OpenAI


class LMStudioClient:
    """Client for interacting with OpenAI-compatible APIs.
    
    Supports:
    - Local: LM Studio
    - Online: DeepSeek, OpenAI, and any OpenAI-compatible API
    
    Endpoints:
    - GET /v1/models
    - POST /v1/chat/completions
    - POST /v1/completions
    - POST /v1/embeddings
    - POST /v1/responses
    """
    
    def __init__(self, base_url: str = "http://localhost:1234/v1", api_key: Optional[str] = None):
        """
        Initialize the LM Studio or OpenAI-compatible API client.
        
        Args:
            base_url: Base URL for API (default: http://localhost:1234/v1)
            api_key: API key (optional for LM Studio, required for online APIs like DeepSeek/OpenAI)
        """
        self.base_url = base_url
        
        # Use provided API key or default to "lm-studio" for local
        if api_key is None:
            # Default for local LM Studio (doesn't require real key)
            self.api_key = "lm-studio"
        else:
            self.api_key = api_key
        
        # Determine if this is a local or online API
        self.is_local = "localhost" in base_url or "127.0.0.1" in base_url
        
        # Determine default model based on provider
        if "deepseek" in base_url.lower():
            self.default_model = "deepseek-chat"
        elif "openai" in base_url.lower():
            self.default_model = "gpt-3.5-turbo"
        else:
            self.default_model = "local-model"
        
        # Create HTTP client with proper timeout and HTTP/1.1 settings
        import httpx
        
        # Use different settings for local vs online
        if self.is_local:
            # Local: Force HTTP/1.1 for better compatibility with LM Studio
            http_client = httpx.Client(
                timeout=60.0,
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
                http2=False
            )
        else:
            # Online: Use default settings (HTTP/2 supported)
            http_client = httpx.Client(
                timeout=120.0,  # Longer timeout for online APIs
                limits=httpx.Limits(max_keepalive_connections=10, max_connections=20)
            )
        
        self.client = OpenAI(
            base_url=base_url,
            api_key=self.api_key,
            http_client=http_client,
            timeout=120.0,
            max_retries=2
        )
        # Why the last chat_completion returned None (engines surface this in result rows)
        self.last_error: Optional[str] = None
        
    def test_connection(self) -> tuple[bool, str]:
        """
        Test connection to LM Studio.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Try OpenAI client first
            models = self.client.models.list()
            model_list = [model.id for model in models.data]
            if model_list:
                return True, f"Connected successfully. Available models: {', '.join(model_list)}"
            else:
                return False, "Connected but no models loaded. Please load a model in LM Studio."
        except Exception as e:
            # If OpenAI client fails, try direct HTTP as fallback
            try:
                import requests
                # Remove /v1 suffix if present and add it back
                base = self.base_url.rstrip('/')
                if not base.endswith('/v1'):
                    base = base + '/v1'
                
                # Prepare headers with authentication for cloud APIs
                headers = {}
                if not self.is_local and self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                response = requests.get(f"{base}/models", headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data and data['data']:
                        model_list = [m['id'] for m in data['data']]
                        return True, f"Connected successfully. Available models: {', '.join(model_list)}"
                    else:
                        return False, "Connected but no models loaded."
                else:
                    return False, f"HTTP Error {response.status_code}: {response.text[:100]}"
            except requests.exceptions.RequestException as req_err:
                return False, f"Connection failed: {str(e)} (Fallback also failed: {str(req_err)})"
    
    def resolve_model(self, model: Optional[str] = None) -> str:
        """Resolve which model to use: explicit arg > Streamlit session state > provider default.

        ponytail: Streamlit fallback lives here only — the one place core code touches UI state.
        """
        if model:
            return model
        try:
            import streamlit as st
            if hasattr(st, 'session_state') and getattr(st.session_state, 'selected_model', None):
                return st.session_state.selected_model
        except Exception:
            pass
        return self.default_model

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500,
        model: Optional[str] = None,
        seed: Optional[int] = None,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        POST /v1/chat/completions - Send a chat completion request to LM Studio.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            model: Model name (optional, uses loaded model if None)
            seed: Fixed seed for reproducible sampling (provider-dependent)
            response_format: e.g. {"type": "json_object"} for structured output

        Returns:
            Generated response text or None if error
        """
        model = self.resolve_model(model)
        self.last_error = None
        # Provider-optional params: if the server rejects them, retry without
        extras = {}
        if seed is not None:
            extras['seed'] = seed
        if response_format is not None:
            extras['response_format'] = response_format
        try:
            # Try OpenAI client first
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **extras
                )
            except Exception:
                if not extras:
                    raise
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            content = response.choices[0].message.content
            if content:
                return content
            # 200 with empty content — report why; finish_reason=length means the model
            # burned the whole token budget before answering (typical for reasoning models)
            fr = response.choices[0].finish_reason
            if fr == 'length':
                self.last_error = (f"empty completion (finish_reason=length — model used all {max_tokens} "
                                   f"tokens without answering; raise Max Tokens)")
            else:
                self.last_error = f"empty completion (finish_reason={fr})"
            return None
            
        except Exception as e:
            # Fallback to direct HTTP request if OpenAI client fails
            try:
                import requests
                import json
                
                base = self.base_url.rstrip('/')
                if not base.endswith('/v1'):
                    base = base + '/v1'
                
                payload = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                }
                payload.update(extras)
                
                # Prepare headers with authentication for cloud APIs
                headers = {"Content-Type": "application/json"}
                if not self.is_local and self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                response = requests.post(
                    f"{base}/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=120
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        return data['choices'][0]['message']['content']
                    else:
                        self.last_error = f"unexpected response shape: {str(data)[:120]}"
                        print(f"Unexpected response format: {data}")
                        return None
                else:
                    self.last_error = f"HTTP {response.status_code}: {response.text[:120]}"
                    print(f"HTTP Error {response.status_code}: {response.text[:200]}")
                    return None

            except Exception as fallback_error:
                self.last_error = f"{type(e).__name__}: {str(e)[:100]} (fallback: {type(fallback_error).__name__})"
                print(f"Chat completion failed: {str(e)}")
                print(f"Fallback also failed: {str(fallback_error)}")
                return None
    
    def generate_with_messages(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500,
        model: Optional[str] = None,
        seed: Optional[int] = None
    ) -> str:
        """
        Generate response using multi-turn conversation messages (DeepSeek style).
        
        This method is specifically designed for maintaining conversation context
        across multiple turns, following the DeepSeek multi-turn dialogue pattern.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
                     Role can be: 'system', 'user', or 'assistant'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            model: Model name (optional)
            
        Returns:
            Generated response text
            
        Example:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is Python?"},
                {"role": "assistant", "content": "Python is a programming language."},
                {"role": "user", "content": "What is it used for?"}
            ]
            response = client.generate_with_messages(messages)
        """
        response = self.chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model,
            seed=seed
        )
        
        if response is None:
            raise RuntimeError("Failed to generate response from LLM")
        
        return response
    
    def get_available_models(self) -> List[str]:
        """
        GET /v1/models - Get list of available models.
        
        Returns:
            List of model names
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            # Try direct HTTP fallback
            try:
                import requests
                base = self.base_url.rstrip('/')
                if not base.endswith('/v1'):
                    base = base + '/v1'
                
                # Prepare headers with authentication for cloud APIs
                headers = {}
                if not self.is_local and self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                response = requests.get(f"{base}/models", headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data:
                        return [m['id'] for m in data['data']]
            except:
                pass
            
            print(f"Error getting models: {str(e)}")
            return []
    
    def get_models_detailed(self) -> List[Dict[str, Any]]:
        """
        GET /v1/models - Get detailed information about available models.
        
        Returns:
            List of model dictionaries with full details
        """
        try:
            models = self.client.models.list()
            return [
                {
                    "id": model.id,
                    "object": model.object,
                    "created": model.created,
                    "owned_by": model.owned_by if hasattr(model, 'owned_by') else "lm-studio"
                }
                for model in models.data
            ]
        except Exception as e:
            print(f"Error getting detailed models: {str(e)}")
            return []


class AsyncLLMClient:
    """Async version of LLM client for parallel requests (cloud APIs only)."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """Initialize async client.
        
        Args:
            base_url: API base URL
            api_key: API key for authentication
        """
        self.base_url = base_url
        self.api_key = api_key or "lm-studio"
        self.is_local = "localhost" in base_url or "127.0.0.1" in base_url
        
    async def generate_response_async(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        model: Optional[str] = None,
        seed: Optional[int] = None,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """Async version of generate_response for parallel execution.

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            model: Model name
            seed: Fixed seed for reproducible sampling (provider-dependent)
            response_format: e.g. {"type": "json_object"} for structured output

        Returns:
            (text, None) on success, (None, reason) on failure — engines write the
            reason into result rows so failed requests are visible in the data.
        """
        import aiohttp
        import asyncio

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model or "deepseek-chat",  # AsyncLLMClient needs explicit model
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        if seed is not None:
            payload['seed'] = seed
        if response_format is not None:
            payload['response_format'] = response_format

        headers = {
            "Content-Type": "application/json",
        }

        # Add authorization for cloud APIs
        if not self.is_local and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        base = self.base_url.rstrip('/')
        if not base.endswith('/v1'):
            base = base + '/v1'

        url = f"{base}/chat/completions"

        try:
            timeout = aiohttp.ClientTimeout(total=120)
            # Pin the certifi CA bundle: macOS python.org builds have a broken default
            # CA path (Install Certificates.command never ran), so aiohttp's default
            # SSL context fails verification while httpx/OpenAI SDK (certifi-based) works.
            # Verification stays ON — we only fix where the roots are loaded from.
            import certifi
            import ssl
            ssl_ctx = ssl.create_default_context(cafile=certifi.where())
            connector = aiohttp.TCPConnector(ssl=ssl_ctx)
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                # If the provider rejects optional params (seed/response_format), retry without them
                payloads = [payload]
                if seed is not None or response_format is not None:
                    payloads.append({k: v for k, v in payload.items() if k not in ('seed', 'response_format')})
                reason = "unknown error"
                # Up to 2 retries with backoff on transient failures (429/5xx/timeout/conn).
                # Parallel bursts hit provider rate limits; without this every blip
                # became a silent empty row in the results.
                for attempt in range(3):
                    retriable = False
                    for p in payloads:
                        try:
                            async with session.post(url, json=p, headers=headers) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    if 'choices' in data and len(data['choices']) > 0:
                                        choice = data['choices'][0]
                                        content = choice.get('message', {}).get('content')
                                        if content:
                                            return content, None
                                        fr = choice.get('finish_reason')
                                        if fr == 'length':
                                            # Deterministic: the model burned the whole token budget before
                                            # writing any answer (typical for reasoning models) — retrying is waste
                                            reason = (f"empty completion (finish_reason=length — model used all "
                                                      f"{max_tokens} tokens without answering; raise Max Tokens)")
                                            print(f"[AsyncLLMClient] {reason}")
                                            return None, reason
                                        # Other empty completions are provider-load hiccups — worth a retry
                                        reason = f"empty completion (finish_reason={fr})"
                                        print(f"[AsyncLLMClient] {reason}")
                                        retriable = True
                                        break
                                    reason = f"unexpected response shape: {str(data)[:120]}"
                                    print(f"[AsyncLLMClient] {reason}")
                                    return None, reason  # 200 but unusable — retrying won't fix it
                                error_text = await response.text()
                                reason = f"HTTP {response.status}: {error_text[:120]}"
                                print(f"[AsyncLLMClient] {reason}")
                                if response.status == 429 or response.status >= 500:
                                    retriable = True
                                    break  # rate limit / server error: skip payload variant, just back off
                                # other 4xx: fall through to the stripped-payload variant
                        except aiohttp.ClientConnectorCertificateError as e:
                            # Deterministic failure (broken CA store / MITM proxy) — retrying won't help
                            reason = f"ClientConnectorCertificateError: {str(e)[:120]}"
                            print(f"[AsyncLLMClient] {reason}")
                            return None, reason
                        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
                            reason = f"{type(e).__name__}: {str(e)[:120]}"
                            print(f"[AsyncLLMClient] {reason}")
                            retriable = True
                            break
                    if not retriable or attempt == 2:
                        return None, reason
                    await asyncio.sleep(2 ** (attempt + 1))  # 2s, 4s
                return None, reason  # unreachable (loop always returns), keeps analyzers happy
        except Exception as e:
            reason = f"{type(e).__name__}: {str(e)[:120]}"
            print(f"[AsyncLLMClient] Async request failed: {reason}")
            import traceback
            traceback.print_exc()
            return None, reason

