## Initial version
Use app.py to build a small reproducible Python prototype for your workflow.

Minimum expectations:

the script runs from the command line
it makes at least one LLM API call
at least one prompt or system instruction is configurable
output is saved to a file or clearly printed in structured sections
the submission is reproducible by a grader or TA
A strong prototype usually does one task clearly rather than trying to do too many things.

## Reversion 1
Modify app.py ,improve the LLM performance. You are a seasoned executive secretary.
Your task is to transform disorganized meeting transcripts into professional briefings.
Strictly adhere to the following:
1. Base your work solely on the original text; fabricating facts is strictly prohibited.
2. If participants did not reach a consensus on a particular matter, mark it as [To Be Determined].
3. Filter out all verbal fillers (e.g., “um,” “er”).
4. Use third-person objective narration.

### comment
Use the job description to further define the writing style and request additional details, ensuring that the final report aligns more closely with expectations.

## Reversion 2
modify app.py. To highlight the "contrast" in the report, include both the original text length and the compressed length when the task is completed. This provides a clear demonstration of the LLM's value. Additionally, summarize what the LLM did in a few sentences so that users can immediately understand the task that has been completed.

### comment
In addition to completing tasks, showcasing the model’s achievements is also a crucial aspect, as it helps users better understand the role of LLMs.