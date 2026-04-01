import path from "path";
import express from "express";
import cors from "cors";
import helmet from "helmet";
import { config } from "./config.js";
import authRoutes from "./routes/auth.js";
import profileRoutes from "./routes/profile.js";
import dictionaryRoutes from "./routes/dictionary.js";
import searchRoutes from "./routes/search.js";
import audioRoutes from "./routes/audio.js";
import hostsRoutes from "./routes/hosts.js";

const app = express();

app.use(helmet({ crossOriginResourcePolicy: { policy: "cross-origin" } }));
app.use(
  cors({
    origin: config.frontendUrl,
    credentials: true,
  })
);
app.use(express.json());

// Serve static files (host portrait images, etc.)
app.use(express.static(path.join(__dirname, "..", "public")));

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/profile", profileRoutes);
app.use("/api/dictionary", dictionaryRoutes);
app.use("/api/search", searchRoutes);
app.use("/api/audio", audioRoutes);
app.use("/api/hosts", hostsRoutes);

// Health check
app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});

export default app;
