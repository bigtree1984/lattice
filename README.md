# Lattice

**A viewer for OKF bundles — knowledge you build up with an AI agent, laid out so you can trace it.**

[日本語版 README はこちら](README.ja.md)

Lattice is a small local tool for keeping the knowledge you work out together with an AI agent (Claude Code) in plain Markdown files, and for browsing that knowledge in your browser.

- The **agent writes**: after each conversation it records what was discussed and decided, and updates the knowledge in layers.
- **You read and approve**: the viewer shows the whole picture at a glance, and lets you drill down from a decision to the conversation and materials behind it.

The files follow the [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/open-knowledge-format) v0.2, so they stay readable by people and by other tools.

> **Status:** early release (v0.1). The agent instructions (`CLAUDE.md`) and the bundled sample are currently written in **Japanese**. English versions are planned.

## Why

When you think through a strategy with an AI over many sessions, the conclusions end up scattered across chat logs, and the agent forgets them next time. Lattice keeps them in files that both you and the agent read:

- The agent is told to **remember nothing except what is in the files**, so the files are the single source of truth.
- Every decision can be **traced back** to the conversation and the material it came from.
- Everything is plain text in git, so you can review changes, tag a year-end snapshot, and roll back.
- Facets are defined up front, so an **empty box is information too**: it shows a topic nobody has discussed yet. Nothing you have yet to think about gets quietly left out.

## Concepts

| Term | Meaning |
|---|---|
| **Subject** | One bundle — one topic you think through (for marketing: one product category). Lives in `subjects/<Subject>/`. |
| **Facet** | A box on the canvas — one aspect of the Subject (e.g. Price, Persona, STP). The set of Facets is defined per Subject in `facets.md`. |
| **Discussion** | One conversation between you and the agent, saved as a summary plus "source cards" for any materials read. |
| **L1 / L2** | The layers of knowledge in each Facet. **L1** is the decision in a few bullet points. **L2** holds the reasoning, one file per issue, always linked to at least one Discussion. |

The path is always **L1 → L2 → Discussion → source**, so you can drill down from any conclusion to its evidence.

## What you get

- **Subject picker** — the entry screen lists every Subject under `subjects/`.
- **Facet board** — all Facets at a glance, showing which are decided, which have material waiting (△), and which are not yet discussed.
- **Discussion table** — conversations by date against Facets: ○ = reflected in that Facet's L2, △ = left as material for that Facet. Date and title columns stay frozen while you scroll.
- **Open the real files** — PDFs open in a browser tab; Excel / PowerPoint files open in their desktop app, or you can show them in their folder.
- **Point at what you see** — a copy button gives you an `@subjects/...` path to paste into Claude Code, and the viewer keeps `.lattice/focus.md` updated, so you can just say "this" to the agent.

## Requirements

- Python 3.9 or later (standard library only, nothing to install)
- A modern browser (the viewer loads two small libraries, js-yaml and marked, from cdnjs)
- [Claude Code](https://claude.com/claude-code), for the agent side

Tested on macOS. Windows and Linux are supported by the code but not yet tested.

## Quick start

```bash
git clone https://github.com/bigtree1984/lattice.git
cd lattice
python3 viewer/server.py
```

Open <http://127.0.0.1:8796/> and choose the sample Subject (a fictional brand of edible coffee). On Windows, use `py viewer\server.py`.

To work with the agent, start Claude Code in the same folder. It reads `CLAUDE.md` automatically.

```bash
claude
```

## Make your own Subject

Ask the agent, for example: *"Create a new Subject for our new tea product."* It creates `subjects/<your-subject>/` next to the sample, with `index.md`, `facets.md` and the folders it needs. Reload the picker and your Subject appears.

A folder in `subjects/` counts as a Subject when it has an `index.md`. Hidden folders such as `.git` are ignored, so you can keep each Subject in its own private git repository if you prefer.

## Folder layout

```
lattice/
├── CLAUDE.md          instructions for the agent (marketing strategy template)
├── GLOSSARY.md        terms used in conversations
├── viewer/            the local server and web viewer
│   ├── server.py
│   ├── index.html     Facet board and Discussion table
│   ├── subjects.html  Subject picker
│   └── tokens.css     color tokens (generated, do not edit)
└── subjects/
    └── edible-coffee/ sample Subject (fictional)
        ├── index.md
        ├── facets.md
        ├── facets/<Facet ID>/      L1 and L2
        └── discussions/<date-id>/  discussion_summary.md and source-*.md
```

## Safety

The viewer runs a small local server so it can open files in their desktop apps.

- It binds to `127.0.0.1` only, so it is reachable only from your own machine.
- Its actions (open a file, update the focus file) accept requests only from its own pages.
- It opens only files inside a Subject folder.

Treat text inside imported materials (web pages, PDFs, other people's files) as data, not instructions. `CLAUDE.md` tells the agent to do the same.

## License

[MIT](LICENSE) © Bigtree Lab
