# WebSockets and Real-Time Systems Complete Reference


---

# CHAPTER 1: REAL-TIME COMMUNICATION OVERVIEW


## Remarks

Real-time communication enables instant data flow between clients and servers without repeated polling. Chat apps, live dashboards, multiplayer games, collaborative editing, stock tickers, and notifications all require real-time. Choosing the right protocol depends on direction (one-way vs bidirectional), scale, browser support, and complexity requirements.

Key concepts: **WebSockets** (full-duplex TCP), **Server-Sent Events** (one-way server → client), **Long Polling** (HTTP-based fallback), **Socket.IO** (WebSocket abstraction with fallbacks), **MQTT** (IoT lightweight pub/sub), **WebRTC** (peer-to-peer audio/video/data), **Pub/Sub** (publish-subscribe pattern), **Presence** (who is online), **Backpressure** (handling slow consumers).


## Protocol Comparison

```
POLLING (traditional):
  Client sends HTTP request every N seconds.
  Simple but wasteful — most responses are "no new data."
  Latency: up to N seconds.
  Server load: proportional to clients × poll frequency.
  Use: legacy systems, very simple needs.

LONG POLLING:
  Client sends request → server HOLDS until data available → responds.
  Client immediately sends another request.
  Better latency than polling, still HTTP overhead per message.
  Use: fallback when WebSocket unavailable.

SERVER-SENT EVENTS (SSE):
  Server → Client only (unidirectional).
  Uses standard HTTP. Browser auto-reconnects.
  Simple, text-based (event stream).
  Use: notifications, live feeds, stock tickers, log streaming.

WEBSOCKET:
  Full-duplex bidirectional over single TCP connection.
  Low latency, low overhead after handshake.
  Binary and text support.
  Use: chat, gaming, collaborative editing, any bidirectional need.

COMPARISON:
  Feature          Polling    Long Poll   SSE         WebSocket
  ──────────────────────────────────────────────────────────────
  Direction        Client→S   Client→S    Server→C    Both
  Latency          High       Medium      Low         Lowest
  Overhead         High       Medium      Low         Lowest
  Complexity       Simple     Simple      Simple      Medium
  Browser support  All        All         All modern  All modern
  Auto-reconnect   Manual     Manual      Built-in    Manual
  Binary data      No         No          No          Yes
  HTTP compatible  Yes        Yes         Yes         Upgrade
  Through proxies  Easy       Easy        Easy        Sometimes issues
```


---

# CHAPTER 2: WEBSOCKETS


## WebSocket Protocol

```
HANDSHAKE (HTTP Upgrade):

Client:
  GET /chat HTTP/1.1
  Host: server.example.com
  Upgrade: websocket
  Connection: Upgrade
  Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
  Sec-WebSocket-Version: 13

Server:
  HTTP/1.1 101 Switching Protocols
  Upgrade: websocket
  Connection: Upgrade
  Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

After handshake: raw TCP frames (no HTTP overhead).

FRAME FORMAT:
  Opcode: text (0x1), binary (0x2), close (0x8), ping (0x9), pong (0xA)
  Payload: actual data
  Mask: client frames must be masked (security)
  
  Overhead per message: 2-14 bytes (vs ~800 bytes for HTTP headers!)

LIFECYCLE:
  1. Client initiates HTTP Upgrade request
  2. Server accepts → 101 Switching Protocols
  3. Both sides send frames freely (bidirectional)
  4. Either side can send Close frame
  5. Connection terminated
```


## Python WebSocket Server

```python
# pip install websockets

import asyncio
import websockets
import json

# Connected clients
clients = set()

async def handler(websocket):
    # Register client
    clients.add(websocket)
    try:
        # Send welcome
        await websocket.send(json.dumps({
            "type": "welcome",
            "message": "Connected!",
            "online": len(clients),
        }))

        # Broadcast join
        await broadcast({
            "type": "user_joined",
            "online": len(clients),
        })

        # Handle messages
        async for message in websocket:
            data = json.loads(message)
            await handle_message(websocket, data)

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Unregister client
        clients.discard(websocket)
        await broadcast({
            "type": "user_left",
            "online": len(clients),
        })


async def handle_message(sender, data):
    match data.get("type"):
        case "chat":
            await broadcast({
                "type": "chat",
                "user": data.get("user", "Anonymous"),
                "message": data["message"],
            })
        case "typing":
            await broadcast({
                "type": "typing",
                "user": data["user"],
            }, exclude=sender)
        case "ping":
            await sender.send(json.dumps({"type": "pong"}))


async def broadcast(data, exclude=None):
    message = json.dumps(data)
    targets = [c for c in clients if c != exclude]
    if targets:
        await asyncio.gather(
            *[client.send(message) for client in targets],
            return_exceptions=True,
        )


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server on ws://0.0.0.0:8765")
        await asyncio.Future()   # Run forever

asyncio.run(main())
```


