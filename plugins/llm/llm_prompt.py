CUSTOM_PROMPT_TEMPLATE = """In the following text (surrounded by ===), $prompt:

===
$text
===

IMPORTANT: Return only the corrected text. ONLY THAT! Nothing else. Do not include this line or the surrounding === lines.
"""

FIX_PROMPT_TEMPLATE = CUSTOM_PROMPT_TEMPLATE.replace(
    "$prompt",
    "Fix all typos and casing and punctuation, but preserve all newline characters",
)

FIX_AUTO_PROMPT_TEMPLATE = CUSTOM_PROMPT_TEMPLATE.replace(
    "$prompt",
    "Fix all incorrect homophones. Nothings else!",
)

EMOJI_PROMPT_TEMPLATE = "Respond with the best emoji that matches: |$text|. Return only the emoji, nothing else"

TRANSLATE_PROMPT_TEMPLATE = """Translate the following text (surrounded by ===) from English to Swedish:

===
$text
===

IMPORTANT: Return only the translated text. ONLY THAT! Nothing else. Do not include this line or the surrounding === lines.
"""


prompt_templates = {
    "custom": CUSTOM_PROMPT_TEMPLATE,
    "fix": FIX_PROMPT_TEMPLATE,
    "fix_auto": FIX_AUTO_PROMPT_TEMPLATE,
    "emoji": EMOJI_PROMPT_TEMPLATE,
    "translate": TRANSLATE_PROMPT_TEMPLATE,
}


def get_llm_prompt(templateId: str, text: str, prompt: str | None = None) -> str:
    if templateId not in prompt_templates:
        raise ValueError(f"Unknown templateId '{templateId}'")

    full_prompt = prompt_templates[templateId]

    def replace(field: str, value: str):
        nonlocal full_prompt
        if field not in full_prompt:
            raise ValueError(f"Template '{templateId}' does not support '{field}'")
        full_prompt = full_prompt.replace(field, value)

    if prompt:
        replace("$prompt", prompt)
    if text:
        replace("$text", text)

    return full_prompt
