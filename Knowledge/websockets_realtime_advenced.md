# WebSockets Real-Time Reference


---

## Python Server (FastAPI)

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
clients = []

@app.websocket("/ws/{username}")
async def ws_endpoint(ws: WebSocket, username: str):
    await ws.accept()
    clients.append(ws)
    for c in clients: await c.send_text(f"{username} joined")
    try:
        while True:
            data = await ws.receive_text()
            for c in clients: await c.send_text(f"{username}: {data}")
    except WebSocketDisconnect:
        clients.remove(ws)
```


## Node.js Server

```javascript
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });
const clients = new Set();

wss.on('connection', (ws) => {
    clients.add(ws);
    ws.on('message', (data) => {
        for (const c of clients) {
            if (c !== ws && c.readyState === WebSocket.OPEN) c.send(data.toString());
        }
    });
    ws.on('close', () => clients.delete(ws));
});
```


## Client

```javascript
const ws = new WebSocket('ws://localhost:8080');
ws.onopen = () => ws.send('Hello');
ws.onmessage = (e) => console.log('Received:', e.data);
ws.onclose = () => setTimeout(() => connect(), 3000);  // Auto-reconnect
```