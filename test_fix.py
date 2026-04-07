#!/usr/bin/env python3
"""Quick verification for OpenAI helper and agent initialization."""

import os

from agent.business_agent import BusinessGrowthAgent
from agent.openai_client import create_openai_client

print("OPENAI CLIENT + AGENT VERIFICATION")
print("=" * 60)

# Test 1: Check client structure
print("\n1. Testing OpenAI client structure...")
try:
    api_key = os.environ.get("OPENAI_API_KEY", "test-key")
    client = create_openai_client(api_key=api_key, base_url="https://api.openai.com/v1")

    assert hasattr(client, "chat"), "client missing 'chat' attribute"
    assert hasattr(client.chat, "completions"), "client.chat missing 'completions'"
    assert hasattr(client.chat.completions, "create"), "missing create() method"

    print("✅ Client structure is correct")
    print("   client.chat.completions.create() exists")
except Exception as e:
    print(f"❌ Client structure test failed: {e}")

# Test 2: Initialize agent
print("\n2. Testing BusinessGrowthAgent initialization...")
try:
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set - skipping live agent test")
        print("   Set OPENAI_API_KEY to test actual API calls")
    else:
        agent = BusinessGrowthAgent()
        print("✅ BusinessGrowthAgent initialized successfully")
        print(f"   Model: {agent.model}")
        print(f"   Temperature: {agent.temperature}")

except Exception as e:
    print(f"❌ Agent test failed: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print()
print("📝 What was fixed:")
print("   - Renamed ChatCompletions class to Completions")
print("   - Added new Chat class with .completions property")
print("   - Now matches OpenAI API structure: client.chat.completions.create()")
print()
print("🚀 Ready to use with:")
print("   - python main.py")
print("   - python agent/baseline_agent.py")
print("   - All business agent capabilities")
print()
