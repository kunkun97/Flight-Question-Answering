import re
import sys
from Models.io import *
from Models.api import *
import time

def get_question(index):
    questions = {
        1: "Máy bay nào đến thành phố Huế lúc 13:30HR?",
        2: "Máy bay nào bay từ Đà Nẵng đến TP. Hồ Chí Minh mất 1:00 HR?",
        3: "Hãy cho biết mã hiệu các máy bay hạ cánh ở Huế?. -> Máy bay nào đến thành phố Huế?",
        4: "Máy bay nào xuất phát từ Tp. Hồ Chí Minh, lúc mấy giờ?",
        5: "Máy bay nào bay từ TP. Hồ Chí Minh đến Hà Nội?",
        6: "Máy bay VN4 có xuất phát từ Đà Nẵng không?",
        7: "Thời gian máy bay VJ5 bay từ TP. Hà Nội đến Khánh Hòa mất mấy giờ?",
        8: "Có máy bay nào xuất phát từ Hải Phòng không?",
        9: "Máy bay của hãng hàng không VietJet Air bay đến những thành phố nào?",
        10: "Có máy bay nào bay từ Hải Phòng đến Khánh Hòa không?",
        11: "Máy bay VJ1 xuất phát từ HCM 10:HR phải không?",
        12: "Máy bay nào bay từ TP. Hồ Chí Minh đến Đà Nẵng mất 1:00 HR?"
    }

    return questions.get(index, "Invalid question index")

def main():
    sys.stdout.write("\033c")
    sys.stdout.flush()
    preprocess = PreProcessing.getInstance()
    process = Process.getInstance()
    while True:            
        user_input = input("Mời chọn câu hỏi, nhấn q để quit:\n"
                    "1) Máy bay nào đến thành phố Huế lúc 13:30HR?\n"
                   "2) Máy bay nào bay từ Đà Nẵng đến TP. Hồ Chí Minh mất 1:00 HR?\n"
                   "3) Hãy cho biết mã hiệu các máy bay hạ cánh ở Huế?. -> Máy bay nào đến thành phố Huế?\n"
                   "4) Máy bay nào xuất phát từ Tp. Hồ Chí Minh, lúc mấy giờ?\n"
                   "5) Máy bay nào bay từ TP. Hồ Chí Minh đến Hà Nội?\n"
                   "6) Máy bay VN4 có xuất phát từ Đà Nẵng không?\n"
                   "7) Thời gian máy bay VJ5 bay từ TP. Hà Nội đến Khánh Hòa mất mấy giờ?\n"
                   "8) Có máy bay nào xuất phát từ Hải Phòng không?\n"
                   "9) Máy bay của hãng hàng không VietJet Air bay đến những thành phố nào?\n"
                   "10) Có máy bay nào bay từ Hải Phòng đến Khánh Hòa không?\n"
                   "11) Máy bay VJ1 xuất phát từ HCM 10:HR phải không?\n"
                   "12) Máy bay nào bay từ TP. Hồ Chí Minh đến Đà Nẵng mất 1:00 HR? ")
        if user_input.lower() == "q":
            break            
        question = get_question(int(user_input))        
        tokens = preprocess.tokenize(question)
        types = preprocess.getWordTypes(tokens)
        for result in process.pipeline(tokens, types):
            print(result)

        time.sleep(3.5)        

if __name__ == "__main__":
    main()