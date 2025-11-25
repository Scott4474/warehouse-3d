import { WebSocketServer } from "ws";

const PORT = process.env.WS_PORT || 18080;
const wss = new WebSocketServer({ port: PORT });

console.log(`📡 WebSocket server running at ws://0.0.0.0:${PORT}`);

wss.on("connection", (ws) => {
    console.log("🔌 Client connected");

    ws.on("close", () => console.log("❌ Client disconnected"));
});

export function broadcast(message) {
    const msg = JSON.stringify(message);
    wss.clients.forEach((client) => {
        if (client.readyState === 1) {
            client.send(msg);
        }
    });
}