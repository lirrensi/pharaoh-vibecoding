# Pharaoh Coding System for OpenCode

**Vibe coding on steroids** — one single interface for everything, CEO-level workflow, no command-line chaos. 🪙✨

---

## The Core Philosophy

You have one **sole entry point** for your entire project: **Horus**.

Everything you want to do, know, or change happens through Horus. No more writing long PRDs, no more context switching between terminals and docs. Just talk → Horus listens → Horus executes → Done. 💅

The entire system revolves around a sacred canon:
- `docs/product.md` — the **spec** (human-readable, high-level, authoritative)
- `docs/arch.md` — the **tech reference** (machine-readable, implementation details)

Everything in the codebase is **derived** from these docs. Code is never the source of truth — the docs are.

---

## The Workflow: Step-by-Step 🔄

### Step 1: Initialize Documentation (Thoth)
**When to use:** First run, or when you have no docs yet.

```
Thoth: "Generate product.md and arch.md from current codebase"
```

Thoth creates the sacred canon (product.md + arch.md) if they don't exist.

---

### Step 2: Send Ideas to Horus
**When to use:** You have a change you want to make or a question you want answered.

```
You: "I want to add X feature" or "How does Y work?"
```

Horus investigates your request and provides context.

---

### Step 3: Horus Interrogates You (Optional)
**When to use:** Horus needs clarification to make the spec crystal clear.

Horus will ask questions like:
> "What exactly should happen when X occurs?"
> "Should this be available to all users or only admins?"
> "What are the edge cases?"

**Your response:**
```
You: "It should do this and this, and handle this edge case."
```

---

### Step 4: Horus Updates Docs & Creates Plan
**When to use:** Requirements are clarified, ready to formalize.

Horus:
1. Updates `product.md` and `arch.md` as the new canon
2. Generates a detailed plan for Ptah to execute

This step may be combined with Step 3 if the clarification is simple.

---

### Step 5: Ptah Executes the Plan
**When to use:** You've approved the plan, ready to execute.

```
Ptah: "Got it. Executing plan..."
*(Ptah works on the plan)*
*(Ptah returns when done)*
```

**No questions asked. Just execution.**

---

### Step 6: Maat Reviews the Work
**When to use:** Ptah is done, time to check for quality.

```
Maat: "Checking implementation..."
```

Maat reviews against the canon and checks for:
- Correctness
- Edge cases
- Broken assumptions
- Weird behavior

---

### Step 7: If Maat Finds Issues → Loop Back to Ptah
**When to use:** Maat identifies problems or incomplete work.

```
Maat: "I found an issue: X is not implemented correctly. Here's what's wrong."

You: Send corrections to Ptah
Ptah: "Got it. Fixing X..."
```

Repeat Step 5-7 until Maat is satisfied.

---

### Step 8: Read Maat's Report
**When to use:** Maat is done reviewing.

```
Maat: "✅ All checks passed. Implementation is correct and complete."
```

Read Maat's report to confirm the plan is really done.

---

### Step 9: Generate New Ideas (Set or Hathor)
**When to use:** Your todo list is empty and you're bored.

```
Set: "Scan the codebase and find everything that smells."
Hathor: "Give me 10 wild ideas for new features to add."
```

Use Set for code criticism, Hathor for wild ideas.

---

### Step 10: Sync or Refine Documentation (Thoth)
**When to use:** You've manually changed code and want docs to sync, or you want to refine/split documentation.

```
Thoth: "Regenerate docs based on current codebase."
Thoth: "Split product.md into smaller, more readable sections."
Thoth: "Sync arch.md with the recent code changes."
```

**Core goal:** Keep documentation clear, up-to-date, and well-structured.

---

## The Complete Loop

```
Start → Thoth (if needed) → Horus (investigate + clarify) → Ptah (execute) → Maat (check)
                                                                 ↓
                                                         Found issues?
                                                         Yes → Ptah fixes → Maat checks again
                                                         No → Done!
```

---

## Why You'll Love This 💕

### 🙅 No More Long PRDs & Document Juggling
- **Horus generates docs for you first** — no more staring at a blank page for hours
- **Iterate with Horus** — make changes, he updates the canon, you keep moving
- **No juggling 100-line documents** before you start coding. Just tell him what you want, he investigates, you work together.
- **Specs evolve with you**, not the other way around.

### 😌 Longer Breaks, Less Babysitting
- **Once you have a plan**, tell Ptah to execute and walk away
- **Return 10 minutes later**, tell Maat to check the work
- **Return 10 minutes later** to confirm everything is done
- **No babysitting agents** — they work while you focus on other things

