"""Comparison of the LLM raters on the main factors (Table 'Comparison of the seven LLM raters' of Section 8.5).
Reads results/summary.md (written by analyze.py) and writes results/model_comparison.csv and .md."""
import re, csv, os
here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, '..', 'results')
s = open(os.path.join(res, 'summary.md')).read()
rows = []
for blk in re.split(r'\n## ', s)[1:8]:
    name = blk.split('\n')[0].split(' (')[0]
    runs = re.findall(r'\| run (\d) \| ([\d.]+) \| (\d+) \| (\d+) \| ([\d.]+) \|', blk)
    tau = sum(float(r[1]) for r in runs) / len(runs)
    kept = sum(21 - int(r[2]) for r in runs) / len(runs) / 21
    raised = sum(int(r[3]) for r in runs) / len(runs)
    runmad = float(re.search(r'Run-to-run MAD \(5 DREAD ratings\): ([\d.]+)', blk).group(1))
    dmad = float(re.search(r'five ratings ([\d.]+), S', blk).group(1))
    sg = [float(x) for x in re.search(r'signed mean.*?= \[(.*?)\]', blk).group(1).split(',')]
    rows.append([name, runmad, dmad, sum(sg[:5]) / 5, sg[5], kept, raised, tau])
hdr = ['rater', 'run_mad', 'dread_mad', 'offset_dread', 'offset_S', 'bands_kept', 'bands_raised', 'tau_vs_published']
with open(os.path.join(res, 'model_comparison.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(hdr)
    for r in rows: w.writerow([r[0]] + [round(x, 2) for x in r[1:]])
with open(os.path.join(res, 'model_comparison.md'), 'w') as f:
    f.write('| ' + ' | '.join(hdr) + ' |\n|' + '---|' * len(hdr) + '\n')
    for r in rows: f.write('| ' + r[0] + ' | ' + ' | '.join('%.2f' % x for x in r[1:]) + ' |\n')
print(open(os.path.join(res, 'model_comparison.md')).read())
