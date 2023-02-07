import PyPDF2


def get_stats(sheet_contents):
    catagories = ["Str","Dex","Con","Int","Wis","Cha"]
    stats = []
    for x in range(12):
        if x%2:
            stats.append(sheet_contents[x+5])
    return(dict(zip(catagories,stats)))

def get_saving_throws(sheet_contents):
    catagories = ["Str","Dex","Con","Int","Wis","Cha"]
    stats = []
    for x in range(12):
        if x%2:
            stats.append(sheet_contents[x+18])
    
    return(dict(zip(catagories,stats)),sheet_contents[31])

def get_skills(sheet_contents):

    catagories = ["Acrobatics","Animal Handling","Arcana","Athletics","Deception","History","Insight","Intimidation","Investigation","Medicine","Nature","Perception","Performance","Persuasion","Religion","Slight of Hand","Stealth","Survival"]
    stats = []
    for x in range(45):
        if not x%3:
            stats.append(sheet_contents[x+33])
    
    #PDF is scuffed and doesn't have stat for last 3 skills making them every 2
    for x in range(6):
        if x%2:
            stats.append(sheet_contents[x+76])
    
    return(dict(zip(catagories,stats)))

def get_pasive_stats(sheet_contents):
    catagories = ["Pasive Perception","Pasive Insight","Pasive Investigation"]
    stats = []
    for x in range(3):
        stats.append(sheet_contents[x+82])
    
    return(dict(zip(catagories,stats)))

def get_senses(sheet_contents):
    return sheet_contents[85]

def get_initiative(sheet_contents):
    return sheet_contents[86]

def get_ac(sheet_contents):
    return sheet_contents[87]

def get_speed(sheet_contents):
    return sheet_contents[89]

#Converts a given pdf file to dictionary of the characters stats
def get_char_from_pdf(pdf):
    catagories = ["Stats", "Saving Throws", "Skills", "Pasive Stats","Senses","Initiative","AC","Speed"]
    stats = []
    try:
        pdf = open(pdf,"rb")
        pdfReader = PyPDF2.PdfReader(pdf)
        main_page = pdfReader.pages[0]
        sheet_info = []
        for annot in main_page["/Annots"]:
            if annot.get_object()["/Subtype"] == "/Widget":
                obj = annot.get_object()
                if "/V" in obj:
                    sheet_info.append(obj["/V"])
        stats.append(get_stats(sheet_info))
        stats.append(get_saving_throws(sheet_info))
        stats.append(get_skills(sheet_info))
        stats.append(get_pasive_stats(sheet_info))
        stats.append(get_senses(sheet_info))
        stats.append(get_initiative(sheet_info))
        stats.append(get_ac(sheet_info))
        stats.append(get_speed(sheet_info))
    except Exception as e:
        print("Something went wrong")
        print(str(e))
    
    return dict(zip(catagories,stats))
