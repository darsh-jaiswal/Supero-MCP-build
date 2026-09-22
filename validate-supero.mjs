// Local validation helper. It reads the key only from the Windows environment.
import fs from 'node:fs';
import path from 'node:path';

const root = 'hiring-inbox';
const projectUuid = 'bdbed609-0ce0-4bb1-aa11-990f7585aba3';
const files = {};

function collect(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      collect(fullPath);
    } else if (!fullPath.endsWith('.pyc')) {
      files[path.relative(root, fullPath).replaceAll('\\', '/')] = fs.readFileSync(fullPath, 'utf8');
    }
  }
}

collect(root);
const key = process.env.SUPERO_MCP_KEY;
if (!key) throw new Error('SUPERO_MCP_KEY is not configured in the user environment.');

const headers = {
  'X-API-Key': key,
  Accept: 'application/json, text/event-stream',
  'MCP-Protocol-Version': '2025-03-26',
  'Content-Type': 'application/json',
};
const endpoint = 'https://app.supero.dev/mcp/v1/messages';

async function request(body) {
  const response = await fetch(endpoint, { method: 'POST', headers, body: JSON.stringify(body) });
  const text = await response.text();
  if (!response.ok) throw new Error(`Supero returned HTTP ${response.status}: ${text}`);
  return text;
}

await request({
  jsonrpc: '2.0', id: 1, method: 'initialize',
  params: { protocolVersion: '2025-03-26', capabilities: {}, clientInfo: { name: 'Hiring Inbox validator', version: '1.0' } },
});

const tool = process.argv[2] || 'build_validate';
const argumentsForTool = { project_uuid: projectUuid, files };
if (tool === 'build_publish') {
  argumentsForTool.app_type = 'web';
  argumentsForTool.validate = true;
}
if (tool === 'build_e2e_test_status') {
  argumentsForTool.run_id = process.argv[3];
}
if (tool === 'build_go_live') {
  argumentsForTool.version_uuid = '5aeeb1e0-027e-4852-b276-94098d5d4c40';
}
if (tool === 'build_recommend_integrations') {
  argumentsForTool.description = 'A multi-tenant hiring application needs a server-side Anthropic integration for manually triggered candidate assessment. The browser must never receive the API key. It needs structured JSON output, validation before saving, and no automatic hiring decision.';
}
if (tool === 'build_list_capabilities') {
  argumentsForTool.category = 'integration';
  argumentsForTool.service_id = 'ai';
}
if (tool === 'build_get_skills') {
  argumentsForTool.doc = process.argv[3] || 'integrations';
  argumentsForTool.offset = 0;
  argumentsForTool.max_bytes = 16000;
}

const result = await request({
  jsonrpc: '2.0', id: 2, method: 'tools/call',
  params: { name: tool, arguments: argumentsForTool },
});

console.log(result);
