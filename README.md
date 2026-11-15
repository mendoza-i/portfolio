# Ian Mendoza · Portfolio

Personal portfolio of **Ian Mendoza**, IT graduate from the University of the Cordilleras, Baguio City. I build Flutter apps, integrate the Claude API, and automate workflows with n8n and Zapier.

**Live site:** _add your Vercel link here_

---

## What's inside

| Tab | What it shows |
| --- | --- |
| **About** | Name, roles, short bio, photo frame, and a "Now" carousel of active projects |
| **Apps** | Mobile apps: Aura (fitness coaching) and PURRAMEDICS (capstone) |
| **Web** | Web projects, including this site |
| **Automations** | Career-Ops and workflow automation with n8n and Zapier |
| **Certifications** | Degree and certificates, grouped into Earned and In progress |
| **Infrastructure** | Work experience, hardware, Linux and networking |

**Highlights**

- Welcome screen with a curtain-lift transition, followed by a short spotlight tour (shown once per visitor)
- Tab bar with a sliding indicator and direction-aware page transitions
- Light and dark mode, following the visitor's system setting
- Respects "reduce motion" for visitors who turn animations off
- Animations use only `transform` and `opacity`, so they stay smooth on low-power devices

## Tech stack

- **HTML, CSS and vanilla JavaScript.** No framework, no build step, no dependencies.
- **Fonts:** Instrument Serif and Instrument Sans from Google Fonts.
- **Hosting:** Vercel, deployed straight from this repo.

The whole site is one file, `index.html`. All the text on the page comes from a JSON block inside it, so content and layout stay separate.

## Project structure

```
.
├── index.html   # the entire site: markup, styles, script, and content
├── README.md    # this file
└── .gitignore
```

## Run it locally

Open `index.html` in a browser, or serve the folder so it behaves like the live site:

```bash
# Python 3
python -m http.server 8000
# then open http://localhost:8000
```

## Deploy on Vercel

1. Push this repo to GitHub.
2. On [vercel.com](https://vercel.com): **Add New → Project**, then import this repo.
3. **Framework Preset:** Other. Leave Build Command, Output Directory and Root Directory empty.
4. Click **Deploy**. Every push to `main` redeploys automatically.

If Vercel shows a 404, check that the Vercel project is linked to *this* repo and that the latest deployment's source is your newest commit, not "Initial commit".

## Editing content

All content lives in one JSON object near the bottom of `index.html`:

```html
<script type="application/json" id="data"> { "s": {...}, "sm": false, "a": {...} } </script>
```

- `s`: site info (`name`, `role`, `bio`, `line`)
- `a`: one entry per tab (`apps`, `web`, `ai`, `cert`, `infra`), each with a list of projects in `e`
- Each project has a name `n`, type `t`, short blurb `b`, longer text `w`, date `d`, status `s`, links `l`, and stack chips in `x.ks`

To edit, open `index.html` on GitHub, click the pencil icon, change the text, and commit. Two rules keep the page working:

1. **Keep the JSON valid.** Every value in quotes, a comma between items, no trailing comma.
2. **Write `</` as `<\/`** inside the JSON, or the browser will think the script ended early.

## Roadmap

- [ ] Add a profile photo
- [ ] Add GitHub and live links for each project
- [ ] Add project screenshots and dates
- [ ] Add real certifications
- [ ] Contact method for the "Say hello" button
- [ ] Move content into a separate `content.json`
- [ ] Self-host on a home server (Docker, Caddy, Cloudflare Tunnel)

## Contact

GitHub: [@m3rlin-git-old](https://github.com/m3rlin-git-old)

---

© 2026 Ian Mendoza. All rights reserved. The code and content here are shared to show my work; please don't republish them as your own.
