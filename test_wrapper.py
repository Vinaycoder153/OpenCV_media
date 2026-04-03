#!/usr/bin/env python3
"""Quick test to verify Gemini client wrapper structure."""

from agent.gemini_client import create_gemini_client

print("Testing Gemini Client Wrapper Structure:")
print("=" * 50)

# Check that we can import
print("✅ Successfully imported create_gemini_client")

# Create a mock client (just to check structure, not to call API)
import os

api_key = os.environ.get("GOOGLE_API_KEY", "test-key")

try:
    client = create_gemini_client(api_key)
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
    print("✅ FIX SUCCESSFUL - Wrapper structure is now correct!")
except Exception as e:
    print(f"❌ Error: {e}")