## JavaScript WebSocket Client

```javascript
// Browser WebSocket API (built-in, no library needed)
class WebSocketClient {
    constructor(url) {
        this.url = url;
        this.handlers = {};
        this.reconnectDelay = 1000;
        this.maxReconnectDelay = 30000;
        this.connect();
    }

    connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
            console.log('Connected');
            this.reconnectDelay = 1000;   // Reset on success
            this.emit('connected');
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.emit(data.type, data);
            } catch (e) {
                console.error('Invalid message:', event.data);
            }
        };

        this.ws.onclose = (event) => {
            console.log(`Disconnected: ${event.code} ${event.reason}`);
            this.emit('disconnected');
            this.reconnect();
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    reconnect() {
        console.log(`Reconnecting in ${this.reconnectDelay}ms...`);
        setTimeout(() => {
            this.reconnectDelay = Math.min(
                this.reconnectDelay * 2,
                this.maxReconnectDelay
            );
            this.connect();
        }, this.reconnectDelay);
    }

    send(type, data = {}) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ type, ...data }));
        }
    }

    on(event, callback) {
        if (!this.handlers[event]) this.handlers[event] = [];
        this.handlers[event].push(callback);
    }

    emit(event, data) {
        (this.handlers[event] || []).forEach(cb => cb(data));
    }

    close() {
        this.ws.close();
    }
}

// Usage
const ws = new WebSocketClient('wss://api.example.com/ws');

ws.on('connected', () => console.log('Online!'));
ws.on('chat', (data) => displayMessage(data.user, data.message));
ws.on('typing', (data) => showTypingIndicator(data.user));
ws.on('user_joined', (data) => updateOnlineCount(data.online));

ws.send('chat', { user: 'Alice', message: 'Hello everyone!' });
ws.send('typing', { user: 'Alice' });
```


## WebSocket with FastAPI

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket)
    await manager.broadcast({"type": "join", "user": user_id})
    try:
        while True:
            data = await websocket.receive_json()
            data["user"] = user_id
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"type": "leave", "user": user_id})
```


---

# CHAPTER 3: SERVER-SENT EVENTS (SSE)


## SSE Protocol

```
SSE: server pushes events to client over HTTP.
Client opens connection, server streams events.

HTTP RESPONSE:
  Content-Type: text/event-stream
  Cache-Control: no-cache
  Connection: keep-alive

  data: {"message": "Hello"}

  data: {"message": "World"}

  event: notification
  data: {"title": "New order", "id": 123}

  id: 42
  data: {"message": "With ID for resume"}

  : this is a comment (heartbeat)

  retry: 5000

FIELDS:
  data:    payload (multiple data: lines = multiline)
  event:   event type (default: "message")
  id:      event ID (for resume after disconnect)
  retry:   reconnection delay in ms
  :        comment (used as heartbeat to keep connection alive)
```


## SSE Server (Python)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

async def event_generator():
    counter = 0
    while True:
        counter += 1
        data = json.dumps({"count": counter, "time": datetime.utcnow().isoformat()})
        yield f"id: {counter}\ndata: {data}\n\n"
        await asyncio.sleep(1)

@app.get("/events")
async def sse_endpoint():
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",   # Disable Nginx buffering
        },
    )

# Named events
async def notification_generator(user_id: str):
    while True:
        notifications = await get_new_notifications(user_id)
        for notif in notifications:
            yield f"event: notification\ndata: {json.dumps(notif)}\n\n"
        
        # Heartbeat every 30s (keeps connection alive through proxies)
        yield ": heartbeat\n\n"
        await asyncio.sleep(5)
```


## SSE Client (JavaScript)

```javascript
// EventSource API (built-in browser)
const source = new EventSource('/events');

// Default "message" event
source.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

// Named events
source.addEventListener('notification', (event) => {
    const data = JSON.parse(event.data);
    showNotification(data.title, data.body);
});

source.addEventListener('update', (event) => {
    const data = JSON.parse(event.data);
    updateDashboard(data);
});

// Connection events
source.onopen = () => console.log('SSE connected');
source.onerror = (e) => {
    if (source.readyState === EventSource.CLOSED) {
        console.log('SSE connection closed');
    } else {
        console.log('SSE error, will auto-reconnect');
    }
};

// Close connection
source.close();

// With auth (EventSource doesn't support custom headers)
// Use fetch + ReadableStream instead:
async function sseWithAuth(url, token) {
    const response = await fetch(url, {
        headers: { 'Authorization': `Bearer ${token}` },
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = decoder.decode(value);
        // Parse SSE format manually
        const lines = text.split('\n');
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                handleEvent(data);
            }
        }
    }
}
```


