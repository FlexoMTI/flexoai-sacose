import math

def calculeaza_oferta(data, cerere):
    if cerere.material not in ["albă", "maro"]:
        raise ValueError("Material invalid. Alege 'albă' sau 'maro'.")

    key = (cerere.material, cerere.dimensiune)
    if key not in data["preturi"].index:
        raise ValueError("Dimensiunea nu este disponibilă. Alege una dintre dimensiunile existente.")

    maner = cerere.maner or "plat"
    imprim = cerere.imprimare or "mică"
    nr_bucati = cerere.cantitate

    if nr_bucati < 100:
        if cerere.dimensiune not in data["ambalare"]:
            raise ValueError("Nu există ambalare definită pentru această dimensiune.")
        nr_bucati *= int(data["ambalare"][cerere.dimensiune])

    prag = None
    for p in [50000, 20000, 10000, 5000]:
        if nr_bucati >= p:
            prag = f"minim {p}"
            break
    if not prag:
        raise ValueError("Cantitatea minimă este de 5000 bucăți.")

    pret_unitar = data["preturi"].loc[key, prag]

    if imprim == "mică" and maner == "plat":
        if cerere.dimensiune in data["paleti"]:
            cutii = nr_bucati / data["ambalare"].get(cerere.dimensiune, 1)
            if cutii >= data["paleti"][cerere.dimensiune]:
                pret_unitar = data["preturi"].loc[key, "netiparite palet"]

    pret_maner = data["ajustari_maner"].get(maner, 0)
    pret_imprim = data["ajustari_imprimare"].get(imprim, 0)
    pret_total_unitar = pret_unitar + pret_maner + pret_imprim
    total = round(pret_total_unitar * nr_bucati, 2)

    # ✅ Matriță în funcție de număr culori primit explicit
    cost_matrita = 0
    culori = getattr(cerere, "culori", 0)
    if culori and imprim != "mică" and imprim != "fara":
        cost_matrita = culori * data["matrite"].get(cerere.dimensiune, 0)

    # Transport
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

    return (
        f"Pret unitar: {pret_total_unitar:.2f} lei/buc\n"
        f"Total bucati: {nr_bucati}\n"
        f"Total: {total:.2f} lei\n"
        f"Culori: {culori}\n"
        f"Matrita: {cost_matrita} lei\n"
        f"Transport: {transport} lei\n"
        f"Total final: {total_final:.2f} lei"
