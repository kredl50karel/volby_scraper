"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Karel kredl
email: k.kredl@centrum.cz
discord: Karel K.#2080
"""

# import modulu

import requests
import csv
from bs4 import BeautifulSoup as bs

# hlavni fce, uvod

def main():
    print(""""
    Vitejte v SW pro ziskani vysledku voleb,
    vyberte oblast na: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ  
    vyberte region a zkopirujte jej
    """)
    oddelovac = (45 * "-")
    print(oddelovac)
    link = region_odkaz()
    file_name = nazev_souboru()
    soup = parser_data(link)
    data_list = data_to_list(soup)
    with open(file_name + ".csv", "w", newline="") as file:
        hlavicka = data_list[0].keys()
        zapisovac = csv.DictWriter(file, fieldnames=hlavicka)
        zapisovac.writeheader()
        zapisovac.writerows(data_list)

# zadani odkazu

def region_odkaz():
    odkaz = input("Zadejte zkopirovany odkaz: ").strip()
    if "https://volby.cz/pls/ps2017nss/" in odkaz and "&xnumnuts=" in odkaz:
        return odkaz
    else:
        print("Neplatny odkaz, zkuste prosim znovu.")
        exit()

def nazev_souboru():

    nazev = input(
    """
    Zadejte nazev souboru bez pripony: 
    """
    )
    if "csv" and "." not in nazev:
        print("Pripravuje se: ")
        return nazev
    else:
        print("Neplatny nazev souboru.")
        exit()

# parsovani html

def parser_data(odkaz):
    stranka = requests.get(odkaz)
    stranka = bs(stranka.text, "html.parser")
    return stranka

# hledani html znaku

def hlavicka_tabulky(tr):
    tdznak = tr.find_all("td")
    cislo = tdznak[0].getText()
    oblast = tdznak[1].getText()
    link = tdznak[0].find("a").get("href")
    return cislo, oblast, link

# hlavicka data

def slovnik(hlavicka):
    cislo, oblast, link = hlavicka
    datovy_odkaz = "https://volby.cz/pls/ps2017nss/" + link
    soup = parser_data(datovy_odkaz)
    tab = soup.find_all("table")
    bunka = tab[0].find_all("td")
    do_slovnik = {
                 "kod_obce": cislo,
                 "nazev_obce": oblast,
                 "volici_v_seznamu": bunka[3].getText(),
                 "vydane_obalky": bunka[6].getText(),
                 "platne_hlasy": bunka[7].getText()
                  }

    for tabulka in tab[1:]:
        trznak = tabulka.find_all("tr")
        for tr in trznak[2:-1]:
            tdznak = tr.find_all("td")
            strana = tdznak[1].getText()
            hlasy_celkem = tdznak[2].getText()
            do_slovnik[strana] = hlasy_celkem
    return do_slovnik

# zpracovani obsahu

def data_to_list(obsah):
    okresy = obsah.find_all("div", {"class": "t3"})
    data_list = []
    for table in okresy:
        radky = table.find_all("tr")
        for radek in radky[2:]:
            data_list.append(slovnik(hlavicka_tabulky(radek)))
        return data_list

if __name__ == '__main__':
    main()