---

# CHAPTER 4: SOCKET.IO


## Socket.IO Overview

```
Socket.IO = WebSocket abstraction library with:
  ✅ Automatic reconnection
  ✅ Fallback to long-polling (if WebSocket blocked)
  ✅ Rooms (group clients together)
  ✅ Namespaces (logical separation)
  ✅ Acknowledgements (request-response over WebSocket)
  ✅ Binary support
  ✅ Broadcasting

NOT raw WebSocket — has its own protocol on top.
Socket.IO client can't connect to plain WebSocket server (and vice versa).
```


## Socket.IO Server (Node.js)

```javascript
import { Server } from 'socket.io';
import { createServer } from 'http';

const httpServer = createServer();
const io = new Server(httpServer, {
    cors: { origin: "http://localhost:3000" },
    pingInterval: 25000,
    pingTimeout: 20000,
});

// Connection handler
io.on('connection', (socket) => {
    console.log(`Connected: ${socket.id}`);

    // Join room
    socket.on('join_room', (roomId) => {
        socket.join(roomId);
        socket.to(roomId).emit('user_joined', {
            userId: socket.id,
            room: roomId,
        });
    });

    // Chat message
    socket.on('chat_message', (data) => {
        io.to(data.room).emit('chat_message', {
            user: data.user,
            message: data.message,
            timestamp: Date.now(),
        });
    });

    // Typing indicator
    socket.on('typing', (data) => {
        socket.to(data.room).emit('typing', { user: data.user });
    });

    // Request-response pattern (acknowledgement)
    socket.on('get_history', async (roomId, callback) => {
        const history = await getMessageHistory(roomId);
        callback(history);   // Send response back to client
    });

    // Disconnect
    socket.on('disconnect', (reason) => {
        console.log(`Disconnected: ${socket.id} (${reason})`);
    });
});

// Broadcast to all
io.emit('announcement', { message: 'Server restarting in 5 minutes' });

// Broadcast to room (excluding sender)
socket.to('room1').emit('event', data);

// Broadcast to room (including sender)
io.to('room1').emit('event', data);

// To specific client
io.to(socketId).emit('private', data);

httpServer.listen(3001);
```


## Socket.IO Client

```javascript
import { io } from 'socket.io-client';

const socket = io('http://localhost:3001', {
    auth: { token: 'user-jwt-token' },
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 10,
});

socket.on('connect', () => {
    console.log('Connected:', socket.id);
    socket.emit('join_room', 'general');
});

socket.on('chat_message', (data) => {
    displayMessage(data.user, data.message, data.timestamp);
});

socket.on('typing', (data) => {
    showTypingIndicator(data.user);
});

// Send with acknowledgement (request-response)
socket.emit('get_history', 'general', (history) => {
    console.log('Got history:', history.length, 'messages');
    history.forEach(msg => displayMessage(msg.user, msg.message));
});

socket.on('disconnect', (reason) => {
    console.log('Disconnected:', reason);
});
```


---

# CHAPTER 5: MQTT (IoT MESSAGING)


## MQTT Protocol

```
MQTT (Message Queuing Telemetry Transport):
  Lightweight pub/sub protocol for IoT and constrained devices.
  Very low bandwidth (2-byte minimum header).
  TCP-based, supports TLS.
  Used by: AWS IoT, Azure IoT Hub, Facebook Messenger.

CONCEPTS:
  Broker:     central server (routes messages)
  Client:     publisher or subscriber (or both)
  Topic:      hierarchical string (home/livingroom/temperature)
  QoS levels:
    0: At most once (fire and forget)
    1: At least once (may duplicate)
    2: Exactly once (guaranteed, slower)
  
  Retained message: broker stores last message per topic.
    New subscriber immediately gets latest value.
  
  Last Will (LWT): message published if client disconnects unexpectedly.
    "device/sensor1/status" → "offline"

TOPIC PATTERNS:
  home/livingroom/temperature     Exact topic
  home/+/temperature              + = single level wildcard
  home/#                          # = multi-level wildcard (all under home/)
```

