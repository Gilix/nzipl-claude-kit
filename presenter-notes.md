# Presenter Notes: Collective Intelligence for the Lab

**Format:** 90-min Zoom. Pitch presentation (Team plan not yet approved; this meeting surfaces the case for it). Mixed audience: 2-3 people with some Claude experience, the rest new. Pre-recorded demo, no live demos. Kit shared in advance via public GitHub (no login required).

**Time budget:** ~50 min content, ~12 min interactive moments + demo, ~25 min Q&A, buffer at close.

**Rhythm:** three interactive moments (poll, chat rediscovery, closing question), one recorded demo. End on the audience's question, not mine.

**Pre-share:** `pre-read.md` + GitHub link sent today (not homework, curiosity-prime).

---

## Slide 1 -- Title [0:00, 30 sec]

**Core point:** Frame as a proposal, not a tech demo.

- This session is about how we work together with AI, not about AI itself.
- Three acts: what the team knows together, what the team builds together, how the team adopts it.
- "Collective" is deliberate. Not about any one person's Claude usage. About what happens when the whole Lab shares context.
- Move quickly. The poll is where the room wakes up.

> **Transition:** Before I set up the problem, I want to know where everyone is.

---

## Slide 2 -- Problem: Knowledge Stays Local [0:30, 2 min]

**Core point:** Every time two people independently discover the same thing, the Lab pays for it twice.

- Each of us uses Claude independently. Fine for individual productivity. The problem: nothing carries over.
- Real example: DataMexico's /data endpoint silently drops manufacturing sectors 31-33. I found this the hard way. If anyone else queries that endpoint, they hit the same wall &mdash; my session is invisible to theirs.
- Before/after on screen: Person A learns something. Without a shared system, Persons B and C learn it again from scratch. With shared context, they never hit the problem.
- Applies to everything: data sources, API quirks, methodology patterns, design conventions.
- Cost of rediscovery is not just time. It is inconsistency. Two people solving the same problem independently solve it differently.

> **Transition:** Before we go further, a quick read on the room.

---

## Slide 3 -- Where are you today? [2:30, 2 min] INTERACTIVE

**Core point:** Set expectations. Signal this is a conversation.

- Zoom poll: "Which best describes you today?"
  - (A) I use Claude.ai or ChatGPT in a browser
  - (B) I've used an AI coding tool in a terminal or IDE
  - (C) I run pipelines or build automations with Claude
  - (D) I've never used Claude or anything like it
- Give it 60 seconds. Share results.
- Acknowledge the distribution aloud: "Looks like most of us are at A or D. The next two slides are for you. B and C, you'll help fill in the kit once the Team plan lands."
- This slide sets the tone: interactive, non-judgmental, mixed audience welcome.

> **Transition:** Let me level-set for anyone newer to Claude before we talk about the Lab.

---

## Slide 4 -- What Claude is (and isn't) [4:30, 4 min] PRIMER

**Core point:** Claude is a well-read generalist who joined the Lab yesterday. Smart, articulate, no institutional memory.

- Plain framing: Claude is a large language model. It reads what you give it, matches patterns against its training, generates text that continues the pattern.
- Walk the "good at" column. Don't read every line &mdash; pick 3 and expand:
  - Summarizing long documents (key for a research Lab)
  - Drafting prose in a voice you specify
  - Translating between formats (prose &harr; outline, English &harr; Spanish)
- Walk the "limited at" column with equal weight:
  - Facts after training cutoff &mdash; confirm with a live source
  - Exact math &mdash; use a calculator
  - Citing specific papers without source material &mdash; will hallucinate references
  - Things you didn't tell it about &mdash; unpublished work, internal context, private data
- Land the callout: "The kit fills the 'didn't tell it about' gap &mdash; for the Lab."

> **Transition:** Now, how you talk to it matters more than most people realize.

---

## Slide 5 -- How to talk to Claude effectively [8:30, 4 min] PRIMER

**Core point:** Bad answers are usually under-prompted. Five moves improve most prompts.

- Don't read all five tip cards verbatim &mdash; the audience can see them. Narrate the pattern.
- Pick tip #1 and read both examples aloud with emphasis. Let the gap land. Repeat for tip #2.
- Skim tips #3-5 quickly, calling out just the heading and the weak example for each.
- Close with: "Bad answers are usually under-prompted. Good answers are specific, contextualized, iterated."
- Optional if time: invite one person to share a prompt that flopped recently. Reframe it live using one of the five moves. This turns primer into hands-on for 30 seconds without requiring tools.

> **Transition:** Now we're ready to talk about the Lab.

