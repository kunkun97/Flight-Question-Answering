from Models.io import *
from Models.api import *

def main():
    io = IO.getInstance()
    preprocess = PreProcessing.getInstance()
    process = Process.getInstance()

    sentences = io.loadData("Input/question/")
    print(sentences)

    for i, text in enumerate(sentences):     
        tokens = preprocess.tokenize(text)
        types = preprocess.getWordTypes(tokens)

        io.writeData(f"Output/output_{i+1}.txt", "w+", f"Kết quả truy vấn câu hỏi {i+1}\n\n")
        for result in process.pipeline(tokens, types):
            io.writeData(f"Output/output_{i+1}.txt", "a+", str(result))

if __name__ == '__main__':
    main()