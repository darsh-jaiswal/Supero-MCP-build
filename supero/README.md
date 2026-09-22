# Hiring Inbox Supero authoring source

`hiring-inbox.build-spec.yaml` is a complete declarative build brief prepared for the Supero MCP workflow. It contains no credentials, real people, production data, resumes, payment flows, or copied application code.

It is intentionally **not claimed to be a generated Supero bundle**: the Supero MCP tools required to obtain the current native schema (`build_whoami`, `build_get_skills`, and `build_get_examples`) are unavailable in the present runtime. Once enabled, map this source to the schema returned by `build_get_examples`, generate a separate project, validate, publish, go live, and replace the placeholders in `BUILD-NOTES.md` only with the actual results.
