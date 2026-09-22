# Supero MCP Build Notes

Keep this factual and short while building.

## Time

- Preparation began: 2026-09-22 20:55:43 +05:30
- Supero MCP connection verified: 2026-09-22 (HTTP 200)
- Supero project created: `hiring-inbox`
- Build status: source bundle complete; published version 4; local verification continuing
- Supero validation: passed (3 schemas, namespace verified, 0 errors, 0 warnings)
- Supero deploy-readiness check: no errors; fixed the boot-overlay and tenant-picker warnings before publish.
- Supero publish: version 4 published successfully (8 source files, including secure AI scoring and real application writes).
- Behavioral test: queued twice, but the Supero worker restarted before either run could be retained; no test result is claimed.
- Permanent deployment: blocked by the current Supero plan's cloud-server allowance (limit 0), not by a build error.
- Current continuation check: JavaScript syntax and Python compilation pass locally; no new MCP calls made during this session.
- Remaining work: enable a Supero cloud server allowance, deploy, then verify live tenant isolation, closed-opening rejection, and one real AI assessment.

## Scope

- **App:** Hiring Inbox
- **Entities:** Hiring company (tenant), Job Opening, Candidate, Application
- **Roles:** Hiring Admin, Recruiter
- **Why this scope:** It preserves the important AspireQuest rule: a recruiter may review a candidate only through an application to that recruiter's hiring company.

## Model and tenancy

- Native multi-tenancy: required in the build plan before authoring; each hiring company is a tenant.
- Hiring company owns Job Openings and scopes all staff access.
- An Application links one Candidate to one Job Opening and inherits the opening's tenant.
- AI assessment fields live on the Application; they are advisory metadata, not a decision-making entity.
- Tenant isolation must be structural and server-side, not a UI filter added later.

## Permissions and guardrails to verify

- Hiring Admin manages openings and applications inside its tenant.
- Recruiter reviews only applications to its tenant's openings and can manage the private screening prompt there.
- Cross-tenant records must behave as nonexistent.
- A closed opening must reject a new application server-side.
- Private screening prompts must never render publicly.

## AI scoring boundary

- A staff member explicitly triggers assessment; it is never automatic.
- Input excludes candidate name and email.
- The model returns validated structured score, matching skills, and a short rationale.
- AI never changes shortlist or rejection status.
- Relevant candidate or opening edits make the assessment stale.
- On failure: `Assessment unavailable; no hiring decision was changed.`
- Anthropic integration: configured in Supero's secure AI / LLM service. The app uses `services.ai.chat` with a Claude model; the key is not in source or browser code.
- AI verification status: source validates, and the AI service is active in the Domain Admin dashboard. A live Claude request still needs deployment and an authorised dashboard test; it is not claimed as complete yet.
- Application form: now performs Candidate then Application writes through the Supero client after checking that the opening is Live; failures leave no hiring decision changed.

## What fought back

- The first Codex child process did not expose the configured Supero MCP tools, although the configured endpoint and credential were valid.
- Workaround: verified the connection directly with Supero (HTTP 200) and created the `hiring-inbox` project; build authoring now continues through that verified MCP connection.

## Evidence

- GitHub repository: https://github.com/darsh-jaiswal/Supero-MCP-build
- Live URL: pending deployment
- Screenshots: pending deployment and verification

## Technical conversation answers

### Why these entities and not more?

The assessment is metadata on the application it evaluates. Keeping it there makes status ownership and staleness clear while avoiding a separate workflow object that could be mistaken for a hiring decision.

### How does the tenant boundary hold?

Every staff read and write begins from the current tenant, and application ownership is derived from the opening. Cross-tenant resources return not found rather than revealing a permission distinction. Page visibility is never the security boundary.

### What happens if the AI is wrong or unavailable?

The assessment is advisory only. It cannot write application status; a failed request writes no decision and presents the unavailable message. A human reviews every result.

### Why is the screening prompt private?

It is internal evaluation guidance for tenant staff and the server-side scorer, not candidate-facing job content. It is excluded from public queries and rendering.
