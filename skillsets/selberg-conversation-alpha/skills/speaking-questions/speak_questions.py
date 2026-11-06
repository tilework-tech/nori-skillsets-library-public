#!/usr/bin/env python3
"""Turn the questions in a draft Slack reply into labelled spoken MP3 clips.

Reads the draft reply on stdin. One `claude -p` call rewrites every question
directed at the user into a short script written to be heard rather than read.
ElevenLabs voices each script (in parallel, falling back to one at a time when
the account's concurrency limit is hit), and each clip is uploaded into the
Slack thread in question order with `nori-slack upload`.

Prints {"clips": [...], "skipped": ...} as JSON. Exits 0 when every clip
succeeded (or there was nothing to do), 1 when any clip failed, and 2 on
configuration or LLM errors (nothing generated, details on stderr).

The LLM runs with no tools, no MCP servers, no settings, an empty working
directory, and only the environment it needs to authenticate, because the
draft reply may quote untrusted text.

Environment:
  SELBERG_CONVERSATION_MODE  must be "on", otherwise the script does nothing
  ELEVENLABS_API_KEY         required
  ELEVENLABS_VOICE_ID        default 21m00Tcm4TlvDq8ikWAM (Rachel)
  ELEVENLABS_MODEL_ID        default eleven_flash_v2_5
  ELEVENLABS_BASE_URL        default https://api.elevenlabs.io
  SELBERG_TTS_CONCURRENCY    default 4
  SELBERG_LLM_MODEL          default claude-haiku-5-5
  SELBERG_CLAUDE_BIN         default claude
  SELBERG_NORI_SLACK_BIN     default nori-slack
"""

import argparse
import http.client
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

MAX_CLIPS = 10
MAX_CONTEXT_SENTENCES = 5
MAX_SCRIPT_CHARS = 900
RATE_LIMIT_RETRIES = 4
NUMBER_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

PROMPT = """You are preparing spoken audio for a Slack reply that an AI agent is about to send.
The audio will be read aloud by a text-to-speech voice, so the listener cannot see the reply.

Find every question in the draft reply below that is directed at the reader and asks them to
answer or decide something. Ignore rhetorical questions and questions inside quoted text or code.
Keep the questions in the order they appear.

For each question, write:
- "question": the question restated so it makes sense on its own when heard, without the text.
- "context": a list of at most 5 short sentences giving the background the listener needs to answer.

Write for the ear, not the eye:
- Short, plain, conversational sentences.
- No markdown, bullet points, URLs, file paths, code, IDs, or hashes. Describe them in words instead.
- Spell out symbols and abbreviations the way a person would say them.

Respond with only JSON in this exact shape, and nothing else:
{"clips": [{"question": "...", "context": ["...", "..."]}]}
If there are no such questions, respond with {"clips": []}.

Draft reply:
<<<
%s
>>>
"""


class ConfigError(Exception):
    pass


class RateLimited(Exception):
    pass


