```py
from talon import speech_system, actions

def on_phrase(phrase):
    analyzed_phrase = actions.user.analyze_phrase(phrase)
    analyzed_phrase = actions.user.calc_analyzed_phrase_with_actions(analyzed_phrase)
    actions.user.pretty_print_phrase(analyzed_phrase)

speech_system.register("phrase", on_phrase)
```

```json
AnalyzedPhraseWithActions({
  phrase: "test air batt five",
  words: [
    AnalyzedWord({
      text: "test",
      start: 11309.37369797144,
      end: 11309.614126542867,
    }),
    AnalyzedWord({
      text: "air",
      start: 11309.667555114296,
      end: 11309.827840828582,
    }),
    AnalyzedWord({
      text: "batt",
      start: 11309.88126940001,
      end: 11310.06826940001,
    }),
    AnalyzedWord({
      text: "five",
      start: 11310.121697971439,
      end: 11310.468983685725,
    }),
  ],
  rawSim:
    '[1] "test air batt five"\n   path: user\\andreas-talon\\misc\\editor.talon\n   rule: "test [<user.letter>] <user.letter> <number_small>"',
  commands: [
    AnalyzedCommandWithActions({
      num: 1,
      phrase: "test air batt five",
      path: "user\\andreas-talon\\misc\\editor.talon",
      rule: "test [<user.letter>] <user.letter> <number_small>",
      code: 'print("{letter_1} {letter_2} {number_small}")\n# skip()',
      line: 84,
      captures: [
        AnalyzedCapture({ phrase: "test", name: "test", value: "test" }),
        AnalyzedCapture({ phrase: "air", name: "user.letter", value: "a" }),
        AnalyzedCapture({ phrase: "batt", name: "user.letter", value: "b" }),
        AnalyzedCapture({ phrase: "five", name: "number_small", value: 5 }),
      ],
      captureMapping: { letter: ["a", "b"], number_small: [5] },
      actions: [
        AnalyzedAction({
          code: 'print("{letter_1} {letter_2} {number_small}")',
          name: "print",
          params: '"{letter_1} {letter_2} {number_small}"',
          path: "main",
          modDesc: "Display an object in the log",
          ctxDesc: "Display an object in the log",
          explanation: "Log text 'a b 5'",
        }),
      ],
    }),
  ],
});
```
