# mimic("focus code"); actions.sleep(1); actions.speech.replay("/path/to/recording.flac")

from talon import actions, speech_system
from os import walk, path

accepted = 0


def on_phrase(phrase):
    global accepted
    accepted += 1
    spoken = " ".join(phrase["phrase"])
    print(f"    {spoken}", end="")
    phrase["phrase"] = []
    if "parsed" in phrase:
        phrase["parsed"]._sequence = []


def replay_files(filenames):
    speech_system.register("pre:phrase", on_phrase)

    print("----------------------------")
    print("hybrid-d".ljust(30), end="")
    print("conformer-b")

    for file in filenames:
        # print(file)
        phrase = path.basename(file).split("-")[0]
        # phrase = path.basename(file).split("-")[1]
        print(phrase.ljust(30), end="")
        actions.speech.replay(file)
        print()

    print(f"Accepted {accepted} / {len(filenames)}")

    speech_system.unregister("pre:phrase", on_phrase)


def replay_dir(dir):
    for dirpath, dirnames, filenames in walk(dir):
        replay_files([path.join(dirpath, f) for f in filenames])


# replay_dir("C:\\Users\\andre\\AppData\\Roaming\\talon\\rejects\\rejected only noises") # 23 / 236
# replay_dir("C:\\Users\\andre\\AppData\\Roaming\\talon\\rejects\\rejected with speech") 80 / 82
# replay_dir("C:\\Users\\andre\AppData\\Roaming\\talon\\recordings d problems")

# replay_files(
#     [
#         "C:\\Users\\andre\AppData\\Roaming\\talon\\recordings d problems\\gust-8jKb5cdq.flac"
#     ]
# )
