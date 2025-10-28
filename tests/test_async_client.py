"""Test script for AsyncLLMClient"""
import asyncio
from src.llm_client import AsyncLLMClient

async def test_async_client():
    """Test the async client with a simple request."""
    
    # Test with DeepSeek (update with your actual API key)
    client = AsyncLLMClient(
        base_url="https://api.deepseek.com/v1",
        api_key="YOUR_API_KEY_HERE"  # Replace with actual key
    )
    
    print("Testing async client...")
    print(f"Base URL: {client.base_url}")
    print(f"Is local: {client.is_local}")
    
    response = await client.generate_response_async(
        prompt="What is 2+2? Answer in one sentence.",
        system_prompt="You are a helpful assistant.",
        temperature=0.7,
        max_tokens=50,
        model="deepseek-chat"
    )
    
    print(f"\nResponse: {response}")
    
    if response:
        print("\n✅ Async client working!")
    else:
        print("\n❌ Async client failed!")

if __name__ == "__main__":
    asyncio.run(test_async_client())
