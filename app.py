#!/usr/bin/env python3
"""CLI prototype that turns a disorganized conference transcript into a professional briefing."""

from __future__ import annotations

import argparse
import os
import re
import textwrap
from datetime import datetime

import requests
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path or ".env")

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise SystemExit(
        "GOOGLE_API_KEY is missing. Populate `.env` (or your shell) with `GOOGLE_API_KEY=<key>` "
        "and rerun from the repository root."
    )

REQUEST_TIMEOUT = 15

FILLER_PATTERN = re.compile(
    r"\b(?:um|uh|er|ah|you know|like|i mean)\b", flags=re.IGNORECASE
)

DEFAULT_SYSTEM_INSTRUCTION = """You are a seasoned executive secretary. Transform disorganized meeting transcripts into professional briefings using third-person objective narration. Base every statement strictly on the provided transcript, never fabricate facts, and mark any unresolved matter as [To Be Determined] before concluding."""

DEFAULT_PROMPT_TEMPLATE = """Transcript:
{transcript}

Return a polished corporate recap with the following sections:
1. Event Summary — a short paragraph capturing the overall theme.
2. Key Decisions — numbered bullets describing confirmed outcomes.
3. Action Items — table-style bullets listing the owner (if mentioned) and timeline (or "TBD").
4. Formalized Quotes — paraphrases rewritten into clear executive wording.

Keep the narrative rooted in the transcript, flag contradictions or uncertain statements with [To Be Determined], and avoid adding information that is not explicitly present."""


def clean_transcript(raw_transcript: str) -> str:
    """Remove filler words while preserving the original structure."""
    without_fillers = FILLER_PATTERN.sub("", raw_transcript)
    without_fillers = re.sub(r"[ \t]+", " ", without_fillers)
    without_fillers = re.sub(r" *\n *", "\n", without_fillers)
    return without_fillers.strip()


def build_prompt(transcript: str, custom_prompt: str) -> str:
    if not transcript.strip():
        raise ValueError("Transcript input is empty; provide a real transcript file.")

    return custom_prompt.format(transcript=transcript.strip())


def call_llm(system_instruction: str, user_input: str, model_name: str, temperature: float) -> str:
    prompt_text = f"{system_instruction}\n\n{user_input}"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateText"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": {"text": prompt_text},
        "temperature": temperature,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    candidates = data.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini returned no candidates.")

    output = candidates[0].get("output", "")
    if isinstance(output, dict):
        return output.get("text", "").strip()
    return str(output).strip()


def fallback_recap(transcript: str) -> str:
    lines = [line.strip() for line in transcript.splitlines() if line.strip()]
    summary = lines[0] if lines else "Transcript text is unavailable."
    decisions = ["[To Be Determined] — no confirmed decisions are present in the provided text."]
    action_items = ["[To Be Determined] — no owners or timelines are included in the transcript."]
    quotes = []
    if lines:
        quotes.append(f"{lines[0]}")  # reuse first line as paraphrased quote
    if len(lines) > 1:
        quotes.append(f"{lines[1]}")

    recap_lines = [
        "Event Summary:",
        f"- {summary}",
        "Key Decisions:",
        *[f"- {decision}" for decision in decisions],
        "Action Items:",
        *[f"- {item}" for item in action_items],
        "Formalized Quotes:",
        *[f"- {quote}" for quote in quotes],
        "Note: The output was auto-generated without the Gemini response."
    ]
    return "\n".join(recap_lines)


def save_output(contents: str, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(contents)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transform a conference transcript into an executive-ready recap."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the transcript text file that documents the conference session.",
    )
    parser.add_argument(
        "--output",
        default="meeting_record.txt",
        help="Where to write the structured recap.",
    )
    parser.add_argument(
        "--prompt-template",
        default=DEFAULT_PROMPT_TEMPLATE,
        help="Custom user prompt template; include {transcript} where the transcript should be inserted.",
    )
    parser.add_argument(
        "--system-instruction",
        default=DEFAULT_SYSTEM_INSTRUCTION,
        help="Optional override for the system-style instruction sent to the LLM.",
    )
    parser.add_argument(
        "--model",
        default="gemini-1.5-flash",
        help="Generative model to call (e.g., gemini-1.5-flash).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Temperature (unused for Gemini but kept for interface parity).",
    )

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as transcript_file:
        transcript = transcript_file.read()

    cleaned_transcript = clean_transcript(transcript)
    original_length = len(transcript)
    cleaned_length = len(cleaned_transcript)

    prompt = build_prompt(
        transcript=cleaned_transcript,
        custom_prompt=args.prompt_template,
    )

    fallback_note = ""
    try:
        recap = call_llm(
            system_instruction=args.system_instruction,
            user_input=prompt,
            model_name=args.model,
            temperature=args.temperature,
        )
    except (requests.RequestException, RuntimeError) as err:  # pragma: no cover
        fallback_note = f"Fallback triggered: {err}"
        recap = fallback_recap(cleaned_transcript)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fallback_line = f"\nFallback note: {fallback_note}" if fallback_note else ""
    structured_output = textwrap.dedent(
        f"""
        === Generated Meeting Record ===
        Timestamp: {timestamp}

        Original transcript length: {original_length} chars
        Cleaned transcript length: {cleaned_length} chars

        {recap}

        === LLM Summary ===
        The model distilled the session into an event summary, identified confirmed decisions, 
        captured action items with owners/timelines, and reformulated quotes into professional prose 
        while flagging unresolved matters as [To Be Determined].
        {fallback_line}
        """
    ).strip()

    print(structured_output)
    save_output(structured_output, args.output)
    print(f"\nRecap saved to {args.output}")


if __name__ == "__main__":
    main()
