"""
Central AI model registry.

Changing a model name here updates the entire application.
Every service reads this file via AIFactory — never hardcode model names in services.

Available models:
  llama3.1:8b        → general language tasks, chat, fast responses
  qwen2.5-coder:7b   → code generation, evaluation, structured JSON output

Model assignments:
  CHAT_MODEL:    llama3.1:8b      — Conversational responses. No JSON mode.
  CODING_MODEL:  qwen2.5-coder:7b — Code generation, evaluation, reports.
  JSON_MODEL:    qwen2.5-coder:7b — Structured JSON output. qwen follows schemas
                                    more reliably than llama at this size.
  FAST_MODEL:    llama3.1:8b      — General-purpose, low-context tasks.
"""

CHAT_MODEL = "phi4-mini:latest"

CODING_MODEL = "qwen2.5-coder:3b"

JSON_MODEL = "qwen2.5-coder:3b"

FAST_MODEL = "llama3.2:3b"
