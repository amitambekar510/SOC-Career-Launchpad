# Indian Frameworks, Explained Simply

Each section has the same layout: **What it is → Who it applies to → Key points → What it means for you → Remember it as**.

---

## 1. CERT-In Directions (April 2022)

**What it is.** CERT-In is India's national cyber emergency response team. On **28 April 2022** it issued directions under Section 70B(6) of the IT Act, 2000. They took effect on **27 June 2022**.

**Who it applies to.** Service providers, intermediaries, data centres, companies (body corporates) and government organisations.

**Key points**

| Topic | In simple words |
|---|---|
| ⏱️ Reporting | Report the listed cyber incidents to CERT-In **within 6 hours** of noticing them or being told about them |
| 📋 Incident list | The directions list **20 types** of incident (Annexure I). Examples: targeted scanning, compromise of critical systems, unauthorised access, malicious code, website defacement, DoS/DDoS, phishing and spoofing, data breach, data leak, attacks on cloud systems, attacks on AI/ML systems |
| 🗂️ Logs | Turn on logs for **all ICT systems** and keep them securely for a **rolling 180 days**, within Indian jurisdiction |
| 🕒 Clocks | Keep system clocks synchronised to a trusted time source, so timelines from different systems line up |
| 📞 Contact | Name a point of contact that CERT-In can reach |
| 📝 Partial info | You may report what you know within the 6 hours and add details later |

**What it means for you.** You will probably not file the report. But **you are often the person who notices the incident first**, and that moment starts the clock. Write down the exact time you noticed, and escalate fast.

**Remember it as:** *"6 hours to tell, 180 days of memory."*

---

## 2. SEBI CSCRF (2024)

**What it is.** SEBI regulates India's securities (stock) market. On **20 August 2024** it issued the **Cybersecurity and Cyber Resilience Framework (CSCRF)**, one common rulebook replacing many older cyber circulars.

**Who it applies to.** SEBI-regulated entities, such as stock exchanges, clearing corporations and depositories, stockbrokers, mutual funds and asset managers, KYC agencies and more.

**Key points**

| Topic | In simple words |
|---|---|
| 🏷️ Categories | Entities are sorted by size and risk: **MIIs** (Market Infrastructure Institutions), **Qualified REs**, **Mid-size REs**, **Small-size REs** and **Self-certification REs**. Bigger and riskier means more controls |
| 🎯 Goals | Built around five goals: **Anticipate, Withstand, Contain, Recover, Evolve** |
| 🧩 Control mapping | Controls are organised along the lines of the NIST Cybersecurity Framework |
| 📈 Cyber Capability Index (CCI) | A score used by MIIs and Qualified REs to measure their cyber maturity |
| 🏢 SOC | The framework stresses having a Security Operations Centre. Smaller entities can be onboarded to a shared "Market SOC" run by the exchanges |
| 🗓️ Timelines | Deadlines were extended more than once, with 31 August 2025 widely reported as the final one for most entities. Cyber audits now follow the CSCRF |
| 📜 Certification | ISO 27001 certification is reported as required for MIIs and Qualified REs. Confirm in the circular |

**What it means for you.** If your company is a broker or fund house, your SOC work (monitoring, incident response, evidence) is exactly what auditors will ask to see. Good tickets and logs are audit evidence.

**Remember it as:** *"Bigger market player, bigger rulebook."*

---

## 3. RBI IT and Cyber Security Frameworks

**What it is.** The Reserve Bank of India sets rules for banks, NBFCs and payment companies. There is not one document but a **family**:

| RBI document | Mainly for | Simple summary |
|---|---|---|
| **Cyber Security Framework in Banks (2016)** | Banks | The baseline that pushed banks toward cyber policies and a round-the-clock SOC |
| **Digital Payment Security Controls (2021)** | Banks and card-issuing NBFCs | Security for internet banking, mobile banking and card payments |
| **Master Direction on IT Governance, Risk, Controls and Assurance Practices (2023, effective 1 April 2024)** | Banks, NBFCs and other regulated entities (check which layers apply) | Board-level IT governance, risk, asset inventory, audits and assurance |
| **Cyber Resilience and Digital Payment Security Controls for non-bank PSOs (30 July 2024)** | Payment System Operators (wallets, payment aggregators, card networks and similar) | Governance, baseline controls, a Cyber Crisis Management Plan, vendor risk |

**PSO phase-in dates:** large PSOs **1 April 2025**, medium **1 April 2026**, small **1 April 2028**.

**What it means for you.** Finance SOCs usually have stricter monitoring, faster escalation and heavier documentation. Expect questions like "Which system? Which customers? Which payment channel?" in your tickets.

**Remember it as:** *"RBI = money-movers must be resilient."*

---

## 4. DPDP Act 2023 and DPDP Rules 2025

**What it is.** India's data protection law. The **Digital Personal Data Protection Act** was passed in **2023**. The **DPDP Rules** that make it work were notified on **13 November 2025**, with obligations phased in over about 18 months (full operation around **May 2027**).

**Who it applies to.** Organisations that process the digital personal data of people in India.

**Vocabulary (easy!)**

| Term | Plain meaning |
|---|---|
| **Data Principal** | The person the data is about (a customer, an employee) |
| **Data Fiduciary** | The organisation deciding why and how data is used (your company) |
| **Data Protection Board of India** | The body that handles breaches and complaints |
| **Significant Data Fiduciary** | A bigger, higher-risk fiduciary with extra duties |

**Key points**

| Topic | In simple words |
|---|---|
| 🔐 Safeguards | Use reasonable security: encryption, access control, logging, monitoring, backups |
| ⏱️ Breach reporting | Tell the Board **without delay**, then send a **detailed report within 72 hours** (the Board may allow longer on request). Affected people must be told too |
| 🗂️ Logs | The Rules call for keeping certain logs and personal data for **one year** for breach detection and investigation |
| 💰 Penalties | The Act allows heavy fines, for example up to ₹200 crore for failing to notify a breach and up to ₹250 crore for failing to keep reasonable security safeguards |

**What it means for you.** If an alert may involve **personal data** (customer records, employee data), say so loudly in your escalation. That one sentence can start a second legal clock (72 hours) alongside CERT-In's 6 hours.

**Remember it as:** *"People's data, people's rights, 72 hours."*

---

## Side-by-side summary

| | CERT-In | SEBI CSCRF | RBI | DPDP |
|---|---|---|---|---|
| Type | Government directions | Sector regulator framework | Sector regulator directions | Law + rules |
| Mainly for | Almost every organisation in India | Securities market entities | Banks, NBFCs, payment operators | Anyone handling personal data |
| Headline | 6h report, 180d logs | Tiered controls, CCI, SOC | Governance + cyber resilience | 72h breach report, safeguards |
| Your SOC touchpoint | Timestamps, logs | Monitoring, evidence | Escalation, documentation | Flag personal-data impact |
