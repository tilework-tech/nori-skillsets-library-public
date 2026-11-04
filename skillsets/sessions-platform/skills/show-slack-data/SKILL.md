---
name: show-slack-data
description: Use when showing data, trends, or comparisons in Slack with native charts or tables through nori-slack.
---

<required>
1. Read `{{skills_dir}}/nori-slack/SKILL.md`. Use the user's authorized channel or thread and verified data.
2. Propose the visualization for the requested data and confirm its type and concise, exact axis and series labels with the user.
3. Resolve granularity and data-volume issues against Slack's limits; confirm any changes to the agreed view.
4. Build JSON, preview with `--dry-run`, post through `nori-slack`, and check `ok` before reporting success.
</required>

## 2. Propose and confirm the visualization

Propose the smallest useful chart or table for the user's data:

- **Line:** trends over time.
- **Bar:** compare categories or periods. Multiple series produce grouped bars.
- **Area:** filled trends; series overlap in array order, with the first at the back. These are not stacked totals.
- **Pie:** a small part-to-whole comparison with positive values; prefer bars when precise comparison matters.
- **Table:** exact values, missing observations, or more detail than a chart can show; use `nori-slack`'s table guidance.

Show a compact proposal with the exact chart title, X-axis, Y-axis (including units), and series/category labels; for a pie or table, show slice labels or column headings instead. Keep labels short and unambiguous so the user can confirm them easily. For example: `Line: Example measurements | X: UTC day | Y: Value (units) | Series: Reading | Categories: Oct 1, Oct 2, Oct 3`. Obtain confirmation before continuing; use choices the user has already explicitly supplied without asking again.

## 3. Resolve granularity and chart limits

Check the proposed view against the limits below. If it will not fit, propose coarser buckets, explicitly labeled grouping/selection, or multiple charts. Preserve the metric's meaning when aggregating; never silently truncate data. Confirm any changed granularity, selection, or labels with the user before building JSON. If the agreed view fits, proceed.

State the measure, unit, source, and relevant filters; include date range and timezone for time-based data. For time comparisons, use equal complete periods. Missing data is not zero: use zero only for a known zero; otherwise use a table or explain the unavailable interval. For percentage change from zero, say “new/from zero” instead of dividing by zero.

| Field | Limit / requirement |
| --- | --- |
| Chart blocks | At most 2 per message |
| `title` | String, at most 50 characters |
| `chart.type` | `line`, `bar`, `area`, or `pie` |
| Line/bar/area `series` | 1–12; unique `name` strings, at most 20 characters each |
| Each series `data` | 1–20 `{ "label": string, "value": number }` points; finite numbers, negative allowed |
| `axis_config.categories` | Unique labels in display order, at most 20 characters each; every series must have exactly one point per category |
| `axis_config.x_label`, `y_label` | Optional axis titles, at most 50 characters each |
| Pie `segments` | 1–12 `{ "label": string, "value": number }` entries; labels at most 20 characters, values strictly positive |

Keep labels unambiguous when shortening them. Use only documented fields; custom colors, axis bounds, null gaps, and stacking controls are not part of this schema.

### Series colors

Slack colors line, bar, and area series by position in `series`, not by name: naming a series "Red" does not make it red. Positions 1–6 are six base hues and look the same in both themes. Positions 7–12 repeat those hues as an alternate shade that flips with the viewer's theme: lighter in dark mode, darker in light mode. Use positions 1–6 when color must mean the same thing to every viewer. Colors were sampled from rendered charts (October 2026); Slack may change its palette, so verify against a rendered chart when color carries meaning.

| Position | Color | Dark theme | Light theme |
| --- | --- | --- | --- |
| 1 | Orange | `#d56a37` | `#e96825` |
| 2 | Green | `#259b69` | `#20a271` |
| 3 | Purple | `#b26ec3` | `#c474d3` |
| 4 | Blue | `#1699ca` | `#0e9dd3` |
| 5 | Red | `#d94c75` | `#ef3e75` |
| 6 | Indigo | `#4d65c5` | `#4864d2` |
| 7 | Alt orange | `#e4a07f` peach | `#c84600` burnt orange |
| 8 | Alt green | `#8dd2b5` mint | `#0e674d` forest green |
| 9 | Alt purple | `#d8bae1` lavender | `#611f69` plum |
| 10 | Alt blue | `#58bdde` sky blue | `#0071a4` deep blue |
| 11 | Alt red | `#e6a7ba` pink | `#9e0b2e` crimson |
| 12 | Alt indigo | `#899bdc` periwinkle | `#2840a9` navy |

To color categories by status (for example red / yellow / green risk), give each status its own series at the matching position and set every other series' value to 0 for that category. Fill unused positions in between with all-zero series named after their color (for example `Purple`, `Blue`), so the legend stays honest. Every series adds a slot to each bar group, so bars get thinner as positions are added.

## 4. Build JSON and post

Use `blocks` containing `type: "data_visualization"`, a `title`, and a `chart`. Include top-level `text` with a useful textual equivalent for notifications and screen readers; put the visible explanation in a `section` block too. Do not combine `markdown_text` with `text` or `blocks`. Prefer one chart and one sentence explaining the result.

Resolve the channel ID from conversation context or `nori-slack conversations.list --paginate`; set `thread_ts` to the parent message's timestamp for a thread reply and omit it for a channel post. Native charts require an explicit API call; avoid duplicating the post in the final reply.

Serialize the payload to a temporary JSON file. For repeated charts, use a small script to build payloads and invoke `nori-slack` sequentially.

Example with **synthetic data**: replace the destination and data before sending.

```json
{
  "channel": "C_REPLACE_ME",
  "text": "Example measurements — synthetic data, Oct 1–3 2026 UTC: 10, 12, 15 units.",
  "unfurl_links": false,
  "unfurl_media": false,
  "blocks": [
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*Example measurements*\nSynthetic data · Oct 1–3 2026 · UTC · 10 → 12 → 15 units." }
    },
    {
      "type": "data_visualization",
      "title": "Example measurements",
      "chart": {
        "type": "line",
        "series": [{ "name": "Reading", "data": [
          { "label": "Oct 1", "value": 10 },
          { "label": "Oct 2", "value": 12 },
          { "label": "Oct 3", "value": 15 }
        ] }],
        "axis_config": {
          "categories": ["Oct 1", "Oct 2", "Oct 3"],
          "x_label": "UTC day",
          "y_label": "Value (units)"
        }
      }
    }
  ]
}
```

With the prepared payload saved as `/tmp/slack-chart.json`:

```bash
nori-slack --json-input chat.postMessage --dry-run < /tmp/slack-chart.json
nori-slack --json-input chat.postMessage < /tmp/slack-chart.json
```

Dry-run checks the outgoing request, not Slack's schema or the rendered chart. Inspect the send response: require `ok: true` and retain `channel` and `ts`. Resolve the link using `nori-slack chat.getPermalink --channel CHANNEL_ID --message_ts RETURNED_TS`. Report API acceptance accurately; only claim visual verification if the rendered message was inspected.

On `invalid_blocks`, fix the payload against the reference below. Report access restrictions and honor rate-limit retry delays. After an ambiguous timeout, check whether the post exists before retrying.

References: [Slack chart schema](https://docs.slack.dev/reference/block-kit/blocks/data-visualization-block/) and [message posting, fallback text, and errors](https://docs.slack.dev/reference/methods/chat.postMessage/).
