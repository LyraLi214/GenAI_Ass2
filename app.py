#!/usr/bin/env python3
"""CLI prototype that turns a conference transcript into a polished meeting recap."""

from __future__ import annotations

import argparse
import os
import textwrap
from datetime import datetime

try:
    import openai
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: install the OpenAI client via `pip install openai`."
    ) from exc

DEFAULT_SYSTEM_INSTRUCTION = """You are an executive meeting reporter. Take conversational transcripts and build a structured recap that highlights decisions, action items, and formalized language. Keep tone professional, concise, and faithful to speaker intent."""

DEFAULT_PROMPT_TEMPLATE = """Transcript:
{transcript}

Please return a corporate-style recap with the following sections:
1. Event Summary — a short paragraph that captures the overall theme and emotions.
2. Key Decisions — numbered bullets that list the concrete outcomes or agreements.
3. Action Items — table-style bullets that include the owner (if mentioned) and timeline (or "TBD").
4. Formalized Quotes — a handful of high-level quotes or paraphrases rewritten into executive wording.

Avoid adding information that is not present in the transcript, and flag when speakers contradict each other or cite unverified facts."""


def build_messages(transcript: str, custom_prompt: str) -> list[dict[str, str]]:
    if not transcript.strip():
        raise ValueError("Transcript input is empty; provide a real transcript file.")

    filled_prompt = custom_prompt.format(transcript=transcript.strip())

    messages = [
        {"role": "system", "content": DEFAULT_SYSTEM_INSTRUCTION},
        {"role": "user", "content": filled_prompt},
    ]
    return messages


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

    messages = build_messages(
        transcript=transcript,
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

        {recap}
        """
    ).strip()

    print(structured_output)
    save_output(structured_output, args.output)
    print(f"\nRecap saved to {args.output}")


if __name__ == "__main__":
    main()
