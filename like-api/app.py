"""Tiny like counter for Ian Mendoza's portfolio.

Runs next to Nginx on the M710q. No dependencies: only Python's standard library.

  GET  /api/likes   -> {"count": 12}
  POST /api/like    -> {"count": 13, "new": true}   (one like per visitor)
  GET  /api/health  -> {"ok": true}

Privacy: visitor IPs are never stored. Each like is saved as a salted SHA-256 hash,
which is only used to stop the same visitor liking twice.
"""
import hashlib, json, os, secrets, sqlite3, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB_PATH = os.environ.get("LIKE_DB", "/data/likes.db")
PORT = int(os.environ.get("PORT", "8080"))
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "").rstrip("/")  # e.g. https://zenops.dpdns.org
LOCK = threading.Lock()


def db():
    con = sqlite3.connect(DB_PATH)
    con.execute("CREATE TABLE IF NOT EXISTS likes (who TEXT PRIMARY KEY, at TEXT DEFAULT CURRENT_TIMESTAMP)")
    con.execute("CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT)")
    return con


def salt(con):
    row = con.execute("SELECT v FROM meta WHERE k='salt'").fetchone()
    if row:
        return row[0]
    s = os.environ.get("LIKE_SALT") or secrets.token_hex(16)
    con.execute("INSERT INTO meta (k, v) VALUES ('salt', ?)", (s,))
    con.commit()
    return s


def count(con):
    return con.execute("SELECT COUNT(*) FROM likes").fetchone()[0]


class Handler(BaseHTTPRequestHandler):
    server_version = "like-api"

    def visitor_ip(self):
        h = self.headers
        ip = h.get("CF-Connecting-IP") or h.get("X-Real-IP") or (h.get("X-Forwarded-For") or "").split(",")[0].strip()
        return ip or self.client_address[0]

    def send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/likes":
            with LOCK:
                con = db()
                try:
                    return self.send(200, {"count": count(con)})
                finally:
                    con.close()
        if self.path == "/api/health":
            return self.send(200, {"ok": True})
        self.send(404, {"error": "not found"})

    def do_POST(self):
        if self.path.split("?")[0] != "/api/like":
            return self.send(404, {"error": "not found"})
        origin = (self.headers.get("Origin") or "").rstrip("/")
        if ALLOWED_ORIGIN and origin and origin != ALLOWED_ORIGIN:
            return self.send(403, {"error": "origin not allowed"})
        with LOCK:
            con = db()
            try:
                who = hashlib.sha256((salt(con) + self.visitor_ip()).encode()).hexdigest()
                cur = con.execute("INSERT OR IGNORE INTO likes (who) VALUES (?)", (who,))
                con.commit()
                return self.send(200, {"count": count(con), "new": cur.rowcount == 1})
            finally:
                con.close()

    def log_message(self, fmt, *args):  # keep logs short and IP-free
        print("like-api", self.command, self.path, args[1] if len(args) > 1 else "")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    db().close()
    print(f"like-api listening on :{PORT}, database {DB_PATH}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
