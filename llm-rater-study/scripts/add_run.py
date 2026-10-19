#!/usr/bin/env python3
"""Validate one model response (JSON) and append its ratings to ratings/ratings_all_runs.csv.

Usage:
  python3 add_run.py --model "LLM C (Claude Opus 5.5)" --run 1 --json ../raw_responses/llm_c_run1.json
The JSON must be the array the prompt asks for: 21 objects with id, D, R, E, A, D2, S (and rationale).
Checks: all 21 published ids present exactly once, D/R/E/A/D2 integers 1-10, S integer 1-5,
and that the (model, run) pair is not already in the CSV.
"""
import argparse, csv, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument('--model', required=True); ap.add_argument('--run', type=int, required=True)
ap.add_argument('--json', required=True); a = ap.parse_args()
text = open(a.json, encoding='utf-8').read().strip()
text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text)          # tolerate a code fence
data = json.loads(text)
ids = [r['id'] for r in csv.DictReader(open(os.path.join(HERE, '../input/published_ratings.csv')))]
got = [d['id'] for d in data]
err = []
if sorted(got) != sorted(ids): err.append(f'ids differ: missing {sorted(set(ids)-set(got))}, extra/dup {sorted(set(got)-set(ids)) or [g for g in got if got.count(g)>1]}')
for d in data:
    for k, hi in (('D', 10), ('R', 10), ('E', 10), ('A', 10), ('D2', 10), ('S', 5)):
        v = d.get(k)
        if not isinstance(v, int) or isinstance(v, bool) or not 1 <= v <= hi: err.append(f"{d.get('id')}.{k}={v!r} not an integer in 1-{hi}")
path = os.path.join(HERE, '../ratings/ratings_all_runs.csv')
rows = list(csv.reader(open(path)))
if any(r[1] == a.model and r[2] == str(a.run) for r in rows[1:]): err.append(f'{a.model} run {a.run} already in the CSV')
if err: sys.exit('NOT ADDED:\n  ' + '\n  '.join(err))
with open(path, 'a', newline='') as f:
    w = csv.writer(f)
    for i in ids:
        d = next(x for x in data if x['id'] == i); w.writerow([i, a.model, a.run] + [d[k] for k in ('D', 'R', 'E', 'A', 'D2', 'S')])
print(f'added {a.model} run {a.run}: 21 entries')
