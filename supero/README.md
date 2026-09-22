# Hiring Inbox — Supero MCP build

This repository contains the Supero MCP challenge submission for a tenant-safe campus recruitment inbox.

## Current status

- Supero project: `Hiring Inbox`
- Latest published build: version 4
- Source bundle: `../hiring-inbox/`
- Permanent public URL: pending Supero cloud-server allowance

The build is published in Supero, but it cannot be opened publicly until the project has a cloud server enabled. The current plan reported a server allowance of zero.

## Seed data

Fictional seed data is defined in `../hiring-inbox/setup.py` under `TENANT_SEED` and `seed_test_data`:

- Tenants: Northstar Labs and Vertex Systems
- Two openings per tenant: one Live and one Closed
- Two fictional candidates per tenant
- Four applications per tenant: Applied, Shortlisted, Rejected, and Withdrawn

No real people, resumes, credentials, or production data are included.

## Test checklist

After enabling Supero hosting and deploying:

1. Open the permanent `*.supero.live` URL.
2. Select Northstar Labs and confirm only its live opening appears in the candidate view.
3. Submit a fictional candidate application to the live opening.
4. Attempt the same against the closed opening and confirm the server-side rejection message.
5. Sign in as a Northstar recruiter and confirm the private screening prompt is visible only in the staff view.
6. Generate an AI assessment and confirm it returns a score/rationale without changing the application status.
7. Select Vertex Systems and verify Northstar records cannot be listed, opened, edited, or scored across the tenant boundary.

## Security notes

The Anthropic key is configured only in Supero's secure AI/LLM integration. No API key belongs in this repository. Candidate name and email are excluded from AI scoring, and AI output is advisory: a human recruiter makes the final decision.
