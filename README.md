# Vietnamese Flight Question Answering System

A natural language processing system that answers flight-related queries in Vietnamese language. The system processes questions about flights between major Vietnamese cities including Ho Chi Minh City, Hue, Da Nang, Hai Phong, and Hanoi.

## 🎯 System Features

- Dependency grammar parser for Vietnamese language
- Syntactic analysis of query sentences
- Grammar relation generation for flight information
- Logical form conversion
- Procedural semantic generation
- Data retrieval for query answering

## 💡 Supported Queries

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

## 📁 Project Structure
.
├── Input/
│   ├── database/    # Flight database
│   └── question/    # Input questions
├── Output/          # Query results
├── Models/          # Processing modules
└── main.py         # Application entry point

## 🚀 Prerequisites

- Python 3.x
- regex library

* Results will be generated in the Output directory (output_1 → output_10)
