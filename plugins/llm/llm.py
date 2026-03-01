from typing import Optional
from talon import Module, actions

from .codex_cli import codex_run
from .llm_prompt import get_llm_prompt

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
        if result:
            actions.insert(result)

    def model_process_text(
        templateId: str,
        text: str,
        prompt: Optional[str] = None,
    ) -> Optional[str]:
        """Model process text"""
        full_prompt = get_llm_prompt(templateId, text, prompt)
        return codex_run(full_prompt)

    def model_process_prompt(prompt: str) -> Optional[str]:
        """Model process prompt"""
        return codex_run(prompt)