---

## Slide 6 -- Claude Team: What It Solves and What It Doesn't [12:30, 2 min]

**Core point:** A Team plan is necessary but not sufficient. Access is not the bottleneck.

- Left column: the Team plan handles billing, usage limits, web access, Projects. Genuinely useful.
- Right column: what it does not do. No shared memory between team members. No code execution. No awareness of our codebase, data files, or deliverable architecture. No compounding. Every conversation starts fresh.
- Key distinction: the Team plan gives everyone access to a capable AI assistant. It does not give them a capable AI assistant that knows the Lab.

> **Transition:** Before we go further, a quick but important privacy note.

---

## Slide 7 -- What Claude shouldn't see [14:30, 3 min]

**Core point:** Data boundaries before tool adoption. Especially important for a research Lab with confidential client work.

- Read both columns. Pause on "Never share" &mdash; the items there are the ones that would get the Lab in trouble.
- Emphasize the callout: Claude Team plan does not train on conversations. Anthropic's commitment is real and documented. Counters the most common fear.
- But model behavior is not the same as data handling. Treat anything you paste as if it could leave your screen. When in doubt, ask.
- This slide is short because the rule is simple. The point is making sure everyone has heard it before any tool question.

> **Transition:** Now, where the real leverage is.

---

## Slide 8 -- Claude Code: The Step Beyond Chat [17:30, 2 min]

**Core point:** Claude Code reads the repo, runs code, writes files, loads context automatically.

- Claude Code runs in a terminal or IDE, not the browser. Sees the entire project.
- Four capabilities on screen. Walk through briefly &mdash; don't over-explain, the audience will see this in the demo.
- Important: Claude Code is included with every Team subscription. No separate license, no extra cost.

> **Transition:** That auto-loaded context file is the mechanism.

---

## Slide 9 -- How Claude Code Learns from a Repo [19:30, 2 min]

**Core point:** Three mechanisms, all loaded automatically when Claude Code opens in the repo directory.

- CLAUDE.md: auto-loaded context. The briefing every Claude session reads before it talks to you. Data sources, API patterns, deliverable standards, glossary, methodology.
- Skills: invocable expertise. Design system, chart styles, analytical templates.
- Commands: reusable prompts for structured tasks.
- "Auto-loaded" is the important part. No paste, no upload. Open Claude Code in the repo; it reads these on its own.
- This is what makes it collective intelligence. When anyone opens Claude Code here, they inherit everything the team has documented.

> **Transition:** Let me walk you through what's actually in the kit.

---

## Slide 10 -- What's in the Kit [21:30, 2 min]

**Core point:** One repo. Clone it and your Claude sessions know the Lab.

- Walk the five rows. Use the actual snippets:
  - CLAUDE.md: Lab context. OEC auth pattern example.
  - glossary.md: 31 acronyms + 22 internal terms. Relatedness density example.
  - gotchas.md: silent-failure issues. DataMexico /data example.
  - discoveries.md: covered on next slide.
  - Design system: lives in `.claude/skills/nzipl-design/`. This deck is styled with it.
- If they skimmed the pre-read, they've already seen two of these. Reference that: "For those who opened the repo this morning, you've seen CLAUDE.md and gotchas.md already. That's what's loading automatically into any Claude session that opens here."

> **Transition:** discoveries.md is where the compounding happens.

---

## Slide 11 -- discoveries.md [23:30, 2 min]

**Core point:** One line, push, done. The contribution mechanism.

- Show the real file. Date, author, finding, tag. In practice: write the one-liner. Tags optional.
- Walk through 2-3 real entries:
  - 2026-04-07, DataMexico /data drops manufacturing sectors. Workaround: /stats/rca.
  - 2026-04-08, FDI enrichment: one web search per row covers 5-7 of 8 source columns.
- Not just errors. Data sources, patterns, commands, methodology insights. Anything worth sharing.
- Cost: 30 seconds. Return: permanent. Every Claude session from that point forward knows what you wrote.

> **Transition:** I want to try something.

---

## Slide 12 -- Your Turn: What Have You Rediscovered? [25:30, 3 min] INTERACTIVE

**Core point:** Make contribution feel real, not hypothetical.

- Prompt the room: "Post in Zoom chat &mdash; one thing you rediscovered in the last month. A data source, an API quirk, a methodology pattern, a naming convention. 30 seconds to type."
- Wait. Silence is fine. Read 2-3 contributions aloud. Don't evaluate.
- Reframe each one: "That's a discoveries.md entry. Today it lives in your head. With the kit, it's a line every Claude session inherits."
- If the room is quiet, prime it: read one of my own first. "I'll start: HS6 code 870839 has no data in BACI 2022 cube; fall back to baci_a_02. Your turn."
- Keep this crisp &mdash; 3 min max. The point is felt, not exhaustive.

