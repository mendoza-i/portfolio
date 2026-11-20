# like-api: the like counter

A tiny service that stores the portfolio's like count. It runs on the M710q next to Nginx. No dependencies: one Python file plus SQLite.

- `GET /api/likes` returns `{"count": 12}`
- `POST /api/like` adds one like per visitor and returns `{"count": 13, "new": true}`
- `GET /api/health` returns `{"ok": true}`

**Privacy:** visitor IPs are never saved. Each like is stored as a salted SHA-256 hash, only to stop the same visitor liking twice.

---

## How it fits your setup

```
visitor → Cloudflare Tunnel → Nginx ─┬─ /         → your website files (index.html)
                                     └─ /api/...  → like-api container (port 8080)
```

The website calls `/api/likes` on the **same address** it was loaded from, so Nginx has to send `/api/` requests to this container.

## Setup (about 10 minutes)

I can't see your exact Docker and Nginx files, so adjust the names below to match yours. Your setup lives in `~/homelab/websites/portfolio`.

### 1. Add the service to your `docker-compose.yml`

Next to your existing Nginx service:

```yaml
  like-api:
    build: ./like-api
    restart: unless-stopped
    environment:
      - ALLOWED_ORIGIN=https://zenops.dpdns.org
    volumes:
      - like-data:/data

volumes:
  like-data:
```

If you already have a `volumes:` section at the bottom, just add `like-data:` under it.

### 2. Tell Nginx to forward `/api/`

In your Nginx site config, inside the `server { ... }` block:

```nginx
location /api/ {
    proxy_pass http://like-api:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header CF-Connecting-IP $http_cf_connecting_ip;
}
```

`like-api` works as a hostname because Docker Compose puts services on the same network and lets them find each other by service name.

### 3. Start it

```bash
cd ~/homelab/websites/portfolio
docker compose up -d --build like-api
docker compose restart nginx        # use your Nginx service's name
curl https://zenops.dpdns.org/api/health
```

You should see `{"ok": true}`. Open the site, scroll to the bottom, and tap the heart.

## Useful commands

```bash
docker compose logs -f like-api                       # watch it work
docker compose exec like-api python -c "import sqlite3;print(sqlite3.connect('/data/likes.db').execute('select count(*) from likes').fetchone())"
```

**Backups:** the likes live in the `like-data` Docker volume. Back it up along with your other homelab data.

## If something's off

| Symptom | Likely cause |
|---|---|
| Heart works but no number shows | `/api/` isn't reaching the container. Check the Nginx `location` and run `curl https://zenops.dpdns.org/api/likes` |
| `curl` shows HTML instead of JSON | Nginx is serving the website for `/api/`. The `location /api/` block is missing or in the wrong `server` block |
| `403 origin not allowed` | `ALLOWED_ORIGIN` doesn't exactly match your site's address (https, no trailing slash) |
| Container keeps restarting | `docker compose logs like-api` shows why, usually a typo in the compose file |

## Likes vs visitors

A like counts **people who chose to tap the heart**. To see **how many people visit**, use **Cloudflare Web Analytics**: free, privacy-friendly, nothing to install. Open the Cloudflare dashboard → **Web Analytics** and check whether zenops.dpdns.org is already listed (Cloudflare turned it on by default for many free domains in late 2025). If not, add the site there.
