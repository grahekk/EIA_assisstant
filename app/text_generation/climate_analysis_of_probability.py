from .climate_averages import data

def generate_location_info_text(data):
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

location_info = generate_location_info_text(location_info_data)


def generate_drought_description_text(data):
    text_template = (
        "Prosječno maksimalno godišnje trajanje sušnog razdoblja je kroz zadnje {godine:.0f} godine bilo {P0_consecutive_dry_days:.2f} dana "
        "i očekuje se da će se u budućnosti, u prosjeku između {godina_pocetak:.0f} i {godina_kraj:.0f} g., ova vrijednosti povećati: "
        "Za P1 se pokazalo da bi prosječno maksimalno godišnje trajanje sušnog razdoblja bilo {P1_consecutive_dry_days:.2f} dana, "
        "a za P2 se pokazalo da bi prosječno maksimalno godišnje trajanje sušnog razdoblja bilo {P2_consecutive_dry_days:.2f} dana. "
        "Maksimalno godišnje odstupanje (sušno) od srednje količine oborine iz prošlosti je u prosjeku bilo "
        "{P0_spi3_dry_min_periodmean:.2f} standardnih devijacija, a u budućnosti će biti još izraženije: "
        "za P1 {P1_spi3_dry_min_periodmean:.2f} standardnih devijacija,"
        "a za P2 {P2_spi3_dry_min_periodmean}. Ova je lokacija u prošlosti pripadala "
        "{kategorija_suša_prošlost} kategoriji izloženosti suši, a u budućnosti se očekuje porast već izraženih indikatora suše "
        "tako da je za ovu lokaciju procijenjena {kategorija_suša_budućnost} vjerojatnost suše."
    )
    return text_template.format(**data)

# Example usage:
drought_data = {
    "godine": 33,
    "P0_consecutive_dry_days": data.loc["codd_periodmean", "P0"],
    "godina_pocetak": 2024,
    "godina_kraj": 2100,
    "P1_consecutive_dry_days": data.loc["codd_periodmean", "P1"],
    "P2_consecutive_dry_days": data.loc["codd_periodmean", "P2"],
    "P0_spi3_dry_min_periodmean": data.loc["spi3_dry_min_periodmean", "P0"],
    "P1_spi3_dry_min_periodmean": data.loc["spi3_dry_min_periodmean", "P1"],
    "P2_spi3_dry_min_periodmean": data.loc["spi3_dry_min_periodmean", "P2"],
    "kategorija_suša_prošlost": "srednjoj",
    "kategorija_suša_budućnost": "i dalje srednja"
}

drought_description = generate_drought_description_text(drought_data)

def generate_pluvial_description(data):
    text_template = (
        "Prosječni broj dana u godini s dnevnom količinom oborine koja prelazi prag od 95. percentila iz prošlosti je na danoj lokaciji "
        "kroz zadnje {godine:.0f} godine {P0_r95p_periodmean:.2f} dana, a prosječno trajanje vlažnog razdoblja je {P0_cwd_periodmean:.2f} dana. "
        "Očekuje se da će se u budućnosti, između {godina_pocetak:.0f} i {godina_kraj:.0f}. godine ove vrijednosti neznatno promijeniti: "
        "pokazalo se da bi prosječni broj dana u godini s oborinom iznad 95. percentila oborine za P1 razdoblje trebao biti "
        "{P1_r95p_periodmean:.2f}, a prosječno trajanje vlažnog razdoblja {P1_cwd_periodmean:.2f} dana. "
        "Za P2 to bi bilo {P2_r95p_periodmean:.2f}, a prosječno trajanje vlažnog razdoblja {P2_cwd_periodmean:.2f} dana. "
        "Vrijednosti indikatora za obilnu oborinu neće puno odstupati od dosadašnjih i radi se o prosječnim vrijednostima, "
        "a lokacija se nalazi na nepropusnoj površini u {geomorphon} tako da je za ovu lokaciju procijenjena {vjerojatnost_obilne_oborine} vjerojatnost obilnih oborina."
    )
    return text_template.format(**data)

# Example usage:
pluvial_data = {
    "godine": 33,
    "P0_r95p_periodmean": data.loc["r95p_periodmean", "P0"],
    "P0_cwd_periodmean": data.loc["cwd_periodmean", "P0"],
    "godina_pocetak": 2024,
    "godina_kraj": 2100,
    "P1_r95p_periodmean": data.loc["r95p_periodmean", "P1"],
    "P2_r95p_periodmean": data.loc["r95p_periodmean", "P2"],
    "P1_cwd_periodmean": data.loc["cwd_periodmean", "P1"],
    "P2_cwd_periodmean": data.loc["cwd_periodmean", "P2"],
    "geomorphon": "ravnica",
    "vjerojatnost_obilne_oborine": "srednja"
}

pluvial_description = generate_pluvial_description(pluvial_data)

