---
name: using-a-web-browser
description: Use whenever a task needs a real web browser - logging in to a website, clicking through or testing a web app, filling in forms, scraping a JavaScript-rendered page, or taking page screenshots. The session has one always-headed Chrome that the user can watch and take over live.
---

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite, then work them in order:

- Run `nori-browser`. It starts the session's headed Chrome, or reuses it if it is already running, and prints connection instructions and the live view link.
  - If the shell blocks local network connections, request approval for the browser operation through the harness’s permission mechanism.
  - If `nori-browser` is missing or reports that this machine has no built-in browser, tell the user instead of installing one.
- Drive that browser with Playwright over CDP (see below). Never launch your own browser, never pass `headless`, and never install a virtual display or VNC software -- the display and the live view already exist.
- In your first reply after you start browsing, give the user the live view link so they can follow along or take over. Resolve it to the actual URL first.
  - Users can also reach it themselves: the Browser button in the web chat header, or `!urls` in Slack or Discord.
- When a human has to act -- signing in, a 2FA code, a CAPTCHA, a consent screen, a payment -- ask them to do it in the live view, then end your turn. Do not type or click in the browser while they are using it.
<system-reminder> Do not poll -- an open turn never reaches the user so they would never see the link. </system-reminder>
- When they reply, reconnect and continue. Their sign-in is already in the browser profile.
- Leave the browser running when you finish.
</required>

<system-note> To keep a sign-in for future sessions, follow `{{skills_dir}}/connecting-an-app-without-an-api/SKILL.md`. </system-note>

# Driving the browser

Playwright only needs its library here, not a browser download:

```bash
mkdir -p ~/.nori/browser-scripts && cd ~/.nori/browser-scripts
[ -d node_modules/playwright-core ] || npm install --silent playwright-core
```

```js
// ~/.nori/browser-scripts/task.mjs
import { execFileSync } from 'node:child_process';
import { chromium } from 'playwright-core';

const launcher = process.env.NORI_BROWSER_COMMAND || 'nori-browser';
const endpoint = execFileSync(launcher, ['--cdp-url'], { encoding: 'utf8' }).trim();
const browser = await chromium.connectOverCDP(endpoint).catch(() => {
  // Playwright includes the private endpoint in its connection error.
  throw new Error('Could not connect to the session browser. Run nori-browser to check access.');
});
// The default context is the persistent profile the user sees in the live
// view; new contexts would not share its sign-ins.
const context = browser.contexts()[0];
const page = context.pages()[0] ?? (await context.newPage());

await page.goto('https://example.com');
await page.screenshot({ path: 'page.png' });

// Disconnects only; Chrome and its pages stay up for the next step.
await browser.close();
```

- Keep the CDP address inside the script. Share only the Live view link printed by `nori-browser`.
- Older hosted worker images print connection instructions even with `--cdp-url`. On those images, pass the control address from those instructions to `connectOverCDP`.
- Every page and tab is visible in the live view, so keep work in one tab when the user is watching.
- `page.pdf()` works on this browser too.
