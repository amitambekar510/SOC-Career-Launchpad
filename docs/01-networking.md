# 1. Networking: How Computers Talk

Every attack travels over a network, so every alert eventually comes down to **"who talked to whom, how, and was that normal?"**

## 1.1 The OSI model (the 7-layer cake)

Think of sending a parcel: you write the letter, put it in an envelope, address it, hand it to a courier, and it travels roads to the destination. Networks work in layers too.

| Layer | Name | Everyday meaning | Where attacks show up |
|---|---|---|---|
| 7 | Application | The apps: web, email, DNS | Phishing, web attacks, malware calling home |
| 6 | Presentation | Encryption / formatting (TLS) | Bad certificates |
| 5 | Session | Keeping a conversation open | Session hijacking |
| 4 | Transport | TCP/UDP and ports | Port scans, SYN floods |
| 3 | Network | IP addresses and routing | IP spoofing |
| 2 | Data Link | MAC addresses, switches | ARP spoofing, VLAN hopping |
| 1 | Physical | Cables, Wi-Fi, ports | Unplugged or tapped hardware |

Real life mostly uses the shorter **TCP/IP model** (4 layers: Network Access, Internet, Transport, Application). Learn OSI for the vocabulary and TCP/IP for how things really work.

**Handy trick:** when an alert arrives, ask "which layer is this about?" A bad domain is layer 7. A spoofed IP is layer 3.

## 1.2 IP addresses and subnets

- An **IPv4 address** looks like `192.168.1.10` (four numbers, 0–255).
- A **subnet mask / CIDR** like `/24` says how much of the address is the "street" (network) and how much is the "house number" (host). `/24` = 256 addresses, `/28` = 16.
- **Private ranges** (used inside organizations, never routed on the internet):
  - `10.0.0.0/8`
  - `172.16.0.0/12`
  - `192.168.0.0/16`

If you see a private address as a *source* in internet-facing logs, something is odd: spoofing, NAT confusion or a logging gap.

## 1.3 Ports and protocols to memorize

A port is the "door number" for a service on a machine.

| Port | Service | Why a SOC cares |
|---|---|---|
| 20/21 | FTP | Sends passwords in clear text |
| 22 | SSH | Remote admin, so a brute-force favorite |
| 23 | Telnet | Old and unencrypted. Rarely should be active |
| 25 | SMTP | Email sending. Spam and phishing relays |
| 53 | DNS | Name lookups. Abused for hiding command traffic |
| 80 | HTTP | Unencrypted web |
| 443 | HTTPS | Encrypted web. Most modern malware hides here too |
| 445 | SMB | Windows file sharing. Ransomware spreads through it |
| 3389 | RDP | Remote Desktop. Top target for brute force |
| 3306 | MySQL | Databases should rarely face the internet |

**Rule of thumb:** a normal port in an unusual place is a clue (RDP open to the whole internet, SMB leaving your network).

## 1.4 TCP handshakes

### Opening a connection: the 3-way handshake
1. **SYN**: client says "Can we talk?"
2. **SYN-ACK**: server says "Yes, can you hear me?"
3. **ACK**: client says "Yes." The connection is open.

A flood of SYNs that never finish the handshake is a classic sign of a **SYN flood** (a denial-of-service attempt) or a port scan.

### Closing a connection
A normal TCP close uses FIN and ACK packets in each direction (often described as a 4-step close). Sudden resets (RST) in large numbers can indicate scanning or blocked connections.

### TLS (the "secure" handshake)
Before HTTPS data flows, the two sides agree on encryption (client hello, server hello, certificate, key exchange). You won't decrypt it as a beginner, but **certificate clues still help**: self-signed, mismatched name, or brand-new certificates are common for phishing and command servers.

## 1.5 Devices and what they do

| Device | Job | SOC relevance |
|---|---|---|
| Switch | Connects devices inside a network | L3 switches also route between VLANs |
| Router | Connects different networks | Network boundary |
| **Firewall** | Allows or blocks traffic by rules | Its logs are gold |
| Proxy | Middleman for web traffic | Central place to log and filter browsing |
| Load balancer | Spreads traffic over servers | May hide the real client IP unless configured to pass it on |
| IDS / IPS | Detects (IDS) or blocks (IPS) suspicious traffic | Alerts feed the SIEM |

## 1.6 Segmentation: don't keep everything in one room

If an attacker gets into one laptop, segmentation limits where they can go next. This matters a lot for ransomware.

- **VLAN**: splits one physical network into separate logical networks (staff, guests, servers, cameras).
- **DMZ (demilitarized zone)**: a buffer zone for internet-facing servers (web, mail) so that if they're hacked, the internal network is still behind another door.
- **Intranet vs Internet**: trusted inside vs untrusted outside, with firewalls between.
- **Access control lists / firewall rules between segments**: VLANs alone only *separate*. Rules decide who may *cross*.

## 1.7 DNS, DHCP and Wi-Fi access points

- **DNS** turns names (`example.com`) into IPs. Attackers abuse it: random-looking subdomains, huge numbers of lookups, or brand-new domains can mean hidden command traffic or data theft ("DNS tunnelling").
- **DHCP** hands out IP addresses automatically. **DHCP logs tell you which device had which IP at what time.** That's essential for answering "which laptop was that?"
- **Access points (Wi-Fi)**: where wireless devices join the network. Watch for rogue (unauthorised) access points and weak encryption.

## 1.8 Data exfiltration and URL filtering

**Exfiltration** = data leaving the organization when it shouldn't. It rarely looks dramatic. Think: big uploads at odd hours, traffic to newly registered domains or personal cloud storage, unusual DNS volume. **URL filtering** and proxy logs help you block and spot these.

## 1.9 Other words you'll hear
- **Sandbox**: a safe, isolated box where suspicious files are run and watched
- **User enumeration**: attacker tricks a login page into revealing which usernames exist
- **VPN**: encrypted tunnel to the company network (a common attack target)

## ✅ After this page you should be able to
- Tell a private IP from a public one and read `/24`
- Name 8+ common ports and what they do
- Explain the 3-way handshake and what a SYN flood looks like
- Explain why VLAN + firewall rules together limit attacker movement
- Say why DNS and HTTPS are popular hiding places for attackers
