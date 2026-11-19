# Factory requirements (catalog 2.0.0-proposal.2)

Written from Nori's Factory catalog. Do not edit by hand.

## Connections

Each connection is a tool slot. Its `provider` ids come from Nori's tool slot registry.

- `tracker` Task tracker: `linear`, `jira`, `github-issues`, `asana`, `clickup`, `monday`, `basecamp`
- `messaging` Team communication: `slack`, `microsoft-teams`, `discord`
- `code` Code host: `github`, `gitlab`, `bitbucket`
- `telemetry` Observability: `sentry`, `datadog`, `grafana`, `betterstack`, `cloudflare-observability`, `pagerduty`
- `analytics` Product analytics: `posthog`, `amplitude`, `mixpanel`
- `spend` Cloud spend source: `aws`, `google-cloud`, `azure`

## Work item to pull request (`build`)

Turn each ready work item into a pull request.

### `build/item-to-pr` Each ready work item reaches a pull request

- Completion: For each included queue of ready work items, each item is started and produces a pull request with a clear scope and a link to the item. Assess each queue one time, not each origin of the items.
- Evidence: For each queue: the start rule or automation, and dated examples that go from item to pull request with links in the two directions.
- Needs: `tracker`, `code`
- Approved remedy (automation): Start a pull request from each ready work item. Nori sets up a work-item-to-pull-request automation for each queue. A tracker webhook (or a scheduled poll) starts a session for each ready item, and the session opens a pull request with links in the two directions. Nori adds a CI check that enforces the work item ID in each pull request, and a weekly report of the ready items that have no pull request. Needs: the Jiro (by Nori) GitHub app on the repositories, and read and write access to the task tracker. A person reviews and merges.

## Change checks (`checks`)

Run automatic checks on each change, and follow each failure or finding until it is closed.

### `checks/run` Checks run on each relevant change

- Completion: In each included repository, the build, tests, type checks and contract checks that apply run on each change and report a result on the pull request.
- Evidence: The workflow definition, a dated run, and the list of test suites that the workflow does not run.
- Needs: `code`
- Approved remedy (one-time): Add a reusable CI workflow to each repository. Nori writes one reusable CI workflow and adds it to each repository by pull request, with the build, tests, type checks and contract checks that Nori ran successfully in a session. Nori moves the test suites that run only by hand into the workflow, or into a scheduled run with a recorded reason. Needs: the Jiro (by Nori) GitHub app with permission to change workflow files. An admin adds the secrets that the tests need.

### `checks/security` Security checks run on change paths

- Completion: Code and dependencies are scanned on each included change path. A change with higher risk has a recorded risk review.
- Evidence: The scan workflow and a dated run for each path, the paths with no scan, and a risk review record for a higher-risk change.
- Needs: `code`
- Approved remedy (automation): Add code scanning and dependency review to pull requests. Nori adds code scanning and dependency review workflows and a dependency update configuration to each repository by pull request. Nori writes the list of higher-risk paths and a CODEOWNERS rule for them, and sets up an automation that posts a risk review on each pull request that touches those paths. Needs: the Jiro (by Nori) GitHub app with permission to change workflow files. An organization admin turns on secret scanning and push protection, or authorizes Nori to change those settings.

### `checks/failure-repair` Repeated check failures get repaired

- Completion: Each repeated or flaky failure gets an owner and a work item. A later relevant run confirms the repair.
- Evidence: The triage rule or automation, and a dated example that goes from failure to work item to passing run.
- Needs: `code`
- Approved remedy (automation): Find flaky tests each night and track each repair. Nori sets up a nightly flaky-test automation that finds repeated failures in the CI history, opens an owned work item with the evidence for each one, and confirms the repair from later runs. The automation quarantines a test only by pull request and with an expiry date, and reports each quarantine that is past its date. Needs: read access to the CI runs, and write access to the task tracker.

### `checks/security-findings` Security findings get closed

- Completion: Each actionable finding gets a triage decision and a link to a reviewed fix or an accepted exception. A later scan confirms the fix.
- Evidence: Open and closed findings with their links, and the scan that confirms each closed finding.
- Needs: `code`, `tracker`
- Approved remedy (automation): Track each security finding to a fix or an exception. Nori writes a severity table with response times and an exception file as a pull request. Nori sets up a daily automation that turns each actionable finding into an owned work item with a due date, and a weekly report of the findings that are past their due date. Needs: read access to the security alerts of the code host, and write access to the task tracker. A person approves each exception with a merge.

