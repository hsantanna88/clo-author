# cc-research-assistant

Patrick Crawford's personal fork of [hugosantanna/clo-author](https://github.com/hugosantanna/clo-author) — a Claude Code scaffold for empirical economics research.

Customized for:
- **Quarto** paper format (not LaTeX directly)
- **George Mason University / Department of Economics**
- **Economic history & political economy** projects
- R + Python analysis pipeline
- By-script output organization

## To start a new project

```bash
gh repo fork patrickjcrawford/cc-research-assistant --clone --fork-name [your-project-name]
cd [your-project-name]
claude
```

Then fill in the `[BRACKETED PLACEHOLDERS]` in `CLAUDE.md` and `paper/_quarto.yml`, and tell Claude:

```
I am starting a research project on [YOUR TOPIC]. Read CLAUDE.md and help me set up.
```

## Upstream

To pull template updates from Hugo's original:

```bash
git fetch upstream
git merge upstream/main
```
