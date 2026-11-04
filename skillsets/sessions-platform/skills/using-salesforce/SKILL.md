---
name: using-salesforce
description: Use for any Salesforce work from a Nori session - SOQL queries, reading or changing records, describes, composite and Bulk API 2.0 jobs - through the org's managed Salesforce connection.
---

- Salesforce is reached only through the Nori Sessions Salesforce relay. Never sign in to Salesforce from this machine by any other route (`sf` CLI, MCP, browser login, OAuth, a pasted token). Salesforce freezes the user and revokes their logins when API traffic comes from addresses like this machine's; the relay sends every request from Nori's side instead.
- The relay is available when both variables are set (they come from `~/.nori/env.d/salesforce.sh`):
  - `NORI_SALESFORCE_RELAY_URL` - stands in for the org's instance URL.
  - `NORI_SALESFORCE_RELAY_TOKEN` - this session's relay token. Send it as `Authorization: Bearer`; it is not a Salesforce token.
- If they are not set, Salesforce is not connected for this org, or it was connected after this session started; in that case the file appears within the hour, so source it again later. An org admin connects Salesforce from the Integrations page: $NORI_SESSIONS_URL/integrations#integration-salesforce.
- Requests act as the Salesforce user who connected the org, usually an admin. Creating, updating, or deleting records changes the customer's live CRM: confirm the exact change with the user before any write.

## Calling the REST API

Append the usual REST path to the relay URL:

```bash
sf_api() {
  curl --silent --show-error \
    -H "Authorization: Bearer $NORI_SALESFORCE_RELAY_TOKEN" "$@"
}

# API versions
sf_api "$NORI_SALESFORCE_RELAY_URL/services/data/"

# SOQL (follow nextRecordsUrl, a path, for more pages)
sf_api -G "$NORI_SALESFORCE_RELAY_URL/services/data/v62.0/query" \
  --data-urlencode "q=SELECT Id, Name FROM Account ORDER BY CreatedDate DESC LIMIT 10"

# Create a record (after the user confirms)
sf_api -X POST -H 'Content-Type: application/json' \
  -d '{"Name":"Acme"}' \
  "$NORI_SALESFORCE_RELAY_URL/services/data/v62.0/sobjects/Account"
```

jsforce works with the relay URL as its instance URL and the relay token as its access token:

```js
import jsforce from 'jsforce';

const conn = new jsforce.Connection({
  instanceUrl: process.env.NORI_SALESFORCE_RELAY_URL,
  accessToken: process.env.NORI_SALESFORCE_RELAY_TOKEN,
  version: '62.0',
});
const { records } = await conn.query('SELECT Id, Name FROM Account LIMIT 10');
```

Stick to REST calls (`query`, `sobject(...).create/update/destroy`, `describe`, `requestGet/Post`). jsforce's `identity()`, SOAP, Metadata, and Bulk 1.0 APIs are not relayed.

## What the relay allows

- Everything under `/services/data/vNN.N/`: query, queryAll, search, sobjects (CRUD, describe, blobs), composite, limits, Tooling API, and Bulk API 2.0 (`jobs/ingest`, `jobs/query`, CSV bodies up to 32 MB).
- Refused (403): `/services/oauth2/*` and identity URLs, `/services/apexrest`, SOAP and Metadata (`/services/Soap`), Bulk 1.0 (`/services/async`), anonymous Apex (`tooling/executeAnonymous`, including inside composite requests), and path segments containing an encoded `/`, `%`, or `;` (so external ID values with those characters cannot be used in a URL; query by SOQL instead).

## Errors

| Status | Body | Meaning |
|--------|------|---------|
| 401 | `Unauthorized` | Missing relay token, or this session's claim ended. Source `~/.nori/env.d/salesforce.sh` again; if it still fails, the session no longer has access. |
| 401 | `salesforce_needs_reauth` | The Salesforce login expired or was revoked. An org admin reconnects it on the Integrations page. |
| 409 | `salesforce_not_connected` | Salesforce was disconnected for the org. |
| 429 | `salesforce_relay_busy` | Eight Salesforce requests are already running for this org. Wait briefly and retry; do not hammer. |
| 502 | `salesforce_refresh_failed`, `salesforce_unreachable` | Salesforce could not be reached. Retry later. |

Any other status and body come from Salesforce itself (for example `INVALID_FIELD`, or `REQUEST_LIMIT_EXCEEDED` once the org's daily API allowance is spent).

- The daily API allowance is shared with everything else in the customer's org. Prefer one SOQL query over many record reads, use composite requests to batch, and use Bulk API 2.0 for large exports or imports.
