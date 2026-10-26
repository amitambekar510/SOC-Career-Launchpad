# Roles: Intern, L1, and what comes next

## The ladder

| Level | In plain words | Typical work |
|---|---|---|
| **SOC Intern / Trainee** | Learning by shadowing | Watch dashboards, read alerts with a mentor, practice searches, write notes, ask lots of questions |
| **L1 Analyst** | First responder | Triage every incoming alert, do basic checks, decide false positive vs real, contain with approved actions, escalate with clear notes |
| **L2 Analyst** | Investigator | Deep dives, correlate across tools, confirm scope, lead containment, tune noisy detections |
| **L3 / Threat Hunter / IR** | Expert | Hunt for hidden attackers, malware analysis, forensics, build new detections, lead major incidents |
| **SOC Manager** | Runs the team | People, process, reporting, client/management communication |

Titles and exact duties vary between companies. Always read your own team's escalation matrix.

## What an Intern does

- Learns the tools in a safe, supervised way
- Watches live alerts alongside L1/L2 and asks "why did this fire?"
- Practices reading logs and writing simple searches
- Drafts ticket notes for review
- Does **not** close serious alerts alone or take disruptive actions without approval

## What an L1 Analyst does

1. **Watches the queue**, because alerts arrive all day and night.
2. **Triage:** quick checks. Who is the user? Which machine? What time? Known-bad IP? Does this match normal behavior?
3. **Decide:**
   - *False positive / duplicate / already handled* → close with a clear comment
   - *Looks real or unsure* → raise it and escalate
4. **First containment** (only what you're authorised to do), for example isolating a laptop through EDR or blocking a clearly malicious IP.
5. **Document everything** so the next person doesn't repeat your work.
6. **Hand over** cleanly at shift change.

## The golden rules for new analysts

- **When unsure, escalate.** Nobody is ever blamed for a well-documented "I'm not sure". People are blamed for silent guesses.
- **Never delete or "clean up" evidence.** Preserve it.
- **Don't power off an infected machine** unless told to. Memory holds clues. Isolate it from the network instead.
- **Stay inside your authority.** Know what you may block, isolate or reset, and what needs approval.
- **Be factual.** "User X logged in from two countries 5 minutes apart" is a finding. "User X is hacked" is a guess.
- **Write notes a stranger could follow.**

## Skills that matter (beyond tools)

| Skill | Why it matters |
|---|---|
| Curiosity | Alerts are puzzles. The best analysts keep asking "why?" |
| Attention to detail | A single wrong digit in an IP changes the whole story |
| Clear writing | Your ticket is your proof of work |
| Calm under pressure | Real incidents are stressful. Process beats panic |
| Teamwork | You will lean on L2/L3 and they on you |
| Honesty | Admit mistakes early. It is always cheaper |

## After this page you should be able to
- Describe the difference between Intern, L1 and L2
- List 3 things an L1 should always do and 3 things they should never do alone
