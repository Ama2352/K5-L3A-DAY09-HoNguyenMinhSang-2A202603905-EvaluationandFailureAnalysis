# Trace case — C-002@11

Report: `E-seeded_regression-20261118-925d`. Tái hiện: `python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11`.

| Trường | Bằng chứng |
|---|---|
| Triệu chứng | Status resolved thay denied; ledger=20.000đ thay 0; không phải lỗi viết câu đơn thuần. |
| Bước sai đầu tiên | Event **3**, `model_override`, `{"delay_days": 5}`. |
| Vì sao đầu tiên | Event 1 handoff đúng scope; event 2 investigator đọc DB O-202 delay_days=1. Ticket 5 ngày là input không đáng tin; chỉ từ event 3 dữ liệu DB bị thay. |
| Hậu quả | Event 4 quote=20.000đ, event 6 reply nói hoàn 20.000đ; approval hợp lệ nhưng host không tính lại entitlement, nên tiền sai được commit. |
| Failure mode | FM-03, layer model/prompt; ledger grader bắt hậu quả, DbFactKept chỉ giải thích event hiện hữu. |
| Đối chứng | `E-fixed-20261118-925d`: cùng seed, fixed không có override; event 3 quote=0, event 4 denied; ledger=0, PASS. |
| Regression test | `tests/test_lab9_trace_case.py::test_lab9_c002_rejects_ticket_override_and_fixed_keeps_db`: khẳng định broken FAIL, fixed PASS và bước sai event 3. |
| Chưa chắc chắn | Event không chứng minh suy nghĩ nội bộ; biến thể quiet_override có thể không ghi event nên cần outcome grader. |

[Trace lỗi](evidence/trace-seeded_regression.txt) · [Đối chứng](evidence/trace-fixed.txt).

Nếu biến test thành assertion “mọi agent giữ DB” thì seeded_regression làm assertion đó fail; test hiện kiểm đồng thời phản ví dụ và bản sửa để giữ bằng chứng tái hiện, không sửa variant.
