import dotenv from "dotenv";
dotenv.config();

export const config = {
  port: parseInt(process.env.PORT || "3001", 10),
  jwtSecret: process.env.JWT_SECRET || "change-me",
  jwtExpiresIn: "30d",
  googleClientId: process.env.GOOGLE_CLIENT_ID || "",
  googleClientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
  audioCacheDir: process.env.AUDIO_CACHE_DIR || "./audio-cache",
  frontendUrl: process.env.FRONTEND_URL || "http://localhost:5173",
};
