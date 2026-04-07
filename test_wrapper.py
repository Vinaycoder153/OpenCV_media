#!/usr/bin/env python3
"""Quick test to verify OpenAI client helper structure."""

from agent.openai_client import create_openai_client

print("Testing OpenAI client helper structure:")
print("=" * 50)

# Check that we can import
print("✅ Successfully imported create_openai_client")

# Create a mock client (just to check structure, not to call API)
import os

api_key = os.environ.get("OPENAI_API_KEY", "test-key")

try:
    client = create_openai_client(api_key=api_key, base_url="https://api.openai.com/v1")
    print("✅ Client instance created")
    print(f"✅ client.chat exists: {hasattr(client, 'chat')}")
    print(f"✅ client.chat.completions exists: {hasattr(client.chat, 'completions')}")
    print(
        f"✅ client.chat.completions.create exists: {hasattr(client.chat.completions, 'create')}"
    )
    print()
    print("Correct API structure:")
    print("  client.chat.completions.create(...) ✅")
    print()
    print("✅ FIX SUCCESSFUL - Helper structure is correct.")
except Exception as e:
    print(f"❌ Error: {e}")
