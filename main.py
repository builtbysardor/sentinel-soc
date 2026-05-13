"""
SentinelLog - Real-time Threat Detection System
FastAPI Backend with WebSocket Support
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import random
from datetime import datetime
from typing import List, Dict
import uuid

app = FastAPI(title="SentinelLog API", version="2.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
logs: List[Dict] = []
active_connections: List[WebSocket] = []
blocked_ips: set = set()
threat_counters: Dict[str, int] = {}
stats = {
    "eps": 0.0,
    "activeThreats": 0,
    "blockedIps": 0,
    "criticalCount": 0
}

# Threat detection patterns
THREAT_PATTERNS = {
    "ssh_brute": {
        "keywords": ["Failed password", "Invalid user", "authentication failure"],
        "threshold": 10,
        "severity": "critical"
    },
    "sqli": {
        "keywords": ["UNION SELECT", "DROP TABLE", "' OR '1'='1", "--", "/**/"],
        "threshold": 1,
        "severity": "critical"
    },
    "port_scan": {
        "keywords": ["SYN_RECV", "connection attempt", "port scan"],
        "threshold": 100,
        "severity": "warning"
    },
    "priv_esc": {
        "keywords": ["sudo -l", "/etc/passwd", "SUID", "chmod 777"],
        "threshold": 1,
        "severity": "critical"
    },
    "ddos": {
        "keywords": ["rate limit", "too many requests", "flood"],
        "threshold": 500,
        "severity": "critical"
    }
}

# Demo log templates
DEMO_TEMPLATES = [
    {
        "type": "ssh_brute",
        "messages": [
            "Failed password for root from {ip} port 22 ssh2",
            "Invalid user admin from {ip} port 22",
            "authentication failure for user root from {ip}",
            "Disconnecting invalid user test {ip} port 22: Too many authentication failures"
        ]
    },
    {
        "type": "sqli",
        "messages": [
            "SQL Injection attempt detected: UNION SELECT * FROM users WHERE '1'='1'",
            "Malicious query blocked: DROP TABLE users; --",
            "SQL pattern match: ' OR 1=1 -- in request parameter",
            "Database attack prevented: /**/ UNION /**/ SELECT password FROM admin"
        ]
    },
    {
        "type": "port_scan",
        "messages": [
            "Port scan detected from {ip}: {count} ports scanned in 60 seconds",
            "SYN flood detected from {ip}: {count} connection attempts",
            "Nmap scan signature detected from {ip}",
            "Multiple port probing from {ip}: ports 21,22,23,25,80,443,3306,8080"
        ]
    },
    {
        "type": "priv_esc",
        "messages": [
            "Unauthorized sudo execution attempt by user {user}",
            "Suspicious file access: /etc/shadow read attempt",
            "SUID binary execution detected: /usr/bin/passwd",
            "Privilege escalation attempt: chmod 777 /etc/sudoers"
        ]
    },
    {
        "type": "ddos",
        "messages": [
            "DDoS attack detected: {count} requests/sec from {ip}",
            "Rate limit exceeded: {ip} blocked for 1 hour",
            "HTTP flood detected from {ip}: {count} requests in 10 seconds",
            "Application layer DDoS from {ip}: repeated POST requests"
        ]
    },
    {
        "type": "normal",
        "messages": [
            "Successful SSH login for user admin from {ip}",
            "User {user} logged in successfully",
            "API request completed successfully from {ip}",
            "Database query executed: SELECT * FROM logs LIMIT 100"
        ]
    }
]

DEMO_IPS = [
    "218.92.0.115",     # CN
    "103.45.12.88",     # IN
    "45.142.212.61",    # RU
    "185.220.101.5",    # DE
    "94.102.49.190",    # UA
    "192.168.1.100",    # Local
    "10.0.0.50",        # Local
    "172.16.0.200"      # Local
]

COUNTRIES = {
    "218.92.0.115": "CN",
    "103.45.12.88": "IN",
    "45.142.212.61": "RU",
    "185.220.101.5": "DE",
    "94.102.49.190": "UA",
    "192.168.1.100": "US",
    "10.0.0.50": "US",
    "172.16.0.200": "US"
}

def generate_log() -> Dict:
    """Generate a realistic demo log entry"""
    template = random.choice(DEMO_TEMPLATES)
    log_type = template["type"]
    message_template = random.choice(template["messages"])
    
    ip = random.choice(DEMO_IPS)
    
    # Generate message
    message = message_template.format(
        ip=ip,
        count=random.randint(50, 1000),
        user=random.choice(["admin", "root", "user", "test"])
    )
    
    # Determine severity
    if log_type == "normal":
        severity = "info"
        score = random.randint(0, 30)
    else:
        severity = "critical" if random.random() > 0.6 else "warning"
        score = random.randint(60, 100) if severity == "critical" else random.randint(40, 70)
    
    # Check if should be auto-blocked
    blocked = severity == "critical" and score >= 85 and ip not in ["192.168.1.100", "10.0.0.50", "172.16.0.200"]
    
    if blocked:
        blocked_ips.add(ip)
    
    log_entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ip": ip,
        "type": log_type,
        "severity": severity,
        "message": message,
        "detail": f"Full log trace for {log_type} event from {ip}",
        "score": score,
        "country": COUNTRIES.get(ip, "US"),
        "blocked": blocked
    }
    
    return log_entry

def analyze_threat(log: Dict) -> bool:
    """Analyze if log entry is a threat"""
    if log["severity"] == "critical":
        stats["criticalCount"] += 1
        stats["activeThreats"] += 1
        return True
    return False

async def broadcast_log(log: Dict):
    """Broadcast new log to all connected WebSocket clients"""
    message = json.dumps({
        "event": "new_log",
        "data": log
    })
    
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except:
            disconnected.append(connection)
    
    # Remove disconnected clients
    for conn in disconnected:
        active_connections.remove(conn)

async def broadcast_threat_alert(log: Dict):
    """Broadcast threat alert to all clients"""
    action = "auto_blocked" if log["blocked"] else "monitoring"
    
    message = json.dumps({
        "event": "threat_alert",
        "threat": log,
        "action": action
    })
    
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except:
            pass

async def log_generator():
    """Background task to generate logs continuously with controlled threat frequency"""
    last_threat_time = 0
    while True:
        # Generate 1-2 logs per batch
        num_logs = random.randint(1, 2)
        for _ in range(num_logs):
            # Force a 'normal' log most of the time
            # Only allow a threat roughly every 60 seconds
            current_time = asyncio.get_event_loop().time()
            if current_time - last_threat_time > 15:
                log = generate_log() # This can be a threat or normal
                if log["severity"] != "info":
                    last_threat_time = current_time
            else:
                # Force normal log
                log = generate_log()
                if log["severity"] != "info":
                    log["type"] = "normal"
                    log["severity"] = "info"
                    log["score"] = random.randint(0, 30)
                    log["message"] = f"System health check: services operational from {log['ip']}"
            
            logs.insert(0, log)
            
            # Keep only last 500 logs
            if len(logs) > 500:
                logs.pop()
            
            # Update stats
            is_threat = analyze_threat(log)
            if log["blocked"]:
                stats["blockedIps"] = len(blocked_ips)
            
            # Calculate EPS (lower it slightly to look more realistic)
            stats["eps"] = round(random.uniform(1.0, 5.0), 1)
            
            # Broadcast to clients
            await broadcast_log(log)
            
            if is_threat:
                await broadcast_threat_alert(log)
        
        # Wait 3-7 seconds between batches for a more professional pace
        await asyncio.sleep(random.uniform(3.0, 7.0))

@app.on_event("startup")
async def startup_event():
    """Start background tasks on startup"""
    asyncio.create_task(log_generator())
    print("✅ SentinelLog Backend Started")
    print("📡 WebSocket endpoint: ws://localhost:8001/ws/logs")
    print("🌐 API endpoints: http://localhost:8001/api/*")

@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>index.html not found</h1>", status_code=404)

@app.get("/api/logs")
async def get_logs():
    """Get recent logs"""
    return JSONResponse(content=logs[:200])

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    return JSONResponse(content=stats)

@app.get("/api/threats")
async def get_threats():
    """Get active threats"""
    threats = [log for log in logs if log["severity"] == "critical"]
    return JSONResponse(content=threats[:50])

@app.post("/api/block/{ip}")
async def block_ip(ip: str):
    """Block an IP address"""
    blocked_ips.add(ip)
    stats["blockedIps"] = len(blocked_ips)
    
    # Update all logs from this IP
    for log in logs:
        if log["ip"] == ip:
            log["blocked"] = True
    
    return JSONResponse(content={
        "success": True,
        "message": f"IP {ip} has been blocked",
        "blocked_ips": list(blocked_ips)
    })

@app.get("/api/blocked")
async def get_blocked_ips():
    """Get list of blocked IPs"""
    return JSONResponse(content=list(blocked_ips))

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time log streaming"""
    await websocket.accept()
    active_connections.append(websocket)
    
    print(f"✅ WebSocket client connected. Total connections: {len(active_connections)}")
    
    # Send initial stats
    try:
        await websocket.send_text(json.dumps({
            "event": "stats_update",
            "stats": stats
        }))
    except:
        pass
    
    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("action") == "block_ip":
                ip = message.get("ip")
                if ip:
                    blocked_ips.add(ip)
                    stats["blockedIps"] = len(blocked_ips)
                    await websocket.send_text(json.dumps({
                        "event": "ip_blocked",
                        "ip": ip
                    }))
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"❌ WebSocket client disconnected. Total connections: {len(active_connections)}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
