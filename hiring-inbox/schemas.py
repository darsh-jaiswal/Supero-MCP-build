"""Hiring Inbox schema: every operational record is tenant-owned."""

JobOpening = {
    "schema_type": "object",
    "name": "JobOpening",
    "namespace": "hiring_inbox",
    "parent_type": "tenant",
    "description": "A hiring company's opening. The private screening prompt is never candidate-facing.",
    "attributes": [
        {"name": "title", "type": "string", "mandatory": True},
        {"name": "public_description", "type": "text", "mandatory": True},
        {"name": "required_skills", "type": "text", "mandatory": True},
        {"name": "private_screening_prompt", "type": "text"},
        {"name": "opening_state", "type": "string", "mandatory": True,
         "values": ["Draft", "Live", "Closed"]},
        {"name": "created_on", "type": "date"},
        {"name": "scoring_input_version", "type": "integer"},
    ],
}

Candidate = {
    "schema_type": "object",
    "name": "Candidate",
    "namespace": "hiring_inbox",
    "parent_type": "tenant",
    "description": "A fictional candidate profile, isolated to the hiring company that received the application.",
    "attributes": [
        {"name": "full_name", "type": "string", "mandatory": True},
        {"name": "email", "type": "string", "mandatory": True},
        {"name": "branch", "type": "string"},
        {"name": "cgpa", "type": "float"},
        {"name": "skills", "type": "text"},
        {"name": "qualification_version", "type": "integer"},
    ],
}

Application = {
    "schema_type": "object",
    "name": "Application",
    "namespace": "hiring_inbox",
    "parent_type": "tenant",
    "description": "A candidate's application to one opening. AI fields are advisory and cannot make hiring decisions.",
    "attributes": [
        {"name": "application_state", "type": "string", "mandatory": True,
         "values": ["Applied", "Shortlisted", "Rejected", "Withdrawn"]},
        {"name": "job_opening_uuid", "type": "string", "mandatory": True},
        {"name": "candidate_uuid", "type": "string", "mandatory": True},
        {"name": "applied_on", "type": "date"},
        {"name": "reviewed_on", "type": "date"},
        {"name": "ai_score", "type": "integer"},
        {"name": "ai_rationale", "type": "text"},
        {"name": "ai_skill_matches", "type": "text"},
        {"name": "ai_model", "type": "string"},
        {"name": "ai_scored_at", "type": "date"},
        {"name": "assessment_state", "type": "string",
         "values": ["Not assessed", "Current", "Stale", "Unavailable"]},
        {"name": "scoring_input_version", "type": "integer"},
    ],
    "references": [
        {"name": "JobOpening", "cardinality": "one", "back_ref_name": "applications"},
        {"name": "Candidate", "cardinality": "one", "back_ref_name": "applications"},
    ],
}

ALL_SCHEMAS = [JobOpening, Candidate, Application]
PUBLIC_SCHEMAS = ["job_opening"]
