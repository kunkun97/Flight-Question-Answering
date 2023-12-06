import regex
from Models.io import *
from Models.const import *
from typing import List, Tuple
from abc import ABC, abstractmethod


class PreProcessing:
    instance = None

    @staticmethod
    def getInstance():
        if not PreProcessing.instance:
            PreProcessing.instance = PreProcessing()
        
        return PreProcessing.instance


    def tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = text.replace(',', ' , ')
        for phrase, word in PHRASE:
            text = text.replace(phrase, word)

        return text.split()


    def getWordTypes(self, tokens: List[str]) -> List[str]:
        types = []

        for i, token in enumerate(tokens):
            if token in DICTIONARY:
                if isinstance(DICTIONARY[token], str):
                    types.append(DICTIONARY[token])
                else:
                    index = i
                    while index > 0:
                        index -= 1
                        if types[index] == "Prep":
                            types.append(DICTIONARY[token][1])
                            break
                    else:
                        types.append(DICTIONARY[token][0])    
            elif token in PLACE:
                types.append("Name")
            else:
                types.append("ID" if regex.search(r"v.\d", token) else "Time")
                    

        return types


class Process:
    instance = None

    @staticmethod
    def getInstance():
        if not Process.instance:
            Process.instance = Process()

        return Process.instance


    class NLP(ABC):
        def __init__(self) -> None:
            self.variable = []


        def createVariable(self, word: str) -> str:
            i = 0
            while True:
                i += 1
                var = word+str(i)
                if not var in self.variable:
                    return var

        @abstractmethod
        def transform(self):
            pass


    class DependencyParser(NLP):
        def __init__(self, tokens: List[str], types: List[str]) -> None:
            super().__init__()
            self.SHIFT = 0
            self.RIGHTARC = 1
            self.LEFTARC = 2
            self.REDUCE = 3
            self.operator = {0: "SHIFT", 1: "RIGHTARC", 2: "LEFTARC", 3: "REDUCE"}
            self.step = []
            self.relations = []
            self.stack = [("Root", "Root")]
            self.buffer = list(zip(tokens, types))



        def transform(self) -> List[str]:
            """ MaltParser arc-eager """

            while len(self.buffer) > 0:
                token = self.buffer[0]
                word = self.stack[-1]
                op, relation = self.__selectOp(word[1], token[1])

                if op == self.SHIFT:
                    relation = ""
                    self.stack.append(token)
                    del self.buffer[0]
                elif op == self.RIGHTARC:
                    relation = "({}, {}, {})".format(relation, word[0], token[0])
                    self.relations.append(relation)
                    self.stack.append(token)
                    del self.buffer[0]
                elif op == self.LEFTARC:
                    relation = "({}, {}, {})".format(relation, token[0], word[0])
                    self.relations.append(relation)
                    del self.stack[-1]
                elif op == self.REDUCE:
                    relation = ""
                    del self.stack[-1]

                self.step.append("{}\t{}\t{}\t{}".format(self.operator[op], str([ele[0] for ele in self.stack]), str([ele[0] for ele in self.buffer]), relation))

            return self.relations.copy()


        def __selectOp(self, stackType: str, buffType: str) -> Tuple[int, str]:
            if buffType == "Noun":
                if stackType == "Root":
                    return self.SHIFT, None
                elif stackType == "Noun" and (len(self.stack) <= 2 or self.stack[-2][1] != "Noun"):
                    return self.RIGHTARC, "nmod"
                elif stackType == "WH":
                    return self.LEFTARC, "nmod"
                elif stackType == "OVerb":
                    return self.RIGHTARC, "dobj"
                elif stackType == "Prep":
                    return self.RIGHTARC, "pobj"
                elif stackType == "Aux":
                    return self.RIGHTARC, "nmod"
            elif buffType == "WH":
                if stackType == "IVerb" or stackType == "OVerb":
                    return self.SHIFT, None
                elif stackType == "Noun" and (len(self.stack) <= 2 or self.stack[-2][1] != "Noun"):
                    return self.RIGHTARC, "whmod"
                elif stackType == "Aux" or stackType == "Prep":
                    return self.RIGHTARC, "whmod"
            elif buffType == "IVerb":
                if stackType == "Root":
                    return self.RIGHTARC, "root"
                elif stackType == "Noun" and (len(self.stack) <= 2 or self.stack[-2][1] != "Noun"):
                    return self.LEFTARC, "subj"
                elif stackType == "Aux":
                    return self.LEFTARC, "aux"
            elif buffType == "OVerb":
                if stackType == "Root":
                    return self.RIGHTARC, "root"
                elif stackType == "Noun" and (len(self.stack) <= 2 or self.stack[-2][1] != "Noun"):
                    return self.LEFTARC, "subj"
                elif stackType == "Aux":
                    return self.LEFTARC, "aux"
            elif buffType == "Prep":
                if stackType == "IVerb" or stackType == "OVerb":
                    return self.RIGHTARC, "pmod"
            elif buffType == "Aux":
                if stackType == "IVerb" or stackType == "OVerb":
                    return self.RIGHTARC, "aux"
                elif not list(filter(lambda x: "root" in x, self.relations)):
                    return self.SHIFT, None
            elif buffType == "Time":
                if stackType == "Aux":
                    return self.RIGHTARC, "timemod"
            elif buffType == "ID":
                if stackType == "Noun":
                    return self.RIGHTARC, "idmod"
            elif buffType == "Name":
                if stackType == "Noun":
                    return self.RIGHTARC, "namemod"
                elif stackType == "Prep":
                    return self.RIGHTARC, "pobj"
            elif buffType == "Punc":
                if stackType == "IVerb" or stackType == "OVerb":
                    return self.RIGHTARC, "punc"

            return self.REDUCE, None


        def __str__(self) -> str:
            stepStr = "\n".join(step for step in self.step)
            relationStr = " ".join(relation for relation in self.relations)
            return "b) Phân tích cú pháp và xuất ra các quan hệ của các thành phần của từng câu truy vấn: \n" + stepStr + "\n\n" + relationStr + "\n\n\n\n" 


    class GrammarRelation(NLP):
        def __init__(self, relations: List[str]) -> None:
            super().__init__()
            self.variable = ["s1"]
            for i in range(len(relations)):
                relations[i] = regex.sub(r'[,()]', "", relations[i])

                if "namemod" in relations[i]:
                    tokens = relations[i].split()
                    name = ("[NAME-{}-\"{}\"]".format(super().createVariable(tokens[2][0]), tokens[2].upper()))
                    tokens = relations[i-1].split()
                    tokens[2] = name
                    relations[i-1] = " ".join(token for token in tokens)
                elif "pobj" in relations[i]:
                    tokens = relations[i].split()
                    if tokens[2] in PLACE:
                        name = ("[NAME-{}-\"{}\"]".format(super().createVariable(tokens[2][0]), tokens[2].upper()))
                        tokens[2] = name
                        relations[i] = " ".join(token for token in tokens)
                elif "whmod" in relations[i] and "aux" in relations[i-1]:
                    tokens = relations[i-1].split()
                    pred = tokens[1]
                    aux = tokens[2]
                    tokens = relations[i].split()
                    tokens[1] = pred
                    tokens.append(aux)
                    relations[i] = " ".join(token for token in tokens)
                elif "idmod" in relations[i]:
                    tokens = relations[i].split()
                    relations = [relation.replace(tokens[1], "[ID-{}-{}]".format(tokens[2], tokens[1])) for relation in relations]

            self.dep_relation = relations
            self.gram_relation = set()


        def transform(self) -> List[str]:
            for relation in self.dep_relation:
                transformRelation = self.__relationTransform(relation)

                if transformRelation:
                    self.gram_relation.add(transformRelation)

            self.gram_relation = list(self.gram_relation)
            query = list(filter(lambda x: "QUERY" in x, self.gram_relation))
            pred = list(filter(lambda x: "PRED" in x, self.gram_relation))
            subj = list(filter(lambda x: "LSUBJ" in x, self.gram_relation))
            lobj = list(filter(lambda x: "LOBJ" in x, self.gram_relation))
            other = list(filter(lambda x: "QUERY" not in x and "PRED" not in x and "LSUBJ" not in x and "LOBJ" not in x, self.gram_relation))
            self.gram_relation = query+pred+subj+lobj+other
            return self.gram_relation


        def __relationTransform(self, relation: str) -> str:
            result = ""
            relation = relation.split()

            if "root" in relation:
                result = "({} PRED {})".format("s1", relation[2].upper())
            elif "subj" in relation:
                result = "({} LSUBJ {})".format("s1", relation[2].upper())   
            elif "dobj" in relation:
                result = "({} LOBJ {})".format("s1", relation[2])
            elif "timemod" in relation:
                result = "({} TIME {})".format("s1", relation[2].upper())
            elif "whmod" in relation:
                if MAPPING[relation[2]] == "WHICH":
                    result = "({} WHQUERY [WHICH-{}-{}])".format("s1", self.createVariable(relation[1][0]), relation[1].upper())
                elif MAPPING[relation[2]] == "TIME":
                    result = "({} WHQUERY [{}-{}-TIME])".format("s1", MAPPING[relation[3]], "s1")
            elif "pobj" in relation:
                if "từ" in relation:
                    result = "({} PFROM {})".format("s1", relation[2])
                elif "đến" in relation:
                    result = "({} PTO {})".format("s1", relation[2])
            elif "aux" in relation and relation[2] in MAPPING and MAPPING[relation[2]] == "YESNO":
                result = "({} YNQUERY {})".format("s1", relation[1].upper())
            elif "nmod" in relation:
                result = "({} NMOD {})".format(relation[1].upper(), relation[2].upper())

            return result

        
        def __str__(self) -> str:
            relations = "\n".join(relation for relation in self.gram_relation)
            relations = relations.replace("-", " ").replace("[", "(").replace("]", ")")

            return "c) Quan hệ văn phạm cho các chuyến máy bay: \n" + relations + "\n\n\n\n"


    class LogicalForm(NLP):
        def __init__(self, relations: List[str]) -> None:
            super().__init__()
            self.mode = "WH"
            self.relations = relations
            self.verb = "ATTITUDE"

            for relation in self.relations:
                if "LOBJ" in relation:
                    self.verb = "VERB"

            self.logicalForm = ["&"]


        def transform(self) -> Tuple[List[str], str]:
            for i in range(len(self.relations)):
                relation = regex.sub(r'[()]', "", self.relations[i])
                tokens = relation.split()

                if "PRED" in relation:
                    self.logicalForm.append("({} {})".format(tokens[2], tokens[0]))
                elif "LSUBJ" in relation:
                    if self.verb == "ATTITUDE":
                        self.logicalForm.append("(EXPERIENCER {} {})".format(tokens[0], tokens[2]))
                    elif self.verb == "VERB":
                        self.logicalForm.append("(AGENT {} {})".format(tokens[0], tokens[2]))
                elif "LOBJ" in relation:
                    self.logicalForm.append("(THEME {} {})".format(tokens[0], tokens[2]))
                elif "PFROM" in relation:
                    self.logicalForm.append("(FROM_LOC {} {} {})".format("fl", tokens[0], tokens[2]))
                elif "PTO" in relation:
                    self.logicalForm.append("(TO_LOC {} {} {})".format("tl", tokens[0], tokens[2]))
                elif "NMOD" in relation:
                    self.logicalForm.append("(NMOD {} {})".format(tokens[0], tokens[2]))
                elif "WHQUERY" in relation:
                    self.mode = "WH"
                    
                    if "WHICH" in relation:
                        subj = tokens[2][1:-1].split('-')[2]
                        self.relations = [ele.replace(subj, tokens[2]) for ele in self.relations]

                    elif "WHEN" in relation and "TIME" in relation:
                        self.logicalForm.append("(AT_TIME {} {})".format(tokens[0], tokens[2]))

                    elif "WHAT" in relation and "TIME" in relation:
                        self.logicalForm.append("(RUN_TIME {} {})".format(tokens[0], tokens[2])) # CHECK LẠI

                elif "YNQUERY" in relation:
                    self.mode = "YN"
                elif "TIME" in relation:
                    self.logicalForm.append("(AT_TIME {} {})".format(tokens[0], tokens[2]))

            return self.logicalForm, self.mode


        def __str__(self) -> str:
            logicalForm = " ".join(ele for ele in self.logicalForm)

            if self.mode == "WH":
                logicalForm = "(WH-QUERY(" + logicalForm + "))"
            elif self.mode == "YN":
                logicalForm = "(YS-QUERY(" + logicalForm + "))"

            logicalForm = logicalForm.replace("-", " ").replace("[", "(").replace("]", ")")
            return "d) Dạng luận lý từ các quan hệ văn phạm: \n" + logicalForm + "\n\n\n\n"


    class Procedure(NLP):
        def __init__(self, logicalForm: List[str], mode: str) -> None:
            super().__init__()
            self.logicalForm = logicalForm
            self.mode = mode
            self.subj = []
            self.action = None
            self.varmap = {"FLIGHT": "t", "STIME": "st", "DTIME": "dt", "RUN_TIME": "rt"}
            self.variables = ["t", "st", "dt", "rt", "s", "d"]
            self.runtime = [False, ["?t", "?s", "?d", "?rt"]]
            self.atime = [False, ["?t", "?d", "?dt"]]
            self.dtime = [False, ["?t", "?s", "?st"]]

        
        def transform(self) -> None:
            for relation in self.logicalForm:
                relation = regex.sub(r'[()"]', "", relation)
                tokens = relation.split()

                if "ID" in relation:
                    tokens = tokens[2][1:-1].split('-')
                    self.atime[1][0] = tokens[1]
                    self.dtime[1][0] = tokens[1]
                    self.runtime[1][0] = tokens[1]


                if "WH" in relation:
                    tokens = tokens[2][1:-1].split('-')
                    subj = tokens[2] if tokens[2].lower() not in MAPPING else MAPPING[tokens[2].lower()]
                    if subj == "TIME" and "AT_TIME" in relation:
                        self.subj.append("TIME")
                    elif subj == "TIME" and "RUN_TIME" in relation:
                        self.subj.append("RUN_TIME")
                        self.runtime[0] = True
                    else:
                        self.subj.append(subj)
                elif "FROM_LOC" in relation:
                    tokens = tokens[3][1:-1].split('-')
                    self.dtime[0] = True
                    self.dtime[1][1] = MAPPING[tokens[2].lower()]
                    if "TIME" in self.subj:
                        self.subj.append("STIME")
                        self.subj.remove("TIME")
                    self.runtime[1][1] = MAPPING[tokens[2].lower()]
                elif "TO_LOC" in relation:
                    tokens = tokens[3][1:-1].split('-')
                    self.atime[0] = True
                    self.atime[1][1] = MAPPING[tokens[2].lower()]
                    if "TIME" in self.subj:
                        self.subj.append("DTIME")
                        self.subj.remove("TIME")
                    self.runtime[1][2] = MAPPING[tokens[2].lower()]
                elif "AT_TIME" in relation:
                    if self.action == "ARRIVE":
                        self.atime[1][2] = tokens[2]
                    elif self.action == "LEAVE":
                        self.dtime[1][2] = tokens[2]
                elif len(tokens) == 2:
                    self.action = MAPPING[tokens[0].lower()]
                    if self.action == "ARRIVE":
                        self.atime[0] = True
                elif "THEME" in relation:
                    tokens = tokens[2][1:-1].split('-')
                    if self.action == "ARRIVE":
                        self.atime[1][1] = MAPPING[tokens[2].lower()]
                    elif self.action == "LEAVE":
                        self.dtime[1][1] = MAPPING[tokens[2].lower()]


        def __str__(self) -> str:
            procedure = []
            
            if self.runtime[0]:
                procedure.append("(RUN-TIME {} {} {} {})".format(*self.runtime[1]))
            if self.atime[0]:
                procedure.append("(ATIME {} {} {})".format(*self.atime[1]))
            if self.dtime[0]:
                procedure.append("(DTIME {} {} {})".format(*self.dtime[1]))

            if self.mode == "WH":
                prefix = "PRINT-ALL "
                
                for subj in self.subj:
                    var = self.varmap[subj]
                    prefix += "?{} ({} ?{}) ".format(var, subj, var)

                procedure = prefix + " ".join(ele for ele in procedure)
            elif self.mode == "YN":
                procedure = "YES-NO " + " ".join(ele for ele in procedure)
            
            return "e) Ngữ nghĩa thủ tục từ dạng luận lý: \n(" + procedure + ")\n\n\n\n"


        def execute(self) -> str:
            result = ""
            io = IO.getInstance()

            atime = None
            dtime = None
            runtime = None

            ids = set(map(lambda x: x.split()[1], io.queryDatabase("flight")))
            if self.atime[0]:
                atime = io.queryDatabase("atime", *self.atime[1])
                ids = ids.intersection(set(map(lambda x: x.split()[1], atime)))
            if self.dtime[0]:
                dtime = io.queryDatabase("dtime", *self.dtime[1])
                ids = ids.intersection(set(map(lambda x: x.split()[1], dtime)))
            if self.runtime[0]:
                runtime = io.queryDatabase("rtime", *self.runtime[1])
                ids = ids.intersection(set(map(lambda x: x.split()[1], runtime)))

            if self.mode == "WH":
                for id in ids:
                    for subj in self.subj:
                        if subj == "FLIGHT":
                            result += "Máy bay mã số {}. ".format(id)
                        elif subj == "RUN_TIME":
                            time = [ele.split()[4] for ele in runtime if id in ele][0]
                            result += "Thời gian máy bay đi từ nơi xuất phát đến nơi đến mất {}. ".format(time)
                        elif subj == "STIME":
                            time = [ele.split()[3] for ele in dtime if id in ele][0]
                            result += "Máy bay cất cánh lúc {}. ".format(time)
                        elif subj == "DTIME":
                            time = [ele.split()[3] for ele in atime if id in ele][0]
                            result += "Máy bay hạ cánh lúc {}. ".format(time)
                    result += "\n"

            elif self.mode == "YN":
                result += "Có. \n" if ids else "Không. \n"

            if result == "":
                result = "Không tồn tại chuyến bay thỏa yêu cầu câu hỏi. \n"

            return "f) Truy xuất dữ liệu để tìm thông tin trả lời cho các câu truy vấn:\n" + result



    def pipeline(self, tokens: List[str], types: List[str]):
        parser = self.DependencyParser(tokens, types)
        relation = parser.transform()
        yield parser

        grammar = self.GrammarRelation(relation)
        grammartical = grammar.transform()
        yield grammar

        logical = self.LogicalForm(grammartical)
        logicalForm, mode = logical.transform()
        yield logical

        procedure = self.Procedure(logicalForm, mode)
        procedure.transform()
        yield procedure

        result = procedure.execute()
        yield result