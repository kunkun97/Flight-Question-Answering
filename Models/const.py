PLACE = ("hà_nội", "hải_phòng", "đà_nẵng", "hồ_chí_minh", "huế", "khánh_hòa",)


DICTIONARY = {
    "Root": "Root",
    "thành_phố": "Noun",
    "máy_bay" : "Noun",
    "thời_gian": "Noun",
    "nào": "WH",
    "mấy_giờ": "WH",
    "bay": "IVerb",
    "xuất_phát": "IVerb",
    "đến": ("OVerb", "Prep"),
    "từ": "Prep",
    "mất": "Aux",
    "lúc": "Aux",
    "không": "Aux",
    "có": "Aux",
    ",": "Punc",
    "?": "Punc",
    ".": "Punc",
}


PHRASE = (
    ("tp.", "thành_phố "),
    ("thành phố", "thành_phố"),
    ("hà nội", "hà_nội"),
    ("hải phòng", "hải_phòng"),
    ("đà nẵng", "đà_nẵng"),
    ("hồ chí minh", "hồ_chí_minh"),
    ("khánh hòa", "khánh_hòa"),
    ("máy bay", "máy_bay"),
    ("mấy giờ", "mấy_giờ"),
    ("xuất phát", "xuất_phát"),
    ("thời gian", "thời_gian"),
)


MAPPING = {
    "thời_gian": "TIME",
    "từ": "LEAVE",
    "đến": "ARRIVE",
    "bay": "RUN",
    "máy_bay": "FLIGHT",
    "nào": "WHICH",
    "mấy_giờ": "TIME",
    "lúc": "WHEN",
    "có": "YESNO",
    "không": "YESNO",
    "huế": "HUE",
    "hải_phòng": "HAIPHONG",
    "hà_nội": "HN",
    "đà_nẵng": "DANANG",
    "hồ_chí_minh": "HCM",
    "khánh_hòa": "KHANHHOA",  
    "xuất_phát": "RUN",
    "mất": "WHAT",
}