> **Transition:** Let me show a concrete example of a shared command.

---

## Slide 13 -- Example: /enrich-fdi [28:30, 2 min]

**Core point:** A task that started as one person's need, now shared infrastructure anyone can run.

- Context: fDi Markets dataset has 698 FDI rows. Each needs source URLs. Manually: hours per batch.
- Before: xlsx with project data, columns P-W empty.
- After: same file, columns filled. Reuters, PV Magazine, Electrive, press releases.
- The command knows column map, search strategy, quality rules, fallback logic. The person running it doesn't need to know any of that.
- This is the pattern for any recurring structured task. Document it as a command. Share it.

> **Transition:** That was Act 1. Now what we build on top of it.

---

## Slide 14 -- From Deliverables to Platform [30:30, 2 min]

**Core point:** The Lab already produces sophisticated output. The question is whether it stays bespoke or becomes a system.

- Read the big statement aloud. Let it land.
- Four layers on screen. Name each in one phrase:
  - Data: OEC, DataMexico, BNEF, OSM, WRI. Python stdlib only. Cached. Reproducible.
  - Analytical: play selection, subnational RCA, relatedness density, supply chain mapping.
  - Visualization: play cards, infrastructure maps, selectors. Self-contained HTML.
  - Knowledge: the kit. Makes the other three accessible.
- The layers exist for Mexico. The question is whether they stay as one person's toolbox or become team infrastructure.

> **Transition:** So where are we now?

---

## Slide 15 -- Where We Are [32:30, 2 min]

**Core point:** Mexico proved the architecture. Phases are concrete, not aspirational.

- Mexico: three play cards, infrastructure map (15 layers), play selector, Atlas Bot prototype.
- Already in motion: CICE serves cross-country comparisons, WP4 maps competitiveness across 155 countries.
- Phases (read aloud):
  - Phase 1, this summer: systematize Mexico and Brazil pipelines. `/play-card --country=brazil --play=solar` as the goal command.
  - Phase 2, fall: extend to India. Formal CICE integration.
  - Phase 3, winter: Atlas vision. Appendix for details.
- Honest framing: "This is a roadmap, not a promise. Phase 1 is concrete. Phase 3 depends on what we learn in 1 and 2."

> **Transition:** Act 3: how the team actually uses this.

---

## Slide 16 -- Levels of Adoption [34:30, 2 min]

**Core point:** Most of the team is at Level 0. The kit moves everyone to Level 1 on day one.

- Walk five levels briefly:
  - Level 0: Chat. Stateless. Every session starts from zero.
  - Level 1: Kit-informed. Clone the repo, open Claude Code. Immediate win.
  - Level 2: Pipeline. Run commands. Claude handles code; you review output.
  - Level 3: Contributor. Append discoveries. Kit gets smarter because you used it.
  - Level 4 (faint): Agent. Later in the year. Not the focus today.
- Key message: nobody needs to jump to Level 4. Level 1 is the ask.

> **Transition:** The concrete difference between 0 and 1.

---

## Slide 17 -- Level 0 vs. Level 1 [36:30, 2 min]

**Core point:** Same person, same question. Only difference: the kit repo was cloned.

- Left (Level 0): "What is Mexico's comparative advantage in solar equipment?" Generic. Wikipedia-level.
- Right (Level 1): "What is Mexico's RCA for solar supply chain products?" Uses S0 methodology. Cites HS6 products. Points to the pipeline.
- The difference is not that Claude got smarter. Claude got briefed. It knows vocabulary, methodology, data sources, deliverable architecture.
- Effort to get from 0 to 1: clone a repo.

> **Transition:** Here it is in motion.

---

## Slide 18 -- Demo: Watch it happen [38:30, 2 min] RECORDED

**Core point:** The comparison made real. Silent clip, no narration over.

- Play the 60-sec screencast. Silence until it finishes.
- What the clip shows:
  - Left half: Claude.ai in a browser. No context. "What is Mexico's RCA for grid hardware?" Generic answer.
  - Right half: Claude Code in a terminal inside the kit repo. Same prompt. Cites RCA 3.02, $16.8B exports, top states (Nuevo Le&oacute;n, Sonora, Baja California), specific data files.
- After clip, one line: "Same person. Same prompt. The right side is how the Lab could be running, once the Team plan is in."
- If the video fails: read the right-side answer aloud from the clip's caption and mention "this is what the tool can already do &mdash; the kit is public, readable today, waiting for the team's Claude accounts."

