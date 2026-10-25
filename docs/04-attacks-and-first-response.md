# 4. Attacks and First Response

For each attack: **what it looks like** (indicators) and **what to do first** (immediate actions). Always follow your own team's playbook and escalation matrix. This is the common-sense baseline.

> **Containment golden rule:** stop the spread first, investigate second, and never destroy evidence.

## 4.1 Phishing
**Looks like:** unexpected sender, urgency ("act now!"), look-alike domain, mismatched link, odd attachment, a login page that "looks a bit off".

**First actions**
1. Pull the email from all mailboxes (not just the reporter's)
2. Block sender domain and malicious URL
3. Open attachments/links only in a sandbox, never on your own machine
4. Find everyone who received or clicked
5. If someone entered their password → reset it, check recent logins, revoke sessions
6. Notify affected users and share what to watch for

## 4.2 Ransomware
**Looks like:** many files renamed or encrypted, ransom notes, backup or shadow-copy deletion, security tools being switched off.

**First actions**
1. **Isolate** the affected machine(s) from the network right away (use EDR isolation)
2. Do **not** power off (memory evidence) unless instructed
3. Find "patient zero" and how it spread
4. Check that backups are safe and untouched
5. Escalate immediately to IR/management. Decisions about payment or public statements are never an analyst's call

**Early warnings (before encryption):** credential dumping, a burst of lateral movement, backup deletion. Often hours to days before the lock-up. Data is frequently stolen first ("double extortion").

## 4.3 Brute force and password spraying
**Looks like:** many failed logins from one or a few sources, or one password tried across many accounts, followed by a success.

**First actions**
1. Block or rate-limit the source
2. Look hard at the **successful** login: from where, what did it do next?
3. Reset the account password, enforce MFA
4. Check if other accounts were hit

## 4.4 Insider threat
**Looks like:** unusual data access, off-hours downloads, large copies to USB or personal cloud, access to systems unrelated to the person's job.

**First actions**
1. Correlate with DLP/UEBA and access logs
2. Preserve evidence
3. **Involve HR/management per policy before any direct conversation with the person**
4. Review whether access is more than the role needs (least privilege)

Stay neutral. It may be a mistake, a misunderstanding or a compromised account, not necessarily malice.

## 4.5 Malware / trojan
**Looks like:** unexpected processes, unfamiliar scheduled tasks or services, known-bad hashes, calls to suspicious domains.

**First actions**
1. Isolate the host (EDR)
2. Collect the sample for analysis (static, then dynamic in a sandbox)
3. Block related IOCs organization-wide
4. Search other machines for the same indicators

## 4.6 Data exfiltration
**Looks like:** large or odd outbound transfers, rare or brand-new destinations, strange timing, lots of DNS or HTTP POST traffic.

**First actions**
1. Block the destination
2. Isolate the source host
3. Work out *what* data and how sensitive
4. Review proxy, DLP and firewall logs to build the timeline

## 4.7 Web attacks (e.g., SQL injection)
**Looks like:** weird characters or SQL words in URLs, WAF alerts, database errors.

**First actions**
1. Block the source at the WAF/firewall
2. Inform the application owner
3. Check database logs for unauthorised access

### What SQL injection can look like in web logs
Requests where a parameter contains SQL words or quote tricks, for example a login or search URL with text like `' OR '1'='1`, `UNION SELECT`, or `--`, often followed by database errors or unusually large responses. (Illustrative. Real logs encode characters, so you may see `%27` for a quote.)

## 4.7b Malware types in plain English

| Type | What it is | Key trait |
|---|---|---|
| **Virus** | Attaches to a file or program and spreads when it's run | Needs a host file and a user action |
| **Worm** | Spreads by itself across a network | No user action needed, so it spreads fast |
| **Trojan** | Pretends to be useful software | Tricks you into installing it |
| **Ransomware** | Encrypts files and demands payment | Hits availability, often steals data too |
| **Spyware / infostealer** | Quietly collects passwords, cookies, documents | Stealing credentials |
| **RAT (remote access trojan)** | Gives an attacker remote control | Hands-on-keyboard access |
| **Rootkit** | Hides itself deep in the system | Hard to detect |
| **Botnet** | Many infected machines controlled together | Used for DDoS and spam |
| **Fileless malware** | Lives in memory and abuses built-in tools | Leaves little on disk |

## 4.8 Modern attack patterns to recognize

Today's incidents often start with a **valid login or a trusted integration**, not obvious malware.

| Theme | Examples | Key idea |
|---|---|---|
| **AI-assisted scams** | Deepfake voice asking for a payment, perfect-looking executive email, helpdesk trick to reset MFA | Verify by a second, trusted channel before acting |
| **Identity attacks** | Impossible travel, MFA fatigue (push-bombing), new admin accounts, dormant account suddenly active | Look at who, where, when, what device and what next |
| **Cloud & SaaS** | Suspicious app permissions (OAuth), new access keys, public storage buckets, mass downloads | Misuse of legitimate features |
| **Fileless / living off the land** | Office app starting PowerShell, encoded scripts, built-in tools used to move around | Needs behavior-based EDR alerts |
| **Defense tampering** | Antivirus/EDR disabled or altered | High-confidence sign of active intrusion. Escalate |
| **Supply chain** | Trusted software update behaving strangely, compromised partner email | Trust boundaries extend beyond your company |

## 4.9 How to reason about any new alert
1. Which of these categories does it resemble?
2. Is this normal for **this** user, device, time and job?
3. What happened **before** and **after** the alert?
4. Contain the highest-risk item first
5. Tell the right owner
6. Look for the same pattern elsewhere
7. Write it down

## ✅ After this page you should be able to
- Give the first three actions for phishing, ransomware and brute force
- Explain why you isolate instead of power off
- Say why insider cases involve HR before confrontation
