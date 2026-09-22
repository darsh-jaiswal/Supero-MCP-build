# Supero MCP Build

An intentionally small, multi-tenant campus-recruitment application built through Supero MCP for the Software Engineer Intern challenge.

## Reference project

This challenge build is derived from the author’s production project, [AspireQuest](https://github.com/darsh-jaiswal/aspire-quest): a campus-recruitment platform with student intake, recruiter-owned job openings, company-scoped candidate access, AI-assisted applicant scoring, and audit-conscious access controls.

## Challenge scope

- Tenants: fictional hiring companies
- Roles: Hiring Admin and Recruiter
- Entities: Job Opening, Candidate, Application
- Guardrails: tenant-isolated access, closed openings reject applications, and AI assessment never makes a hiring decision automatically
- AI: recruiter-owned private screening prompts produce a structured Anthropic assessment with a score, matching skills, and rationale

Only fictitious data is used. No AspireQuest source code, credentials, payments, resumes, private data, university branding, or production configuration is included here.

## Build submission

The final submission will contain a live Supero URL, a screenshot, a short data-model explanation, the tenant-isolation test, the closed-opening failure case, and notes on the AI decision boundary.
