```py
from talon import speech_system, actions

def on_phrase(phrase):
    analyzed_phrase = actions.user.analyze_phrase(phrase)
    analyzed_phrase = actions.user.calc_analyzed_phrase_with_actions(analyzed_phrase)
    actions.user.pretty_print_phrase(analyzed_phrase)

speech_system.register("phrase", on_phrase)
```

```js
AnalyzedPhraseWithActions({
  phrase: "test air batt five",
  words: [
    AnalyzedWord({
      text: "test",
      start: 29000.987656018176,
      end: 29001.226292381816,
    }),
    AnalyzedWord({
      text: "air",
      start: 29001.279322684844,
      end: 29001.438413593936,
    }),
    AnalyzedWord({
      text: "batt",
      start: 29001.464928745452,
      end: 29001.677049957572,
    }),
    AnalyzedWord({
      text: "five",
      start: 29001.70356510909,
      end: 29002.18083783636,
    }),
  ],
  rawSim:
    '[1] "test air batt five"\n   path: user\\andreas-talon\\misc\\editor.talon\n   rule: "test [<user.letter>] <user.letter> <number_small>"',
  commands: [
    AnalyzedCommandWithActions({
      num: 1,
      phrase: "test air batt five",
      rule: "test [<user.letter>] <user.letter> <number_small>",
      code: 'print("{letter_1} {letter_2} {number_small}")\n',
      path: "user\\andreas-talon\\misc\\editor.talon",
      line: 84,
      captures: [
        AnalyzedCapture({ phrase: "test", value: "test", name: None }),
        AnalyzedCapture({ phrase: "air", value: "a", name: "user.letter" }),
        AnalyzedCapture({ phrase: "batt", value: "b", name: "user.letter" }),
        AnalyzedCapture({ phrase: "five", value: 5, name: "number_small" }),
      ],
      captureMapping: { letter: ["a", "b"], number_small: [5] },
      actions: [
        AnalyzedAction({
          code: 'print("{letter_1} {letter_2} {number_small}")',
          name: "print",
          params: '"{letter_1} {letter_2} {number_small}"',
          path: "main",
          line: None,
          modDesc: "Display an object in the log",
          ctxDesc: "Display an object in the log",
          explanation: "Log text 'a b 5'",
        }),
      ],
    }),
  ],
});
```
