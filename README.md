## Enterprise Conference Meeting Recap

In a large enterprise conference or seminar, stakeholders expect a polished, complete record of what transpired. The session may involve multiple panels, breakout discussions, and live Q&A, and attendees often speak informally or interrupt each other. As a professional enterprise administrative assistant, the AI agent ensures the documentation not only captures who said what but also restructures the conversation into a concise summary with key conclusions and rephrased, professional prose that suits corporate archives or executive distribution while minimizing transcription errors or misinterpretations.

### Workflow

1. **Selection & Verification:** The AI agent begins by selecting the most complete transcript or high-quality audio recording and cross-checking speaker labels, timestamps, and agenda markers against the official event program to catch missing segments or mislabeled participants.
2. **Segmentation & Context tagging:** The AI agent maps conference segments to agenda items, flags overlapping conversations, and annotates any references to prior decisions or external documents that will need to be clarified in the recap, reducing the chance of omitting dependencies.
3. **System Enrichment:** The automated helper consumes the cleaned transcript, detects speaker roles, standardizes terminology, formalizes colloquial language, and surfaces the key decisions, possible risks, and next steps while honoring the intent behind each statement.
4. **Error Checking:** The AI agent compares the generated recap against the annotated transcript, resolves contradictions (e.g., conflicting dates), confirms unverified claims, and ensures action items have clear owners or asks a human reviewer for verification before finalizing.
5. **Polish & Distribution:** Once verified, the AI agent tidies the recap for tone consistency, adds metadata (event name, date, attendees), and routes the final document to leadership or archives it for future reference.

### User

- The user is the enterprise event coordinator or executive assistant responsible for post-session documentation.

### Input

- A transcript (or audio recording) of the conference or seminar, optionally tagged with speaker identities and timestamps.

### Output

- A structured, readable meeting record containing a scene summary, key decisions, clarified action items, and formalized quotes or paraphrases suitable for sharing with senior leadership.

### Value

Automating this task saves hours of manual editing, ensures nothing important is omitted, and raises the quality of the deliverable by replacing casual speech with executive-ready language while preserving the actual intent of each participant.

### Prototype CLI

1. **Install requirements**: `pip install openai` and export `OPENAI_API_KEY` to point at a valid key before running the script.
2. **Run the prototype**: execute `python app.py --input path/to/transcript.txt --output recap.txt`. The script prints a timestamped recap with sections such as the event summary, decisions, action items, and formalized quotes, and it writes the same text to `recap.txt`.
3. **Customize instructions**: pass `--prompt-template` to adjust the user prompt (just include `{transcript}` where the transcript should go) and `--system-instruction` to tweak the assistant role. Change `--model` or `--temperature` if you want a different style.
4. **Review & distribute**: after generating the record, scan for nuance, then share the saved file with stakeholders or attach it to the official minutes.
