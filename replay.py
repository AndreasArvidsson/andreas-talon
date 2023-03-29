# mimic("focus code"); actions.sleep(1); actions.speech.replay("/path/to/recording.flac")

from talon import actions, speech_system
from os import walk, path


def on_phrase(phrase):
    spoken = " ".join(phrase["phrase"])
    print(f"    {spoken}")
    phrase["phrase"] = []
    phrase["parsed"]._sequence = []


def replay_files(filenames):
    speech_system.register("pre:phrase", on_phrase)

    print("----------------------------")
    print("hybrid-d".ljust(30), end="")
    print("conformer-b")

    for file in filenames:
        phrase = path.basename(file).split("-")[0]
        # print(file)
        print(phrase.ljust(30), end="")
        actions.speech.replay(file)

    speech_system.unregister("pre:phrase", on_phrase)


def replay_dir(dir):
    for dirpath, dirnames, filenames in walk(dir):
        replay_files([path.join(dirpath, f) for f in filenames])


# replay_dir("C:\\Users\\andre\AppData\\Roaming\\talon\\recordings d problems")

# replay_files(
#     [
#         "C:\\Users\\andre\AppData\\Roaming\\talon\\recordings d problems\\gust-8jKb5cdq.flac"
#     ]
# )

# 2023-03-21 17:24:46    IO ----------------------------
# 2023-03-21 17:24:46    IO hybrid -d                         conformer-b
# 2023-03-21 17:24:46    IO air                               arrow
# 2023-03-21 17:24:46    IO bring id then bang fine           bring item pink fine
# 2023-03-21 17:24:46    IO cap                               clippy
# 2023-03-21 17:24:46    IO clear core                        clear core
# 2023-03-21 17:24:46    IO deli                              deli two
# 2023-03-21 17:24:46    IO dot                               one
# 2023-03-21 17:24:46    IO dotted file                       git add file
# 2023-03-21 17:24:46    IO enter                             righter
# 2023-03-21 17:24:46    IO enter                             righter
# 2023-03-21 17:24:46    IO gust                              jest
# 2023-03-21 17:24:46    IO ink two dot                       ink two dot
# 2023-03-21 17:24:46    IO jig one pit pit                   jig urn pit pit
# 2023-03-21 17:24:46    IO leap it                           pipe
# 2023-03-21 17:24:46    IO pit                               dot
# 2023-03-21 17:24:46    IO pit                               dot
# 2023-03-21 17:24:46    IO round                             round
# 2023-03-21 17:24:46    IO sam word rejection                say word rejection
# 2023-03-21 17:24:46    IO say that tip                      say that tip
# 2023-03-21 17:24:47    IO snake red image                   snake read image
# 2023-03-21 17:24:47    IO string that up                    say in that tip
# 2023-03-21 17:24:47    IO three                             troll
# 2023-03-21 17:24:47    IO twin                              drill
# 2023-03-21 17:24:47    IO wipe                              righter
# 2023-03-21 17:24:47    IO wipe                              righter
# 2023-03-21 17:24:47    IO word green dot                    word green dot

# 2023-03-29 07:43:25    IO ----------------------------
# 2023-03-29 07:43:25    IO hybrid -d                         hybrid -d, new acoustic file
# 2023-03-29 07:43:25    IO air                               air
# 2023-03-29 07:43:25    IO bring id then bang fine           bring id then bang fine
# 2023-03-29 07:43:26    IO cap                               cap
# 2023-03-29 07:43:26    IO clear core                        clear core
# 2023-03-29 07:43:26    IO deli                              deli two
# 2023-03-29 07:43:26    IO dot                               dot
# 2023-03-29 07:43:26    IO dotted file                       git add file
# 2023-03-29 07:43:26    IO enter                             righter
# 2023-03-29 07:43:26    IO enter                             righter
# 2023-03-29 07:43:26    IO gust                              jest
# 2023-03-29 07:43:26    IO ink two dot                       ink two dot
# 2023-03-29 07:43:27    IO jig one pit pit                   jig one pit pit
# 2023-03-29 07:43:27    IO leap it                           leap it
# 2023-03-29 07:43:27    IO pit                               pit
# 2023-03-29 07:43:27    IO pit                               batt
# 2023-03-29 07:43:27    IO round                             round
# 2023-03-29 07:43:27    IO sam word rejection                say word rejection
# 2023-03-29 07:43:27    IO say that tip                      say that tip
# 2023-03-29 07:43:27    IO snake red image                   snake read image
# 2023-03-29 07:43:27    IO string that up                    say that up
# 2023-03-29 07:43:27    IO three                             troll
# 2023-03-29 07:43:28    IO twin                              twin
# 2023-03-29 07:43:28    IO wipe                              righter
# 2023-03-29 07:43:28    IO wipe                              righter
# 2023-03-29 07:43:28    IO word green dot                    word green dot
