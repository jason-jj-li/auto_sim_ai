"""OpenAI-Compatible API Client for LM Studio, DeepSeek, OpenAI, and other providers."""
import os
from typing import List, Dict, Optional, Any
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
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500,
        model: Optional[str] = None
    ) -> Optional[str]:
        """
        POST /v1/chat/completions - Send a chat completion request to LM Studio.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            model: Model name (optional, uses loaded model if None)
            
        Returns:
            Generated response text or None if error
        """
        try:
            # Get model from session state if available
            if model is None:
                try:
                    import streamlit as st
                    if hasattr(st, 'session_state') and hasattr(st.session_state, 'selected_model'):
                        model = st.session_state.selected_model
                except:
                    pass
            
            # Try OpenAI client first
            response = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
            
        except Exception as e:
            # Fallback to direct HTTP request if OpenAI client fails
            try:
                import requests
                import json
                
                base = self.base_url.rstrip('/')
                if not base.endswith('/v1'):
                    base = base + '/v1'
                
                payload = {
                    "model": model or self.default_model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                }
                
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
                        print(f"Unexpected response format: {data}")
                        return None
                else:
                    print(f"HTTP Error {response.status_code}: {response.text[:200]}")
                    return None
                    
            except Exception as fallback_error:
                print(f"Chat completion failed: {str(e)}")
                print(f"Fallback also failed: {str(fallback_error)}")
                return None
    
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
    
    def completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        stop: Optional[List[str]] = None,
        **kwargs
    ) -> Optional[str]:
        """
        POST /v1/completions - Generate text completion (non-chat format).
        
        Args:
            prompt: The prompt to complete
            model: Model name (uses session state if None)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stop: Optional stop sequences
            **kwargs: Additional parameters
            
        Returns:
            Generated completion text or None if error
        """
        try:
            # Get model from session state if available
            if model is None:
                try:
                    import streamlit as st
                    if hasattr(st, 'session_state') and hasattr(st.session_state, 'selected_model'):
                        model = st.session_state.selected_model
                except:
                    pass
            
            response = self.client.completions.create(
                model=model or self.default_model,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                **kwargs
            )
            return response.choices[0].text
        except Exception as e:
            print(f"Error in completion: {str(e)}")
            return None
    
    def create_embedding(
        self,
        text: str,
        model: Optional[str] = None
    ) -> Optional[List[float]]:
        """
        POST /v1/embeddings - Create embeddings for text.
        
        Args:
            text: Text to embed
            model: Model name (optional)
            
        Returns:
            Embedding vector or None if error
        """
        try:
            if model is None:
                try:
                    import streamlit as st
                    if hasattr(st, 'session_state') and hasattr(st.session_state, 'selected_model'):
                        model = st.session_state.selected_model
                except:
                    pass
            
            response = self.client.embeddings.create(
                model=model or self.default_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error creating embedding: {str(e)}")
            return None
    
    def create_embeddings_batch(
        self,
        texts: List[str],
        model: Optional[str] = None
    ) -> Optional[List[List[float]]]:
        """
        POST /v1/embeddings - Create embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            model: Model name (optional)
            
        Returns:
            List of embedding vectors or None if error
        """
        try:
            if model is None:
                try:
                    import streamlit as st
                    if hasattr(st, 'session_state') and hasattr(st.session_state, 'selected_model'):
                        model = st.session_state.selected_model
                except:
                    pass
            
            response = self.client.embeddings.create(
                model=model or self.default_model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"Error creating embeddings: {str(e)}")
            return None
    
    def stream_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500,
        model: Optional[str] = None,
        **kwargs
    ):
        """
        POST /v1/chat/completions - Stream chat completion responses.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            model: Model name (optional)
            **kwargs: Additional parameters
            
        Yields:
            Chunks of response text
        """
        try:
            if model is None:
                try:
                    import streamlit as st
                    if hasattr(st, 'session_state') and hasattr(st.session_state, 'selected_model'):
                        model = st.session_state.selected_model
                except:
                    pass
            
            stream = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"Error in streaming completion: {str(e)}")
            yield None


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
        model: Optional[str] = None
    ) -> Optional[str]:
        """Async version of generate_response for parallel execution.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            model: Model name
            
        Returns:
            Generated text or None if failed
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
        
        # Simplified logging for parallel requests
        # Only log the request initiation, not every detail
        # print(f"[AsyncLLMClient] → Request to {model}")
        
        try:
            import ssl
            
            # Create SSL context that doesn't verify certificates (for development)
            # For production, you should use proper certificates
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            timeout = aiohttp.ClientTimeout(total=120)
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    # Only log errors or completion, not every success
                    if response.status == 200:
                        data = await response.json()
                        if 'choices' in data and len(data['choices']) > 0:
                            content = data['choices'][0]['message']['content']
                            # Only log first request to verify it's working
                            # print(f"[AsyncLLMClient] ✓ Got response: {content[:30]}...")
                            return content
                        else:
                            print(f"[AsyncLLMClient] ⚠️ Unexpected response format: {data}")
                            return None
                    else:
                        error_text = await response.text()
                        print(f"[AsyncLLMClient] ❌ HTTP Error {response.status}: {error_text[:200]}")
                        return None
        except asyncio.TimeoutError:
            print(f"[AsyncLLMClient] Request timeout for prompt: {prompt[:50]}...")
            return None
        except Exception as e:
            print(f"[AsyncLLMClient] Async request failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
        
        return None

