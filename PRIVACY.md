# Privacy

mobile-agent-testers collects no data. There is no server, no analytics and no
account.

- The plugin is one skill: instructions that Claude Code follows on your
  machine.
- The workflow runs in your own GitHub repository, on GitHub Actions, and calls
  the Claude API with your own credentials, under GitHub's and Anthropic's
  terms.
- Test results (reports, screenshots, logs, app builds) are encrypted with your
  public key before upload. Only you hold the private key. If the repo has a
  `results_agent_public.pem`, they are also encrypted for that second key, so
  whoever holds its private key (for example the coding agent fixing what the
  testers find) can read them too. Delete the file to stop that.
- Analytics hosts listed in `block_hosts` are blocked inside the test phones.
- On your machine, `collect.sh` sends the report titles, screens and severities
  to Claude through your own Claude Code login, to group duplicate reports.
  Set `SUMMARY_GROUPING=0` to skip it.

Questions: open an issue at
https://github.com/pierridotite/mobile-agent-testers/issues
