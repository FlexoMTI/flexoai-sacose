import pandas as pd

def load_data():
    xls = pd.ExcelFile("oferta_ai_sacose_REFORMAT_GL+GLOSAR.xlsx")

    preturi = xls.parse("Preturi Baza")
    manere = xls.parse("Ajustari Maner")
    imprimari = xls.parse("Ajustari Imprimare")
    ambalare = xls.parse("Ambalare")
    paleti = xls.parse("Cutii per Palet")
    matrite = xls.parse("Matrite")
    transport = xls.parse("Transport")

    # Normalizează datele în dicturi pentru acces rapid
    preturi.set_index(["Material", "Dimensiune"], inplace=True)
    manere = dict(zip(manere["Tip maner"], manere["Ajustare pret"]))
    imprimari = dict(zip(imprimari["Categorie"].fillna("fara"), imprimari["Ajustare pret"].fillna(0)))
    amb = dict(zip(ambalare["Dimensiune"], ambalare["Buc/cutie"]))
    pal = dict(zip(paleti["Dimensiune"], paleti["Cutii/palet"]))
    matr = dict(zip(matrite["Dimensiune"], matrite["Matrita/culoare"]))
    transp = dict(zip(transport["Tip Transport"], transport["Cost (lei)"]))

    return {
        "preturi": preturi,
        "ajustari_maner": manere,
        "ajustari_imprimare": imprimari,
        "ambalare": amb,
        "paleti": pal,
        "matrite": matr,
        "transport": transp
    }