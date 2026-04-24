# Hugging Face Spaces — Deploy Guide

**Source:** HF Spaces documentation
**URL:** https://huggingface.co/docs/hub/spaces
**Type:** Platform documentation (summary, own words)

## What HF Spaces is

A free tier for hosting ML demos. You push a git repo; HF builds it and serves it on a public URL (`<username>-<space-name>.hf.space`). Supported SDKs:
- **Streamlit** — fastest path for data/ML demos.
- **Gradio** — similar goals, more ML-flavored.
- **Docker** — bring your own container.
- **Static** — HTML/JS/CSS only.

## Free tier specs

- 2 vCPU, 16 GB RAM.
- Sleeps after ~48 hours of inactivity (wakes on visit, cold start ~30s).
- Model cache and persistent storage available.
- No GPU on free tier — for GPU, upgrade or use Inference Endpoints.

## Minimum repo layout

```
my-space/
├── app.py              # streamlit entry point (or gradio)
├── requirements.txt    # pip dependencies
├── README.md           # YAML header drives Space config
└── .gitignore
```

### README YAML header

```yaml
---
title: RAG Document Q&A
emoji: 📚
colorFrom: indigo
colorTo: purple
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: mit
---
```

This header controls how HF builds and displays the Space. `app_file` must match your entry point.

## Deploying

1. Create a Space on huggingface.co (select SDK + name).
2. Clone the resulting git repo locally (`git clone https://huggingface.co/spaces/<user>/<name>`).
3. Add your code, commit, push.
4. HF builds automatically; watch logs under the Space's "Logs" tab.

Alternative: add the HF Space as a second remote on an existing repo and push a branch.

## Secrets

Environment variables go under Settings → Variables and secrets. Never hardcode API keys in repo files. Your code reads them via `os.environ["KEY"]`.

## Local-to-remote parity

- Match `python_version` in your dev venv to HF's default (3.10–3.12 typical).
- Pin transitive dependencies: export `pip freeze` once it works locally, commit as `requirements.txt`.
- `.env.example` stays in repo; real `.env` in `.gitignore`.

## Common pitfalls

- **Port.** Streamlit runs on port 7860 on HF Spaces — if you hardcode another port locally, your Space's health check will fail.
- **Cold start.** First-load embedding models downloads weights (MiniLM: ~80 MB). Factor into cold start UX — show a spinner.
- **Chroma persistence.** You can commit the built `chroma_db/` folder to repo to skip rebuild on cold start. Keeps first-query fast.
- **Build times.** Installing torch + sentence-transformers in CI takes 3–5 min on free tier. Use `--index-url` tricks only if needed.

## Cost

Free tier is free, indefinitely, for public Spaces. Upgrade (CPU Upgrade $0.03/h, GPU from $0.40/h) is per-hour billed only when Space is running.

## For a portfolio RAG demo

HF Spaces is almost purpose-built for this use case:
- Free.
- Public URL recruiters can click.
- Same ecosystem as the models (credibility signal).
- Easy to iterate: `git push` → new deploy in ~2 minutes.
