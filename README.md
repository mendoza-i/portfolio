# Ian Mendoza · automation specialist

Personal portfolio of **Ian Mendoza**, an IT graduate (University of the Cordilleras, Baguio City) focused on **workflow automation with n8n**, plus the apps and websites those automations plug into.

**Live site:** https://zenops.dpdns.org

---

## What's inside

| Tab | What it shows |
| --- | --- |
| **About** | A live animation of how my projects work (trigger → step → result), my name and a short bio, and a "Now" carousel |
| **Automations** | n8n workflows as pipelines: trigger, steps, result, tools, and **before → after** time saved |
| **Apps** | Mobile apps: Aura (fitness coaching) and PURRAMEDICS (vet clinics) |
| **Web** | Web projects, including this site |
| **Certifications** | A growth timeline: what I'm learning now, then every certificate by year. Click one to see it full size |
| **Infrastructure** | Hardware, Linux, networking and self-hosting |

The footer has a **like button** backed by a tiny self-hosted counter (see `like-api/`).

## How it's hosted

Self-hosted on my own mini PC, no cloud bill:

```
GitHub (this repo) → Lenovo M710q pulls changes (Git) → Docker + Nginx → Cloudflare Tunnel → zenops.dpdns.org
                                                          └─ like-api container serves /api/
```

## Tech

- **Site:** HTML, CSS and vanilla JavaScript in one file, `index.html`. No framework, no build step.
- **Fonts:** Instrument Serif and Instrument Sans (Google Fonts).
- **Like counter:** Python standard library + SQLite in a small Docker container (`like-api/`). Stores no IP addresses, only salted hashes.
- **Analytics:** Cloudflare Web Analytics (privacy-friendly, no cookies).
- Respects **reduce motion**, works in light and dark mode, animations use only `transform` and `opacity`.

## Project structure

```
.
├── index.html                 # the whole site: markup, styles, script and content
├── assets/                    # everything public besides index.html
│   ├── images/
│   │   └── ian.jpg            # profile photo (480×480 JPEG)
│   ├── icons/
│   │   ├── favicon.svg        # browser tab icon (main)
│   │   ├── favicon-32.png     # tab icon for browsers without SVG support
│   │   ├── favicon.ico        # 16/32/48 px, for older browsers and tools
│   │   └── apple-touch-icon.png  # 180×180, iPhone home screen
│   └── projects/              # project screenshots and short demo videos
├── like-api/                  # the like counter service (backend, never public)
├── README.md
└── .gitignore
```

## What belongs in `assets/`

`assets/` holds **only files a visitor's browser downloads**: images, icons, screenshots and short videos. If a file isn't shown on the page, it doesn't go in `assets/`.

| Folder | Put here | Example |
| --- | --- | --- |
| `assets/images/` | Photos of me and general site images | `assets/images/ian.jpg` |
| `assets/icons/` | Favicons and app icons | `assets/icons/favicon.svg` |
| `assets/projects/` | Screenshots and demo clips of projects | `assets/projects/aura-home.jpg` |

**Never in `assets/`:** backend code (`like-api/`), `.env` files, tokens, keys, passwords, Docker, Nginx or Cloudflare config, database files, or anything from `.git/`.

**Why:** a web server hands out every file in the folders it serves, to anyone who asks. If backend code or config sat in a public folder, anyone could download it by guessing its name, for example `/assets/app.py` or `/assets/.env`. Backend code shows attackers how the service works, and a leaked token or key can give them access to it. Keeping public files in one clearly named folder makes it easy to see what is public.

## Image and icon paths

- **Write paths relative to `index.html`, starting with `assets/`:** `assets/images/ian.jpg`, `assets/projects/aura-home.jpg`. Never use computer paths like `/home/ian/...` or `C:\Users\...`.
- **Profile photo:** `PHOTO_FILE` in the script points to `assets/images/ian.jpg`. To change the photo, replace that file and keep the name. If it fails to load, the circle shows the initials, and the browser console (F12 → Console) says which path failed.
- **Favicons:** the four icon lines at the top of `index.html` point into `assets/icons/` and end in `?v=4`. **Bump that number** (`?v=5` and so on) whenever you change an icon. Browsers keep favicons for a long time, and a new URL makes them fetch the new file.
- **File names:** lowercase, no spaces, words joined with `-` (`aura-home.jpg`, not `Aura Home.JPG`). Linux servers treat `Aura.jpg` and `aura.jpg` as different files.
- **File size:** JPG or WebP for photos and screenshots, ideally under 300 KB each. Don't re-save `ian.jpg` or the icons unless you mean to change them.

## Adding a project screenshot

1. Save the image in `assets/projects/`, for example `assets/projects/aura-home.jpg`. Phone screenshots fill the card's phone frame (portrait). Browser screenshots fill the browser frame (landscape, about 3:2).
2. In `index.html`, find the project in the JSON data block and set its image field `"i"` to the path:
   ```json
   {"n":"Aura","t":"Mobile app", ... ,"i":"assets/projects/aura-home.jpg"}
   ```
   For a short looping video, use `"v":"assets/projects/aura-demo.mp4"` (muted, a few seconds, small file).
3. Check it locally (`python -m http.server 8000`), then commit and push.

No deploy change is needed: everything in `assets/` is already published (see below).

Images uploaded in the Claude editor are stored on Claude's servers and **don't show on the live site**. Always use a file in `assets/projects/`.

## Deployment: an allowlist

The M710q keeps two folders:

```
~/homelab/websites/portfolio          ← git clone of this repo (public and private files)
        │  deploy step copies ONLY the allowlist
        ▼
~/homelab/websites/portfolio-public   ← the only folder Nginx serves (127.0.0.1:8082 → Cloudflare Tunnel → zenops.dpdns.org)
```

**Allowlist** means the deploy step names exactly what to publish, instead of copying everything and trying to remember what to leave out (a "blocklist"). With an allowlist a new private file is safe by default: it stays private unless it is on the list.

The allowlist for this site is just two entries:

```
index.html
assets/
```

That is the point of the `assets/` folder: new public files go inside it and are published automatically, and everything outside it (`like-api/`, `README.md`, `.git/`) never is. If a file the page uses is missing from the public folder, the page still loads, but that file returns `404 not found`, for example a missing photo or icon.

## Run it locally

```bash
python -m http.server 8000
# open http://localhost:8000
```

The like button works without the counter. It just won't show a number until `/api/` is available.

## Updating the site

1. Edit `index.html` (content lives in the JSON block near the bottom, `<script type="application/json" id="data">`). New images go in `assets/` (see above).
2. `git add . && git commit -m "describe the change" && git push`
3. The M710q pulls the change, the deploy step copies `index.html` and `assets/` to the public folder, and it's live.

**JSON rules:** keep it valid (quotes, commas, no trailing comma), and write `</` as `<\/` inside the JSON.

## Roadmap

- [ ] Replace the placeholder automations with real projects and before/after numbers
- [ ] Move content into `content.json` and build a small local editor (see the CMS plan)

---

© 2026 Ian Mendoza. All rights reserved. The code and content here are shared to show my work; please don't republish them as your own.