def speakable(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\bwww\.\S+", "", text)
    text = re.sub(r"[*_`#>|~]+", "", text)
    text = text.replace("[", "").replace("]", "")
    return re.sub(r"\s+", " ", text).strip()


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


def build_script(number, question, context):
    context_sentences = [s for item in context for s in sentences(speakable(item))]
    parts = [f"Question {NUMBER_WORDS[number - 1]}.", speakable(question), *context_sentences[:MAX_CONTEXT_SENTENCES]]
    return " ".join(p for p in parts if p)[:MAX_SCRIPT_CHARS]


LLM_ENV_PASSTHROUGH = ("PATH", "HOME", "CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL")


def summarize(reply_text):
    model = os.environ.get("SELBERG_LLM_MODEL", "claude-haiku-5-5")
    claude = os.environ.get("SELBERG_CLAUDE_BIN", "claude")
    env = {k: os.environ[k] for k in LLM_ENV_PASSTHROUGH if k in os.environ}
    with tempfile.TemporaryDirectory() as empty_cwd:
        try:
            result = subprocess.run(
                [
                    claude, "-p", "--model", model, "--output-format", "text",
                    "--tools", "", "--strict-mcp-config", "--setting-sources", "", "--disable-slash-commands",
                ],
                input=PROMPT % reply_text,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=empty_cwd,
                env=env,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise ConfigError(f"LLM call failed: {error}") from error
    if result.returncode != 0:
        raise ConfigError(f"LLM call failed: {result.stderr.strip()[:300]}")
    match = re.search(r"\{.*\}", result.stdout, re.DOTALL)
    try:
        clips = json.loads(match.group(0))["clips"] if match else None
    except (json.JSONDecodeError, KeyError, TypeError):
        clips = None
    if not isinstance(clips, list):
        raise ConfigError("LLM did not return the expected JSON")
    items = []
    for item in clips:
        if not isinstance(item, dict) or not isinstance(item.get("question"), str) or not item["question"].strip():
            continue
        context = item.get("context") or []
        if isinstance(context, str):
            context = [context]
        items.append({"question": item["question"], "context": [c for c in context if isinstance(c, str)]})
    return items[:MAX_CLIPS]


def synthesize(script, path, api_key):
    base = os.environ.get("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io").rstrip("/")
    voice = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    model = os.environ.get("ELEVENLABS_MODEL_ID", "eleven_flash_v2_5")
    request = urllib.request.Request(
        f"{base}/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
        data=json.dumps({"text": script, "model_id": model}).encode(),
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            path.write_bytes(response.read())
    except http.client.HTTPException as error:
        raise RuntimeError(f"ElevenLabs response was cut off: {type(error).__name__}") from None
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")[:300].replace(api_key, "***")
        if error.code == 429:
            raise RateLimited(detail) from None
        raise RuntimeError(f"ElevenLabs returned {error.code}: {detail}") from None


def synthesize_all(clips, api_key):
    def attempt(clip):
        try:
            synthesize(clip["script"], Path(clip["path"]), api_key)
        except RateLimited:
            return clip
        except (RuntimeError, urllib.error.URLError, OSError) as error:
            clip["error"] = str(error).replace(api_key, "***")
        return None

    concurrency = max(1, int(os.environ.get("SELBERG_TTS_CONCURRENCY", "4")))
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        limited = [c for c in pool.map(attempt, clips) if c is not None]

    for clip in limited:
        for retry in range(RATE_LIMIT_RETRIES):
            time.sleep(0.5 * 2**retry)
            if attempt(clip) is None:
                break
        else:
            clip["error"] = "ElevenLabs rate limit: retries exhausted"


def upload(clip, channel, thread_ts):
    slack = os.environ.get("SELBERG_NORI_SLACK_BIN", "nori-slack")
    env = {k: v for k, v in os.environ.items() if k != "ELEVENLABS_API_KEY"}
    result = subprocess.run(
        [
            slack, "upload",
            "--file", clip["path"],
            "--channel", channel,
            "--thread-ts", thread_ts,
            "--title", clip["label"],
            "--initial-comment", f"*{clip['label']}:* {clip['question']}",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
    )
    if result.returncode != 0:
        clip["error"] = f"Slack upload failed: {result.stderr.strip()[:300]}"
    else:
        clip["uploaded"] = True


def run(args, reply_text):
    if os.environ.get("SELBERG_CONVERSATION_MODE") != "on":
        return {"clips": [], "skipped": "SELBERG_CONVERSATION_MODE is not on"}
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise ConfigError("ELEVENLABS_API_KEY is not set; run `source ~/.nori/env.d/custom.sh` or set it first")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    clips = []
    for number, item in enumerate(summarize(reply_text), start=1):
        clips.append({
            "number": number,
            "label": f"Question {number}",
            "question": speakable(item["question"]),
            "script": build_script(number, item["question"], item["context"]),
            "path": str(out_dir / f"question-{number}.mp3"),
            "uploaded": False,
            "error": None,
        })

    synthesize_all(clips, api_key)

    if args.channel and args.thread_ts:
        for clip in clips:
            if clip["error"] is None:
                upload(clip, args.channel, args.thread_ts)
    return {"clips": clips, "skipped": None}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", required=True, help="Directory to write question-N.mp3 files into")
    parser.add_argument("--channel", help="Slack channel ID to upload clips into")
    parser.add_argument("--thread-ts", help="Root ts of the Slack thread to upload clips into")
    args = parser.parse_args()

    try:
        output = run(args, sys.stdin.read())
    except ConfigError as error:
        print(f"speak_questions: {error}", file=sys.stderr)
        return 2
    print(json.dumps(output, indent=2))
    return 1 if any(c["error"] for c in output["clips"]) else 0


if __name__ == "__main__":
    sys.exit(main())
