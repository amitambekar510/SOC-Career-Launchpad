# 2. Linux Basics for Analysts

You don't need to be a Linux admin. You do need to **move around a server, read logs, and notice what looks wrong.** Many servers, log collectors and security tools run on Linux.

## 2.1 Where things live

| Folder | What's in it |
|---|---|
| `/etc` | Configuration files |
| `/var/log` | Most logs (your main hunting ground) |
| `/home` | User files |
| `/tmp` | Temporary files. Attackers love dropping tools here |
| `/bin`, `/usr/bin` | Programs |
| `/root` | The admin user's home |
| `/etc/passwd`, `/etc/shadow` | User accounts, password hashes |

## 2.2 Commands to practice

**Moving and reading**

| Command | Does |
|---|---|
| `pwd` | Where am I? |
| `ls -la` | List everything, including hidden files |
| `cd <folder>` | Go somewhere |
| `cat`, `less` | Read a file |
| `tail -f <file>` | Watch a log live |
| `grep "text" <file>` | Find lines containing text. **Your best friend** |
| `find / -name "x"` | Search for files |

**Investigating a machine**

| Command | Answers |
|---|---|
| `ps aux` | What's running? |
| `top` / `htop` | What's using resources right now? |
| `ss -tulnp` or `netstat -tulnp` | What's listening and who's connected? |
| `who`, `last` | Who's logged in? Who logged in before? |
| `history` | What commands were typed? (can be wiped by an attacker) |
| `systemctl status <svc>` | Is a service running? |
| `crontab -l` | What's scheduled? |

**Permissions**

- `rwx` = read, write, execute for **owner / group / others**
- `chmod 755 file` = owner can do everything, others can read and run
- `sudo` = run one command with admin rights (logged in auth logs)

> **First four commands on a suspicious Linux host:** `ps aux`, `ss -tulnp`, `last`, `history`. They answer *what's running, what's connected, who came in, what did they type.*

## 2.3 The logs that matter

| Log | What it tells you |
|---|---|
| `/var/log/auth.log` (Debian/Ubuntu) or `/var/log/secure` (RHEL/CentOS) | Logins, SSH, sudo. Brute force shows up here |
| `/var/log/syslog` or `/var/log/messages` | General system events |
| `/var/log/kern.log` | Kernel events |
| `/var/log/cron` | Scheduled jobs (a common place for persistence) |
| `/var/log/nginx/`, `/var/log/apache2/` or `httpd` | Web server access and errors |

Try it (in your own lab): count failed SSH logins by source IP

```bash
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr | head
```

## 2.4 Signs of compromise on Linux

- Unknown entries in `crontab` or `/etc/cron.d`
- New SSH keys in `~/.ssh/authorized_keys`
- New user accounts, or another account with UID 0 (root power)
- Strange SUID programs (programs that run with the owner's power)
- New services you can't match to known software
- Outbound connections from processes that shouldn't talk to the internet

## ✅ After this page you should be able to
- Find the right log for "who logged in via SSH?"
- Use `grep`, `tail -f`, `ps`, `ss` comfortably
- Name 3 ways attackers stay on a Linux machine (persistence)
- Explain why unexpected sudo or new admin accounts matter