> **Transition:** Let me make this concrete for researchers in the room.

---

## Slide 19 -- Research use cases [40:30, 4 min]

**Core point:** Six workflow stages where a Lab-informed Claude actually helps.

- Don't read all six card bodies. Pick the two most relevant to the room and expand:
  - Literature review: the prompt shown (8 papers, three claims they agree on, the one they disagree about). Concrete.
  - Drafting: draft the Findings section using the voice of published Mexico play cards. Under 600 words.
- For the other four, name them in one sentence each:
  - Data sense-making: "Why might Nuevo Le&oacute;n's RCA have dropped?"
  - Peer review: "Where would a different school push back?"
  - Visualization: "Suggest three chart types for this comparison."
  - Translation: "Translate this abstract to Spanish, preserve technical terms."
- Close: "Pick one. Try it next week against something on your actual plate. That's the Level 1 experience."

> **Transition:** Level 2 is where the team runs pipelines.

---

## Slide 20 -- Level 2: Pipeline Users [44:30, 2 min]

**Core point:** Run the analysis, review the output, refine what matters.

- Refer back to Demo 2 context ( `/enrich-fdi`). That was a Level 2 session.
- The person running it didn't write a line of code. They typed a command name.
- Pattern for all pipeline-level work: run a command, Claude handles mechanics, you review and apply judgment.
- Critical skill at Level 2 is not coding. It is knowing what the output means and whether it is right. That is analytical judgment, which the Lab already has.

> **Transition:** Level 3: the norm that makes this compound.

---

## Slide 21 -- Level 3: The Norm That Makes It Work [46:30, 2 min]

**Core point:** The kit grows because the team uses it. One line at a time.

- Four scenarios on screen. Walk quickly:
  - API quirk &rarr; one line to discoveries.md
  - Better data source &rarr; discoveries.md with details
  - Recurring task &rarr; draft a command, PR it
  - Claude misreads the kit &rarr; that's also a discovery; fix the kit
- Footnote on Level 4: "Eventually, some checks run on their own. Appendix has details. Not today's ask."

> **Transition:** Why this compounds.

---

## Slide 22 -- The Compounding Effect [48:30, 2 min]

**Core point:** Chat is linear. Collective intelligence compounds.

- Read the big statement aloud: "Every discovery makes every future session smarter. Every command makes every future task faster."
- Bar chart: compounding curve over 8 months.
- Callout is the sharpest line in the deck: "The team that treats Claude as a chatbot gets a calculator. The team that builds collective intelligence gets an operating system."
- Let it land. This is the conceptual climax.

> **Transition:** Before the ask, two honest notes.

---

## Slide 23 -- What Claude doesn't replace [50:30, 2 min]

**Core point:** Draw the line around what stays human.

- Four cards. Read each heading; speak one sentence:
  - Lab judgment: contested decisions belong to humans.
  - Peer review: Claude can spot gaps, not confer validity.
  - Fieldwork: the signal is in the room, not in the transcript.
  - Client trust: reputation rests on humans in the room.
- Close: "The kit is a force multiplier, not a substitute. A Lab without judgment, peer review, fieldwork, and trust doesn't become a Lab by adding Claude."

> **Transition:** And what could break.

---

## Slide 24 -- Honest limits [52:30, 2 min]

**Core point:** Pre-empt the skeptic's three questions.

- **What breaks?** The kit drifts from reality if nobody updates it. The first stale entry erodes trust. Mitigation: quarterly review, named maintainer, team contributes.
- **What's the risk?** Wrong discoveries propagate. Mitigation: two-lane system. discoveries.md is free-for-all (fast, append-only). Promotion to gotchas.md or glossary.md requires PR review. High-trust / high-signal separation.
- **What's the cost?** Claude Team: ~$30/seat/month. Contribution: 30 seconds per discovery, maybe once a week. That's the full operating cost.

> **Transition:** So here's how we get from yes to working.

---

## Slide 25 -- Implementation timeline [54:30, 3 min]

**Core point:** The ask is not vague. Here's week-by-week.

- Walk the six timeline items:
  - Week 1: Team plan signed, seats provisioned, kit shared at Lab level.
  - Week 2: 30-min hands-on per person. One real prompt against their actual work.
  - Week 3: first discoveries.md entry from someone other than me. Celebrate it publicly.
  - Month 1: first pipeline run from a new author &mdash; goes into a live deliverable.
  - Month 3: first contributed command from a new author. PR, review, merge.
  - Quarterly: review, measure, decide what to systematize next.
