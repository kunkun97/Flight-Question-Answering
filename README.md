### Yêu cầu viết chương trình để hiện thực
a) Xây dựng bộ phân tích cú pháp của văn phạm phụ thuộc.\
b) Phân tích cú pháp và xuất ra các quan hệ của các thành phần của từng câu truy vấn.\
c) Từ kết quả ở b) tạo các quan hệ văn phạm cho các chuyến máy bay giữa thành phố Hồ Chí Minh, Huế, Đà Nẵng, Hải Phòng và Hà Nội với cơ sở dữ liệu đã cho ở trên.\
d) Tạo dạng luận lý từ các quan hệ văn phạm ở c).\
e) Tạo ngữ nghĩa thủ tục từ dạng luận lý ở d).\
f) Truy xuất dữ liệu để tìm thông tin trả lời cho các câu truy vấn trên.

### Các câu truy vấn:
1) Máy bay nào đến thành phố Huế lúc 13:30HR ?. 
2) Máy bay nào bay từ Đà Nẵng đến TP. Hồ Chí Minh mất 1:00 HR ?. 
3) Hãy cho biết mã hiệu các máy bay hạ cánh ở Huế ?. -> Máy bay nào đến thành phố Huế  ?. (*)
4) Máy bay nào xuất phát từ Tp. Hồ Chí Minh, lúc mấy giờ ?. 
5) Máy bay nào bay từ TP. Hồ Chí Minh đến Hà Nội ?.
6) Máy bay VN4 có xuất phát từ Đà Nẵng không ?.
7) Thời gian máy bay VJ5 bay từ TP. Hà Nội đến Khánh Hòa mất mấy giờ ?.
8) Có máy bay nào xuất phát từ Hải Phòng không ?. 
9) Máy bay của hãng hàng không VietJet Air bay đến những thành phố nào ?.
10) Có máy bay nào bay từ Hải Phòng đến Khánh Hòa không ?.
11) Máy bay VJ1 xuất phát từ HCM 10:HR phải không ?.
12) Máy bay nào bay từ TP. Hồ Chí Minh đến Đà Nẵng mất 1:00 HR ?.
(*) -> Vì chưa thể thực hiện được yêu cầu cô đưa nên em đã thay thế bằng 1 câu hỏi có văn phạm khác nhưng nội dung thì tương tự.

### Cấu trúc thư mục
* Input/database: Cơ sở dữ liệu đầu vào của bài toán.
* Input/question: Chứa các câu hỏi đầu vào của bài toán.
* Output: Kết quả thực thi của mỗi câu hỏi.
* Models: Các module con thực thi bài toán.
* main.py: Entry point cho chương trình với ngôn ngữ Python.

### Cách chạy ứng dụng:
# 1. Bước chuẩn bị:
* Cài đặt thư viện regex (dùng để thao tác với chuỗi trên python) nếu chưa có:
```
$ pip install regex
```

# 2. Chạy ứng dụng:
```
$ cd VoBaDat_2170307   # Trỏ đến thư mục cần chạy chương trình

$ python main.py  # Chạy chương trình
```
* File kết quả xuất ra nằm trong thư mục Output (output_1 → output_10), output_9 là kết quả của câu hỏi 10 và output_10 là kết quả của câu hỏi 12
