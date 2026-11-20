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
├── index.html        # the whole site: markup, styles, script and content
├── like-api/         # the like counter service (Dockerfile, app.py, setup guide)
├── README.md
└── .gitignore
```

## Run it locally

```bash
python -m http.server 8000
# open http://localhost:8000
```

The like button works without the counter. It just won't show a number until `/api/` is available.

## Updating the site

1. Edit `index.html` (content lives in the JSON block near the bottom, `<script type="application/json" id="data">`).
2. `git add . && git commit -m "describe the change" && git push`
3. The M710q pulls the change and it's live.

**JSON rules:** keep it valid (quotes, commas, no trailing comma), and write `</` as `<\/` inside the JSON.

## Roadmap

- [ ] Replace the placeholder automations with real projects and before/after numbers
- [ ] Add a photo
- [ ] Move content into `content.json` and build a small local editor (see the CMS plan)

---

© 2026 Ian Mendoza. All rights reserved. The code and content here are shared to show my work; please don't republish them as your own.
