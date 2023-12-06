import os
from typing import List




class IO:
    instance = None

    @staticmethod
    def getInstance():
        if not IO.instance:
            IO.instance = IO()
        
        return IO.instance


#    def loadData(self, folder: str) -> List[str]:
    def loadData(self, folder: str):
        data = []
        for file in sorted(os.listdir(folder)):
            with open(folder+file, "r", encoding='utf8') as f:
                data.append(f.readline())

        return data


#    def writeData(self, file: str, mode: str, data: str) -> None:
    def writeData(self, file: str, mode: str, data: str):    
        with open(file, mode, encoding='utf8') as f:
            f.write(data)

    
#    def queryDatabase(self, database: str, *filterData) -> List[str]:
    def queryDatabase(self, database: str, *filterData):        
        data = None
        with open('Input/database/{}.txt'.format(database), "r", encoding='utf8') as f:
            data = f.readlines()

        for key in filterData:
            if "?" not in key:
                data = list(filter(lambda x: key in x, data))

        return data