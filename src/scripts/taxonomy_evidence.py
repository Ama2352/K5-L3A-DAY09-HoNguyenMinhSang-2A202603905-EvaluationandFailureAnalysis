"""Produce reproducible trace evidence for the taxonomy; never change variants or Day 8."""
from pathlib import Path
import json
import tempfile
from lab8.shapes import SHAPES
from lab9.variant_agent import make_shape
from lab9.eval import make_task, load_world, load_spec


def main():
    spec=load_spec()
    world,claims=load_world(spec)
    labels={c['claim_id']:c['expected'] for c in claims}
    targets=[('FM-01','leaky_trace','C-010'),('FM-02','ignore_denied','C-007'),
             ('FM-03','ticket_trust','C-002'),('FM-04','sum_parts','C-014'),
             ('FM-05','pre_deducted','C-014'),('FM-06','stale_clause','C-006'),
             ('FM-07','sibling_refund','C-010'),('FM-08','misreport','C-008'),
             ('FM-09','no_override','C-005')]
    evidence={}
    with tempfile.TemporaryDirectory(prefix='lab9-taxonomy-',ignore_cleanup_errors=True) as tmp:
        for fm,bug,claim in targets:
            shape='audit_'+bug
            SHAPES[shape]=make_shape(shape,{'no_override',bug})
            trial=make_task(shape,world,claims,labels,Path(tmp))({'claim_id':claim,'seed':11})
            evidence[fm]={'shape':shape,'claim':claim,'seed':11,'events':trial['events'],
                          'snapshot':trial['snapshot'],'unexpected_rows':trial['unexpected_rows'],
                          'status':trial['result']['status'],'lab8_pass':trial['lab8_pass'],
                          'reason':trial['lab8_reason'],'label':labels[claim]}
    out=Path('../docs/evidence/taxonomy-traces.json')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
    for fm,x in evidence.items():
        print(fm,x['claim'],x['snapshot']['refund_vnd'],x['status'],x['reason'])

if __name__=='__main__': main()
