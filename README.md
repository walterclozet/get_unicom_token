# China Unicom Token Extractor (`get_unicom_token`)

A lightweight Python tool to retrieve `token_online` and `appId` for China Unicom automated tasks (e.g., Qinglong panel scripts).

### Why This Tool?
Direct password logins and CLI SMS requests often trigger anti-bot slide CAPTCHAs (Error `[2]`). This tool bypasses the CAPTCHA by utilizing the universal 6-digit SMS code requested directly from the official **China Unicom App**, submitting it to `radomLogin.htm` to exchange for credentials.

---

## Prerequisites & Installation

### 1. Requirements
- Python 3.8+
- Required packages: `requests`, `pycryptodome`

Install via pip:
```bash
pip install requests pycryptodome
```

    Note for Linux Users (PEP 668):

    Modern Linux distributions (Ubuntu 23.04+, Debian 12+) require a virtual environment:
    Bash

    python3 -m venv .venv
    source .venv/bin/activate
    pip install requests pycryptodome

Usage

    Run the script:

```Bash
    python get_unicom_token.py
    Enter your 11-digit China Unicom mobile number.
```

    Open the China Unicom Official App, navigate to the login page, enter your number, and tap "Get Verification Code" (获取验证码).

    Enter the 6-digit SMS code into the terminal when prompted.

    Copy the generated credential string and paste it into your Qinglong environment variable chinaUnicomCookie.

Output Format

The output string is formatted as:
Plaintext

<token_online>#<appId>#<mobile>

Example:
Plaintext

chinaUnicomCookie="a3e4c1ff2xxxxxxxxx#912d30xxxxxx#18600000000"
