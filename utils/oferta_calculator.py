def calculeaza_oferta(data, cerere):
    # Validări de bază
    if cerere.material not in ["albă", "maro"]:
        raise ValueError("Material invalid. Alege 'albă' sau 'maro'.")

    key = (cerere.material, cerere.dimensiune)
    if key not in data["preturi"].index:
        raise ValueError("Dimensiunea nu este disponibilă. Alege una dintre dimensiunile existente.")

    # Convertim maner + imprimare
    maner = cerere.maner or "plat"
    imprim = cerere.imprimare or "mică"
    nr_bucati = cerere.cantitate

    # Ambalare: verificăm dacă e exprimat în cutii (ex: 10 cutii)
    if nr_bucati < 100:  # presupunem că e număr de cutii
        if cerere.dimensiune not in data["ambalare"]:
            raise ValueError("Nu există ambalare definită pentru această dimensiune.")
        nr_bucati *= int(data["ambalare"][cerere.dimensiune])

    # Selectăm pragul de tiraj
    prag = None
    for p in [50000, 20000, 10000, 5000]:
        if nr_bucati >= p:
            prag = f"minim {p}"
            break
    if not prag:
        raise ValueError("Cantitatea minimă este de 5000 bucăți.")

    # Preț de bază
    pret_unitar = data["preturi"].loc[key, prag]

    # Preț special palet neimprimate
    if imprim == "mică" and maner == "plat":
        if cerere.dimensiune in data["paleti"] and nr_bucati >= data["paleti"][cerere.dimensiune] * 1:
            pret_unitar = data["preturi"].loc[key, "netiparite palet"]

    # Ajustări
    pret_maner = data["ajustari_maner"].get(maner, 0)
    pret_imprim = data["ajustari_imprimare"].get(imprim, 0)

    pret_total_unitar = pret_unitar + pret_maner + pret_imprim
    total = round(pret_total_unitar * nr_bucati, 2)

    # Cost matriță dacă e imprimare diferită de "mică"
    cost_matrita = 0
    if imprim != "mică" and imprim != "fara":
        culori = 2 if "25" in imprim else 3 if "50" in imprim else 4 if "fontă" in imprim else 1
        cost_matrita = culori * data["matrite"].get(cerere.dimensiune, 0)

    # Cost transport (1 palet sau cutie)
import math

buc_per_cutie = data["ambalare"].get(cerere.dimensiune, 1)
cutii = math.ceil(nr_bucati / buc_per_cutie)

cutii_per_palet = int(data["paleti"].get(cerere.dimensiune, 40))
nr_paleti = cutii // cutii_per_palet
cutii_extra = cutii % cutii_per_palet

transport = 0
if nr_paleti > 0:
    transport += nr_paleti * data["transport"]["Palet"]
if cutii_extra > 0:
    transport += cutii_extra * data["transport"]["Cutie"]  

    total_final = total + cost_matrita + transport

    return f"Pret unitar: {pret_total_unitar:.2f} lei/buc\nTotal bucati: {nr_bucati}\nTotal: {total:.2f} lei\nMatrita: {cost_matrita} lei\nTransport: {transport} lei\nTotal final: {total_final:.2f} lei (oferta valabila 30 zile)"
