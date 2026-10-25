# Progress Card Template (for AI tutors)

Use this exact layout so learners always know where they stand.

## After every gate attempt (mini line)

```
📍 <Section title>: <correct>/<total> (<percent>%)  ·  pass mark 80%  ·  <PASSED ✅ | NOT YET 🔁>  ·  hints used: <n>
```

## After every passed section (full card)

```
════════ SOC-CAREER-LAUNCHPAD · PROGRESS CARD ════════
Learner: <name>        Goal: <goal>        Level: <Starting out | Explorer | Builder | Defender | SOC-Ready>
Record: <VERIFIED | NOT YET VERIFIED (no tool access) >

Progress: [██████░░░░░░░░░░] <n> of <total> gated sections (<pct>%)

 ✅ Start Here ................. best 100%  (2 attempts)
 ✅ Networking ................. best 100%  (1 attempt)
 ▶  Linux basics ............... UP NEXT
 🔒 Security fundamentals ...... locked
 ...

Strong: <sections passed first try>
Review again: <objectives missed>
Notes written: <n> in learner/notes/
Next step: <section title>   ·   Gate rule: 80%+ to unlock the next section
══════════════════════════════════════════════════════
```

## Final scorecard (all gated sections passed)

```
🎓 FINAL SCORECARD
Overall: <average best score>%   Attempts: <total attempts>   Sections: <total>/<total>
Top 3 strengths: ...
Top 3 areas to keep practising: ...
Suggested next steps:
  1. Do the 8-week plan labs (docs/08-study-plan-8-weeks.md)
  2. Practise interview questions out loud (docs/10-interview-questions.md)
  3. Build a small portfolio piece (e.g. a phishing analysis write-up with defanged indicators)
Reminder: this card shows your learning journey. It is not a certificate or a job guarantee.
```

If you have shell access, `python scripts/checkpoint.py --card` also generates `learner/progress-card.png` and `.md`.
