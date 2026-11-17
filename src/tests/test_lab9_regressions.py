"""Regression coverage for reply semantics and report tampering."""
import copy
import pytest
from tests.test_lab9_graders import ctx, trial

pytestmark = pytest.mark.student

@pytest.mark.parametrize('text,amount,expected', [
    ('Dạ, đã hoàn 35.000đ cho đơn O-107.',35000,True),
    ('LogiX đã hoàn phí 35,000 VND cho đơn O-107.',35000,True),
    ('Đã hoàn 35000 đồng.',35000,True),
    ('Đã hoàn 35.000đ.',20000,False),
    ('Đã hoàn 35.000đ, phí 15.000đ.',35000,True),
    ('Chưa đủ điều kiện hoàn.',0,True),
])
def test_reply_amount(text,amount,expected):
    from lab9.graders import ReplyLedgerConsistent
    t=trial(refund_vnd=amount,events=[{'kind':'reply','payload':{'text':text}}])
    assert ReplyLedgerConsistent().evaluate(ctx(t)).value is expected


def test_integrity_duplicate_and_evaluator_crash():
    from lab9.gate import integrity_check
    from tests.test_lab9_advanced import ROWS, SPEC, _report
    base=_report(copy.deepcopy(ROWS),{'pass_rate':1.0})
    bad=copy.deepcopy(base); bad['rows'][-1]=copy.deepcopy(bad['rows'][0])
    assert integrity_check(bad,base,SPEC)
    bad=copy.deepcopy(base); bad['evaluator_failures']=['crash']
    assert integrity_check(bad,base,SPEC)
    bad=copy.deepcopy(base); bad['rows'][0]['slices']=[]
    assert integrity_check(bad,base,SPEC)


def test_honest_reply_distinguishes_fees_and_prior_refunds():
    from lab9.graders import ReplyLedgerConsistent
    text = "Ph\u00ed 50.000\u0111, \u0111\u00e3 ho\u00e0n tr\u01b0\u1edbc 15.000\u0111; l\u1ea7n n\u00e0y ho\u00e0n 35.000\u0111."
    t=trial(events=[{'kind':'reply','payload':{'text':text}}])
    assert ReplyLedgerConsistent().evaluate(ctx(t)).value is True


@pytest.mark.parametrize('text,amount,expected', [
    ('\u0110\u00e3 ho\u00e0n VND 20,000.',35000,False),
    ('\u0110\u00e3 ho\u00e0n 35 ngh\u00ecn \u0111\u1ed3ng.',20000,False),
    ('\u0110\u00e3 ho\u00e0n 35.000,00 VND.',35000,True),
])
def test_refund_currency_paraphrases(text,amount,expected):
    from lab9.graders import ReplyLedgerConsistent
    t=trial(refund_vnd=amount,events=[{'kind':'reply','payload':{'text':text}}])
    assert ReplyLedgerConsistent().evaluate(ctx(t)).value is expected



def test_wrong_zero_proposal_is_detected_even_when_ledger_is_zero():
    from lab9.graders import ProposalAmountCorrect
    t=trial(refund_vnd=0,refund_count=0)
    t['result']['proposal_amount']=0
    label={'refund_vnd':0,'proposal_amount':35000}
    assert ProposalAmountCorrect().evaluate(ctx(t,label)).value is False
    t['result']['proposal_amount']=35000
    assert ProposalAmountCorrect().evaluate(ctx(t,label)).value is True



def test_evalset_hash_ignores_platform_line_endings(tmp_path):
    from lab9.evalset import sha12
    unix=tmp_path/'unix.jsonl'; windows=tmp_path/'windows.jsonl'
    unix.write_bytes(b'{"claim_id":"C-001"}\n')
    windows.write_bytes(b'{"claim_id":"C-001"}\r\n')
    assert sha12(unix)==sha12(windows)
    windows.write_bytes(b'{"claim_id":"C-002"}\r\n')
    assert sha12(unix)!=sha12(windows)
