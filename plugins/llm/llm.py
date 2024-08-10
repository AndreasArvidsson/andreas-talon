# linux: `TALON_HOME/bin/pip install ollama`
# win:   `TALON_HOME/venv/3.11/Scripts/pip.bat install ollama`
# https://github.com/ollama/ollama-python
# https://github.com/ollama/ollama/blob/main/docs/api.md

from typing import Optional
from talon import Module, actions
from .llm_prompt import get_llm_prompt
from .ollama import ollama_generate_get, ollama_generate_insert_streaming

mod = Module()


@mod.action_class
class Action:
    def model_process_selected_text(templateId: str, prompt: Optional[str] = None):
        """Model process selected text and replace with result"""
        text = actions.edit.selected_text()
        actions.user.model_insert_processed_text(templateId, text, prompt)

    def model_insert_processed_text(
        templateId: str,
        text: str,
        prompt: Optional[str] = None,
    ):
        """Model process text and insert result"""
        full_prompt = get_llm_prompt(templateId, text, prompt)
        actions.user.model_insert_processed_prompt(full_prompt)

    def model_insert_processed_prompt(prompt: str):
        """Model process prompt and insert result"""
        result = actions.user.model_process_prompt(prompt)
        if result is not None:
            actions.insert(result)

    def model_insert_processed_prompt_streaming(prompt: str):
        """Model process prompt and insert result using streaming"""
        ollama_generate_insert_streaming(prompt)

    def model_process_text(
        templateId: str, text: str, prompt: str = ""
    ) -> Optional[str]:
        """Model process text"""
        full_prompt = get_llm_prompt(templateId, text, prompt)
        return ollama_generate_get(full_prompt)

    def model_process_prompt(prompt: str) -> Optional[str]:
        """Model process prompt"""
        return ollama_generate_get(prompt)
