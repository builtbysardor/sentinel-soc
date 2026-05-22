# Contributing to Sentinel SOC

## Setup

```bash
git clone https://github.com/builtbysardor/sentinel-soc.git
cd sentinel-soc
pip install -r requirements.txt
python main.py
# → http://localhost:8000
```

## Detection Rules

Rules are defined in `main.py`. Each rule has:
- **pattern**: regex matching log entries
- **severity**: critical / high / medium / info
- **category**: ssh / sqli / xss / ddos / etc.

To add a new rule, extend the `DETECTION_RULES` list.

## Running on Custom Logs

Pass your log file via query param: `?logfile=/var/log/auth.log`
