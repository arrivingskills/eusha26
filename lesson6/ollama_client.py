"""
ollama_client.py — A generic, reusable interface to a locally running Ollama instance.

Usage:
    from eusha.ollama_client import OllamaClient

    client = OllamaClient(model="llama3")
    response = client.chat("What is the capital of France?")
    print(response)
"""

import json

try:
    import ollama as _ollama_lib
    _HAS_OLLAMA_LIB = True
except ImportError:
    import requests as _requests
    _HAS_OLLAMA_LIB = False


class OllamaClient:
    """Generic interface to a locally running Ollama model.

    Parameters
    ----------
    model : str
        The Ollama model name to use (e.g. "llama3", "mistral").
    base_url : str
        Base URL of the Ollama REST API (default: http://localhost:11434/api).
    system_prompt : str | None
        Optional system-level instruction prepended to every conversation.
    """

    def __init__(
        self,
        model: str = "llama3",
        base_url: str = "http://localhost:11434/api",
        system_prompt: str | None = None,
    ):
        self.model = model
        self.base_url = base_url
        self.system_prompt = system_prompt

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def chat(self, prompt: str, *, json_mode: bool = False) -> str:
        """Send a single prompt and return the model's reply as a string.

        Parameters
        ----------
        prompt : str
            The user message to send.
        json_mode : bool
            When True, ask Ollama to return valid JSON (sets format="json").

        Returns
        -------
        str
            The raw text response from the model.

        Raises
        ------
        RuntimeError
            If the request fails or the model returns an empty response.
        """
        full_prompt = self._build_prompt(prompt)
        fmt = "json" if json_mode else None

        if _HAS_OLLAMA_LIB:
            return self._call_library(full_prompt, fmt)
        return self._call_requests(full_prompt, fmt)

    def chat_json(self, prompt: str) -> dict | list:
        """Send a prompt and parse the response as JSON.

        Parameters
        ----------
        prompt : str
            The user message to send.

        Returns
        -------
        dict | list
            Parsed JSON object returned by the model.

        Raises
        ------
        ValueError
            If the response cannot be parsed as JSON.
        RuntimeError
            If the underlying request fails.
        """
        raw = self.chat(prompt, json_mode=True)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Model did not return valid JSON.\nRaw response:\n{raw}") from exc

    def list_models(self) -> list[str]:
        """Return the names of all models available in the local Ollama instance.

        Returns
        -------
        list[str]
            Model name strings (e.g. ["llama3:latest", "mistral:latest"]).
        """
        if _HAS_OLLAMA_LIB:
            result = _ollama_lib.list()
            return [m["name"] for m in result.get("models", [])]

        resp = _requests.get(f"{self.base_url}/tags")
        resp.raise_for_status()
        return [m["name"] for m in resp.json().get("models", [])]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_prompt(self, user_prompt: str) -> str:
        if self.system_prompt:
            return f"{self.system_prompt}\n\n{user_prompt}"
        return user_prompt

    def _call_library(self, prompt: str, fmt: str | None) -> str:
        kwargs = {"model": self.model, "prompt": prompt}
        if fmt:
            kwargs["format"] = fmt
        try:
            response = _ollama_lib.generate(**kwargs)
            text = response.get("response", "").strip()
        except Exception as exc:
            raise RuntimeError(f"ollama library error: {exc}") from exc
        if not text:
            raise RuntimeError("Ollama returned an empty response.")
        return text

    def _call_requests(self, prompt: str, fmt: str | None) -> str:
        payload: dict = {"model": self.model, "prompt": prompt, "stream": False}
        if fmt:
            payload["format"] = fmt
        try:
            resp = _requests.post(f"{self.base_url}/generate", json=payload)
            resp.raise_for_status()
            text = resp.json().get("response", "").strip()
        except Exception as exc:
            raise RuntimeError(f"HTTP request to Ollama failed: {exc}") from exc
        if not text:
            raise RuntimeError("Ollama returned an empty response.")
        return text
