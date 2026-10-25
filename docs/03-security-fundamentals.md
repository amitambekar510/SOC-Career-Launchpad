# 3. Security Fundamentals

The core ideas behind almost every alert and every decision in a SOC.

## 3.1 The CIA triad: what are we protecting?

| Letter | Meaning | Example of failure |
|---|---|---|
| **C**onfidentiality | Only the right people can see it | Customer data leaked |
| **I**ntegrity | Data is correct and untouched | Someone silently edits records or logs |
| **A**vailability | It works when needed | Ransomware or DDoS takes systems offline |

Every incident hurts at least one of these. Asking "which of C, I, A is at risk?" helps you judge how serious it is.

## 3.2 AAA: who are you, what can you do, what did you do?

- **Authentication**: proving who you are (password, MFA, certificate)
- **Authorization**: what you're allowed to do once in
- **Accounting**: a record of what you did (logs, audit trails)

Most SOC work is reading the **accounting** part.

## 3.3 Security controls

| Type | Purpose | Examples |
|---|---|---|
| Preventive | Stop it happening | Firewall, MFA, patching |
| Detective | Notice it happening | SIEM, IDS, logging |
| Corrective | Fix it after | Isolation, restore from backup |
| Compensating | Backup plan when the ideal control isn't possible | Extra monitoring where MFA can't be used |

SOC analysts live mainly in **detective** and **corrective** controls.

## 3.4 The Cyber Kill Chain: the 7 steps of an attack

Developed by Lockheed Martin. It helps you see *where* in an attack you are, and where you can still stop it.

| # | Stage | What the attacker does | What you might see |
|---|---|---|---|
| 1 | Reconnaissance | Researches and scans the target | Port scans, odd probing |
| 2 | Weaponization | Prepares the malicious file/link | (Usually invisible to you) |
| 3 | Delivery | Sends it (phishing email, USB, website) | Email alerts, suspicious attachments |
| 4 | Exploitation | Triggers a weakness | EDR exploit alerts |
| 5 | Installation | Plants something to stay | New services, scheduled tasks, registry run keys |
| 6 | Command & Control (C2) | Malware "phones home" | Regular beacons, strange DNS, rare destinations |
| 7 | Actions on Objectives | Steals, encrypts or destroys | Mass file changes, huge uploads |

**The earlier you catch it, the less it costs.** That's why even a "simple" phishing alert deserves respect.

## 3.5 MITRE ATT&CK: the attacker's playbook catalogue

ATT&CK (by MITRE) is a public library of real attacker behaviors, organized as:
- **Tactics**: the *goal* (e.g., Initial Access, Persistence, Lateral Movement)
- **Techniques**: the *how* (e.g., T1059 Command and Scripting Interpreter)

SOC teams tag detections with ATT&CK IDs so everyone speaks the same language and can see which behaviors they cover or miss.

## 3.6 Pyramid of Pain: which clues hurt the attacker most?

Created by David Bianco. It ranks indicators by how annoying they are for an attacker to change:

```
        /\        TTPs            ← hardest to change (their habits)
       /  \       Tools
      /----\      Network/host artifacts
     /------\     Domain names
    /--------\    IP addresses
   /----------\   File hashes     ← easiest to change
```

- Blocking a **hash** is quick but the attacker just recompiles.
- Detecting **behavior** (TTPs) forces them to change how they work.

Use easy blocks for fast relief, but build detections on behavior for lasting value.

## 3.7 IOC vs IOA

| | IOC (Indicator of Compromise) | IOA (Indicator of Attack) |
|---|---|---|
| Is | A clue left behind | Behavior happening now |
| Example | Known-bad file hash on disk | Word launching PowerShell that downloads a file |
| Timing | Usually after the fact | Can catch an attack in progress |

More on IOCs in [06-iocs-explained.md](06-iocs-explained.md).

## 3.8 Zero-day

A vulnerability the vendor doesn't know about yet (no patch). Signature-based tools often miss them. **Behavior-based detection**, segmentation and quick patching once a fix exists are the defenses.

## ✅ After this page you should be able to
- Give a real example for each letter of CIA
- Walk through the 7 Kill Chain stages with an example
- Explain why behavior-based detection beats hash-blocking long term
- Tell an IOC from an IOA
