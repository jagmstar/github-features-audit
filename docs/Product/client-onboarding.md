# Client Onboarding Flow for Audit Service

This document defines the standard onboarding flow for JAGM IT Company's audit service.

## Flow Overview

### Step 1: Client fills intake form
- The client completes `docs/client-intake-form.md`.
- The form captures company details, repository details, audit tier selection, and request notes.
- The audit team checks that the submission is complete before moving forward.

### Step 2: Team reviews request, assigns audit lead
- The team reviews the intake request for scope, timing, and fit.
- A designated audit lead is assigned to own the engagement.
- The audit lead confirms the scope, timeline, and any access or security constraints.

### Step 3: Audit pipeline runs
- The audit lead triggers the audit pipeline.
- The pipeline runs automatically via GitHub Actions.
- The automated run gathers repository signals, workflow status, and audit evidence for the report.

### Step 4: Manual review by QAO
- QAO performs a manual quality check on the automated findings.
- The review confirms that the results are accurate, complete, and client-ready.
- Any questionable findings are validated or removed before reporting.

### Step 5: Report generated from template
- The report is prepared from `docs/Templates/audit-report-template.md`.
- The audit lead adds the validated findings, recommendations, and next-step guidance.
- The final report is formatted for client delivery.

### Step 6: Report delivered to client
- Roman sends the final report to the client.
- Delivery includes the report file and a short summary of the outcome.
- Roman confirms receipt and offers to answer follow-up questions.

### Step 7: Follow-up for upsell
- The team follows up after delivery to discuss the next best step.
- The primary upsell options are **audit+fix** or **retainer**.
- Follow-up messaging should focus on value, priority remediation, and ongoing support.

## Roles and Ownership
- **Client:** submits the intake form and provides required access details.
- **Audit Lead:** owns the audit from scope confirmation through final report preparation.
- **QAO:** validates report quality and finding accuracy.
- **Roman:** delivers the completed report to the client.

## Expected Outputs
- Completed intake request
- Confirmed scope and audit lead assignment
- Automated audit results from GitHub Actions
- Manually reviewed and validated findings
- Client-ready report based on the report template
- Delivery and follow-up for expansion opportunities
