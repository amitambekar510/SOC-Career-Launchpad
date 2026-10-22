# Self-Check Quiz

Try each question first, then open the answer.

## Part A: Multiple choice

**1. Which OSI layer deals with IP addresses and routing?**
A) 2  B) 3  C) 4  D) 7
<details><summary>Answer</summary>B) Layer 3 (Network)</details>

**2. Which port is used by RDP?**
A) 22  B) 443  C) 3389  D) 3306
<details><summary>Answer</summary>C) 3389</details>

**3. Correct order of the TCP 3-way handshake?**
A) ACK, SYN, SYN-ACK  B) SYN, SYN-ACK, ACK  C) SYN-ACK, SYN, ACK
<details><summary>Answer</summary>B)</details>

**4. A DMZ is mainly used to:**
A) Encrypt traffic  B) Separate internet-facing servers from the internal network  C) Assign IPs
<details><summary>Answer</summary>B)</details>

**5. Which log records SSH logins on Ubuntu?**
A) /var/log/kern.log  B) /var/log/auth.log  C) /var/log/cron
<details><summary>Answer</summary>B) /var/log/auth.log</details>

**6. Ransomware encrypting files mainly breaks which part of CIA?**
A) Confidentiality  B) Integrity  C) Availability
<details><summary>Answer</summary>C) Availability (though data theft also hits confidentiality)</details>

**7. In the Kill Chain, malware setting up persistence is:**
A) Delivery  B) Exploitation  C) Installation  D) Actions on Objectives
<details><summary>Answer</summary>C) Installation</details>

**8. Which is an IOA rather than an IOC?**
A) A known bad hash  B) Word spawning PowerShell to download a file  C) A blacklisted IP
<details><summary>Answer</summary>B)</details>

**9. Hardest indicator for an attacker to change (Pyramid of Pain)?**
A) Hash  B) IP  C) Domain  D) TTPs
<details><summary>Answer</summary>D) TTPs</details>

**10. First action on a machine with active ransomware?**
A) Power it off  B) Isolate it from the network  C) Pay the ransom
<details><summary>Answer</summary>B) Isolate (don't power off unless told to)</details>

**11. In ELK, which part is the dashboard and search screen?**
A) Elasticsearch  B) Logstash  C) Kibana  D) Beats
<details><summary>Answer</summary>C) Kibana</details>

**12. What can EDR do that a SIEM alone can't?**
A) Store logs  B) Show endpoint process trees and isolate a host  C) Draw charts
<details><summary>Answer</summary>B)</details>

**13. Which Windows event ID is a failed logon?**
A) 4624  B) 4625  C) 4688
<details><summary>Answer</summary>B) 4625</details>

**14. A /28 network has how many addresses?**
A) 8  B) 16  C) 32  D) 256
<details><summary>Answer</summary>B) 16</details>

**15. Which is a private IP range?**
A) 8.8.8.0/24  B) 192.168.0.0/16  C) 203.0.113.0/24
<details><summary>Answer</summary>B)</details>

## Part B: Short answers

1. Explain IOC vs IOA in your own words.
2. Why is network segmentation important during ransomware?
3. Why do attackers like DNS and HTTPS for hiding traffic?
4. What is normalization in a SIEM and why does it matter?
5. Why should an L1 not close a Critical alert alone?

<details><summary>Model answers</summary>

1. IOC is a static clue that something already happened; IOA is behavior showing an attack is underway.
2. It limits how far the malware can spread from the first infected machine.
3. Both are allowed almost everywhere and blend into normal traffic; HTTPS also hides content.
4. It maps different log formats into common fields so one search works across all sources.
5. Critical alerts often mean active compromise or high impact, so they need senior review and coordinated response.
</details>

## Part C: Scenarios

**S1.** A host sends DNS queries to random-looking subdomains of an unfamiliar domain every few seconds. What could it be, and what do you check?

**S2.** An internal server has RDP open to the internet. What worries you, and what's your first move?

**S3.** A cron job runs a script from `/tmp` every 5 minutes, added by a non-admin account. What do you do?

**S4.** A user clicked a link in an email and typed their password. What are your first steps?

**S5.** EDR shows Word starting PowerShell with an encoded command. How do you build the full picture?

<details><summary>Model answers</summary>

**S1.** Possible DNS tunnelling or beaconing. Check domain age and reputation, query pattern and volume, the host's other activity, and correlate with proxy and firewall logs. Escalate if suspicious.

**S2.** High risk of brute force or unauthorised access. Restrict external RDP, review logs for attempts, confirm MFA/VPN protection, escalate.

**S3.** Likely persistence. Don't run the script. Preserve it, inspect its contents safely, check the account's other activity, and escalate to L2.

**S4.** Reset the password and revoke sessions, review recent sign-ins, block the URL, find other recipients, notify the user and document.

**S5.** Use the EDR storyline for parent/child processes and follow-on actions, check the SIEM for network connections from the host, check firewall/log analyzer for outbound traffic, isolate the host if malicious, escalate.
</details>
