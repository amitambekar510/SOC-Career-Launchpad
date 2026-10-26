# 8. An 8-Week Study Plan

About **1–2 hours a day**, 5–6 days a week. Adjust freely. Consistency beats cramming.

| Week | Focus | Do this |
|---|---|---|
| **1** | Foundations | Read [Start Here](00-start-here/). Learn IP, ports, OSI. Set up a free Linux VM or WSL. |
| **2** | Networking in practice | Install Wireshark. Capture a web visit and find the TCP handshake and a DNS query. Learn the port table by heart. |
| **3** | Linux & logs | Practice every command in [Linux](02-linux.md). Read `auth.log` on your VM. Cause failed SSH logins on your *own* VM and find them in the log. |
| **4** | Security fundamentals | CIA, AAA, Kill Chain, MITRE ATT&CK, Pyramid of Pain. Browse the ATT&CK website and pick 5 techniques to explain in your own words. |
| **5** | Attacks & response | Read [Attacks](04-attacks-and-first-response.md). Write a one-page playbook for phishing in your own words. |
| **6** | SIEM basics | Stand up a free SIEM lab (Wazuh, Elastic or Security Onion, or a Splunk free tier). Ingest sample logs. Build one search and one dashboard. |
| **7** | EDR, IOCs & workflow | Read [IOCs](06-iocs-explained.md) and [Workflow](05-alert-handling-workflow.md). Take a free blue-team lab or room on alert triage. |
| **8** | Review & interview prep | Take the [quiz](../quiz/self-check-quiz.md). Practice [interview questions](10-interview-questions.md) out loud. Write your own handover note and 3 sample ticket notes. |

## Optional extension (weeks 9 to 12)

| Week | Focus | Do this |
|---|---|---|
| **9** | Windows and Active Directory | Read [Windows and AD](12-windows-and-active-directory.md). Install Sysmon in your lab and find process-creation events. |
| **10** | Network monitoring and detection | Read [Network monitoring](13-network-monitoring-and-ids.md) and [Detection engineering](14-detection-engineering-and-hunting.md). Write three detections and test them. |
| **11** | Incident response and tools | Read [IR and reporting](15-incident-response-and-reporting.md) and [SOAR and tools](16-soar-ticketing-and-investigation-tools.md). Write a full incident report from a training lab. |
| **12** | Cloud, vulnerabilities and career | Read [Cloud, UEBA and vulnerability management](17-cloud-ueba-vulnerability-management.md) and [Career paths](19-career-paths-and-transitions.md). Finish your [home lab](18-home-lab-guide.md) portfolio. |

## Weekly habit
- 🧠 Explain one concept out loud or in writing without looking
- 🧪 One hands-on activity
- 📰 15 minutes of security news
- 📓 Add to your own glossary

## Portfolio ideas (show employers you did the work)
- A GitHub repo of your lab notes and cheat sheets (no confidential info)
- A write-up of an investigation from a public training lab
- A small detection query collection with explanations
- A phishing-email analysis write-up using defanged indicators
