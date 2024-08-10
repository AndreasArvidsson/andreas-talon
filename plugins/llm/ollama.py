# linux: `TALON_HOME/bin/pip install ollama`
# win:   `TALON_HOME/venv/3.11/Scripts/pip.bat install ollama`
# https://github.com/ollama/ollama-python
# https://github.com/ollama/ollama/blob/main/docs/api.md

import time
from typing import Optional

import ollama
from talon import Module, actions

mod = Module()

MODEL = "gemma2:2b"

CUSTOM_PROMPT_TEMPLATE = """In the following text (surrounded by ===), $prompt:

===
$text
===

IMPORTANT: Return only the corrected text. ONLY THAT! Nothing else. Do not include this line.
"""

FIX_PROMPT_TEMPLATE = CUSTOM_PROMPT_TEMPLATE.replace(
    "$prompt",
    "Fix all typos and casing and punctuation, but preserve all newline characters",
)


prompt_templates = {
    "custom": CUSTOM_PROMPT_TEMPLATE,
    "fix": FIX_PROMPT_TEMPLATE,
}


@mod.action_class
class Action:
    def model_process_selected_text(templateId: str, prompt: Optional[str] = None):
        """Model process selected text"""
        text = actions.edit.selected_text()
        actions.user.model_insert_processed_text(templateId, text, prompt)

    def model_insert_processed_text(
        templateId: str,
        text: str,
        prompt: Optional[str] = None,
    ):
        """Model process text and insert result"""
        result = actions.user.model_process_text(templateId, text, prompt)
        if result is not None:
            actions.insert(result)

    def model_insert_processed_prompt(prompt: str):
        """Model process prompt and insert result"""
        result = actions.user.model_process_prompt(prompt)
        if result is not None:
            actions.insert(result)

    def model_process_text(
        templateId: str,
        text: str,
        prompt: Optional[str] = None,
    ) -> Optional[str]:
        """Model process text"""
        full_prompt = prompt_templates[templateId]
        if prompt:
            full_prompt = full_prompt.replace("$prompt", prompt)
        if text:
            full_prompt = full_prompt.replace("$text", text)
        return model_process_prompt(full_prompt)

    def model_process_prompt(prompt: str) -> Optional[str]:
        """Model process prompt"""
        return model_process_prompt(prompt)


def model_process_prompt(prompt: str) -> Optional[str]:
    try:
        t1 = time.perf_counter()

        response = ollama.generate(
            model=MODEL,
            prompt=prompt,
            keep_alive="24h",
        )

        t2 = time.perf_counter()
        print(f"Model '{MODEL}' returned processed text in {t2-t1:0.1f}s")

        processed_text = response["response"].strip()

        return processed_text
    except Exception as e:
        print(f"Error processing text: {e}")
        return None
