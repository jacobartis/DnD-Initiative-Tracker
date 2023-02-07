import PyPDF2
pdf = open("CumGurglerDickInAss_63856309.pdf","rb")
pdfReader = PyPDF2.PdfReader(pdf)
main_page = pdfReader.pages[0]

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


#print(main_page.extract_text())

stuff = []

if "/Annots" in main_page:
    for annot in main_page["/Annots"]:
        if annot.get_object()["/Subtype"] == "/Widget":
            obj = annot.get_object()
            if "/V" in obj:
                stuff.append(obj["/V"])

print(get_stats(stuff))
print(get_saving_throws(stuff))