```python
# pip install paho-mqtt

import paho.mqtt.client as mqtt
import json

# Publisher
client = mqtt.Client()
client.connect("broker.example.com", 1883)

# Publish sensor data
client.publish(
    "sensors/temperature/livingroom",
    json.dumps({"value": 22.5, "unit": "celsius"}),
    qos=1,
    retain=True,   # New subscribers get latest value
)

# Subscriber
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    print(f"Topic: {msg.topic}, Data: {data}")

client = mqtt.Client()
client.on_message = on_message
client.connect("broker.example.com", 1883)
client.subscribe("sensors/#", qos=1)   # All sensor topics
client.loop_forever()
```


---

# CHAPTER 6: SCALING REAL-TIME SYSTEMS


## Scaling WebSockets

```
PROBLEM: One server can handle ~10K-100K concurrent WebSocket connections.
Need millions? Must scale horizontally.

CHALLENGE: WebSocket connections are STATEFUL.
User A on Server 1 sends message to User B on Server 2.
Server 1 doesn't know about User B!

SOLUTION: Pub/Sub backplane (Redis, NATS, Kafka)

  Client A ←→ Server 1 ←→ Redis Pub/Sub ←→ Server 2 ←→ Client B
  
  Server 1 publishes message to Redis.
  Server 2 receives from Redis, sends to Client B.

ARCHITECTURE:
  Load Balancer (sticky sessions or IP hash)
      ├── WS Server 1 (handles 50K connections)
      ├── WS Server 2 (handles 50K connections)
      ├── WS Server 3 (handles 50K connections)
      └── All connected to Redis Pub/Sub

STICKY SESSIONS:
  WebSocket connections must stay on same server.
  Load balancer uses: IP hash, cookie, or connection ID.
  Nginx: ip_hash or sticky cookie.
  
CONNECTION LIMITS:
  File descriptors: ulimit -n 65535
  Ephemeral ports: net.ipv4.ip_local_port_range
  Memory: each connection uses ~10-50 KB
  100K connections × 50 KB = ~5 GB RAM just for connections
```

```python
# Redis pub/sub backplane for scaling WebSockets
import redis.asyncio as aioredis

redis = aioredis.from_url("redis://localhost")

async def publish_to_channel(channel: str, message: dict):
    await redis.publish(channel, json.dumps(message))

async def subscribe_to_channel(channel: str):
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            # Forward to local WebSocket clients
            await broadcast_local(channel, data)

# When client sends message:
#   1. Server receives via WebSocket
#   2. Server publishes to Redis channel
#   3. ALL servers subscribed to channel receive it
#   4. Each server forwards to their local clients
```


---

# CHAPTER 7: COMMON PITFALLS


## Real-Time System Pitfalls

```
PITFALL 1: No reconnection logic
  Network blip → connection lost → user sees nothing.
  Fix: auto-reconnect with exponential backoff + jitter.

PITFALL 2: No heartbeat/ping
  Stale connections accumulate (client disconnected but server doesn't know).
  Fix: ping/pong every 25-30 seconds. Close if no pong received.

PITFALL 3: Sending too much data
  Broadcasting every keystroke to 10K users.
  Fix: debounce/throttle, send diffs not full state, compress.

PITFALL 4: No authentication on WebSocket
  Anyone can connect and receive messages.
  Fix: authenticate during handshake (token in query param or first message).

PITFALL 5: No message ordering guarantees
  Messages arrive out of order.
  Fix: sequence numbers, timestamps, or ordered message queues.

PITFALL 6: Blocking the event loop
  CPU-heavy work in WebSocket handler → all connections stall.
  Fix: offload to worker thread/process, keep handlers async and fast.

PITFALL 7: Memory leaks from connections
  Not cleaning up disconnected clients → memory grows.
  Fix: proper cleanup in disconnect handler. Monitor connection count.

PITFALL 8: No backpressure
  Server sends faster than client can consume → buffer grows → OOM.
  Fix: monitor send buffer, drop messages or disconnect slow clients.

PITFALL 9: Using WebSocket when SSE suffices
  Server → client only (notifications, feeds) → SSE is simpler.
  Fix: use SSE for unidirectional. WebSocket only when bidirectional needed.

PITFALL 10: Not handling reconnect state
  Client reconnects but misses messages during disconnect.
  Fix: message IDs + "catch up" on reconnect (send missed messages).

PITFALL 11: Proxy/firewall issues
  Some corporate proxies kill WebSocket connections.
  Fix: Socket.IO (auto-fallback), or wss:// (TLS usually passes through).

PITFALL 12: Single server bottleneck
  All connections on one server → can't scale.
  Fix: Redis/NATS pub/sub backplane, sticky sessions on load balancer.
```