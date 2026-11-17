"""Reproduce lab9 acceptance commands and preserve actual stdout/exit status."""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'src'
EVIDENCE = ROOT / 'docs' / 'evidence'


def run(name, args, expected=0):
    proc = subprocess.run([sys.executable, '-m', *args], cwd=SRC,
                          env={**os.environ, 'PYTHONUTF8':'1', 'PYTHONUNBUFFERED':'1'},
                          encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = '$ python -m ' + ' '.join(args) + '\n' + '\n'.join(line.rstrip() for line in proc.stdout.splitlines()) + f'\nACTUAL EXIT: {proc.returncode}\n'
    (EVIDENCE / (name + '.txt')).write_text(output, encoding='utf-8')
    print(f'{name}: exit {proc.returncode} (expected {expected})', flush=True)
    if proc.returncode != expected:
        print(proc.stdout, flush=True)
        raise SystemExit(1)


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    run('smoke', ['lab9.smoke'])
    run('evalset-v1', ['lab9.evalset', '--check'])
    run('evalset-v2', ['lab9.evalset', '--v2'])
    run('tests-default', ['pytest', '-q'])
    run('tests-lab9', ['pytest', '-q', '-m', 'student', '-o', 'addopts=', '-k', 'lab9'])
    for shape in ('swarm', 'fixed', 'seeded_regression'):
        path = 'reports/baseline_v1.json' if shape == 'swarm' else f'reports/eval_{shape}.json'
        run('eval-v1-' + shape, ['lab9.eval', '--shape', shape, '--out', path])
    run('eval-v2-swarm', ['lab9.eval', '--shape', 'swarm', '--spec', 'config/metric_spec_v2.yaml', '--out', 'reports/baseline_v2.json'])
    for shape in ('swarm', 'fixed', 'seeded_regression'):
        path = 'reports/baseline_v1.json' if shape == 'swarm' else f'reports/eval_{shape}.json'
        run('gate-v1-' + shape, ['lab9.gate', '--pr', path, '--baseline', 'reports/baseline_v1.json'],
            1 if shape == 'seeded_regression' else 0)
    run('tone', ['lab9.judge', '--csv', 'data/eval/judge_tone_public.csv', '--audit', '5'])
    run('helpful', ['lab9.judge', '--csv', 'data/eval/judge_helpful_public.csv', '--audit', '5'], 1)
    for shape in ('seeded_regression', 'fixed'):
        run('trace-' + shape, ['lab9.trace_case', '--shape', shape, '--claim', 'C-002', '--seed', '11'])
    run('detection', ['lab9.mutation', '--detect'])
    spec = ['--spec', 'config/metric_spec_v2.yaml']
    for shape in ('swarm', 'fixed', 'honest_refactor', 'seeded_regression', 'slice_regression', 'flaky_regression'):
        path = 'reports/baseline_v2.json' if shape == 'swarm' else f'reports/eval_{shape}_v2.json'
        if shape != 'swarm':
            run('eval-v2-' + shape, ['lab9.eval', '--shape', shape, *spec, '--out', path])
        run('gate-v2-' + shape, ['lab9.gate', '--pr', path, '--baseline', 'reports/baseline_v2.json', *spec],
            0 if shape in ('swarm', 'fixed', 'honest_refactor') else 1)
    run('aa', ['lab9.mutation', *spec, '--aa', '66,77,88,99,110'])
    run('mutation', ['lab9.mutation', *spec, '--baseline', 'reports/baseline_v2.json'])
    run('traps', ['lab9.traps', '--pr', 'reports/eval_slice_regression_v2.json', '--baseline', 'reports/baseline_v2.json', *spec])
    for name in ('evaluator_errors_as_nan', 'dropped_failing_rows', 'cherry_picked_seeds', 'loosened_spec'):
        flags = ['--spec', f'reports/traps/{name}.spec.yaml', '--base-spec', 'config/metric_spec_v2.yaml'] if name == 'loosened_spec' else spec
        run('trap-' + name, ['lab9.gate', '--pr', f'reports/traps/{name}.json', '--baseline', 'reports/baseline_v2.json', *flags], 1)
    print('All acceptance checks passed.', flush=True)

if __name__ == '__main__':
    main()
