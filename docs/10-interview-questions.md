# 10. Interview Questions (with simple answers)

Say the answers in your own words. Interviewers want to hear that you understand, not that you memorized.

## Basics
**What is a SOC?**
A team that monitors an organization's systems around the clock, spots suspicious activity, responds to it and learns from it.

**What is the CIA triad?**
Confidentiality (only the right people see data), Integrity (data is accurate and unaltered), Availability (systems work when needed).

**What is the difference between a false positive and a true positive?**
A false positive is an alert for something harmless. A true positive is a real threat.

**IDS vs IPS?**
IDS detects and alerts. IPS sits inline and can also block.

**What is a firewall?**
A device or software that allows or blocks traffic using rules. Stateful firewalls also track the state of connections.

**What is the 3-way handshake?**
SYN, SYN-ACK, ACK: how TCP opens a connection.

**What is DNS and why do attackers abuse it?**
It turns names into IPs. Attackers hide command traffic or data theft inside DNS queries.

**What is a zero-day?**
A flaw the vendor doesn't know about yet, so no patch exists.

## Frameworks
**Explain the Cyber Kill Chain.**
Reconnaissance, Weaponization, Delivery, Exploitation, Installation, Command & Control, Actions on Objectives. It shows where in an attack you are and where to break it.

**What is MITRE ATT&CK?**
A public catalogue of real attacker tactics and techniques that teams use to label detections and find coverage gaps.

**IOC vs IOA?**
IOC = a clue it already happened (hash, IP). IOA = behavior suggesting an attack is happening now.

**What is the Pyramid of Pain?**
It ranks indicators by how hard they are for attackers to change. Hashes are easy, TTPs are hard.

## Tools
**What is a SIEM?**
A platform that collects and normalizes logs from many sources, correlates them and raises alerts. It's also used to search history.

**What is normalisation in a SIEM, and why does it matter?**
It maps different log formats into common field names, so one search works across every source.

**Which SIEM products do you know?**
Name one or two you've practised (for example Elastic or Wazuh) and say the idea carries over: collect, parse, normalise, enrich, detect, alert.

**Your SIEM dashboard suddenly goes quiet. What do you check?**
Whether the log sources and collectors are still reporting. Silence can mean an outage or an attacker.

**What does EDR give you that a SIEM doesn't?**
Deep endpoint detail (process tree, files, registry, memory) and direct actions like isolating a host.

**What is host isolation?**
Cutting an endpoint off from the network while keeping the EDR connection so you can still investigate it.

## Scenarios
**You see 200 failed SSH logins then one success from the same foreign IP. What do you do?**
Treat the success as possibly compromised. Check what that session did, block or rate-limit the IP, reset the account, enable MFA, check for similar activity on other accounts, escalate with notes.

**A user says they entered their password on a strange page.**
Reset the password and revoke sessions, review recent sign-ins, block the URL, find other recipients of the same email, notify the user.

**Antivirus quarantined a file but the process is still running.**
Not resolved. Investigate the running process, isolate the host if needed, look for other dropped files and persistence.

**A "low" alert involves a domain that threat intel marks as a known command server.**
Re-evaluate the severity because context changed. Document why and escalate.

**You're not sure whether something is malicious.**
Collect evidence, write down what you know and don't know, and escalate. Never guess silently.

**A manager asks you to close a ticket quickly but you have doubts.**
Politely explain the open question, ask for confirmation in writing, and follow the closure process.

## More technical questions
**What's the difference between a virus, a worm and a trojan?**
A virus needs a host file and a user action to spread. A worm spreads by itself across networks. A trojan pretends to be useful software.

**How would you detect a SYN flood?**
Many SYN packets with few completed handshakes, often from many sources, in flow data, firewall logs or an IDS alert.

**Which Windows events show a failed and a successful login?**
4625 failed, 4624 successful. Also check the logon type (type 10 is RDP).

**What is Kerberoasting?**
An attacker requests service tickets for service accounts and cracks them offline to learn the passwords. You'd look for unusual bursts of service-ticket requests.

**How would you investigate a phishing email end to end?**
Check sender and headers, inspect links and attachments safely in a sandbox, find all recipients, remove the mail, block the sender and URL, check who clicked, reset exposed credentials, document.

**How does SQL injection appear in logs?**
SQL keywords or quote tricks in URL or form parameters, database errors and unusually large responses.

## More scenario questions
**You receive 500 alerts at 2 AM. How do you prioritise?**
Group by severity and type. Look first at Critical/High, anything involving privileged accounts or sensitive systems, and alerts that correlate (same host or user). Bulk-handle obvious noise with documented reasons, and escalate if there's a pattern.

**A user's account is logging in from India and the USA at the same time.**
Treat as possible account compromise (impossible travel). Check device and VPN use, review the sessions' activity, reset the password and revoke sessions if suspicious, and escalate.

**Your SIEM alerts on many failed logins to an admin account.**
Check the source and timing, whether any login succeeded, whether the account is locked, whether other accounts are targeted. Block or rate-limit the source, protect the account, escalate if there was a success.

**You find malware on an endpoint. What are your first steps?**
Isolate the host (don't power off), preserve evidence, collect the sample or hash, check other hosts for the same indicators, block IOCs, and escalate with notes.

**How do you explain an incident to a non-technical manager?**
Situation, Impact, Action, Next: plain words, what you don't know yet, and when the next update comes.

**A vendor's IP is flagged by threat intelligence. What's your process?**
Check the intel's source and confidence, whether the vendor's traffic to us is expected, recent activity from that IP, then ask the vendor contact and the owner. Don't auto-block a critical partner. Escalate if unclear.

## Questions you can ask them
- What does a typical first month look like for a new analyst?
- Which tools will I work with and who will mentor me?
- How does the escalation process work?
- How do you measure success for an L1 analyst?
