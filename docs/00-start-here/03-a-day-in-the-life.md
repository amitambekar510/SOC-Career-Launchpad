# A Day in the Life of an L1 Analyst

> Illustrative. Real shifts differ by company.

## Start of shift: handover (15–30 min)
- Read the previous shift's notes: open incidents, things to watch, systems under maintenance
- Check the dashboards: alert volume, any spikes overnight, tools' health (are all log sources reporting?)
- Confirm who is on-call above you (L2/L3) and how to reach them

## Through the shift: the alert loop

```
New alert → Quick triage → Enough info? ─ no → Advanced checks ┐
                              │ yes                            │
                              ▼                                ▼
                    False positive? ── yes → Close with comment
                              │ no
                              ▼
                  Raise incident → Contain → Notify → Hand to L2 if needed
```

A typical alert, step by step:

1. **Read it:** what rule fired, what severity, which user and device?
2. **Enrich it:** is the IP/domain known-bad in threat intelligence? Is this user normally active at this hour?
3. **Check the endpoint** in EDR: what process ran, what spawned it, any network connections?
4. **Check the network side** in your log analyzer or firewall logs: was the traffic allowed or blocked?
5. **Decide** and document: closed (why), or escalated (what you found, what you did, what you need).

## Examples of what lands in your queue

- 40 failed logins then 1 success from a foreign IP
- Antivirus quarantined a file on a finance laptop
- A user reported a strange email
- A server started talking to a rarely seen external domain at 3 AM

## Quiet moments
Quiet doesn't mean idle:
- Review the day's closed false positives. Is a rule too noisy?
- Practice a search you don't fully understand
- Read a threat advisory or newsletter
- Update your personal notes and runbook ideas

## End of shift
- Update every open ticket with current status and next step
- Write the handover note (clear, short, honest)
- Flag anything that felt "off" even if you couldn't prove it

## What you should be able to do after this page
- Walk through the life of one alert from arrival to closure
- Write a 5-line handover note
