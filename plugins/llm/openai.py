import json
import time
import os
from urllib import error, request

# powershell
# [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
# [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key-here", "User")


timeout_seconds = 10
model = "gpt-5.4-nano"
base_url = "https://api.openai.com/v1"


def openai_run(prompt: str) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("OpenAI API error: OPENAI_API_KEY is not set")
        return None

    payload = json.dumps(
        {
            "model": model,
            "input": prompt,
        }
    ).encode("utf-8")

    req = request.Request(
        f"{base_url}/responses",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        t1 = time.perf_counter()

        with request.urlopen(req, timeout=timeout_seconds) as response:
            response_text = response.read().decode("utf-8")

        t2 = time.perf_counter()

        print(f"OpenAI API returned in {t2 - t1:0.1f}s using model {model}")

        data = json.loads(response_text)

        if data.get("output_text"):
            return data["output_text"].strip()

        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") == "output_text" and content.get("text"):
                    return content["text"].strip()

        return None

    except error.HTTPError as ex:
        error_body = ex.read().decode("utf-8", errors="replace")
        print(f"OpenAI API error ({ex.code}): {error_body}")
        return None
    except error.URLError as ex:
        print(f"OpenAI API connection error: {ex}")
        return None
    except TimeoutError:
        print(f"Error processing text: OpenAI API timed out after {timeout_seconds}s")
        return None
    except Exception as ex:
        print(f"Error processing text with OpenAI API: {ex}")
        return None