## Signal to work item (`signal`)

Turn each alert or regression that needs action into one tracked work item, and close that item with a result.

### `signal/work-item` Each actionable signal becomes a tracked work item

- Completion: Each actionable alert, production regression or performance regression creates or updates one work item with a link to its source. The item closes with a link to a verified fix, a customer recovery record or a written decision not to fix.
- Evidence: The rule or automation that creates items, and dated examples that go from signal to item to closure link.
- Needs: `telemetry`, `tracker`
- Approved remedy (automation): Open one work item for each actionable alert. Nori sets up a webhook automation and points the alert rules of the observability tool at it. Each actionable alert starts a session that investigates the signal, and creates or updates one deduplicated work item with evidence. Nori adds a scheduled closure check: an item closes only with a fix link, a recovery record or a written decision. Needs: write access to the alert rules (or an admin who adds the webhook URL), and write access to the task tracker.

## Review and merge (`review`)

Review each pull request and apply the rules that control a merge.

### `review/coverage` Each eligible pull request gets a review

- Completion: Each included source of pull requests gets a timely review that examines the change. This includes pull requests that are not part of project work.
- Evidence: The review rule or automation for each source, and review records on a dated sample of pull requests.
- Needs: `code`
- Approved remedy (automation): Post an agent review on each pull request. Nori sets up a review automation that starts on each opened pull request (a scheduled poll, or a workflow step that calls a Nori webhook) and posts a review that examines the change. Nori writes a CODEOWNERS file for each repository from the commit history, as a pull request. Nori adds a daily report of the pull requests that have no review after the target time. Needs: the Jiro (by Nori) GitHub app with write access to pull requests. The agent review does not replace an approval by a person that the merge rules require.

### `review/merge-rules` Merge rules are enforced

- Completion: Each protected branch enforces the necessary reviews and the necessary checks. Each exception has a recorded owner and reason.
- Evidence: The branch rules for each protected branch, compared with the checks that run. The list of exceptions.
- Needs: `code`
- Approved remedy (automation): Write a branch ruleset and audit it each week. Nori writes one ruleset for the default and release branches as a file in a repository: a required approval, each CI check that runs as a required check, and no direct pushes. Nori applies the ruleset through the code host API if an admin authorizes that. If not, an admin imports the file. Nori adds a weekly audit automation that compares the required checks with the checks that run, and reports each difference and each bypass. Needs: admin authorization on the code host, one time.

## Repository knowledge (`repo`)

Keep agent instructions and documentation in each repository correct and available.

### `repo/agent-context` Agents get current context at the start of a task

- Completion: Each included repository has agent instructions, an architecture entry point and safe task limits. An agent gets them at the start of a task.
- Evidence: The instruction files in each repository, and one task start that shows the agent loaded them.
- Needs: `code`
- Approved remedy (one-time): Write AGENTS.md with tested build and test commands. Nori reads each repository and writes an AGENTS.md file as a pull request: the build and test commands that Nori ran successfully, an architecture entry point and safe task limits. Nori adds a CI check that fails when the file is missing or when a linked document does not exist. Needs: the Jiro (by Nori) GitHub app with permission to change workflow files.

### `repo/docs-current` Stale documentation and agent guidance get fixed

- Completion: Each included repository finds stale documentation and stale agent guidance. Each accepted correction goes through review and is published.
- Evidence: The check or automation for each repository, and a dated correction that merged.
- Needs: `code`
- Approved remedy (automation): Open weekly pull requests that correct stale docs. Nori sets up a weekly docs-upkeep automation that opens correction pull requests for stale documentation and stale agent instructions. Nori adds a link check to CI. Needs: the Jiro (by Nori) GitHub app on the repositories. A person merges the corrections.

## Intake and triage (`intake`)

Record each request or report as a work item, and make a decision about it.

### `intake/record` Each request or report becomes a complete work item

- Completion: Each included source records a work item with a link to the original message. A feature item gives the necessary outcome, acceptance notes and an owner. A bug item gives the observed and expected behavior, the steps to reproduce, the environment and the impact.
- Evidence: For each source: the automation, form or template, and a sample of recent items with all fields. Record the items that do not have all fields.
- Needs: `tracker`, `messaging`
- Approved remedy (automation): Turn chat requests and reports into complete work items. Nori sets up an intake automation on the feedback and support channels. The automation creates one work item for each request or report, and asks the reporter in the thread for the fields that are missing. Needs: the Nori Slack app in those channels, and write access to the task tracker.

