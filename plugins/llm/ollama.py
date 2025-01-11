# linux: `TALON_HOME/bin/pip install ollama`
# win:   `TALON_HOME/venv/3.11/Scripts/pip.bat install ollama`

# https://github.com/ollama/ollama-python
# https://github.com/ollama/ollama/blob/main/docs/api.md

import time
from typing import Any, Mapping
from talon import actions
from .StringBuilder import StringBuilder

try:
    import ollama
except Exception as ex:
    # print(f"ERROR: {ex}")
    pass


OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_KEEP_ALIVE = -1


def ollama_generate_get(prompt: str) -> str | None:
    try:
        t1 = time.perf_counter()

        response = ollama.generate(
            model=OLLAMA_MODEL,
            keep_alive=OLLAMA_KEEP_ALIVE,
            prompt=prompt,
        )
        processed_text = response["response"].strip()

        t2 = time.perf_counter()
        actions.user.debug(
            f"Ollama model '{OLLAMA_MODEL}' returned processed text in {t2-t1:0.1f}s"
        )
        # print_verbose(response)

        return processed_text
    except Exception as e:
        print(f"Error processing text: {e}")
        return None


def ollama_generate_insert_streaming(prompt: str) -> None:
    try:
        t1 = time.perf_counter()
        string_builder = StringBuilder()

        stream = ollama.generate(
            model=OLLAMA_MODEL,
            keep_alive=OLLAMA_KEEP_ALIVE,
            stream=True,
            prompt=prompt,
        )

        for chunk in stream:
            response = chunk["response"]
            string_builder.append(response)

            if chunk["done"]:
                if not string_builder.is_empty():
                    actions.insert(string_builder.to_string())

                t2 = time.perf_counter()
                actions.user.debug(
                    f"Ollama model '{OLLAMA_MODEL}' processed streaming text in {t2-t1:0.1f}s"
                )
                print_verbose(chunk)

            elif string_builder.size() > 25:
                actions.insert(string_builder.to_string())
                string_builder.clear()

    except Exception as e:
        print(f"Error processing text: {e}")


def print_verbose(response: Mapping[str, Any]) -> None:
    print_pair("total duration", convert_time(response["total_duration"]))
    print_pair("load duration", convert_time(response["load_duration"]))
    print_pair("prompt eval count", response["prompt_eval_count"], "token(s)")
    print_pair("prompt eval duration", convert_time(response["prompt_eval_duration"]))
    print_pair(
        "prompt eval rate",
        convert_eval_rate(
            response["prompt_eval_count"], response["prompt_eval_duration"]
        ),
    )
    print_pair("eval count", response["eval_count"], "token(s)")
    print_pair("eval duration", convert_time(response["eval_duration"]))
    print_pair(
        "eval rate",
        convert_eval_rate(response["eval_count"], response["eval_duration"]),
    )


def convert_time(duration_ns: int) -> str:
    duration_ms = duration_ns / 1e6
    if duration_ms < 1000:
        return f"{duration_ms:.4f}ms"
    return f"{duration_ms/1000:.4f}s"


def convert_eval_rate(count: int, duration: int) -> str:
    return f"{count / duration*1e9:.2f} token/s"


def print_pair(key: str, value: Any, suffix="") -> None:
    key += ":"
    print(f"{key.ljust(21)} {value} {suffix}")
