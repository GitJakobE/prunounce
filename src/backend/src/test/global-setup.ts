import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

export function setup() {
  const backendRoot = path.resolve(
    path.dirname(fileURLToPath(import.meta.url)),
    "../.."
  );
  // Push schema to test database before all test files
  execSync("npx prisma db push --force-reset --skip-generate", {
    env: { ...process.env, DATABASE_URL: "file:./test.db" },
    cwd: backendRoot,
    stdio: "inherit",
  });
}
