# 5. Alert Handling Workflow

The same lifecycle applies to nearly every alert.

```
  Alert received
       │
  1. Initial triage  (basic checks)
       │
  Is the analysis enough? ── no ──► 2. Advanced checks ──┐
       │ yes                                              │
       ◄──────────────────────────────────────────────────┘
       │
  False positive / duplicate / already handled?
       │ yes ─────────► Close (with proper comment, confirmation if required)
       │ no
       ▼
  Raise alert / incident
       ▼
  3. Immediate containment (isolate system, block malicious IPs)
       ▼
  4. Notify and coordinate (stakeholders, IT/IR team, vendors)
       ▼
  5. Mitigation (workarounds, patching, tighter access, segmentation)
       ▼
  6. Detailed investigation (correlate in SIEM, find attack vector, hunt for related activity)
       ▼
  7. Post-incident (document, review, update plans, improve detections)
       ▼
  8. Regular checklist (health checks, anomaly checks, update threat intel)
```

## Step 1: Initial triage checklist
- Severity (Critical / High / Medium / Low / Info)
- Source IP, destination IP, hostname, user
- Which attack stage (Kill Chain / MITRE) does it suggest?
- Quick threat-intel check on IPs, domains, hashes
- Read the message or rule text carefully. Is it what you think?

## Step 2: Advanced checks
- Port and service review
- Related logs before and after (old logs, event IDs, logon types)
- IOC / IOA matches
- Process, file path, DLL or service analysis on the endpoint
- Blacklist checks, suspicious activity, trojan-like behavior
- Back-tracking: where did this start?

## Severity levels

| Level | Means | Response |
|---|---|---|
| **Critical** | Confirmed compromise, active ransomware, data theft, privileged-account abuse | Immediate containment, declare incident, notify management |
| **High** | Strong evidence of malicious activity, impact still unclear | Rapid containment, escalate to L2/L3 |
| **Medium** | Suspicious, not confirmed | Investigate, collect evidence, escalate if it grows |
| **Low** | Weak signal or blocked attempt | Document, watch, tune if noisy |
| **Info** | Useful telemetry | No action unless correlated |

## When to escalate
- Critical or High severity
- You can't rule out compromise
- Privileged accounts, sensitive data or many systems involved
- Something is outside your approved actions
- Your gut says so. **Say so and explain why.**

## How to write a good ticket note

```
What fired:   <rule / alert name, time>
Who / what:   <user, host, IPs>
What I checked: <logs, EDR, threat intel, firewall>
What I found: <facts only>
What I did:   <actions taken, time>
Verdict:      <false positive / true positive / unsure>
Next step:    <who needs to do what>
```

## Closing an alert safely
- Always add a reason. "FP" alone is not a reason.
- Some environments require **customer/owner confirmation by email** before closing as false positive. Follow your process.
- A "false positive" that still matches fresh threat intel should be reopened and re-reviewed.

## ✅ After this page you should be able to
- Draw the workflow from memory
- Classify an alert's severity and justify it
- Write a clear ticket note
