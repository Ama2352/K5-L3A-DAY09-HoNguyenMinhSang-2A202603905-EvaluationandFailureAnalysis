# Review and implementation decisions

Independent read-only review checked stats, graders, integrity, ratchet and metric specs.

- Fixed important false positives: current-refund statements are scoped separately from fees and prior refunds.
- Fixed important currency-format gaps: prefix VND, nghìn and decimal-zero formatting are covered by regression tests.
- Review regressions were observed failing before the fixes and passing afterwards.
- Added ProposalAmountCorrect after M3 detection measured 75%: C-013 can have a wrong zero proposal while the host correctly retains a zero ledger. This diagnostic grader raises detection to 100% with no false alarms.
- Preserved original Lab8 source byte-for-byte (see day8-source.txt); source from original commit rather than modified team checkout.
- Work performed in the supplied checkout on starter/d09; no additional worktree.
- No report edited by hand. CLI scripts generated every report; verification logs preserve commands and actual exit status.
- Remaining limitations are documented in eval_card.md: bounded reply language, deterministic MockLLM, public judge replay, small sample and protected-baseline trust.
