import { Server } from "socket.io";

export default function handler(req, res) {
  if (!res.socket.server.io) {
    console.log("🔌 New Socket.io server...");
    const io = new Server(res.socket.server);
    res.socket.server.io = io;

    io.on("connection", (socket) => {
      socket.on("offer", (data) => socket.broadcast.emit("offer", data));
      socket.on("answer", (data) => socket.broadcast.emit("answer", data));
      socket.on("ice", (data) => socket.broadcast.emit("ice", data));
    });
  }
  res.end();
}
