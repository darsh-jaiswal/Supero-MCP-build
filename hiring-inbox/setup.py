import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from supero.app_setup import AppSetup, PolicyDef, PolicyRule, make_seed_record
from config import AppConfig
from schemas import ALL_SCHEMAS, PUBLIC_SCHEMAS

seed_record = make_seed_record(ALL_SCHEMAS)

# Native tenant scoping is the primary isolation control. Recruiters have only the
# minimum operational access inside their own tenant; no client-side check is relied on.
POLICIES = [
    PolicyDef(role="tenant_admin", default_access="full", rules=[]),
    PolicyDef(role="tenant_user", default_access="none", rules=[
        PolicyRule(entity="job_opening", can_read=True, can_update=True),
        PolicyRule(entity="candidate", can_read=True),
        PolicyRule(entity="application", can_read=True, can_update=True),
    ]),
]

WORKFLOW_DEFINITIONS = []
EVENT_BINDINGS = []

TENANT_SEED = {
    "northstar-labs": {
        "openings": [
            {"name": "northstar-platform-intern", "title": "Platform Engineering Intern", "state": "Live",
             "description": "Help build reliable developer tools for distributed engineering teams.",
             "skills": "Python, APIs, PostgreSQL, testing", "prompt": "Prioritise evidence of debugging, API design, and careful testing."},
            {"name": "northstar-data-intern", "title": "Data Engineering Intern", "state": "Closed",
             "description": "Work on internal data pipelines and quality checks.",
             "skills": "Python, SQL, ETL", "prompt": "Look for practical SQL and data-quality experience."},
        ],
        "candidates": [
            {"name": "northstar-isha", "full_name": "Isha Rao", "email": "isha.rao@example.test", "branch": "Computer Science", "cgpa": 8.7, "skills": "Python, PostgreSQL, React, testing"},
            {"name": "northstar-kabir", "full_name": "Kabir Mehta", "email": "kabir.mehta@example.test", "branch": "Information Technology", "cgpa": 8.1, "skills": "Python, SQL, Docker"},
        ],
    },
    "vertex-systems": {
        "openings": [
            {"name": "vertex-backend-intern", "title": "Backend Engineering Intern", "state": "Live",
             "description": "Build dependable backend services and integration tooling.",
             "skills": "TypeScript, APIs, databases", "prompt": "Assess clear reasoning about failure handling and service boundaries."},
            {"name": "vertex-qa-intern", "title": "Quality Engineering Intern", "state": "Closed",
             "description": "Design tests that catch workflow failures before release.",
             "skills": "Testing, JavaScript, CI", "prompt": "Prioritise candidates who can explain an unhappy path they tested."},
        ],
        "candidates": [
            {"name": "vertex-sana", "full_name": "Sana Kapoor", "email": "sana.kapoor@example.test", "branch": "Computer Science", "cgpa": 9.0, "skills": "TypeScript, Node.js, PostgreSQL, Playwright"},
            {"name": "vertex-arjun", "full_name": "Arjun Shah", "email": "arjun.shah@example.test", "branch": "Electronics", "cgpa": 7.9, "skills": "JavaScript, Python, testing"},
        ],
    },
}


def seed_test_data(s, base, domain, tenant_uuid, progress):
    """Seed only fictional records. Applications remain tenant-local by construction."""
    for tenant_name, data in TENANT_SEED.items():
        opening_ids = []
        candidate_ids = []
        for index, opening in enumerate(data["openings"]):
            record = seed_record(s, base, domain, "JobOpening", {
                "name": opening["name"],
                "display_name": opening["title"],
                "description": opening["description"],
                "title": opening["title"],
                "public_description": opening["description"],
                "required_skills": opening["skills"],
                "private_screening_prompt": opening["prompt"],
                "opening_state": opening["state"],
                "created_on": "2026-09-%02d" % (10 + index),
                "scoring_input_version": 1,
            }, progress=progress, tenant_name=tenant_name)
            opening_ids.append(record)
        for candidate in data["candidates"]:
            record = seed_record(s, base, domain, "Candidate", {
                "name": candidate["name"],
                "display_name": candidate["full_name"],
                "description": "%s candidate profile" % candidate["branch"],
                "full_name": candidate["full_name"],
                "email": candidate["email"],
                "branch": candidate["branch"],
                "cgpa": candidate["cgpa"],
                "skills": candidate["skills"],
                "qualification_version": 1,
            }, progress=progress, tenant_name=tenant_name)
            candidate_ids.append(record)

        application_states = ["Applied", "Shortlisted", "Rejected", "Withdrawn"]
        for index, app_state in enumerate(application_states):
            # The operational UI reads references after setup; these fields make every
            # seeded workflow state inspectable even if records are viewed in Data Explorer.
            seed_record(s, base, domain, "Application", {
                "name": "%s-application-%d" % (tenant_name, index + 1),
                "display_name": "%s application %d" % (tenant_name, index + 1),
                "description": "Fictional application in %s state." % app_state,
                "application_state": app_state,
                "applied_on": "2026-09-%02d" % (12 + index),
                "reviewed_on": "2026-09-16" if app_state in ("Shortlisted", "Rejected") else None,
                "ai_score": 86 if index == 1 else (42 if index == 2 else None),
                "ai_rationale": "Strong evidence of relevant skills and careful implementation." if index == 1 else ("Partial skills match; human review required." if index == 2 else None),
                "ai_skill_matches": "Python, PostgreSQL, testing" if index == 1 else "JavaScript, testing",
                "ai_model": "Anthropic — configure secure keystore" if index in (1, 2) else None,
                "ai_scored_at": "2026-09-16" if index in (1, 2) else None,
                "assessment_state": "Current" if index in (1, 2) else "Not assessed",
                "scoring_input_version": 1,
            }, progress=progress, tenant_name=tenant_name)
        progress.ok("Seeded fictional Hiring Inbox data for %s." % tenant_name)


def main():
    setup = AppSetup(AppConfig(), ALL_SCHEMAS, PUBLIC_SCHEMAS)
    setup.run(seed_fn=seed_test_data, policies=POLICIES,
              workflow_definitions=WORKFLOW_DEFINITIONS, event_bindings=EVENT_BINDINGS)


if __name__ == "__main__":
    main()
