from typing import Optional
import ollama
import time
from talon import Module, actions

OLLAMA_MODEL = "gemma2:2b"

mod = Module()

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
        updated_text = actions.user.model_process_text(templateId, text, prompt)
        actions.insert(updated_text)

    def model_process_text(templateId: str, text: str, prompt: Optional[str] = None):
        """Model process text"""
        full_prompt = prompt_templates[templateId]
        if prompt:
            full_prompt = full_prompt.replace("$prompt", prompt)
        if text:
            full_prompt = full_prompt.replace("$text", text)
        return actions.user.model_process_prompt(full_prompt)

    def model_process_prompt(prompt: str):
        """Model process prompt"""
        try:
            t1 = time.perf_counter()
            response = ollama.generate(
                model=OLLAMA_MODEL,
                prompt=prompt,
                keep_alive="24h",
            )
            t2 = time.perf_counter()
            processed_text = response["response"].strip()
            print(f"Time taken: {t2-t1:0.1f}s")
            print(f"Using prompt:\n{prompt}\n...")
            print(f"Model returned processed text:\n{processed_text}\n...")
            return processed_text
        except Exception as e:
            print(f"Error processing text: {e}")
            return None
