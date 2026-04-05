# VPS Deployment Guide

This project is cheapest and simplest to deploy on a small VPS because:

- The frontend expects the API at `/api`.
- The backend serves additional assets at `/hosts`.
- The backend uses SQLite, which is easiest to keep on a local disk.

## Recommended Host

Recommended starting point: Hetzner Cloud.

- Lowest entry plan currently shown: about EUR 2.99/month for the cost-optimized tier.
- More practical starting point: about EUR 4.49/month for a regular shared VPS.
- Good fit for this app because one VPS can run Nginx, the FastAPI backend, and the built frontend on the same domain.

Reasonable alternative: DigitalOcean Basic Droplet.

- Starts at about USD 4/month for 512 MiB RAM.
- Safer starting point for this app: USD 6/month for 1 GiB RAM.

Railway is workable, but less ideal for this repo as-is because the app is easier to run behind one reverse proxy and SQLite is simpler on a VPS disk than on a metered platform volume.

## Recommended Shape

Use one Ubuntu VPS with:

- Nginx serving the frontend build.
- Nginx proxying `/api` and `/hosts` to FastAPI on `127.0.0.1:3001`.
- FastAPI managed by `systemd`.
- SQLite stored on the server disk with regular backups.

## Server Requirements

- Ubuntu 24.04 LTS
- 1 vCPU
- 1 GB RAM minimum
- 20 GB disk preferred
- A domain name pointed to the server IP

## Upload And Deploy

These steps assume:

- domain: `app.example.com`
- app path: `/opt/prunounce`
- backend port: `3001`

### 1. Create the server

- Provision an Ubuntu 24.04 VPS.
- Add your SSH key during setup.
- Point your domain's `A` record to the server IP.

### 2. Install packages

```bash
sudo apt update
sudo apt install -y git nginx python3 python3-venv python3-pip nodejs npm
```

If your distro image gives you an old Node version, install Node 20 before building the frontend.

### 3. Upload the app

Using Git:

```bash
sudo mkdir -p /opt/prunounce
sudo chown $USER:$USER /opt/prunounce
git clone https://github.com/GitJakobE/prunounce.git /opt/prunounce
cd /opt/prunounce
```

If the repo is private, upload an SSH deploy key or push a zip/tarball and extract it under `/opt/prunounce`.

### 4. Build the frontend

```bash
cd /opt/prunounce/src/frontend
npm ci
npm run build
```

The built site will be in `/opt/prunounce/src/frontend/dist`.

### 5. Install the backend

```bash
cd /opt/prunounce/src/backend-python
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install poetry
poetry config virtualenvs.create false
poetry install --only main
```

### 6. Create backend environment file

You can start from `src/backend-python/.env.example`.

Create `/opt/prunounce/src/backend-python/.env`:

```env
PORT=3001
JWT_SECRET=replace-with-a-long-random-secret
FRONTEND_URL=https://app.example.com
DATABASE_URL=sqlite:////opt/prunounce/src/backend-python/app.db
```

Notes:

- `FRONTEND_URL` must match your real site URL for CORS.
- The default SQLite path already works, but setting `DATABASE_URL` explicitly is clearer in production.

### 7. Seed the database if needed

If you want the preloaded content on the server:

```bash
cd /opt/prunounce/src/backend-python
source .venv/bin/activate
python seed_data.py
python seed_stories.py
python seed_test_user.py
```

Skip `seed_test_user.py` if you do not want a seeded login in production.

### 8. Create the systemd service

You can start from `deploy/prunounce-backend.service.example`.

Create `/etc/systemd/system/prunounce-backend.service`:

```ini
[Unit]
Description=Prunounce FastAPI backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/prunounce/src/backend-python
EnvironmentFile=/opt/prunounce/src/backend-python/.env
ExecStart=/opt/prunounce/src/backend-python/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 3001
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo chown -R www-data:www-data /opt/prunounce/src/backend-python
sudo systemctl daemon-reload
sudo systemctl enable prunounce-backend
sudo systemctl start prunounce-backend
sudo systemctl status prunounce-backend
```

### 9. Configure Nginx

You can start from `deploy/nginx-prunounce.conf.example`.

Create `/etc/nginx/sites-available/prunounce`:

