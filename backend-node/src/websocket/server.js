// backend-node/src/websocket/server.js
import { WebSocketServer } from "ws";
import http from "http";

// Render / Node 本地都會用 process.env.PORT
const PORT = process.env.PORT || 9000;

// HTTP server (required by Render)
const server = http.createServer();
const wss = new WebSocketServer({ server });

console.log(`🚀 WebSocket server starting on port ${PORT}...`);

// Record all connected clients
let clients = new Set();

// When a client connects
wss.on("connection", (ws) => {
  console.log("🔌 Client connected");
  clients.add(ws);

  ws.on("message", (message) => {
    console.log("📩 Received:", message.toString());
    
    // Broadcast message to all clients (AGV real-time broadcasting)
    for (const client of clients) {
      if (client.readyState === 1) {
        client.send(message.toString());
      }
    }
  });

  ws.on("close", () => {
    console.log("❌ Client disconnected");
    clients.delete(ws);
  });
});

// Start HTTP server (Render will call this)
server.listen(PORT, () => {
  console.log(`✅ WebSocket server running on port ${PORT}`);
});
