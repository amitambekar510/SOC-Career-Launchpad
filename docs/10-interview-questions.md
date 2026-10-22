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

**What are the parts of ELK?**
Elasticsearch (store/search), Logstash (ingest/transform), Kibana (visualize), Beats (ship logs).

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

## Questions you can ask them
- What does a typical first month look like for a new analyst?
- Which tools will I work with and who will mentor me?
- How does the escalation process work?
- How do you measure success for an L1 analyst?
