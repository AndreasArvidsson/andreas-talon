# linux: `TALON_HOME/bin/pip install ollama`
# win:   `TALON_HOME/venv/3.11/Scripts/pip.bat install ollama`

# https://github.com/ollama/ollama-python
# https://github.com/ollama/ollama/blob/main/docs/api.md

import time
import ollama
from talon import actions


OLLAMA_MODEL = "gemma2:2b"
OLLAMA_KEEP_ALIVE = -1


def ollama_generate_get(prompt: str) -> str | None:
    try:
        t1 = time.perf_counter()

        response = ollama.generate(
            model=OLLAMA_MODEL,
            keep_alive=OLLAMA_KEEP_ALIVE,
            prompt=prompt,
        )

        t2 = time.perf_counter()
        actions.user.debug(
            f"Ollama model '{OLLAMA_MODEL}' returned processed text in {t2-t1:0.1f}s"
        )

        processed_text = response["response"].strip()

        return processed_text
    except Exception as e:
        print(f"Error processing text: {e}")
        return None


def ollama_generate_insert_streaming(prompt: str) -> None:
    try:
        t1 = time.perf_counter()

        stream = ollama.generate(
            model=OLLAMA_MODEL,
            keep_alive=OLLAMA_KEEP_ALIVE,
            stream=True,
            prompt=prompt,
        )
        for chunk in stream:
            actions.insert(chunk["response"])

            if chunk["done"]:
                t2 = time.perf_counter()
                actions.user.debug(
                    f"Ollama model '{OLLAMA_MODEL}' processed streaming text in {t2-t1:0.1f}s"
                )

    except Exception as e:
        print(f"Error processing text: {e}")
