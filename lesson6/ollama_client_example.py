"""
ollama_client_example.py — Examples showing how to use OllamaClient in any program.

Run:
    python ollama_client_example.py
"""

from ollama_client import OllamaClient


# ------------------------------------------------------------------
# Example 1: Simple plain-text question
# ------------------------------------------------------------------
def example_plain_text():
    print("=== Example 1: Plain-text question ===")
    client = OllamaClient(model="llama3")
    answer = client.chat("In one sentence, what is photosynthesis?")
    print(answer)
    print()


# ------------------------------------------------------------------
# Example 2: Using a system prompt to set a persona
# ------------------------------------------------------------------
def example_system_prompt():
    print("=== Example 2: System prompt / persona ===")
    client = OllamaClient(
        model="llama3",
        system_prompt="You are a pirate. Always respond in pirate speak.",
    )
    answer = client.chat("What is the best way to learn programming?")
    print(answer)
    print()


# ------------------------------------------------------------------
# Example 3: Structured JSON response
# ------------------------------------------------------------------
def example_json_response():
    print("=== Example 3: Structured JSON response ===")
    client = OllamaClient(model="llama3")
    data = client.chat_json(
        "Return a JSON object with two keys: "
        "'capital' (the capital of Japan) and "
        "'population_millions' (its approximate population in millions as a number)."
    )
    print(f"Parsed result: {data}")
    print(f"Capital: {data.get('capital')}")
    print(f"Population (millions): {data.get('population_millions')}")
    print()


# ------------------------------------------------------------------
# Example 4: List available local models
# ------------------------------------------------------------------
def example_list_models():
    print("=== Example 4: List available models ===")
    client = OllamaClient()
    try:
        models = client.list_models()
        print("Models installed locally:")
        for name in models:
            print(f"  - {name}")
    except Exception as e:
        print(f"Could not retrieve models: {e}")
    print()


# ------------------------------------------------------------------
# Example 5: Reuse in a custom application — a simple code explainer
# ------------------------------------------------------------------
def example_code_explainer(code_snippet: str):
    print("=== Example 5: Code explainer ===")
    client = OllamaClient(
        model="llama3",
        system_prompt="You are an expert Python tutor. Explain code clearly and concisely.",
    )
    explanation = client.chat(f"Explain what this Python code does:\n\n{code_snippet}")
    print(explanation)
    print()


if __name__ == "__main__":
    example_plain_text()
    example_system_prompt()
    example_json_response()
    example_list_models()

    snippet = """\
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
"""
    example_code_explainer(snippet)