def generate_heat_wave_description(data):
    text_template = (
        "Broj dana s minimalnim temperaturama zraka iznad 20 °C bitno je razmotriti u ovoj procjeni zato što on utječe na zdravlje. "
        "U protekle {godine:.0f} godine u prosjeku ih je godišnje bilo {P0_tr:.2f}, a pokazalo se da će u budućnosti, "
        "između {godina_pocetak:.0f}. i {godina_kraj:.0f}. g. ovaj broj narasti do čak {P1_tr:.2f} dana u godini za razdoblje P1. "
        "Za razdoblje P2 taj će broj dana iznositi {P2_tr:.2f}. "
        "Broj dana sa temperaturom iznad 30 °C dosad je u prosjeku bio {P0_SU30:.2f} dana u godini i očekuje se značajan porast, "
        "odnosno trebao bi u budućnosti iznositi {P1_SU30:.2f} dana u godini za P1 razdoblje, a {P2_SU30:.2f} za P2 razdoblje. "
        "Razmatrana je i prividna temperatura, odnosno osjet temperature koju doživljava čovjek s obzirom na temperaturu i vlagu zraka. "
        "Njena maksimalna godišnja vrijednost je dosad u prosjeku bila {P0_hi_max:.2f} °C, a u budućnosti se može očekivati "
        "porast na {P1_hi_max:.2f} °C u prosjeku za P1 razdoblje, te na prosječnih {P2_hi_max:.2f} °C za P2 razdoblje. "
        "Također, radi se o urbanom krajoliku bez visoke vegetacije koja obično pruža zaštitu od izrazito visokih temperatura zraka tijekom vrućih dana. "
        "Iz danih rezultata zaključuje se da je lokacija dosad pripadala u {vjerojatnost_postojeća} kategoriju izloženosti toplinskim valovima, međutim u budućnosti "
        "se očekuje porast temperatura zraka i otežani uvjeti pri čemu je za ovu lokaciju procijenjena {vjerojatnost_toplval} vjerojatnost toplinskih valova u budućnosti."
    )
    return text_template.format(**data)

# Example usage:
heat_wave_data = {
    "godine": 33,
    "P0_tr": data.loc["tr_periodmean", "P0"],
    "godina_pocetak": 2024,
    "godina_kraj": 2100,
    "P1_tr": data.loc["tr_periodmean", "P1"],
    "P2_tr": data.loc["tr_periodmean", "P2"],
    "P0_SU30": data.loc["su30_periodmean", "P0"],
    "P1_SU30": data.loc["su30_periodmean", "P1"],
    "P2_SU30": data.loc["su30_periodmean", "P2"],
    "P0_hi_max": data.loc["hi_max_periodmean", "P0"],
    "P1_hi_max": data.loc["hi_max_periodmean", "P1"],
    "P2_hi_max": data.loc["hi_max_periodmean", "P2"],
    "vjerojatnost_postojeća": "srednju",
    "vjerojatnost_toplval": "i dalje srednja"
}

heat_wave_description = generate_heat_wave_description(heat_wave_data)

def generate_wildfire_description(data):
    text_template = (
        "Prosječna vrijednost maksimalnih godišnjih vrijednosti požarnog indeksa (eng. Fire Weather Index) je u posljednje {godine:.0f} godine "
        "za ovu lokaciju iznosila {P0_fwi_max_periodmean:.2f}, a očekuje se da će u razdoblju između {godina_pocetak:.0f}. i {godina_kraj:.0f}. "
        "prosječna vrijednost maksimalnih godišnjih vrijednosti ovog požarnog indeksa porasti na {P1_fwi_max_periodmean:.2f} "
        "za P1 razdoblje, a bit će {P2_fwi_max_periodmean:.2f} za P2 razdoblje. "
        "Dana lokacija ne nalazi se u blizini šume (udaljenost je veća od {udaljenost_suma:.0f} m) te se nalazi u urbanom krajoliku, "
        "pa je za ovu lokaciju procijenjena {vjerojatnost_pozari} vjerojatnost šumskih požara."
    )
    return text_template.format(**data)

# Example usage:
wildfire_data = {
    "godine": 33,
    "P0_fwi_max_periodmean": data.loc["fwi_max_periodmean", "P0"],
    "godina_pocetak": 2024,
    "godina_kraj": 2100,
    "P1_fwi_max_periodmean": data.loc["fwi_max_periodmean", "P1"],
    "P2_fwi_max_periodmean": data.loc["fwi_max_periodmean", "P2"],
    "udaljenost_suma": 4000,
    "vjerojatnost_pozari": "mala"
}
wildfire_description = generate_wildfire_description(wildfire_data)

def generate_severe_wind_description(data):
    text_template = (
        "U protekle {godine:.0f} godine je u prosjeku godišnje bilo {P0_fg10_172_periodmean:.2f} dana s olujnim (ili jačim) udarima vjetra, "
        "a pokazalo se da bi u budućnosti, u razdoblju između {godina_pocetak:.0f}. i {godina_kraj:.0f}. moglo biti u prosjeku {P1_fg10_172_periodmean:.2f} dana "
        "za P1 razdoblje te u prosjeku {P2_fg10_172_periodmean:.2f} dana za P2 razdoblje. "
        "Ovo su {kat_vrijednost} vrijednosti, a lokacija se nalazi u {geomorphon}, ali u neposrednom okruženju nema stabala ni struktura koje bi mogle popustiti pod utjecajem vjetra "
        "i dovesti do oštećenja pa je prema tome za ovu lokaciju procijenjena umjerena vjerojatnost olujnih udara vjetra."
    )
    return text_template.format(**data)

# Example usage:
severe_wind_data = {
    "godine": 33,
    "P0_fg10_172_periodmean": data.loc["fg10_172_periodmean", "P0"],
    "godina_pocetak": 2024,
    "godina_kraj": 2100,
    "P1_fg10_172_periodmean": data.loc["fg10_172_periodmean", "P1"],
    "P2_fg10_172_periodmean": data.loc["fg10_172_periodmean", "P2"],
    "kat_vrijednost": "niske",
    "geomorphon": "ravnici"
}

severe_wind_description = generate_severe_wind_description(severe_wind_data)

result_text = location_info + "\n\n\n" + drought_description + pluvial_description + heat_wave_description + wildfire_description + "\n\n\n" + severe_wind_description