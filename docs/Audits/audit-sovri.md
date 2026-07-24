# Automated Audit Report

- Source: `C:\Users\jagm\AppData\Local\Temp\audit-pipeline-7yu9x05o`
- Repository: `Sovri/sovri`
- Branch: `main`
- Generated: `2026-07-24T10:28:14.362345+00:00`
- Overall severity: **Critical**

## Summary

| Section | Severity | Findings |
|---|---:|---:|
| Secrets | Critical | 27 |
| CI Coverage | Critical | 4 |
| Branch Protection | Warning | 1 |
| Security Policy | Info | 1 |
| Code Quality | Info | 2 |

## Secrets

Severity: **Critical**

- Found 56 potential secret(s).
- apps\community-bot\tests\commands\handlers\dismiss.test.ts:356 - Hardcoded API key :: token: InstallationToken,
- apps\community-bot\tests\runtime-env.deployment-llm.test.ts:125 - OpenAI-style key :: SOVRI_DEFAULT_LLM_API_KEY_SECRET: "sk-live-abc123secret",
- apps\community-bot\tests\runtime-env.deployment-llm.test.ts:140 - OpenAI-style key :: SOVRI_DEFAULT_LLM_API_KEY_SECRET: "sk-live-abc123secret",
- apps\community-bot\tests\runtime-env.deployment-llm.test.ts:147 - OpenAI-style key :: expect(error.message).not.toContain("sk-live-abc123secret");
- packages\config\src\types\SovriConfig.test.ts:720 - OpenAI-style key :: ["sk-ant-api03-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "real-looking Anthropic key"],
- packages\config\src\types\SovriConfig.test.ts:721 - OpenAI-style key :: ["sk-proj-xxxxxxxxxxxxxxxxxxxxx", "real-looking OpenAI key"],
- packages\llm-providers\src\providers\AnthropicProvider.ts:72 - Hardcoded API key :: apiKey: readAnthropicApiKey(options.env ?? process.env),
- packages\llm-providers\src\providers\MistralProvider.ts:59 - Hardcoded API key :: const apiKey = resolveApiKey(options.apiKey);
- packages\llm-providers\src\providers\OpenAICompatibleProvider.no-network.test.ts:49 - Hardcoded API key :: apiKey: CompatibleProviderFixture.apiKey,
- packages\llm-providers\src\providers\OpenAICompatibleProvider.no-network.test.ts:90 - Hardcoded API key :: apiKey: CompatibleProviderFixture.apiKey,
- packages\llm-providers\src\providers\OpenAICompatibleProvider.protocol.test.ts:83 - Hardcoded API key :: apiKey: OpenAIApiKey,
- packages\llm-providers\src\providers\OpenAICompatibleProvider.protocol.test.ts:88 - Hardcoded API key :: apiKey: CompatibleApiKey,
- packages\llm-providers\src\providers\OpenAICompatibleProvider.protocol.test.ts:120 - Hardcoded API key :: apiKey: CompatibleApiKey,
- packages\llm-providers\src\providers\OpenAICompatibleProvider.protocol.test.ts:150 - Hardcoded API key :: apiKey: CompatibleApiKey,
- packages\llm-providers\src\providers\OpenAIProvider.no-network.test.ts:81 - Hardcoded API key :: const source = `new OpenAIProvider({ apiKey: "test-openai-key" });\n${sample}`;
- packages\llm-providers\src\providers\OpenAIProvider.options.ts:43 - Hardcoded API key :: apiKey: resolveApiKey(options.apiKey),
- packages\llm-providers\test\providers\OpenAICompatibleProvider.no-network-patterns.ts:5 - Hardcoded API key :: apiKey: "test-openai-compatible-key",
- packages\observability\README.md:73 - Hardcoded API key :: log.info({ token: "gho_xxxxxxxxxxxxxxxx" }, "ping");
- packages\observability\src\logger.test.ts:283 - Hardcoded API key :: logger.info({ token: "gho_xxxxxxxxxxxxxxxx" }, "ping");
- packages\observability\src\logger.test.ts:301 - Hardcoded API key :: logger.info({ token: "gho_real_token" });
- packages\observability\src\logger.test.ts:348 - Hardcoded API key :: child.info({ token: "gho_inherited_secret" });
- packages\observability\src\logger.test.ts:389 - Hardcoded API key :: logger.info({ a: { b: { token: "leaked-because-too-deep" } } });
- packages\observability\src\logger.test.ts:424 - Hardcoded API key :: log.info({ token: "gho_smoke_test_secret" }, "redacted?");
- packages\observability\src\redaction.test.ts:142 - GitHub token :: github_token: "ghp_FAKE0123456789abcdef",
- packages\observability\src\redaction.test.ts:156 - GitHub token :: ["llm.provider", "ghp_FAKE0123456789abcdef"],
- ... and 31 more finding(s).

## CI Coverage

Severity: **Critical**

- Found 4 valid workflow file(s) under `.github/workflows/`.
- YAML validation found errors in one or more files.
- Found 1 YAML file(s) with syntax errors.
- packages\config\test-fixtures\malformed\.sovri.yml: while parsing a flow sequence
  in "<unicode string>", line 3, column 10:
      model: [unterminated array
             ^
expected ',' or ']', but got ':'
  in "<unicode string>", line 4, column 15:
      apiKeySecret: ANTHROPIC_API_KEY
                  ^

## Branch Protection

Severity: **Warning**

- Branch `main` is not protected according to GitHub API.

## Security Policy

Severity: **Info**

- `SECURITY.md` found at `.github\SECURITY.md`.

## Code Quality

Severity: **Info**

- No Python files were found.
- JavaScript syntax check passed for 6 file(s).
