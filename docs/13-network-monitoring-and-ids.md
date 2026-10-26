# 13. Network Monitoring, Packets and IDS/IPS

[Networking basics](01-networking.md) taught how computers talk. This page is about **watching** them talk.

## 13.1 Three ways to watch the network

| Method | What you keep | Analogy | Good for | Examples of tools |
|---|---|---|---|---|
| **Full packet capture (PCAP)** | Every packet, including content | A security camera with sound | Deep dives, proof. Big and expensive to store | Wireshark, tcpdump |
| **Flow data** | Who talked to whom, when, how much (no content) | A phone bill | Spotting big transfers, scans, beacons cheaply | NetFlow / IPFIX |
| **Network metadata logs** | Rich summaries: connections, DNS, HTTP, TLS details | A receptionist's visitor log | Everyday hunting and investigations | Zeek, Suricata logs |

Because most traffic is encrypted (HTTPS), **metadata and flow often tell you more than payloads**: who, when, how often, how much.

## 13.2 IDS and IPS

| | IDS (Intrusion **Detection** System) | IPS (Intrusion **Prevention** System) |
|---|---|---|
| Job | Watches a *copy* of traffic and **alerts** | Sits **in the path** and can **block** |
| Risk | Can miss things nobody told it about | A bad rule can block legitimate traffic |
| Analogy | Burglar alarm | Alarm plus automatic door lock |

**How they detect:** *signatures* (known bad patterns), *anomalies* (unusual behaviour) or both. Common open-source engines include Snort and Suricata.

### Anatomy of a rule (illustrative)
```
alert tcp any any -> $HOME_NET 22 (msg:"Possible SSH brute force"; flow:to_server; sid:1000001; rev:1;)
 └──┬──┘ └─┬─┘ └┬┘ └┬┘  └───┬────┘ └┬┘  └───────────────┬──────────────────────────────────────┘
  action protocol src  dir  destination port         options (what to match, message, ID, version)
```
Syntax differs between products and versions. Learn the **idea**: action + who-to-whom + what to match + a message.

## 13.3 Reading packets with Wireshark-style filters

| You want to see | Filter |
|---|---|
| Everything for one IP | `ip.addr == 203.0.113.45` |
| Only DNS | `dns` |
| TCP connection attempts (SYN, not yet answered) | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |
| Web form submissions | `http.request.method == "POST"` |
| Anything on port 3389 | `tcp.port == 3389` |

## 13.4 Patterns to recognise

| Pattern | What it looks like | Might be |
|---|---|---|
| **Port scan** | One source touching many ports or many hosts quickly | Attacker reconnaissance |
| **SYN flood** | A burst of SYNs, few completed handshakes, often from many sources | Denial-of-service |
| **Beaconing** | Small connections to the same outside address at regular intervals (every 60 s, say) | Malware phoning home (C2) |
| **DNS tunnelling** | Huge numbers of lookups to random-looking subdomains of one domain | Data theft or hidden control channel |
| **Large outbound transfer** | A host sending far more data out than normal, often at odd hours | Exfiltration |
| **Cleartext credentials** | FTP, Telnet or plain HTTP logins | Exposure risk, plus easy sniffing |

## 13.5 Practice (in your own lab)
1. Capture your own traffic while browsing. Find a DNS lookup, then the TCP handshake, then the HTTPS connection.
2. Run a port scan against **your own** lab machine and see how it looks in the capture.
3. Find the "heartbeat" of a repeating connection.

## ✅ After this page you should be able to
- Compare packet capture, flow data and metadata, and say when you'd use each
- Explain IDS vs IPS with an analogy
- Read a simple rule and a Wireshark-style filter
- Name five network attack patterns and how each looks in the data
