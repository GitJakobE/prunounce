import { Router, Response } from "express";
import { HOSTS } from "../hosts.js";

const router = Router();

// GET /api/hosts
router.get("/", (_req, res: Response): void => {
  res.json({ hosts: HOSTS });
});

export default router;
