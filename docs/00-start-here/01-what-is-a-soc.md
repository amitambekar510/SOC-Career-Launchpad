# What is a SOC?

## The simple picture

A **Security Operations Center (SOC)** is a team (and a room, or a virtual room) that watches over a company's digital world around the clock. Their job is to **notice trouble early, decide if it's real, and stop it before it becomes a disaster.**

Imagine a shopping mall security office:

| Mall security | SOC |
|---|---|
| CCTV cameras | Logs from servers, laptops, firewalls, cloud |
| Door alarms | Security alerts from tools |
| Guard checking a beeping alarm | Analyst investigating an alert |
| "It was just a cat" | False positive |
| "Someone is forcing the back door" | True positive, start the response |
| Calling the manager / police | Escalating to L2/L3 or Incident Response |
| Incident report | Ticket and documentation |

## What a SOC protects against

**External threats** (from outside)
- Phishing emails trying to steal passwords
- Ransomware that locks files and demands money
- Hackers guessing passwords (brute force) or exploiting unpatched software
- Malware, botnets, scanners probing the internet-facing systems

**Internal threats** (from inside)
- An employee clicking a bad link by accident
- Someone copying sensitive files to a personal drive or cloud account
- A stolen or shared account being misused
- A disgruntled or leaving employee abusing access

Most internal incidents are mistakes, not villains. A good analyst stays calm and factual, and never accuses anyone. They report evidence and let the right people decide.

## The three things every SOC does

1. **Detect:** collect logs and alerts from everywhere, then spot the suspicious ones.
2. **Respond:** contain the problem (isolate a laptop, block an IP, reset a password).
3. **Improve:** learn from every incident so the same trick doesn't work twice.

## The people, processes and technology

- **People:** Interns, L1, L2, L3 analysts, threat hunters, incident responders, SOC manager
- **Process:** playbooks, runbooks, escalation matrix, shift handover, ticketing
- **Technology:** SIEM (central log brain), EDR (eyes on laptops/servers), firewalls, email security, threat intelligence, SOAR (automation)

## Why companies need a SOC

Attackers don't work 9 to 5. Breaches that are found in hours cost far less than those found in months. The SOC shortens the time between "attacker got in" and "we noticed and stopped them".

## What you should be able to do after this page
- Explain a SOC to a friend in two sentences
- Name two external and two internal threats
- Explain what "false positive" and "true positive" mean
