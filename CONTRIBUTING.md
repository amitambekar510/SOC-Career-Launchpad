# Contributing

Thanks for helping beginners find their way into security! 💙

## Ways to help
- **Fix errors or unclear explanations.** Open an Issue or a Pull Request.
- **Add real-world analogies.** Simple beats clever.
- **Add free lab or resource links** that you have personally used.
- **Translate** pages into other languages.

## Writing style
- Write like you're explaining to a smart friend who's new to this.
- Define every acronym the first time it appears.
- Short sentences. Short paragraphs. Examples over theory.
- Keep it vendor-neutral where possible. Tool names are fine as examples.

## Please do NOT submit
- Anything confidential from an employer or client (real IPs, hostnames, ticket data, internal procedures)
- Copyrighted books, course material or paid content copied in full. Summaries in your own words are fine.
- Working malware, exploit code, or step-by-step attack instructions against real targets

## How to submit
1. Fork the repo, create a branch, make your change.
2. Open a Pull Request describing what and why.
3. Be kind in reviews. Everyone here is learning.

## Adding or changing quiz questions
1. Edit `ai/_ai-only/questions.source.json`. This is the only file with answers and rationales.
2. Run `python scripts/build_question_bank.py`.
3. Run `python scripts/validate_repo.py`. Every gated section needs at least 3 multiple-choice questions and 1 scenario.
4. Never put answers in learner-facing pages or in `ai/question-bank.json`.

## Updating regulations
Verify against the official sources in `docs/11-regulations-and-standards/sources.md`, update the "Last verified" date, then run `python scripts/make_visuals.py` to refresh the charts.
