import subprocess
import time
import os


timeout_seconds = 10


def codex_run(prompt: str) -> str | None:
    if os.name == "nt":
        codex = "codex.cmd"
        # Prevent spawning a visible cmd/console window on Windows.
        creationflags = subprocess.CREATE_NO_WINDOW
    else:
        codex = "codex"
        creationflags = 0

    cmd = [
        codex,
        "exec",
        "-",
        "--skip-git-repo-check",
        "--ephemeral",
        "--color",
        "never",
        "--profile",
        "talon",
    ]

    try:
        t1 = time.perf_counter()
        result = subprocess.run(
            cmd,
            input=prompt,
            timeout=timeout_seconds,
            creationflags=creationflags,
            # Use text mode to automatically encode/decode input and output as UTF-8 strings.
            text=True,
            # Capture both stdout and stderr
            capture_output=True,
            # Do not raise exception on non-zero exit code
            check=False,
        )
        t2 = time.perf_counter()

        print(f"Codex CLI returned in {t2 - t1:0.1f}s with code {result.returncode}")

        if result.returncode != 0:
            print(f"Codex CLI error: {result.stderr}")
            return None

        if result.stdout:
            return result.stdout.strip()

        return None

    except subprocess.TimeoutExpired:
        print(f"Error processing text: Codex CLI timed out after {timeout_seconds}s")
        return None
    except Exception as ex:
        print(f"Error processing text with Codex CLI: {ex}")
        return None