```nginx
server {
    listen 80;
    server_name app.example.com;

    root /opt/prunounce/src/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:3001/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /hosts/ {
        proxy_pass http://127.0.0.1:3001/hosts/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/prunounce /etc/nginx/sites-enabled/prunounce
sudo nginx -t
sudo systemctl reload nginx
```

### 10. Add HTTPS

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d app.example.com
```

### 11. Verify

Open the site and verify:

- `/` loads the frontend.
- `/api/health` returns `{"status":"ok","database_writable":true,"audio_cache_writable":true}`.
- `/hosts/...` images load.
- Registration and login work.
- Audio and stories work.

## Updating The Server

```bash
cd /opt/prunounce
git pull

cd /opt/prunounce/src/frontend
npm ci
npm run build

cd /opt/prunounce/src/backend-python
source .venv/bin/activate
poetry install --only main

# Restore ownership so the service user can write to the database and audio cache
sudo chown -R www-data:www-data /opt/prunounce/src/backend-python/app.db
sudo chown -R www-data:www-data /opt/prunounce/src/backend-python/audio-cache

sudo systemctl restart prunounce-backend
sudo systemctl reload nginx
```

After restarting, verify the health check returns fully healthy:

```bash
curl -s http://127.0.0.1:3001/api/health
# Expected: {"status":"ok","database_writable":true,"audio_cache_writable":true}
```

If `database_writable` or `audio_cache_writable` is `false`, fix file ownership as shown above.

## Backups

At minimum, back up:

- `/opt/prunounce/src/backend-python/app.db`
- `/opt/prunounce/src/backend-python/audio-cache`

SQLite on one VPS is acceptable for a small app, but you should schedule backups before inviting real users.

## How Long This Stays Valid

This setup remains valid through the early stage of growth if your traffic is still modest and you are optimizing for low cost.

It is still a good fit when:

- You have a small to moderate number of daily users.
- Most traffic is read-heavy.
- Audio files are cached and reused instead of regenerated constantly.
- You can tolerate brief maintenance windows for server upgrades.
- One server outage would be inconvenient but not business-critical.

This setup starts to become a constraint when:

- SQLite write contention becomes noticeable from concurrent signups, progress updates, or content changes.
- Audio generation creates CPU, memory, or network spikes.
- The audio cache grows enough that disk management becomes operational work.
- You need zero-downtime deploys, failover, or multi-region availability.
- You expect marketing spikes or classroom-scale concurrent usage.

## Practical Growth Path

Do not replace everything at once. Upgrade in this order.

### Stage 1: Small growth

Keep the same architecture and just resize the VPS.

- Move from the smallest plan to 2 vCPU and 2 to 4 GB RAM.
- Put backups on a schedule.
- Add basic uptime monitoring and disk alerts.
- Pre-generate popular audio to reduce burst load.

### Stage 2: Moderate growth

Keep one app server, but move the database off SQLite.

- Replace SQLite with managed Postgres.
- Keep frontend and backend on the same VPS or same reverse-proxied domain.
- Move large or frequently accessed audio assets to object storage plus CDN if needed.

This is usually the first real architectural change worth making.

### Stage 3: Higher growth

Split responsibilities.

- Run the backend separately from static frontend hosting.
- Put audio generation onto a background worker or queue.
- Serve cached media from object storage or CDN.
- Run multiple backend instances behind a load balancer.

## Recommended Trigger Points

Start planning the next step when one of these becomes true:

- CPU is regularly above about 60 to 70 percent during busy periods.
- Memory pressure causes swapping or restarts.
- Disk usage from `app.db` and `audio-cache` grows faster than you can comfortably back up.
- Page loads are fine but authenticated actions become inconsistent under concurrent use.
- Deployments or maintenance windows start affecting real users.

## Bottom Line

For this repo today, a cheap VPS is still the right answer.

It is valid for:

- prototype
- pilot
- early production
- modest paid usage

It stops being the right default once reliability, concurrent writes, and audio workload matter more than minimizing monthly cost.

## Why This Is The Best Low-Cost Option For This Repo

- No frontend API rewrite is required because `/api` stays on the same domain.
- No external managed database is required.
- Host media paths at `/hosts` keep working.
- Total monthly cost can stay around EUR 3-5 or about USD 4-6 plus domain.