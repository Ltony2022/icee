# DNS Proxy

`dns_proxy.py` is a small UDP DNS proxy that:

- logs incoming DNS queries and outgoing DNS responses (including queried domain)
- blocks configured domains (and their subdomains) by returning `NXDOMAIN`

## Run

```bash
python proxy/dns_proxy.py --listen-host 127.0.0.1 --listen-port 5353 --upstream-host 1.1.1.1 --upstream-port 53
```

Write logs to a file too:

```bash
python proxy/dns_proxy.py --listen-host 127.0.0.1 --listen-port 53 --block-file proxy/blocked_domains.txt --log-file proxy/dns_proxy.log --log-level INFO
```

## Block Domains

Block from CLI:

```bash
python proxy/dns_proxy.py --block facebook.com --block ads.example.com
```

Block from file:

```bash
python proxy/dns_proxy.py --block-file proxy/blocked_domains.txt
```

`blocked_domains.txt` format:

```text
# comments are allowed
facebook.com
doubleclick.net
```

## Notes

- default listen port is `5353` to avoid privileged-port requirements
- change your client DNS to `127.0.0.1:5353` while testing
- Windows system DNS only uses port `53`; for full system-wide interception, run proxy on `127.0.0.1:53`
