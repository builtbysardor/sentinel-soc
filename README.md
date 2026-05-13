<div align="center">

# 🛡️ SentinelLog v2.0 — Real-Time SOC Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=ffdd54" />
  <img src="https://img.shields.io/badge/WebSocket-Real--time-010101?style=for-the-badge&logo=socketdotio&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/builtbysardor/sentinellog-real-time-threat-detection?style=flat-square" />
  <img src="https://img.shields.io/github/forks/builtbysardor/sentinellog-real-time-threat-detection?style=flat-square" />
  <img src="https://img.shields.io/github/last-commit/builtbysardor/sentinellog-real-time-threat-detection?style=flat-square" />
  <img src="https://img.shields.io/badge/Auto--Block-85%2B_Score-red?style=flat-square" />
  <img src="https://img.shields.io/badge/Latency-Milliseconds-brightgreen?style=flat-square" />
</p>

<br/>

> **Professional-grade Security Operations Center (SOC) dashboard** — detects, visualizes, and mitigates  
> network threats in milliseconds via FastAPI backend + WebSocket streaming + cyberpunk UI.

<br/>

**[🚀 Quick Start](#-quick-start) • [📡 API Docs](#-api-reference) • [🛡️ Detection Logic](#️-security-logic) • [🤝 Contribute](#-contributing)**

</div>

---

## 📸 Dashboard Preview

<div align="center">

![Demo Video](screenshots/demo_video.webp)
*Real-time dashboard — log streaming, modal analysis & premium notifications*

![Main Dashboard](screenshots/dashboard_main.png)
*Full-scale monitoring console with live threat metrics*

</div>

---

## ⚡ Key Features

| Feature | Description |
|---------|-------------|
| 🕵️ **Intelligent Threat Detection** | SSH Brute-force · SQL Injection · Port Scanning · Privilege Escalation · DDoS |
| 📡 **Reactive WebSocket Stream** | Instant log delivery with automatic reconnection logic |
| 📊 **Advanced Analytics** | Attack type distribution charts + 12-minute activity heatmaps |
| 🚫 **Auto-Blocking** | IPs scoring 85+ are automatically blacklisted |
| 🎨 **Cyberpunk UI** | Dark glassmorphism interface with smooth micro-animations |
| 📑 **JSON Export** | Export live log data for forensic analysis |
| 🔁 **Auto-Reconnect** | WebSocket client auto-reconnects on disconnect |
| 📋 **Threat Modal** | Deep-dive analysis panel for any suspicious event |

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI (Python) | High-concurrency API & detection logic |
| **Real-time** | WebSockets | Low-latency bi-directional streaming |
| **Frontend** | Vanilla JS / CSS3 | Modern UI without framework overhead |
| **Detection** | Pattern Matching | Heuristic threat identification |
| **Analytics** | Map-Reduce | Real-time statistical aggregation |

---

## 🛡️ Security Logic

Threats are scored using a weighted mechanism:

```
Score Range  │  Classification        │  Action
─────────────┼────────────────────────┼──────────────────────
  0 – 30     │  Normal Traffic        │  ✅ Log as INFO
 40 – 70     │  Suspicious Activity   │  ⚠️  Log as WARNING
 80 – 100    │  High-Confidence Attack│  🚨 CRITICAL + Auto-block (85+)
```

**Detected Attack Types:**
- 🔐 **SSH Brute-force** — multiple failed auth attempts from same IP
- 💉 **SQL Injection** — malicious query patterns in request payloads
- 🔍 **Port Scanning** — sequential port probe detection
- ⬆️ **Privilege Escalation** — unauthorized sudo/root access attempts
- 💥 **DDoS** — abnormal request rate from single source

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/builtbysardor/sentinellog-real-time-threat-detection.git
cd sentinellog-real-time-threat-detection
```

### 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

### 3. Launch

```bash
python3 main.py
```

Open **http://localhost:8000** — dashboard loads instantly! 🎯

---

## 📡 API Reference

### WebSocket

| Endpoint | Description |
|----------|-------------|
| `WS /ws/logs` | Real-time bi-directional threat log stream |

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/logs` | Fetch most recent 200 security events |
| `GET` | `/api/stats` | Global system telemetry snapshot |
| `POST` | `/api/block/{ip}` | Manually blacklist a source IP |
| `GET` | `/api/blocked` | List all currently blacklisted IPs |

---

## 📁 Project Structure

```
sentinellog-real-time-threat-detection/
├── main.py                  # 🚀 FastAPI app entry point
├── detector.py              # 🔍 Threat pattern matching engine
├── websocket_manager.py     # 📡 WebSocket connection manager
├── requirements.txt         # 📦 Python dependencies
├── frontend/
│   ├── index.html           # Dashboard UI
│   ├── style.css            # Cyberpunk glassmorphism theme
│   └── app.js               # WebSocket client & charts
├── screenshots/
│   ├── demo_video.webp      # Live demo recording
│   └── dashboard_main.png   # Dashboard screenshot
└── README.md
```

---

## 🔮 Roadmap

- [ ] 🗄️ **Persistent storage** — SQLite/PostgreSQL event history
- [ ] 📧 **Email alerts** — SMTP notifications for critical threats
- [ ] 💬 **Telegram bot** — instant mobile threat notifications
- [ ] 🌍 **GeoIP mapping** — visualize threat origins on world map
- [ ] 🐳 **Docker support** — one-command containerized deployment
- [ ] 📊 **ML detection** — scikit-learn anomaly detection model
- [ ] 🔐 **Auth layer** — password-protected dashboard access
- [ ] 📄 **PDF reports** — automated daily/weekly threat summaries

---

## 🤝 Contributing

1. Fork the repo
2. Create your branch: `git checkout -b feature/AmazingFeature`
3. Commit: `git commit -m 'Add AmazingFeature'`
4. Push: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ by [Sardor Buriyev](https://github.com/builtbysardor)**

*FastAPI · WebSockets · Python · Cyberpunk UI*

⭐ **Star this repo if SentinelLog is watching over your network!**

</div>
