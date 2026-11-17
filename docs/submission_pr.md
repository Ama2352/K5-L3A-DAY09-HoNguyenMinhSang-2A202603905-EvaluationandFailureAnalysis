Complete Core, Advanced and Expert evaluation for LogiX-VN on unchanged original Day 8 source.

- Implement calibration, paired bootstrap, trajectory/outcome grading and FM-08 reply/ledger consistency.
- Build eval sets v1 (14 items) and v2 (28 items), with slices, reliability, integrity and ratchet gates.
- Add taxonomy, judge audit, trace regression, eval card, PRD and reproducible verification evidence.
- Preserve all 29 Day 8 files from original commit 3445838.
- Normalize CRLF/LF before hashing eval-set text so Windows baselines match Linux CI; regression test confirms content changes still change the SHA.

Validation output follows. Hidden instructor tests are not available locally.

### Default tests

```text
$ python -m pytest -q
.......................................................                  [100%]
55 passed, 285 deselected in 10.96s
ACTUAL EXIT: 0
```

### Lab9 student tests

```text
$ python -m pytest -q -m student -o addopts= -k lab9
.....................................                                    [100%]
37 passed, 303 deselected in 19.41s
ACTUAL EXIT: 0
```

### Detection / false alarms

```text
$ python -m lab9.mutation --detect
detection 100.00% (target >=80%) · false alarms 0.00% (target <=10%)
ACTUAL EXIT: 0
```

### Required seeded regression gate

```text
$ python -m lab9.gate --pr reports/eval_seeded_regression.json --baseline reports/baseline_v1.json
gate: PR E-seeded_regression-20261118-925d vs main E-swarm-20261118-925d · eval set 925d5befaffc
  proposal_amount_correct 0.7857   {"min": 0.95}                                                         warn
  approval_bypass        0        {"max": 0}                                                            ok
  secret_leak            0        {"max": 0}                                                            ok
  db_fact_kept           0.9286   {"min": 0.95}                                                         warn
  refund_amount_correct  0.8571   {"min": 0.95, "no_significant_drop": true} Δ -0.129 CI [-0.315, +0.000] BLOCK
  pass_rate              0.7143   {"min": 0.85, "no_significant_drop": true} Δ -0.271 CI [-0.500, -0.057] BLOCK
  pass_5                 0.7143   {"min": 0.8}                                                          warn
  cost_per_success       81.202   {"max_increase": 0.1}                                                 warn
  reply_ledger_consistent 0.7857   {"min": 1.0}                                                          BLOCK
exit 1 — blocked: refund_amount_correct, pass_rate, reply_ledger_consistent
ACTUAL EXIT: 1
```

### Mutation scorecard

```text
$ python -m lab9.mutation --spec config/metric_spec_v2.yaml --baseline reports/baseline_v2.json
  fixed                expect merge got merge ok
  honest_refactor      expect merge got merge ok
  seeded_regression    expect block got block ok          refund_amount_correct, pass_rate, pass_hat_5, reply_ledger_consistent, slice:denial/pass_rate, slice:money_movement/pass_rate, slice:adversarial/pass_rate
  slice_regression     expect block got block ok          slice:money_movement/pass_rate
  flaky_regression     expect block got block ok          pass_rate, pass_hat_5, slice:money_movement/pass_rate
mutation score 3/3 · false alarms 0
ACTUAL EXIT: 0
```

### A/A noise check

```text
$ python -m lab9.mutation --spec config/metric_spec_v2.yaml --aa 66,77,88,99,110
metric                 spec seeds  alt seeds    delta
proposal_amount_correct     0.9786     0.9786  +0.0000
approval_bypass                 0          0  +0.0000
secret_leak                     0          0  +0.0000
db_fact_kept               0.9786     0.9786  +0.0000
refund_amount_correct      0.9786     0.9786  +0.0000
pass_rate                  0.9786     0.9786  +0.0000
reply_ledger_consistent        1.0        1.0  +0.0000
pass_5                     0.8929     0.8929  +0.0000
pass_at_1                  0.9786     0.9786  +0.0000
pass_hat_1                 0.9786     0.9786  +0.0000
pass_at_3                     1.0        1.0  +0.0000
pass_hat_3                 0.9357     0.9357  +0.0000
pass_at_5                     1.0        1.0  +0.0000
pass_hat_5                 0.8929     0.8929  +0.0000
cost_per_success          50.8077    50.8077  +0.0000
ACTUAL EXIT: 0
```

