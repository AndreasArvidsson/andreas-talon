tag: user.ollama
-

ollama:                     "ollama "
ollama version:             "ollama -v\n"
ollama help:                "ollama -h\n"
ollama list:                "ollama list\n"
ollama ps:                  "ollama ps\n"

ollama run {user.ollama_model}:
    "ollama run {ollama_model} "
ollama run {user.ollama_model} verbose:
    "ollama run {ollama_model} --verbose "

ollama show:
    "ollama show "
ollama show {user.ollama_model}:
    "ollama show {ollama_model}\n"