### `intake/triage` Each new work item is triaged

- Completion: Each new item from each included source gets one recorded result: accepted, rejected, duplicate or more information necessary. An automation examines each item, compares a bug report with known items, and records the result or a proposed result with evidence. A person confirms a proposed decision to accept or reject.
- Evidence: The triage automation or rule for each source, and dated items that show the result, the evidence and who or what recorded it.
- Needs: `tracker`
- Approved remedy (automation): Triage each new work item with evidence. Nori sets up a triage automation that starts on each new work item (a tracker webhook or a scheduled poll). The automation examines the item, records a result with evidence, and reports the items that are older than the target. Nori writes the triage rules to a file that the team can change. Needs: read and write access to the task tracker, and read access to the repositories. A person keeps the decision to accept or reject a request.

### `intake/ready` Accepted work is ready to build

- Completion: Each accepted item has an owner, a scope, acceptance conditions and the product or policy decisions that the work needs.
- Evidence: A sample of accepted items with these fields, and the rule that marks an item as ready.
- Needs: `tracker`
- Approved remedy (automation): Write scope and acceptance conditions on accepted work. Nori sets up a readiness automation that starts when an item is accepted. The automation writes the scope and the acceptance conditions from the request and the code, asks the open questions on the item, and marks the item ready when they have answers. Needs: read and write access to the task tracker, and read access to the repositories.

## Team reporting (`team-report`)

Tell the team what shipped and how delivery is going, with links to the source records.

### `team-report/change-record` Shipped changes are recorded for the team

- Completion: Each relevant shipped change is added to an internal change record with a link to its source.
- Evidence: The change record, the automation or procedure that writes it, and a comparison with a dated list of shipped changes.
- Needs: `code`
- Approved remedy (automation): Post a change record to the team after each release. Nori adds a release step that calls a Nori automation. The automation generates the internal change record from the merged pull requests and posts a summary to the team channel. Nori adds a workflow that labels pull requests by area, to select and group the changes. Needs: the Nori Slack app in the team channel, and the Jiro (by Nori) GitHub app with permission to change workflow files.

### `team-report/delivery` Delivery reports agree with source records

- Completion: Each delivery report traces changes, deployments, defects and recovery to their source records. Data that is not available is shown as not available.
- Evidence: A dated report with its source links, and an example of data shown as not available.
- Needs: `code`, `tracker`
- Approved remedy (automation): Send a weekly delivery report with source links. Nori sets up a weekly report automation that reads the code host and the task tracker, keeps a link for each number, and shows a source that it cannot read as not available. Nori writes the metric definitions to a document in the repository. Needs: read access to the code host, the deployments and the task tracker, and the Nori Slack app in the report channel.

### `team-report/agent-outcomes` Delegated work is measured by results

- Completion: Each report on delegated engineering work records the completed work, the checks and the failures, with links to their sources. A count of sessions is not sufficient.
- Evidence: A dated report with links to the completed work, the checks and the failures.
- Needs: `tracker`
- Approved remedy (automation): Report agent work by merged and reverted results. Nori adds a rule to the agent instructions: put an agent label on each pull request and work item that an agent creates. Nori sets up a weekly report automation that counts results (merged, reverted, failed checks, stopped tasks) from those labels, with links. The report does not give session counts alone. Needs: read access to the code host and the task tracker.

## Product QA (`qa`)

Use the running product in the way a user does, and record what fails.

### `qa/journeys` Changed journeys are tested

- Completion: Each applicable user journey and supported surface gets repeatable QA. Failures and blocked scope are recorded.
- Evidence: The QA automation or procedure, a dated run record, and the list of journeys that the run did not test.
- Needs: `code`
- Approved remedy (automation): Test critical journeys in a browser after each staging deployment. Nori writes the critical journeys as repeatable scripts (end-to-end tests or agent QA procedures) and adds them to the repository by pull request. Nori sets up an automation that the deployment workflow calls after each staging deployment. The automation runs the journeys in a real browser, posts the record and creates a work item for each failure. Needs: a staging address and a test account, kept as Nori secrets.

