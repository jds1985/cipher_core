# Cipher → Zeo → Agents Starter Kit (MVP)

This repo boots a **multi‑agent build system** where **Cipher** (the orchestrator) can spawn agents
to build, test, and deploy code — with guardrails and a dashboard (**Zeo Shell**).

## Structure
```
/cipher_core      # LangGraph orchestrator (Cipher + worker agents)
/zeo_kernel       # Jobs, tool adapters, memory, RBAC
/zeo_shell        # Next.js dashboard (tasks, runs, logs, approvals)
/runner           # FastAPI sandbox: /exec /fs /git /test /deploy
/services
  /frontend       # Placeholder Next.js app
  /backend        # Placeholder FastAPI app
/infra            # GitHub Actions, deploy configs
.env.template     # Copy to .env and fill secrets
```

## Quick Start
1) **Create a new GitHub repo** and upload this folder’s contents.
2) **Add GitHub Action secrets** (Settings → Secrets and variables → Actions):
   - `OPENAI_API_KEY`
   - `VERCEL_TOKEN`
   - `VERCEL_PROJECT_NAME` (e.g., `zeo-shell` in Vercel)
   - `GITHUB_TOKEN` (repo + PR scopes; optional if Actions’ default permissions suffice)
   - If using Firebase: `FIREBASE_API_KEY`, `FIREBASE_PROJECT_ID`
   - If using Supabase instead: `SUPABASE_URL`, `SUPABASE_ANON_KEY`
3) **Deploy services**:
   - `runner`: deploy via Railway/Render (Dockerfile provided). Expose URL as `RUNNER_BASE_URL` secret.
   - `zeo_shell`: connect repo to Vercel; set env in Vercel (same as above).
   - `services/backend`: deploy via Railway/Render (Python/FastAPI) or Vercel Serverless if you switch to Node.
   - `services/frontend`: example app — optional; Zeo Shell is the main dashboard.
4) **CI/CD**: GitHub Actions will lint/test on PRs. A `/deploy` comment or merge to `main` triggers deploy.
5) **Run locally** (optional):
   - Python 3.11+, Node 18+
   - `cd runner && uvicorn app.main:app --reload --port 8081`
   - `cd zeo_shell && npm i && npm run dev`
   - `cd services/backend && uvicorn app.main:app --reload --port 8082`

## Env Vars
Copy `.env.template` to `.env` in each service as needed.
- `OPENAI_API_KEY` – required
- `RUNNER_BASE_URL` – e.g., https://your-runner.onrender.com
- `PROJECT_DB_URL` – e.g., postgres://... (or use Supabase)
- `VECTOR_DB_*` – optional if you wire Pinecone/pgvector

## Safety & Guardrails
- Runner only exposes **allow‑listed** commands.
- Per‑agent tool permissions enforced via Zeo Kernel (RBAC).
- PRs require QA checks; merges can require your `/approve` in the Zeo Shell UI (toggleable).

## What works today (MVP)
- Spawn worker agents (Architect, Frontend, Backend, QA, Deployer) via Cipher.
- Generate code to `/services/*`, open PRs via Runner Git helper, trigger CI.
- Zeo Shell shows tasks, runs, logs, and deploy status.

## Roadmap
- Skill Registry + Compression (distill best patterns into a Nexus profile)
- More tools: Stripe, SendGrid/Twilio, Cloud storage
- Auth + roles in Shell
```