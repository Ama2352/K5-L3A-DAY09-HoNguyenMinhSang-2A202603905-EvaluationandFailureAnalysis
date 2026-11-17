# Judge audit

| Judge | n | κ | Precision | Recall | Ma trận (tp/fp/fn/tn) | Quyết định |
|---|---|---|---|---|---|---|
| tone | 100 | 0.757 | 0.857 | 0.8 | {'tp': 24, 'fp': 4, 'fn': 6, 'tn': 66} | Dùng cho tone |
| helpful | 100 | 0.375 | 1.0 | 0.3 | {'tp': 9, 'fp': 0, 'fn': 21, 'tn': 70} | Loại khỏi gate |

## Audit thủ công các bất đồng

| Case | Judge | Người | Ai đúng và vì sao | Sửa rubric |
|---|---|---|---|---|
| H-008 | PASS | FAIL | Người: xưng em/anh và nha quá suồng sã cho chuẩn hỗ trợ đã định. | Nêu rõ cách xưng hô chuẩn, ví dụ âm tính dùng nha. |
| H-017 | PASS | FAIL | Người: có Dạ nhưng bạn ơi/rồi nha không đạt chuẩn xưng hô. | Không dùng chỉ một từ Dạ làm điều kiện đủ. |
| H-029 | PASS | FAIL | Người: không cần nhắn thêm mang ý ngăn khách hỏi tiếp. | Thêm ví dụ câu lịch sự bề mặt nhưng dismissive. |
| H-042 | FAIL | PASS | Người: thông báo ngắn nhưng lịch sự và có thời gian chờ. | Độ dài không phải tiêu chí tone; chấp nhận câu ngắn. |
| H-051 | FAIL | PASS | Người: từ refund không khiến câu thiếu tôn trọng. | Không đánh FAIL chỉ vì một thuật ngữ tiếng Anh. |
| HL-015 | PASS | FAIL | Người: sai tiền; ledger ghi 40.000đ. | So sánh tiền với ledger bằng code; lời xin lỗi không bù được sai kết quả. |
| HL-016 | PASS | FAIL | Người: sai tiền; ledger ghi 35.000đ. | So sánh tiền với ledger bằng code; lời xin lỗi không bù được sai kết quả. |
| HL-020 | PASS | FAIL | Người: sai tiền; ledger ghi 120.000đ. | So sánh tiền với ledger bằng code; lời xin lỗi không bù được sai kết quả. |
| HL-028 | PASS | FAIL | Người: sai tiền; ledger ghi 35.000đ. | So sánh tiền với ledger bằng code; lời xin lỗi không bù được sai kết quả. |
| HL-035 | PASS | FAIL | Người: sai tiền; ledger ghi 35.000đ. | So sánh tiền với ledger bằng code; lời xin lỗi không bù được sai kết quả. |

Tone đạt floors κ≥0.6, P≥0.8, R≥0.7; vẫn bỏ sót 6/30 lỗi nên chỉ đánh giá cách nói, không đánh giá tiền/approval. Helpful precision=1 nhưng recall=0.3, bỏ sót 21/30 lỗi và κ=0.375: dùng nó làm gate sẽ cho nhiều kết quả sai đi qua.

Rogan–Gladen: tone observed=0.28 → corrected=0.3; helpful observed=0.09 → corrected=0.3. Hiệu chỉnh tỉ lệ tổng thể không sửa nhãn từng case và không cứu một classifier kém.

Đây là replay CSV công khai; audit là phân tích nhãn người có sẵn, chưa phải nhãn độc lập mới. Cần held-out do hai người chấm, xử lý bất đồng rồi hiệu chuẩn lại trước model thật. Xem [output tone](evidence/tone.txt) và [helpful](evidence/helpful.txt).