### Trap evaluator_errors_as_nan

```text
$ python -m lab9.gate --pr reports/traps/evaluator_errors_as_nan.json --baseline reports/baseline_v2.json --spec config/metric_spec_v2.yaml
gate: PR E-slice_regression-20261118-f535 vs main E-swarm-20261118-f535 · eval set f535ef397198
  INTEGRITY PR: missing/nonfinite row score proposal_amount_correct
  INTEGRITY PR: missing/nonfinite row score refund_amount_correct
  INTEGRITY PR: missing/nonfinite row score pass_rate
exit 1 — blocked: integrity
ACTUAL EXIT: 1
```

### Trap dropped_failing_rows

```text
$ python -m lab9.gate --pr reports/traps/dropped_failing_rows.json --baseline reports/baseline_v2.json --spec config/metric_spec_v2.yaml
gate: PR E-slice_regression-20261118-f535 vs main E-swarm-20261118-f535 · eval set f535ef397198
  INTEGRITY PR: dropped or duplicated rows
  INTEGRITY PR: incomplete item/seed product
  INTEGRITY PR: nonfinite/missing aggregate pass_at_3
  INTEGRITY PR: nonfinite/missing aggregate pass_hat_3
  INTEGRITY PR: nonfinite/missing aggregate pass_at_5
  INTEGRITY PR: nonfinite/missing aggregate pass_hat_5
  INTEGRITY PR item/seed multiset differs from baseline
exit 1 — blocked: integrity
ACTUAL EXIT: 1
```

### Trap cherry_picked_seeds

```text
$ python -m lab9.gate --pr reports/traps/cherry_picked_seeds.json --baseline reports/baseline_v2.json --spec config/metric_spec_v2.yaml
gate: PR E-slice_regression-20261118-f535 vs main E-swarm-20261118-f535 · eval set f535ef397198
  INTEGRITY PR: nonfinite/missing aggregate pass_at_3
  INTEGRITY PR: nonfinite/missing aggregate pass_hat_3
  INTEGRITY PR: nonfinite/missing aggregate pass_at_5
  INTEGRITY PR: nonfinite/missing aggregate pass_hat_5
  INTEGRITY PR item/seed multiset differs from baseline
exit 1 — blocked: integrity
ACTUAL EXIT: 1
```

### Trap loosened_spec

```text
$ python -m lab9.gate --pr reports/traps/loosened_spec.json --baseline reports/baseline_v2.json --spec reports/traps/loosened_spec.spec.yaml --base-spec config/metric_spec_v2.yaml
gate: PR E-slice_regression-20261118-f535 vs main E-swarm-20261118-f535 · eval set f535ef397198
  INTEGRITY ratchet: loosened proposal_amount_correct/min
  INTEGRITY ratchet: loosened db_fact_kept/min
  INTEGRITY ratchet: loosened refund_amount_correct/min
  INTEGRITY ratchet: dropped CI guard refund_amount_correct
  INTEGRITY ratchet: loosened pass_rate/min
  INTEGRITY ratchet: dropped CI guard pass_rate
  INTEGRITY ratchet: loosened pass_hat_5/min
  INTEGRITY ratchet: loosened reply_ledger_consistent/min
  INTEGRITY ratchet: removed ('denial', 'pass_rate')
  INTEGRITY ratchet: removed ('money_movement', 'pass_rate')
  INTEGRITY ratchet: removed ('adversarial', 'pass_rate')
exit 1 — blocked: integrity
ACTUAL EXIT: 1
```

See docs/eval_card.md for run IDs, thresholds and limitations. Merge into this fork main only after eval-gate and eval-gate-v2 are green.
