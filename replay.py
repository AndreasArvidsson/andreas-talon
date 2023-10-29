# mimic("focus code"); actions.sleep(1); actions.speech.replay("/path/to/recording.flac")

from talon import actions, speech_system
from os import walk, path
import json
import re

delimiter = ","
expected = {}
accepted = 0
match_expected = 0
res = ""
filename = ""


def store_results():
    out_file = path.join(actions.path.user_home(), "Downloads", "replay.csv")
    with open(out_file, "a", encoding="utf-8") as f:
        f.write(res)


def read_expected(dir):
    expected_file = path.join(dir, "expected.json")
    try:
        with open(expected_file, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def get_spoken_phrase_from_file_name(filename: str) -> str:
    if re.match(r"^\d+-", filename):
        return filename.split("-")[1]
    return filename.split("-")[0]


def on_pre_phrase(phrase):
    global accepted, match_expected, res
    spoken = " ".join(phrase["phrase"])
    if spoken:
        accepted += 1
    else:
        spoken = "[REJECTED]"

    if expected:
        if filename not in expected:
            print("--- MISSING EXPECTED: {filename}")
        else:
            ext = expected[filename]
            res += f"{ext}{delimiter}"
            if ext == spoken:
                match_expected += 1
            else:
                res += spoken
    else:
        res += spoken

    phrase["phrase"] = []
    if "parsed" in phrase:
        phrase["parsed"]._sequence = []


def replay_files(files):
    global res, filename
    speech_system.register("pre:phrase", on_pre_phrase)
    res += f"Filename{delimiter}Original{delimiter}"
    if expected:
        res += f"Expected{delimiter}"
    res += f"{speech_system.engine.engine}\n"

    for file in files:
        filename = path.basename(file)[:-5]
        # print(f'"{filename}": "",')
        phrase = get_spoken_phrase_from_file_name(filename)
        res += f"{filename}{delimiter}{phrase}{delimiter}"
        actions.speech.replay(file)
        res += "\n"

    res += f"> Accepted {accepted} / {len(files)}\n"
    if expected:
        res += f"> Expected {match_expected} / {len(files)}\n"
    res += "\n"
    store_results()
    print(f"Accepted {accepted} / {len(files)}\n")
    print(f"Expected {match_expected} / {len(files)}\n")

    speech_system.unregister("pre:phrase", on_pre_phrase)


def replay_dir(dir):
    global expected
    expected = read_expected(dir)
    for dirpath, dirnames, filenames in walk(dir):
        filenames = [path.join(dirpath, f) for f in filenames if f.endswith(".flac")]
        replay_files(filenames)


# replay_dir("C:\\Users\\andre\\AppData\\Roaming\\talon\\rejects\\rejected with speech")
# replay_dir("C:\\Users\\andre\\AppData\\Roaming\\talon\\rejects\\rejected only noises")
# replay_dir("C:\\Users\\andre\\AppData\\Roaming\\talon\\recordings d problems")

# replay_files(
#     [
#         "C:\\Users\\andre\AppData\\Roaming\\talon\\recordings d problems\\gust-8jKb5cdq.flac"
#     ]
# )

# Rejected with speech (-604)
# b108: 202 / 202
# D-20: 64 / 202

# Rejected only noises (-604)
# b108: 71 / 500
# D-20: 1 / 500

# Problems (-604)
# b108: 73 / 104
# D-20: 64 / 104


# Rejected with speech (-596)
# b108: 202 / 202
# D-28: 33 / 202
# D-19: 63 / 202
# D-11: 109 / 202
# D-06: 109 / 202

# Rejected only noises (-596)
# b108: 71 / 500
# D-28: 1 / 500
# D-19: 1 / 500
# D-11: 4 / 500
# D-06: 4 / 500

# Problems (-596)
# b108: 70 / 79
# D-28: 21 / 79
# D-19: 46 / 79
# D-11: 43 / 79
# D-06: 43 / 79

# Rejected with speech (attempted hotfix)
# b108: 198 / 202
# D-28: 162 / 202
# D-19: 184 / 202
# D-11: 178 / 202
# D-06: 178 / 202

# Rejected only noises (attempted hotfix)
# b108: 23 / 500
# D-28: 8 / 500
# D-19: 10 / 500
# D-11: 8 / 500
# D-06: 8 / 500

# Problems (attempted hotfix)
# b108: 56 / 79
# D-28: 30 / 79
# D-19: 42 / 79
# D-11: 40 / 79
# D-06: 40 / 79
