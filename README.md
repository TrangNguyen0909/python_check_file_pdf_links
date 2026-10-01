# PDF Link Checker
## English

A simple Python tool that checks whether the links in a PDF file are still working.

### Features

- Extracts both clickable hyperlinks and plain-text URLs from every page
- Removes duplicate links and records the first page where each one appears
- Checks links concurrently (10 at a time) for speed
- Retries with GET when a site does not support HEAD requests
- Saves a CSV report next to the PDF

### Requirements

- Python 3.8+
- `pymupdf`
- `requests`

### Installation

```bash
pip install pymupdf requests
```

### Usage

```bash
python check_pdf_links.py file.pdf
```

If you run the script without a file name, a dialog box opens so you can choose the PDF.

### Output

The results are printed to the console and saved as `link_report.csv` in the same folder as the PDF.

| Column | Description |
|---|---|
| Page | First page where the link appears |
| URL | The link that was checked |
| Status Code | HTTP status code (`-` if the request failed) |
| Result | `OK` or `ERROR` |
| Final URL / Error | Final URL after redirects, or the error type |

### Result classification

| Result | Meaning |
|---|---|
| OK | Status code below 400 |
| OK (protected) | Status code 401, 403, 429 or 999: the page requires login or blocks bots, but usually opens in a real browser |
| ERROR | Page not found (404), server error, timeout, dead domain, etc. |

### Notes

- SSL certificate verification is disabled (`verify=False`), so sites with certificate problems may still be counted as OK.
- Pages that block bots are counted as OK even though they may not actually be reachable.
- The CSV file uses `utf-8-sig` encoding so it opens correctly in Excel.

---

## Tiếng Việt

Công cụ Python đơn giản giúp kiểm tra các link trong file PDF còn hoạt động hay không.

### Tính năng

- Lấy cả link bấm được (hyperlink) lẫn URL dạng chữ thường trong từng trang
- Loại link trùng và ghi lại trang đầu tiên link xuất hiện
- Kiểm tra song song (10 link cùng lúc) cho nhanh
- Tự thử lại bằng GET khi web không hỗ trợ HEAD
- Lưu báo cáo CSV cạnh file PDF

### Yêu cầu

- Python 3.8 trở lên
- `pymupdf`
- `requests`

### Cài đặt

```bash
pip install pymupdf requests
```

### Cách dùng

```bash
python check_pdf_links.py file.pdf
```

Nếu chạy không kèm tên file, một hộp thoại sẽ hiện ra để bạn chọn file PDF.

### Kết quả

Kết quả được in ra màn hình và lưu thành `link_report.csv` trong cùng thư mục với file PDF.

| Cột | Mô tả |
|---|---|
| Page | Trang đầu tiên link xuất hiện |
| URL | Link được kiểm tra |
| Status Code | Mã trạng thái HTTP (`-` nếu yêu cầu thất bại) |
| Result | `OK` hoặc `ERROR` |
| Final URL / Error | URL cuối sau khi chuyển hướng, hoặc loại lỗi |

### Phân loại kết quả

| Kết quả | Ý nghĩa |
|---|---|
| OK | Mã trạng thái dưới 400 |
| OK (bảo mật) | Mã 401, 403, 429 hoặc 999: trang cần đăng nhập hoặc chặn bot, nhưng thường vẫn mở được bằng trình duyệt |
| ERROR | Trang không tồn tại (404), lỗi server, hết thời gian chờ, domain chết, v.v. |

### Lưu ý

- Code tắt kiểm tra chứng chỉ SSL (`verify=False`), nên trang có chứng chỉ lỗi vẫn có thể được tính là OK.
- Trang chặn bot được tính là OK dù thực tế có thể không vào được.
- File CSV dùng mã hóa `utf-8-sig` để Excel hiển thị đúng.
