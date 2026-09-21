"""Test script for AsyncLLMClient"""
import asyncio
from src.llm_client import AsyncLLMClient

async def run_async_client_check():
    """Manual integration check; intentionally not collected by pytest."""
    
    # Test with DeepSeek (update with your actual API key)
    client = AsyncLLMClient(
        base_url="https://api.deepseek.com/v1",
        api_key="YOUR_API_KEY_HERE"  # Replace with actual key
    )
    
    print("Testing async client...")
    print(f"Base URL: {client.base_url}")
    print(f"Is local: {client.is_local}")
    
    response, err = await client.generate_response_async(
        prompt="What is 2+2? Answer in one sentence.",
        system_prompt="You are a helpful assistant.",
        temperature=0.7,
        max_tokens=50,
        model="deepseek-chat"
    )

    print(f"\nResponse: {response}\nError: {err}")
    
    if response:
        print("\n✅ Async client working!")
    else:
        print("\n❌ Async client failed!")

if __name__ == "__main__":
    asyncio.run(run_async_client_check())