### 👑 CEO-Level Workflow
This is how a real CEO works:
- **You** = The CEO with the vision
- **Horus** = Your Chief Technical Officer (CTO) who translates vision into specs
- **Ptah** = The implementation team (you delegate to them)
- **Maat** = Quality assurance (they check everything before you sign off)

You don't write code. You **set the vision**. Horus handles the details. You're free to focus on what matters: decisions, strategy, and results.

---

## How It Differs From Other Systems 🆚

### OpenAgentsControl (Darren Hinde)
**Similar vibes**, but with a key difference:

| Feature | OpenAgentsControl | Pharaoh |
|---------|-------------------|---------|
| Workflow | Step-by-step confirmation | **No step-by-step confirmation** |
| Your Role | Confirm each step | **Sit and think, delegate, then return** |
| Execution | Paused for your approval at each stage | **Ptah executes fully, you return later** |
| Workflow | "Plan step 1 → confirm → Plan step 2 → confirm" | "Plan everything → Execute everything → Check everything" |

**Pharaoh Advantage:** You don't get interrupted. Horus does all the thinking, Ptah does all the work, you only return to review.

---

### OhMyOpenCode (Code Yeongyu)
**Overcomplicated mess** with too many moving parts:

| Feature | OhMyOpenCode | Pharaoh |
|---------|--------------|---------|
| Complexity | **Too much stuff**, unclear how it works | **Clear, simple workflow** |
| Structure | Over-engineered, hard to follow | **Straightforward: Horus → Ptah → Maat** |
| Model Hardcoding | **Hardcodes specific models** | **Flexible, works with small models** |
| Customization | Limited, rigid | **Full control over your workflow** |
| Philosophy | Too many agents, unclear purpose | **Focused on CEO-level delegation** |

**Pharaoh Advantage:** You have complete control. No hardcoded models, no unnecessary complexity. Just the workflow you need.

---

### Why Pharaoh Wins 🏆

1. **No Step-by-Step Confirmation** — You don't confirm each step. Horus thinks, Ptah executes, you return later to check.
2. **Simple & Clear** — No over-engineering, no unclear workflows. Just three agents: Horus (plan), Ptah (execute), Maat (check).
3. **Flexible & Model-Agnostic** — Works with small models, no hardcoded model requirements.
4. **CEO-Level Workflow** — You delegate, you don't babysit. This is how real CEOs work.

---

## Installation 🛠️

### Step 1: Get the Repo
```bash
# Clone it
git clone <your-repo-url>
cd PharaohSystemRepo

# OR download the zip
# https://github.com/<your-username>/PharaohSystemRepo
```

### Step 2: Copy Agents to OpenCode
```bash
# Copy the agents folder to your OpenCode config
cp -r agents ~/.config/opencode/agents/
```

### Step 3: Install PromptPaste (Optional but Recommended)
This is a mini tool to get small prompt snippets easily.

```bash
# Install with UV (Python tool manager)
uv tool install promptpaste

# Use it
pp add lead
```

**OR** if you don't like PromptPaste, just tell Ra to modify Horus's prompt:
```
Ra, change Horus's prompt to use cat + path to the agent files instead of PromptPaste.
```

### Step 4: Verify Installation
In OpenCode, use Tab to switch between them

---

## The Core Idea: Prompts, Not Tools 💭

**This is the most important principle:**

The entire Pharaoh system is **just fancy prompts**. That's it.

- **Horus** = One sophisticated prompt
- **Ptah** = One sophisticated prompt
- **Maat** = One sophisticated prompt
- **Set, Hathor, Thoth, Ra** = One sophisticated prompt each

**You can copy these prompts and use them in ANY coding agent:**
- Claude
- GPT-4
- OpenAI Agents
- Cursor
- Continue
- Codeium
- Or any other agent that accepts custom prompts

**How to use the agents anywhere:**
1. Copy the text of the prompt from the `agents/` folder
2. Paste it into your AI agent's custom prompt field
3. Done! You have Horus, Ptah, Maat, etc. in any environment

**Why this matters:**
- The **principle** is what's valuable: structured workflow, CEO-level delegation, no babysitting
- The **implementation** (prompts) can be copied anywhere
- You're not locked into a specific tool
- You can adapt the workflow to whatever agent you're using
- It's about **organization**, not software

