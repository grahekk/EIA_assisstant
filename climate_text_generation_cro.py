def location_info_text(data):
    udio_vegetacije_sum = data["udio_drveca"] + data["udio_raslinja"] + data["udio_travnjaka"]
    if udio_vegetacije_sum < 33:
        udio_kat = "vrlo mali"
    elif 33 <= udio_vegetacije_sum <= 66:
        udio_kat = "osrednji"
    else:
        udio_kat = "veliki"
    
    template = (
        "Navedena lokacija nalazi se u urbanom krajoliku na nadmorskoj visini od {nadmoska_visina:.2f} m. "
        "Nije prekrivena krošnjama, na području od {povrsina_podrucja:.2f} km2 oko dane lokacije je {udio_kat} "
        "udio vegetacije: {udio_drveca:.2f} % drveća, {udio_raslinja:.2f} % niskog raslinja i {udio_travnjaka:.2f} % travnjaka, "
        "a vlažnost tla pripada suhoj kategoriji. Orijentirana je prema {strana_svijeta} uz nagib tla "
        "od {nagib_tla:.2f}° i smještena u {geomorphon}. Najbliža šuma udaljena je više od {udaljenost_suma:.2f} km."
    )

    return template.format(udio_kat=udio_kat, **data)

# Example usage:
location_info_data = {
    "nadmoska_visina": 117.67,
    "povrsina_podrucja": 1,
    "udio_drveca": 15.59,
    "udio_raslinja": 14.92,
    "udio_travnjaka": 16.02,
    "strana_svijeta": "sjeveroistoku",
    "nagib_tla": 1.16,
    "geomorphon": "ravnici",
    "udaljenost_suma": 4
}

result_text = location_info_text(location_info_data)
print(result_text)


def drought_description_text(data):
    text_template = (
        "Prosječno maksimalno godišnje trajanje sušnog razdoblja je kroz zadnje {godine:.0f} godine bilo {trajanje:.2f} dana "
        "i očekuje se da će se u budućnosti, u prosjeku između {godina_pocetak:.0f} i {godina_kraj:.0f} g., ova vrijednosti povećati: "
        "pokazalo se da bi prosječno maksimalno godišnje trajanje sušnog razdoblja bilo {trajanje_budućnost:.2f} dana. "
        "Maksimalno godišnje odstupanje (sušno) od srednje količine oborine iz prošlosti je u prosjeku bilo "
        "{odstupanje_prošlost:.2f} standardnih devijacija dok se očekuje da će u budućnosti biti još izraženije, "
        "{odstupanje_budućnost:.2f} standardnih devijacija. Ova je lokacija u prošlosti pripadala "
        "{kategorija_suša_prošlost} kategoriji izloženosti suši, a u budućnosti se očekuje porast već izraženih indikatora suše "
        "tako da je za ovu lokaciju procijenjena visoka vjerojatnost suše."
    )
    return text_template.format(**data)

# Example usage:
drought_data = {
    "godine": 33,
    "trajanje": 28.21,
    "godina_pocetak": 2024,
    "godina_kraj": 2100,
    "trajanje_budućnost": 31.98,
    "odstupanje_prošlost": -1.43,
    "odstupanje_budućnost": -1.57,
    "kategorija_suša_prošlost": "srednjoj"
}

result_text = drought_description_text(drought_data)
print(result_text)

def generate_pluvial_description(data):
    text_template = (
        "Prosječni broj dana u godini s dnevnom količinom oborine koja prelazi prag od 95. percentila iz prošlosti je na danoj lokaciji "
        "kroz zadnje {godine:.0f} godine {prosječni_broj_dana:.2f} dana, a prosječno trajanje vlažnog razdoblja je {prosječno_trajanje:.2f} dana. "
        "Očekuje se da će se u budućnosti, između {godina_pocetak:.0f} i {godina_kraj:.0f}. godine ove vrijednosti neznatno promijeniti: "
        "pokazalo se da bi prosječni broj dana u godini s oborinom iznad 95. percentila oborine iz prošlosti trebao biti "
        "{prosječni_broj_dana_budućnost:.2f}, a prosječno trajanje vlažnog razdoblja {prosječno_trajanje_budućnost:.2f} dana. "
        "Vrijednosti indikatora za obilnu oborinu neće puno odstupati od dosadašnjih i radi se o prosječnim vrijednostima, "
        "a lokacija se nalazi na nepropusnoj površini u dolini tako da je za ovu lokaciju procijenjena srednja vjerojatnost obilnih oborina."
    )
    return text_template.format(**data)

# Example usage:
pluvial_data = {
    "godine": 33,
    "prosječni_broj_dana": 20.18,
    "prosječno_trajanje": 8.90,
    "godina_pocetak": 2024,
    "godina_kraj": 2100,
    "prosječni_broj_dana_budućnost": 21.03,
    "prosječno_trajanje_budućnost": 10.16
}