### `qa/accessibility` Accessibility checks run on each journey

- Completion: Each applicable journey gets automated accessibility checks and a recorded keyboard-only check by an agent or a person. Each issue has a work item.
- Evidence: The automated check and a dated run, the dated record of the keyboard-only check, and the issue links.
- Needs: `code`
- Approved remedy (automation): Add automated and keyboard accessibility checks to QA. Nori adds automated accessibility checks to the end-to-end test suite by pull request, with a baseline file so that only new serious issues fail the build. Nori adds a keyboard-only check of each journey to the QA automation, and creates a work item for each issue. Needs: the end-to-end suite and the staging access from the journey QA requirement. Limit: Nori cannot do a screen reader test. That test stays a task for a person and is not a condition of this requirement.

## Work records (`records`)

Keep the state of work items and the shared project context correct.

### `records/state` Work item state agrees with code and deployments

- Completion: Each included tracker source agrees with the related pull requests, deployments and project state, and has links to them.
- Evidence: The sync rule or automation, and a dated comparison of a sample of items with their pull requests and deployments.
- Needs: `tracker`, `code`
- Approved remedy (automation): Update work item status from pull requests and deployments. Nori sets up status rules for pull request open, merge and deployment. If the task tracker has an integration with the code host, an admin installs it and Nori configures the rules. If not, a Nori automation makes the updates. Nori adds a nightly reconciliation automation that corrects or reports the items whose state does not agree with the code. Needs: write access to the task tracker, and read access to the code host.

### `records/context` Project context stays usable

- Completion: Shared decisions, blockers and results are kept current. A later worker can find them.
- Evidence: The location of the project context, its dated revisions, and the rule or automation that updates it.
- Needs: `tracker`
- Approved remedy (automation): Keep one context document for each project. Nori creates one context document for each project and links it from the tracker project. Nori adds a rule to the agent instructions to record durable decisions there, and sets up a weekly automation that adds the results of merged work and marks the entries that are out of date. Needs: write access to the task tracker and to the location of the document.

## Customer updates (`customer-update`)

Prepare updates for customers from changes that shipped, and send them after a person approves.

### `customer-update/deliver` Customer updates are prepared and approved

- Completion: An update for each audience is written from verified shipped changes. Each delivery has an approval by a person and a delivery record.
- Evidence: The draft with its source links, the approval record and the delivery record.
- Needs: `code`, `messaging`
- Approved remedy (automation): Draft customer updates from shipped changes for approval. Nori adds a "customer-facing" label and an automation that the release workflow calls. The automation drafts the update for each audience from the labeled shipped changes and opens it for approval. Publication runs only after a named person approves, and the delivery record stays with the release. Needs: the Jiro (by Nori) GitHub app on the repository that holds the changelog. The approval by a person is deliberate: Nori does not send a message to customers without it.

## Incident response (`incident`)

Open an owned response for each incident, and close the corrective actions.

### `incident/response` Each incident has a lead and a timeline

- Completion: Each actionable incident opens a response record with an owner and a timeline that has evidence. No message goes to customers automatically.
- Evidence: The rule or automation that opens a response, and a dated incident record with its lead and timeline.
- Needs: `telemetry`, `messaging`
- Approved remedy (automation): Open an incident thread and timeline from high-severity alerts. Nori sets up an incident automation: the alert rules with high severity call a Nori webhook, and the session opens the incident thread, names the lead and starts a timeline with evidence. Nori writes the severity levels to a file as a pull request, from the alert rules that exist. Needs: the Nori Slack app in the incident channel, write access to the alert rules, and an on-call schedule that Nori can read. If there is no schedule, Nori asks in the thread and records the first person who takes the lead. Nori sends no message to customers.

### `incident/actions` Corrective actions get closed

- Completion: Each action after an incident has an owner and a link to a completed fix or an accepted risk.
- Evidence: The action list of a dated incident with owners and closure links.
- Needs: `tracker`
- Approved remedy (automation): Draft the incident review and track each corrective action. Nori sets up a post-incident automation that drafts the review from the timeline and creates an owned work item for each confirmed action. Nori adds a weekly report of the open incident actions, until each one has a fix link or an accepted risk. Needs: write access to the task tracker, and the Nori Slack app in the incident channel. A person confirms the action list and accepts each risk.

## Watch the product (`watch`)

