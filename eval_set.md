# Evaluation Set

1. **Normal case – multi-panel recap**  
   **Input:** Transcript from a 90-minute internal leadership summit where the CEO, CTO, and HR lead rotate through updates on product roadmap, engineering capacity, and recruiting goals, with each speaker referencing the same quarterly OKRs.  
   **Good output note:** Clearly separate summaries per agenda item, note aligned decisions, highlight dependencies between departments, and convert casual remarks (“we’re kinda drowning in tickets”) into polished observations (“engineering capacity remains strained due to elevated ticket volume”).

2. **Edge case – terse breakout with overlapping speech**  
   **Input:** Short, choppy transcript of a breakout discussion between three product managers who overlap sentences, switch between English and industry shorthand, and skip explicit action items.  
   **Good output note:** Fill in implied follow-up steps, assign owners inferred from context, and articulate the technical shorthand into accessible prose without inventing new facts.

3. **Failure-prone case – ambiguous or conflicting statements**  
   **Input:** A “hot topic” session where two directors debate contradictory rollout dates (“ships next week” vs “we’re still targeting May”), plus an attendee referencing unverified vendor commitments.  
   **Good output note:** Flag contradictions, avoid fabricating a single timeline, call out that dates require confirmation, and suggest reviewing the vendor claim instead of accepting it as fact.

4. **Case with external reference needs**  
   **Input:** Transcript where a speaker repeatedly mentions a study or metric (“the Gartner report said 47%”) but does not provide context or the actual summary.  
   **Good output note:** Summarize the speaker’s intent, note that the statistic was cited without sourcing details, and phrase the need for follow-up verification (e.g., “Confirm the Gartner percentage before distributing externally”).

5. **Case with non-native speakers and filler words**  
   **Input:** A European regional forum where speakers pause often, say “kind of,” “you know,” and mix British and American idioms while describing risk mitigation plans.  
   **Good output note:** Produce a fluent narrative that removes filler, harmonizes terminology, retains the speaker’s proposed risk controls, and preserves any nuance about uncertainty (“planning to…” vs “committing to…”).
