#!/usr/bin/env python3
"""CLI prototype that turns a disorganized conference transcript into a professional briefing."""

from __future__ import annotations

import argparse
import os
import re
import textwrap
from datetime import datetime

try:
    import openai
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: install the OpenAI client via `pip install openai`."
    ) from exc

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


def build_messages(transcript: str, custom_prompt: str) -> list[dict[str, str]]:
    if not transcript.strip():
        raise ValueError("Transcript input is empty; provide a real transcript file.")

    filled_prompt = custom_prompt.format(transcript=transcript.strip())

    return [
        {"role": "system", "content": DEFAULT_SYSTEM_INSTRUCTION},
        {"role": "user", "content": filled_prompt},
    ]


def call_llm(messages: list[dict[str, str]], model: str, temperature: float) -> str:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise SystemExit("Set OPENAI_API_KEY in your environment before running this script.")

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    choices = response.get("choices") or []
    if not choices:
        raise RuntimeError("LLM returned no choices.")

    return choices[0]["message"]["content"].strip()


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
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM model to call.")
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Temperature for the model: lower = more deterministic.",
    )

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as transcript_file:
        transcript = transcript_file.read()

    cleaned_transcript = clean_transcript(transcript)
    original_length = len(transcript)
    cleaned_length = len(cleaned_transcript)

    messages = build_messages(
        transcript=cleaned_transcript,
        custom_prompt=args.prompt_template,
    )

    if args.system_instruction != DEFAULT_SYSTEM_INSTRUCTION:
        messages[0]["content"] = args.system_instruction

    recap = call_llm(messages, model=args.model, temperature=args.temperature)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        """
    ).strip()

    print(structured_output)
    save_output(structured_output, args.output)
    print(f"\nRecap saved to {args.output}")


if __name__ == "__main__":
    main()
