# 6. IOCs Explained: The Clues Attackers Leave Behind

An **Indicator of Compromise (IOC)** is evidence that something bad happened or that a system touched something malicious. Think fingerprints and footprints at a crime scene.

## 6.1 Common IOC types

| Type | What it is | Example (defanged) |
|---|---|---|
| Domain name | Website name used for phishing or control | `bad-update[.]example` |
| URL | A specific malicious link | `hxxp://bad-site[.]example/login` |
| IPv4 / IPv6 address | A server used by attackers | `203.0.113.45` |
| File hash (MD5/SHA-1/SHA-256) | Unique fingerprint of a file | `e3b0c442…` |
| Email address / email message | Phishing sender or message | `urgent-pay@lookalike[.]example` |
| Hostname | Machine name tied to activity | `DESKTOP-ABC123` |
| User-agent | Browser/tool signature in web requests | An unexpected scripting library |
| User account | Account being misused | `svc_backup` logging in interactively |
| X.509 certificate | TLS certificate of attacker infrastructure | Self-signed cert issued minutes ago |
| Windows registry key | Place malware hides to survive reboot | `...\CurrentVersion\Run\<odd name>` |
| Mutex | A name malware creates to avoid double-infecting | `Global\<random-looking>` |
| Phone number | Used in SMS/voice scams | |
| Cryptocurrency wallet | Payment address in ransom notes | |
| Text / unknown | Other unique strings | Marker in a phishing kit |

> **Defanging:** write `.` as `[.]` and `http` as `hxxp` when sharing so nobody clicks by accident.

## 6.2 Where you find them

| Category | Where | Examples |
|---|---|---|
| Host / file based | On the endpoint | Hashes, registry keys, mutexes, dropped files |
| Network based | In traffic | IPs, domains, URLs, odd ports |
| Email based | In mail | Sender, headers, attachments |
| Behavioral | In patterns | Mass file renames, script spawned by Office |

## 6.3 Not all IOCs last equally

Hashes and IPs expire fast because attackers change them. Behaviors and habits last. Block known-bad things immediately, but don't think of it as permanent protection.

## 6.4 IOC vs IOA again
- **IOC** = a clue that it already happened
- **IOA** = actions that suggest an attack is underway

Good SOCs use both.

## 6.5 Which tool shows which IOC?

| Tool | Best for |
|---|---|
| **SIEM (ELK)** | Matching threat-intel feeds against all logs; searching history |
| **EDR (SentinelOne, CrowdStrike)** | Hashes, files, processes, registry, mutexes on endpoints |
| **Log analyzer / firewall reports** | IPs, domains, URLs, allowed/blocked traffic |

## ✅ After this page you should be able to
- Name 8+ IOC types
- Explain why a hash block is short-lived
- Defang an IP or URL before sharing
