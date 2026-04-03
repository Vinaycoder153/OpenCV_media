#!/usr/bin/env python3
"""
Google Gemini API client wrapper for chat completions.

Provides an interface similar to OpenAI's client for easier migration.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import google.generativeai as genai


class GeminiChatCompletion:
    """Response wrapper for chat completions to match OpenAI interface."""

    def __init__(self, text: str) -> None:
        self.choices = [Choice(text)]


class Choice:
    """Choice wrapper to match OpenAI interface."""

    def __init__(self, text: str) -> None:
        self.message = Message(text)


class Message:
    """Message wrapper to match OpenAI interface."""

    def __init__(self, content: str) -> None:
        self.content = content


class GeminiClient:
    """
    Wrapper for Google Gemini API to provide an interface similar to OpenAI's client.

    This class encapsulates the Gemini API calls and provides a `chat.completions.create()`
    method that matches OpenAI's interface for easier migration.

    Parameters
    ----------
    api_key : str
        Google API key for Gemini API access.
    """

    def __init__(self, api_key: str) -> None:
        """Initialize the Gemini client with an API key."""
        genai.configure(api_key=api_key)
        self.chat = Chat()


class Chat:
    """Chat interface matching OpenAI's format (client.chat.completions.create)."""

    def __init__(self) -> None:
        """Initialize the Chat interface."""
        self.completions = Completions()


class Completions:
    """Completions interface for chat.completions.create() method."""

    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> GeminiChatCompletion:
        """
        Create a chat completion using Gemini API.

        Parameters
        ----------
        model : str
            Model name (e.g., 'gemini-1.5-flash', 'gemini-1.5-pro').
        messages : List[Dict[str, str]]
            List of messages with 'role' and 'content' keys.
        temperature : float, optional
            Sampling temperature (0.0-2.0). Default is 0.7.
        **kwargs
            Additional arguments (for compatibility, may be ignored).

        Returns
        -------
        GeminiChatCompletion
            Response object with choices[0].message.content interface.

        Raises
        ------
        ValueError
            If the API call fails or model is invalid.
        """
        try:
            # Initialize the model
            gemini_model = genai.GenerativeModel(model_name=model)

            # Format messages for Gemini (system message handling)
            formatted_messages = []
            system_prompt = None

            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")

                # Gemini uses "user" and "model" instead of "assistant"
                if role == "system":
                    system_prompt = content
                elif role == "assistant":
                    formatted_messages.append({"role": "model", "parts": [content]})
                else:
                    formatted_messages.append({"role": "user", "parts": [content]})

            # Start a chat session with system prompt if provided
            if system_prompt:
                response = gemini_model.generate_content(
                    [system_prompt, *[msg["parts"][0] for msg in formatted_messages]],
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=2048,
                    ),
                )
            else:
                # For simple message exchanges
                response = gemini_model.generate_content(
                    (
                        formatted_messages[-1]["parts"][0]
                        if formatted_messages
                        else "Hello"
                    ),
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=2048,
                    ),
                )

            # Extract text from response
            if response.parts:
                text = response.parts[0].text
            else:
                text = ""

            return GeminiChatCompletion(text)

        except Exception as exc:
            raise ValueError(f"Gemini API error: {exc}") from exc


def create_gemini_client(api_key: str) -> GeminiClient:
    """
    Factory function to create a Gemini client.

    Parameters
    ----------
    api_key : str
        Google API key for Gemini API access.

    Returns
    -------
    GeminiClient
        Initialized Gemini client instance.
    """
    return GeminiClient(api_key)