Measure the health, errors and speed of the critical journeys, and send alerts that a person can act on.

### `watch/coverage` Critical journeys have owned signals

- Completion: Each critical journey has health and error signals with an owner and alert thresholds. The journeys without coverage are listed.
- Evidence: The list of critical journeys. For each journey: the signal, the owner and the threshold in the observability or analytics tool.
- Needs: `telemetry`, `analytics`
- Approved remedy (automation): Add monitors and alerts for each critical journey. Nori reads the routes and the analytics events, and writes a catalog of critical journeys as a pull request. For each journey without coverage, Nori adds error tracking in the code and creates an uptime monitor and an alert rule in the observability tool. Nori adds a weekly automation that keeps the catalog and the monitors in agreement. Needs: write access to the observability tool. A person confirms the list of journeys in the pull request.

### `watch/alerts` Alerts identify impact

- Completion: Each alert from an included service gives its source and its user impact, has an owner, and does not repeat for the same cause.
- Evidence: Alert rules with owners, and a dated sample of alerts that shows source, impact and grouping.
- Needs: `telemetry`
- Approved remedy (automation): Add owner, impact and runbook to each alert rule. Nori reads each alert rule through the observability API and adds the owner, the service, the impact statement and a runbook link. Nori writes the missing runbooks as a pull request and turns on grouping. Nori adds a monthly automation that reads the alert history, changes the rules that make noise and reports each change. Needs: write access to the alert rules.

### `watch/performance` Critical journeys have a performance baseline

- Completion: Each critical journey has a measured baseline, a target and an alert on the target. Each missed target has a recorded exception or an open work item.
- Evidence: The dated baseline measurement, the target and the alert for each journey, and the exception or work item for each missed target.
- Needs: `telemetry`
- Approved remedy (automation): Set a p95 target and an alert for each critical journey. Nori measures the current p95 of each critical journey from the traces, and proposes a target for each journey in a pull request to the journey catalog. After the merge, Nori creates a metric alert for each target, and adds a weekly automation that records the baseline and opens a work item for each missed target. Needs: performance data in the observability tool (Nori adds tracing by pull request if there is none), and write access to alerts. A person approves the targets.

## Release (`release`)

Deploy merged changes with a record, and keep a tested way to go back.

### `release/provenance` Each release has a record of its source and gates

- Completion: Each included release path records the source, the gates that passed, the approval, the artifact and the deployment result.
- Evidence: The release workflow and a dated run for each path, and the approval rule for each path.
- Needs: `code`
- Approved remedy (one-time): Write a gated deployment workflow with a release record. Nori writes a deployment workflow for each release path as a pull request. The workflow builds from a tagged commit, runs only after the required checks pass, waits for approval in a protected environment, and writes a release record with the source, the gates, the artifact and the result. Nori changes the scripts and documents that deploy from a personal computer so that they start the workflow. Needs: the Jiro (by Nori) GitHub app with permission to change workflow files. An admin adds the deployment secrets and names the approvers.

### `release/recovery` A bad release can be recovered

- Completion: Each critical service has a rollback or recovery procedure, and a recorded result from a real use or a rehearsal.
- Evidence: The procedure or workflow for each service, and the dated result of a real use or a rehearsal.
- Needs: `code`
- Approved remedy (automation): Write a rollback workflow and rehearse it each month. Nori writes a rollback workflow and a recovery runbook for each critical service as a pull request. Nori sets up a monthly automation that rehearses the rollback in staging and keeps the dated result with the runbook. Needs: the Jiro (by Nori) GitHub app with permission to change and start workflows, and a staging environment. A person starts a rollback in production.

## Cost review (`cost`)

Compare spend with use, and record the decisions.

### `cost/review` Spend is reviewed against use

- Completion: Each included service has visible spend and usage data, a budget with an owner, and tracked decisions about cost.
- Evidence: The spend source and its scope, the budget owner, a dated review and the work items for its decisions.
- Needs: `spend`, `tracker`
- Approved remedy (automation): Review spend against use each month. Nori adds service tags in the infrastructure code by pull request. Nori proposes a budget for each service from the spend of the last three months and, after approval, adds the budgets and the budget alerts to the infrastructure code. Nori sets up a monthly cost review automation that records each proposed decision as a work item. Needs: read access to the billing data, which a cloud admin must give. A person approves the budget amounts and the cost decisions.
