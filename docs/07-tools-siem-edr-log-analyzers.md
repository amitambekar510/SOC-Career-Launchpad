# 7. The Tools: SIEM, EDR and Log Analyzers

Three kinds of "eyes" work together. No single tool tells the full story.

| Layer | Question it answers | Examples |
|---|---|---|
| **SIEM** | "What's happening across everything?" | Elastic Stack (ELK), Splunk |
| **EDR** | "What exactly happened on this laptop/server?" | SentinelOne, CrowdStrike Falcon |
| **Log / event analyzers** | "What did the network devices see?" | ManageEngine EventLog Analyzer, FortiAnalyzer |

## 7.1 SIEM: the central brain

A **Security Information and Event Management** platform collects logs from firewalls, servers, endpoints, apps and cloud, converts them into a common format, correlates them and raises alerts. It's also your **search engine for the past**.

### The ELK stack
| Part | Job |
|---|---|
| **Elasticsearch** | Stores and indexes the data; the search engine |
| **Logstash** | Receives, cleans and reshapes logs before storing |
| **Kibana** | The screen you use: search, dashboards, alerts |
| **Beats** (Filebeat, Winlogbeat…) | Small shippers that send logs from machines into the stack |

### Normalisation: why it matters
A Linux server, a Windows server and a firewall all record "login failed" differently. Normalisation maps them to shared field names (like `source.ip`, `user.name`, `host.name`, `event.action`) so one search covers everything.

### Skills to build
- Searching with KQL (Kibana Query Language), for example: `event.action : "logon-failed" and source.ip : "203.0.113.45"`
- Reading a normalised event and knowing what each field means
- Using dashboards to spot spikes (failed logins, alert volume by severity)
- Pivoting from an alert to the raw logs and building a timeline

> **Beginner tip:** learn to *read* dashboards accurately first. Misreading a chart causes missed attacks or false alarms.

### Windows event IDs worth knowing
| ID | Meaning |
|---|---|
| 4624 / 4625 | Successful / failed logon |
| 4688 | New process created |
| 4672 | Special privileges assigned |
| 4720 | User account created |
| 4732 | Member added to a local group |
| 1102 | Audit log cleared (suspicious) |

Sysmon (a free Microsoft tool) adds richer endpoint logs: process creation (ID 1), network connection (3), file creation (11), and more.

## 7.2 EDR: eyes on the endpoint

An **Endpoint Detection and Response** agent runs on each laptop/server. It records processes, files, registry changes and network connections, and can **respond** directly.

| Capability | Plain meaning |
|---|---|
| Behavioral detection | Flags suspicious *behavior*, not just known files |
| Process tree / storyline | Shows what started what: "Word → PowerShell → unknown exe" |
| **Host isolation** | Cuts the machine off from the network but keeps the EDR link so you can still work on it |
| Kill / quarantine | Stop a process, move a file to safe storage |
| Rollback (some products) | Undo file changes made by ransomware |
| Threat hunting | Search recent history across all endpoints for an IOC or behavior |

SentinelOne and CrowdStrike are both cloud-managed EDR platforms. Their screens differ, but the workflow is the same: open the alert → read the timeline → decide containment → document → escalate if needed.

## 7.3 Log / event analyzers

These collect logs from network and infrastructure devices (firewalls, routers, switches, domain controllers) for reporting, compliance and investigation.

- **FortiAnalyzer**: central logging and reporting for Fortinet firewalls (traffic, threat, events)
- **ManageEngine EventLog Analyzer**: log management, compliance reports, Active Directory auditing
- Similar tools exist from many vendors

Use them to answer: "Did the firewall allow or block that connection? How much data went out?"

## 7.4 How the three work together

```
SIEM alert (many sources correlated)
     │
     ├─► EDR: what did the endpoint actually do? (process tree, files)
     │
     ├─► Log analyzer / firewall: what did the network see? (allowed/blocked, volume)
     │
     └─► Threat intel: is this IP/domain/hash known-bad?
                │
                ▼
      Build ONE timeline → decide → act → document
```

## 7.5 Alerts that deserve context
Enrich every alert with asset owner, user role, and threat-intel reputation before acting. It cuts false positives dramatically.

## ✅ After this page you should be able to
- Name the four ELK parts and what each does
- Explain what EDR sees that a SIEM can't
- Describe an investigation that uses all three tools
- Explain host isolation and when you'd use it
