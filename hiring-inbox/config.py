import os
from dataclasses import dataclass, field

DEMO_PASSWORD = os.getenv("SUPERO_DEMO_PASSWORD", "") or "DemoHiring@2026"


@dataclass
class AppConfig:
    app_name: str = "Hiring Inbox"
    app_emoji: str = "✦"
    app_description: str = "A tenant-safe, AI-assisted recruitment inbox for campus hiring drives."
    domain_name: str = field(default_factory=lambda: os.getenv("SUPERO_DOMAIN", "darsh-jaiswal"))
    admin_email: str = field(default_factory=lambda: os.getenv("SUPERO_ADMIN_EMAIL", "admin@northstarlabs.example"))
    admin_password: str = field(default_factory=lambda: os.getenv("SUPERO_PASSWORD", "") or DEMO_PASSWORD)
    project_name: str = field(default_factory=lambda: os.getenv("SUPERO_PROJECT", "hiring-inbox"))

    # Each hiring company is a native tenant. The default tenant carries only platform setup.
    tenants: list = field(default_factory=lambda: [
        {"name": "default-tenant", "display_name": "Hiring Inbox — Platform"},
        {"name": "northstar-labs", "display_name": "Northstar Labs"},
        {"name": "vertex-systems", "display_name": "Vertex Systems"},
    ])

    # Platform role mapping: tenant_admin is presented as Hiring Admin; tenant_user as Recruiter.
    users: list = field(default_factory=lambda: [
        {"email": "admin@northstarlabs.example", "password": DEMO_PASSWORD, "role": "tenant_admin",
         "full_name": "Avery Chen — Hiring Admin", "tenant": "northstar-labs"},
        {"email": "recruiter@northstarlabs.example", "password": DEMO_PASSWORD, "role": "tenant_user",
         "full_name": "Maya Patel — Recruiter", "tenant": "northstar-labs"},
        {"email": "admin@vertexsystems.example", "password": DEMO_PASSWORD, "role": "tenant_admin",
         "full_name": "Jordan Kim — Hiring Admin", "tenant": "vertex-systems"},
        {"email": "recruiter@vertexsystems.example", "password": DEMO_PASSWORD, "role": "tenant_user",
         "full_name": "Noah Wilson — Recruiter", "tenant": "vertex-systems"},
        {"email": "testapp@test.com", "password": "Password123!", "role": "developer",
         "full_name": "App Tester", "tenant": "default-tenant"},
    ])

    # The Anthropic credential is configured only in Supero's secure service keystore.
    services: list = field(default_factory=lambda: ["ai"])
    public_schemas: list = field(default_factory=lambda: ["job_opening"])