pluvial_description = generate_pluvial_description(pluvial_data)
print(pluvial_description)

def generate_heat_wave_description(data):
    text_template = (
        "Broj dana s minimalnim temperaturama zraka iznad 20 °C bitno je razmotriti u ovoj procjeni zato što on utječe na zdravlje. "
        "U protekle {godine:.0f} godine u prosjeku ih je godišnje bilo {broj_dana_iznad_20:.2f}, a pokazalo se da će u budućnosti, između {godina_pocetak:.0f}. i {godina_kraj:.0f}. g. ovaj broj narasti do čak {budući_broj_dana_iznad_20:.2f} dana u godini. "
        "Broj dana sa temperaturom iznad 30 °C dosad je u prosjeku bio {broj_dana_iznad_30:.2f} dana u godini i očekuje se značajan porast, "
        "odnosno trebao bi u budućnosti iznositi {budući_broj_dana_iznad_30:.2f} dana u godini. "
        "Razmatrana je i prividna temperatura, odnosno osjet temperature koju doživljava čovjek s obzirom na temperaturu i vlagu zraka. "
        "Njena maksimalna godišnja vrijednost je dosad u prosjeku bila {maksimalna_prividna_temperatura:.2f} °C, a u budućnosti se može očekivati "
        "porast na, u prosjeku, {buduća_maksimalna_prividna_temperatura:.2f} °C. "
        "Također, radi se o urbanom krajoliku bez visoke vegetacije koja obično pruža zaštitu od izrazito visokih temperatura zraka tijekom vrućih dana. "
        "Iz danih rezultata zaključuje se da je lokacija dosad pripadala u srednju kategoriju izloženosti toplinskim valovima, međutim u budućnosti "
        "se očekuje porast temperatura zraka i otežani uvjeti pri čemu je za ovu lokaciju procijenjena visoka vjerojatnost toplinskih valova u budućnosti."
    )
    return text_template.format(**data)

# Example usage:
heat_wave_data = {
    "godine": 33,
    "broj_dana_iznad_20": 70.37,
    "godina_pocetak": 2024,
    "godina_kraj": 2100,
    "budući_broj_dana_iznad_20": 90.29,
    "broj_dana_iznad_30": 51.79,
    "budući_broj_dana_iznad_30": 68.75,
    "maksimalna_prividna_temperatura": 43.68,
    "buduća_maksimalna_prividna_temperatura": 45.81
}

heat_wave_description = generate_heat_wave_description(heat_wave_data)
print(heat_wave_description)

def generate_wildfire_description(data):
    text_template = (
        "Prosječna vrijednost maksimalnih godišnjih vrijednosti požarnog indeksa (eng. Fire Weather Index) je u posljednje {godine:.0f} godine "
        "za ovu lokaciju iznosila {prosječna_vrijednost:.2f}, a očekuje se da će u razdoblju između {godina_pocetak:.0f}. i {godina_kraj:.0f}. "
        "prosječna vrijednost maksimalnih godišnjih vrijednosti ovog požarnog indeksa porasti na {buduća_vrijednost:.2f}. "
        "Dana lokacija ne nalazi se u blizini šume (udaljenost je veća od {udaljenost_suma:.0f} m) te se nalazi u urbanom krajoliku, "
        "pa je za ovu lokaciju procijenjena mala vjerojatnost šumskih požara."
    )
    return text_template.format(**data)

# Example usage:
wildfire_data = {
    "godine": 33,
    "prosječna_vrijednost": 41.82,
    "godina_pocetak": 2024,
    "godina_kraj": 2100,
    "buduća_vrijednost": 46.34,
    "udaljenost_suma": 4000
}

wildfire_description = generate_wildfire_description(wildfire_data)
print(wildfire_description)

def generate_severe_wind_description(data):
    text_template = (
        "U protekle {godine:.0f} godine je u prosjeku godišnje bilo {prosjecni_broj_dana:.2f} dana s olujnim (ili jačim) udarima vjetra, "
        "a pokazalo se da bi u budućnosti, u razdoblju između {godina_pocetak:.0f}. i {godina_kraj:.0f}. moglo biti u prosjeku {buduci_broj_dana:.2f} dana. "
        "Ovo su umjerene do visoke vrijednosti, lokacija nalazi u dolini, ali u neposrednom okruženju nema stabala ni struktura koje bi mogle popustiti pod utjecajem vjetra "
        "i dovesti do oštećenja pa je prema tome za ovu lokaciju procijenjena umjerena vjerojatnost olujnih udara vjetra."
    )
    return text_template.format(**data)

# Example usage:
severe_wind_data = {
    "godine": 33,
    "prosjecni_broj_dana": 12.62,
    "godina_pocetak": 2024,
    "godina_kraj": 2100,
    "buduci_broj_dana": 13.18
}

severe_wind_description = generate_severe_wind_description(severe_wind_data)
print(severe_wind_description)