**The beauty of this approach:**
- Small models work fine (you're just prompting, not running complex logic)
- No framework dependencies
- No installation headaches
- Just copy → paste → use
- Works in any environment, any language, any model size

---

## The Workflow Loop (Detailed)

```
You → Horus → Ptah → Maat → (loop until done) → ✨
```

### 1. Horus: Your Architect & Manager 🦅
**Horus is your ONLY interaction point.** Literally. Everything flows through him/her.

**What Horus does:**
- Listens to your ideas, questions, or requests
- Interviews you to clarify requirements (asks the "why" and "how")
- Investigates the current codebase and docs
- Updates `product.md` and `arch.md` as the **absolute canon**
- Generates a detailed, idiot-proof plan for Ptah to execute

**Example interview questions Horus might ask:**
> "You want dark mode? Is this for admin users only? Should it persist across sessions? What about existing themes?"
> "How should the API behave when dark mode is toggled? Should it return a 200 with the new theme, or a 201 with the new setting?"

### 2. Ptah: YOLO Execution Mode 🔨
Once Horus gives you a plan, Ptah becomes a **paperclip maximizer**.

**Ptah's role:**
- Receives the plan from Horus
- Executes it with extreme focus (literally doesn't stop until done)
- Can stop if something is obviously wrong (env issues, wrong target, etc.)
- Reports back when complete or when errors occur

**No questions asked. No hesitation. Just execution.**

### 3. Maat: Paranoid Review Mode⚖️
After Ptah finishes, Maat enters the loop to **check** everything.

**Maat's role:**
- Reviews the plan against the canon (`product.md` + `arch.md`)
- Checks that everything was implemented correctly
- Looks for edge cases, broken assumptions, or weird behavior
- Reports back to you (or Horus) with findings

If Maat finds issues, the loop restarts:
```
Horus → fixes/refines → Ptah → Maat → ...
```
On a good day, this completes in 1 iteration. On a bad day, 2-3. 🙏

---

## The Optional Agents (Manual Invocations)

These agents are **not part of the main loop** — you call them manually when you need them:

### Ra: Environment Manager ☀️
**When to use:** You want to change OpenCode itself, manage configs, or modify prompt behaviors.

**What Ra does:**
- Knows where all documentation and config files live
- Manages OpenCode environment and settings
- Can modify prompts, plugins, or system behavior
- Answers questions about the OpenCode setup

**Example use cases:**
> "Ra, make my Horus persona more angry and sarcastic"
> "Ra, where are my config files located?"
> "Ra, create a new plugin for me"
> "Ra, change how Thoth generates documentation"

---

### Set: Code Critic 👿
**When to use:** You want to find smells, technical debt, or bad patterns in the codebase.

**What Set does:**
- Scans the entire codebase
- Identifies anti-patterns, code smells, and areas that need refactoring
- Returns a TODO list of improvements

**Example use case:**
> "Set, run a code audit and find everything that smells."

### Hathor: Product Improver 💃
**When to use:** You want wild, fancy, new features — or you're brainstorming the next big thing.

**What Hathor does:**
- Focuses on NEW and FANCY features to add, support, or extend
- Generates wild TODO lists of exciting possibilities
- Encourages you to think outside the box

**Example use case:**
> "Hathor, give me 10 wild ideas for this project that we could add."

### Thoth: Documentation Manager 📜
**When to use:** First run, or when you've manually changed code and want the docs to sync back.

**What Thoth does:**
- Creates `product.md` and `arch.md` from scratch (on first run)
- Syncs docs with code changes you make manually
- Ensures the canon is up-to-date

**Example use case:**
> "Thoth, regenerate the docs based on the current codebase."

---

## The Agent Roster 📋

| Agent | Role | Main Loop | When to Call |
|-------|------|-----------|--------------|
| **Horus** 🦅 | Architect & Manager | ✅ Yes | Your ONLY interaction point for all changes |
| **Ptah** 🔨 | Execution Mode | ✅ Yes | Receives plans and executes them (YOLO) |
| **Maat** ⚖️ | Review Mode | ✅ Yes | Reviews implementations for correctness |
| **Ra** ☀️ | Environment Manager | ❌ No | Changes OpenCode itself, manages configs |
| **Set** 👿 | Code Critic | ❌ No | Finds smells, anti-patterns, technical debt |
| **Hathor** 💃 | Product Improver | ❌ No | Brainstorms wild, fancy new features |
| **Thoth** 📜 | Documentation Manager | ❌ No | Generates initial docs, syncs manual changes |

**Main Loop Agents (Horus → Ptah → Maat):** This is your core workflow. Everything else is optional or manual.

---

## A Concrete Example: Adding Dark Mode

Here's how the full workflow looks in action:

**You:**
> "I want to add dark mode to the application."

**Horus:**
> "Got it! Let me investigate. (Scans code, reviews existing docs) Okay, I have a few questions to clarify:
>
> 1. Is dark mode for all users or just admin users?
> 2. Should it persist across sessions (localStorage, cookies)?
> 3. What about existing themes — should dark mode replace them or coexist?
> 4. Should the API return the current theme state, or just update it?
> 5. What about mobile — do we need specific dark mode rules there?"

**You (responding):**
> "Admin users only. Yes, persist in localStorage. Coexist with light mode. API should return current state. No special mobile handling needed."

**Horus:**
> "Perfect! Now I'm updating the canon..."

**(Horus updates `product.md` and `arch.md`)**
> "✅ Updated `product.md` with dark mode specs:
> - Feature: Admin-only dark mode
> - Storage: localStorage
> - API endpoint: `GET /api/theme` returns `{ theme: 'dark' | 'light' }`
> - Frontend: Toggle button in admin settings, theme class applied to body

> ✅ Updated `arch.md` with implementation notes:
> - Use CSS variables for theming
> - Add `localStorage.getItem('theme')` on init
> - API route: `/api/theme` with GET handler

> ✅ Generated plan for Ptah:"
> ```markdown
> 1. Create `/api/theme` GET endpoint
> 2. Create frontend theme toggle component
> 3. Apply theme class to body element based on localStorage
> 4. Add admin-only middleware to theme toggle
> 5. Update existing pages to use CSS variables
> ```

**Ptah:**
> "Got it. Executing plan..."
> *(10 minutes later)*
> "Done! API endpoint created, toggle added, localStorage implemented."

**Maat:**
> "Checking implementation..."
> ✅ API returns correct theme state
> ✅ Toggle works for admin users only
> ✅ Theme persists across refresh
> ✅ CSS variables applied correctly

**You:**
> "Perfect! Let's deploy."

**🎉 Done!**


---

## How It Works

### The Golden Rule
**Code ≠ Source of Truth**
The docs (`product.md` + `arch.md`) are the source of truth. Everything else is derived from them. If it's not in the docs, it doesn't exist.

### The Workflow in Detail
1. **You** describe what you want (high-level, vague, whatever).
2. **Horus** investigates, interviews you, clarifies requirements.
3. **Horus** updates `product.md` and `arch.md` as the new canon.
4. **Horus** generates a detailed plan for Ptah.
5. **Ptah** executes the plan (YOLO mode, no questions).
6. **Maat** reviews the implementation against the canon.
7. If Maat finds issues → loop back to step 2.
8. If Maat approves → you're done! 🎉

### Why This Matters
- **No context switching:** Everything happens in OpenCode, no terminals.
- **One source of truth:** `product.md` and `arch.md` are always in sync.
- **Human-centric specs:** `product.md` is written for humans, not machines.
- **Execution-focused:** Horus plans, Ptah executes, Maat checks.
- **CEO workflow:** You set the vision, Horus handles the details. (It's vibe coding, not wipe coding!)

---

## Quick Start

1. **First run:**
   ```bash
   # Call Thoth to generate initial docs
   Thoth: "Generate product.md and arch.md from current codebase"
   ```

2. **Making changes:**
   ```bash
   # Talk to Horus about what you want
   You: "I want to add X feature"
   Horus: (investigates, interviews, updates canon, generates plan)
   Ptah: (executes plan)
   Maat: (reviews)
   ```

3. **Code criticism:**
   ```bash
   # Call Set when you want a code audit
   Set: "Scan the codebase and find all smells"
   ```

4. **Brainstorming:**
   ```bash
   # Call Hathor for wild ideas
   Hathor: "Give me 10 crazy ideas for new features"
   ```

5. **Environment management:**
   ```bash
   # Call Ra for OpenCode management
   Ra: "Make my plugin more cute"
   Ra: "Change how Thoth writes docs"
   Ra: "What are all my config files?"
   ```

---

## Tips & Tricks

✨ **Talk to Horus like a human:** You don't need to know technical details. Horus will extract them for you.

✨ **Iterate on ideas:** Horus will interview you until the spec is crystal clear. That's the point!

✨ **Let Ptah do the work:** Once you approve the plan, Ptah will execute it without questions. Trust the process.

✨ **Maat is your safety net:** If something feels wrong, Maat will catch it. Don't skip the review loop.

✨ **Optional agents are your toys:** Use Set, Hathor, Thoth, and Ra manually when you need them. They're not part of the main loop.

✨ **Ra is your environment conductor:** Ask Ra to tweak OpenCode itself, change prompts, manage configs, or create plugins. He's the only one who knows how everything is wired together!

---

## Want to make it better? (Future Improvements)

- Change Horus to spawn subagents instead
- Ask Horus to split big plan into several small plans
- Somehow manage Ptah and Maat talk to each other without copypaste

---

**Remember:** Horus is your interface. Ptah is your engine. Maat is your safety net. Together, they're the ultimate CEO workflow for vibe coding. 🪙✨