- Close: "None of this depends on everyone becoming technical. It depends on one norm: when you learn something, add it."

> **Transition:** The ask.

---

## Slide 26 -- The Ask [57:30, 3 min]

**Core point:** Four things. All proportional.

- Walk each card. Don't rush &mdash; this is the business end of the deck:
  - **Claude Team plan**: shared subscription. Claude.ai for everyone plus Claude Code for pipeline work. One invoice, one admin.
  - **Kit as Lab resource**: repo is public at github.com/Gilix/nzipl-claude-kit. Readable today. Usable for real work once the Team plan lands.
  - **One norm**: when you learn something worth sharing, add a line to discoveries.md. 30 seconds. Permanent return.
  - **Quarterly review**: measure discoveries, commands, pipeline runs. Review the roadmap. First review 90 days after approval.
- Close: "The gap between 'I learned something' and 'the whole Lab knows it' should be one line and one push. That's what a yes gets us."

> **Transition:** One question before Q&A.

---

## Slide 27 -- One question before Q&A [60:30, 3 min] INTERACTIVE

**Core point:** End on the audience's question, not mine.

- Prompt: "Post in Zoom chat &mdash; what question would you most want answered by a Lab-informed Claude? One sentence."
- Give it 90 seconds. Read 3-4 aloud.
- Frame what those become: "These are the first entries on the list of things we prove the kit can do, once the Team plan is in. I'll come back with answers as we roll this out."
- Thank the room.

> **Transition:** Q&A. Going over 90 is fine. I'll stay as long as questions come.

---

## Q&A [63:30, 25+ min]

**Likely questions and short answers:**

- *"Can we try it without the Team plan?"* → Anyone with a personal Claude Pro account can clone the repo and run Claude Code today. It works. But collective intelligence requires everyone on the same plan so contributions flow back.
- *"What if someone adds a wrong discovery?"* → discoveries.md is free-for-all; gotchas.md and glossary.md require review. Wrong entries get caught in the promotion step or corrected in-line.
- *"How much time does this take per week?"* → 30 seconds per discovery, if you have one. Usually 1-2 things a week worth logging. So 1-2 minutes.
- *"Do I need to know Git?"* → Basics help (clone, pull, commit). Not required for Levels 0-2. For Level 3 contributions, yes &mdash; and we can pair the first time.
- *"What about confidentiality / JHU compliance?"* → Team plan does not train on your inputs. But treat pastes as if they could leave your screen. Never paste anything covered by NDA or marked confidential. When in doubt, ask.
- *"What does this cost the Lab?"* → ~$30/seat/month for Team. Time: ~1-2 min per person per week for contributions. Smaller than most existing software line items.
- *"Why not GPT / another tool?"* → Pragmatic answer: the kit is built around Claude Code's file-loading behavior, which is distinctive. If you'd rather use another tool for chat, that's fine &mdash; the kit works best with Claude Code for pipelines.
- *"What if I want to build an agent?"* → Level 4. We'll run a separate session on this in Q3 after the Team plan is seasoned. Come find me if you want to prototype sooner.
- *"Can I start contributing to the kit now?"* → The repo is public. PRs welcome. Discoveries via comment/issue if that's easier. Real use with Claude starts once the Team plan is in.

---

## Appendix A -- Atlas Vision [NOT PRESENTED, reference only]

CICE evolves from cross-country snapshots to subnational depth.

- Subnational data: state-level RCA, municipality trade, supply chain employment, infrastructure readiness. Replicated per country.
- More technologies: process chain products alongside supply chain products. Connects to WP4's capability cluster framework.
- Temporal dimension: competitiveness trajectories over time. Which regions are building capability, which losing it.
- Policy interface: constraint maps, sequencing timelines, finance architecture alongside the data.
- Platform produces the analytical layer. CICE displays it.

---

## Appendix B -- Level 4: Scheduled Agents [NOT PRESENTED, reference only]

Aspirational tier. Scheduled tasks that run without prompting.

- **Data freshness:** check whether OEC BACI has been updated. Flag stale caches.
- **Consistency audit:** verify all play cards use the same HS6 taxonomy version.
- **Deliverable QA:** scan HTML files for broken chart containers, missing data sections, design token violations.
- **Discoveries triage:** cluster new discoveries by topic. Propose promotions for quarterly review.

Not speculative in general. Scheduled Claude agents already run in production for other parts of this work. Weekly status reports, risk scans, compliance checks. Pattern transfers to the Lab's pipeline. Post-approval, Q3 2026.
