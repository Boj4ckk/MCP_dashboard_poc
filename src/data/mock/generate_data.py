#!/usr/bin/env python3
"""
Patissier Electronics - Mock OLAP Data Generator
Generates realistic CSV data for a large French electronics retail company.
3 years of data (2022-2024), ~500K fact_sales rows, full star schema.
"""

import csv
import random
import os
from datetime import date, timedelta

random.seed(42)

OUTPUT_DIR = "data/csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)

START_DATE = date(2022, 1, 1)
END_DATE   = date(2024, 12, 31)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def write_csv(filename, rows, fieldnames):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {filename:<45} {len(rows):>10,} rows")


# ---------------------------------------------------------------------------
# DIM_DATE
# ---------------------------------------------------------------------------

def generate_dim_date():
    rows = []
    date_map = {}
    current = START_DATE
    date_id = 1
    while current <= END_DATE:
        rows.append({
            "date_id":     date_id,
            "full_date":   current.isoformat(),
            "day":         current.day,
            "week":        current.isocalendar()[1],
            "month":       current.month,
            "quarter":     (current.month - 1) // 3 + 1,
            "year":        current.year,
            "day_of_week": current.weekday(),   # 0=lundi … 6=dimanche
            "is_weekend":  1 if current.weekday() >= 5 else 0,
        })
        date_map[current.isoformat()] = date_id
        current += timedelta(days=1)
        date_id += 1
    write_csv("dim_date.csv", rows, list(rows[0].keys()))
    return date_map


# ---------------------------------------------------------------------------
# DIM_CHANNEL
# ---------------------------------------------------------------------------

def generate_dim_channel():
    rows = [
        {"channel_id": 1, "channel_name": "online",      "channel_type": "digital"},
        {"channel_id": 2, "channel_name": "in_store",    "channel_type": "physical"},
        {"channel_id": 3, "channel_name": "marketplace", "channel_type": "digital"},
        {"channel_id": 4, "channel_name": "partner",     "channel_type": "digital"},
    ]
    write_csv("dim_channel.csv", rows, list(rows[0].keys()))
    return rows


# ---------------------------------------------------------------------------
# DIM_WAREHOUSE
# ---------------------------------------------------------------------------

def generate_dim_warehouse():
    rows = [
        {"warehouse_id": 1, "warehouse_name": "Entrepôt Paris Nord",   "city": "Saint-Denis",  "region": "Île-de-France",          "country": "France"},
        {"warehouse_id": 2, "warehouse_name": "Entrepôt Lyon Sud",     "city": "Vénissieux",   "region": "Auvergne-Rhône-Alpes",   "country": "France"},
        {"warehouse_id": 3, "warehouse_name": "Entrepôt Bordeaux",     "city": "Mérignac",     "region": "Nouvelle-Aquitaine",     "country": "France"},
    ]
    write_csv("dim_warehouse.csv", rows, list(rows[0].keys()))
    return rows


# ---------------------------------------------------------------------------
# DIM_STORE  (30 magasins)
# ---------------------------------------------------------------------------

_STORES_RAW = [
    # (nom, ville, région, type, opening_date)
    ("Patissier Paris Opéra",           "Paris",                "Île-de-France",                    "flagship", "2015-03-01"),
    ("Patissier Paris La Défense",      "Paris",                "Île-de-France",                    "flagship", "2016-09-15"),
    ("Patissier Paris République",      "Paris",                "Île-de-France",                    "standard", "2017-04-01"),
    ("Patissier Boulogne-Billancourt",  "Boulogne-Billancourt", "Île-de-France",                    "standard", "2018-01-10"),
    ("Patissier Versailles",            "Versailles",           "Île-de-France",                    "standard", "2019-06-01"),
    ("Patissier Lyon Part-Dieu",        "Lyon",                 "Auvergne-Rhône-Alpes",             "flagship", "2014-11-01"),
    ("Patissier Lyon Confluence",       "Lyon",                 "Auvergne-Rhône-Alpes",             "standard", "2018-03-15"),
    ("Patissier Villeurbanne",          "Villeurbanne",         "Auvergne-Rhône-Alpes",             "standard", "2020-02-01"),
    ("Patissier Marseille Centre",      "Marseille",            "Provence-Alpes-Côte d'Azur",       "flagship", "2015-06-01"),
    ("Patissier Marseille La Valentine","Marseille",            "Provence-Alpes-Côte d'Azur",       "standard", "2019-09-01"),
    ("Patissier Toulouse Capitole",     "Toulouse",             "Occitanie",                        "flagship", "2016-01-15"),
    ("Patissier Toulouse Blagnac",      "Blagnac",              "Occitanie",                        "standard", "2020-10-01"),
    ("Patissier Bordeaux Mériadeck",    "Bordeaux",             "Nouvelle-Aquitaine",               "flagship", "2016-05-01"),
    ("Patissier Bordeaux Lac",          "Bordeaux",             "Nouvelle-Aquitaine",               "standard", "2021-01-15"),
    ("Patissier Lille Grand Place",     "Lille",                "Hauts-de-France",                  "flagship", "2015-09-01"),
    ("Patissier Villeneuve-d'Ascq",     "Villeneuve-d'Ascq",   "Hauts-de-France",                  "standard", "2019-03-01"),
    ("Patissier Nantes Centre",         "Nantes",               "Pays de la Loire",                 "flagship", "2017-02-01"),
    ("Patissier Saint-Herblain",        "Saint-Herblain",       "Pays de la Loire",                 "standard", "2020-11-01"),
    ("Patissier Strasbourg",            "Strasbourg",           "Grand Est",                        "standard", "2018-08-01"),
    ("Patissier Montpellier Polygone",  "Montpellier",          "Occitanie",                        "standard", "2019-01-15"),
    ("Patissier Nice Étoile",           "Nice",                 "Provence-Alpes-Côte d'Azur",       "standard", "2017-11-01"),
    ("Patissier Rennes Centre",         "Rennes",               "Bretagne",                         "standard", "2020-03-01"),
    ("Patissier Grenoble Grand Place",  "Grenoble",             "Auvergne-Rhône-Alpes",             "standard", "2018-06-15"),
    ("Patissier Rouen Saint-Sever",     "Rouen",                "Normandie",                        "standard", "2019-04-01"),
    ("Patissier Tours",                 "Tours",                "Centre-Val de Loire",              "standard", "2021-03-01"),
    ("Patissier Clermont-Ferrand",      "Clermont-Ferrand",     "Auvergne-Rhône-Alpes",             "standard", "2020-07-01"),
    ("Patissier Dijon",                 "Dijon",                "Bourgogne-Franche-Comté",          "standard", "2021-06-01"),
    ("Patissier Reims",                 "Reims",                "Grand Est",                        "standard", "2021-09-15"),
    ("Patissier Outlet Serris",         "Serris",               "Île-de-France",                    "outlet",   "2017-09-01"),
    ("Patissier Outlet Troyes",         "Troyes",               "Grand Est",                        "outlet",   "2019-11-01"),
]


def generate_dim_store():
    rows = [
        {
            "store_id":     i,
            "store_name":   name,
            "city":         city,
            "region":       region,
            "country":      "France",
            "store_type":   stype,
            "opening_date": opening,
        }
        for i, (name, city, region, stype, opening) in enumerate(_STORES_RAW, 1)
    ]
    write_csv("dim_store.csv", rows, list(rows[0].keys()))
    return rows


# ---------------------------------------------------------------------------
# DIM_PRODUCT  (~100 références réalistes)
# ---------------------------------------------------------------------------

_PRODUCTS_RAW = [
    # (product_name, brand, category, subcategory, price, cost)
    # --- TV & Displays ---
    ("Samsung QLED QE55Q80C",           "Samsung",       "TV & Displays", "QLED TV",      1299.00,  850.00),
    ("Samsung OLED S95C 65\"",          "Samsung",       "TV & Displays", "OLED TV",      2499.00, 1650.00),
    ("Samsung Crystal UHD 50\"",        "Samsung",       "TV & Displays", "LED TV",        499.00,  310.00),
    ("Samsung Crystal UHD 43\"",        "Samsung",       "TV & Displays", "LED TV",        349.00,  215.00),
    ("LG OLED C3 55\"",                 "LG",            "TV & Displays", "OLED TV",      1499.00,  990.00),
    ("LG OLED C3 65\"",                 "LG",            "TV & Displays", "OLED TV",      2199.00, 1450.00),
    ("LG NanoCell 50\"",                "LG",            "TV & Displays", "LED TV",        599.00,  380.00),
    ("Sony Bravia XR A80L 55\"",        "Sony",          "TV & Displays", "OLED TV",      1799.00, 1190.00),
    ("Sony Bravia X90L 65\"",           "Sony",          "TV & Displays", "LED TV",       1299.00,  860.00),
    ("Philips OLED+908 65\"",           "Philips",       "TV & Displays", "OLED TV",      2799.00, 1850.00),
    ("Philips PUS8518 50\"",            "Philips",       "TV & Displays", "LED TV",        449.00,  275.00),
    ("Hisense U8K 65\"",                "Hisense",       "TV & Displays", "QLED TV",       899.00,  560.00),
    ("Hisense A6K 43\"",                "Hisense",       "TV & Displays", "LED TV",        349.00,  215.00),
    ("TCL C845 55\"",                   "TCL",           "TV & Displays", "QLED TV",       749.00,  465.00),
    ("TCL S5400A 40\"",                 "TCL",           "TV & Displays", "LED TV",        299.00,  185.00),
    ("Samsung Odyssey G7 27\"",         "Samsung",       "TV & Displays", "Monitor",       449.00,  280.00),
    ("LG UltraGear 27GR95QE",           "LG",            "TV & Displays", "Monitor",       699.00,  440.00),
    ("Dell UltraSharp U2723QE",         "Dell",          "TV & Displays", "Monitor",       599.00,  380.00),
    ("BenQ EW2880U",                    "BenQ",          "TV & Displays", "Monitor",       399.00,  250.00),
    # --- Audio & Home Entertainment ---
    ("Sony WH-1000XM5",                 "Sony",          "Audio & Home Entertainment", "Headphones",  349.00, 195.00),
    ("Bose QuietComfort 45",            "Bose",          "Audio & Home Entertainment", "Headphones",  329.00, 185.00),
    ("Sennheiser Momentum 4",           "Sennheiser",    "Audio & Home Entertainment", "Headphones",  299.00, 165.00),
    ("Audio-Technica ATH-M50xBT2",      "Audio-Technica","Audio & Home Entertainment", "Headphones",  179.00,  95.00),
    ("Apple AirPods Pro 2",             "Apple",         "Audio & Home Entertainment", "Earbuds",     279.00, 155.00),
    ("Samsung Galaxy Buds2 Pro",        "Samsung",       "Audio & Home Entertainment", "Earbuds",     199.00, 110.00),
    ("JBL Charge 5",                    "JBL",           "Audio & Home Entertainment", "Speaker",     179.00,  95.00),
    ("Bose SoundLink Flex",             "Bose",          "Audio & Home Entertainment", "Speaker",     149.00,  82.00),
    ("Sonos Era 100",                   "Sonos",         "Audio & Home Entertainment", "Speaker",     249.00, 140.00),
    ("Sonos Arc",                       "Sonos",         "Audio & Home Entertainment", "Soundbar",    999.00, 600.00),
    ("Samsung HW-Q990C",                "Samsung",       "Audio & Home Entertainment", "Soundbar",   1299.00, 800.00),
    ("LG S95QR",                        "LG",            "Audio & Home Entertainment", "Soundbar",   1099.00, 680.00),
    ("Bose Smart Soundbar 900",         "Bose",          "Audio & Home Entertainment", "Soundbar",    899.00, 540.00),
    ("Sony HT-A5000",                   "Sony",          "Audio & Home Entertainment", "Soundbar",    799.00, 480.00),
    ("JBL Bar 1000",                    "JBL",           "Audio & Home Entertainment", "Soundbar",    999.00, 620.00),
    ("Pioneer VSX-935",                 "Pioneer",       "Audio & Home Entertainment", "AV Receiver", 699.00, 420.00),
    ("Yamaha RX-V6A",                   "Yamaha",        "Audio & Home Entertainment", "AV Receiver", 599.00, 360.00),
    # --- Home Appliances ---
    ("Samsung WW90T684DLH",             "Samsung",  "Home Appliances", "Washing Machine",   799.00,  510.00),
    ("Bosch WAJ28002FF",                "Bosch",    "Home Appliances", "Washing Machine",   699.00,  445.00),
    ("Miele WCG660",                    "Miele",    "Home Appliances", "Washing Machine",  1399.00,  880.00),
    ("LG F4V910WTSE",                   "LG",       "Home Appliances", "Washing Machine",   749.00,  475.00),
    ("Whirlpool FWF91496",              "Whirlpool","Home Appliances", "Washing Machine",   549.00,  345.00),
    ("Samsung RS67A8811B1",             "Samsung",  "Home Appliances", "Refrigerator",     1199.00,  760.00),
    ("LG GSX961NSAZ",                   "LG",       "Home Appliances", "Refrigerator",     1499.00,  950.00),
    ("Bosch KGN56XLEA",                 "Bosch",    "Home Appliances", "Refrigerator",      899.00,  570.00),
    ("Whirlpool WQ9 E2L",               "Whirlpool","Home Appliances", "Refrigerator",      799.00,  505.00),
    ("Samsung BF641FST",                "Samsung",  "Home Appliances", "Oven",              499.00,  315.00),
    ("Bosch HBA171ES3F",                "Bosch",    "Home Appliances", "Oven",              599.00,  380.00),
    ("De Longhi ECAM290.61.SB",         "De Longhi","Home Appliances", "Coffee Machine",    699.00,  430.00),
    ("Philips EP3347/90",               "Philips",  "Home Appliances", "Coffee Machine",    499.00,  305.00),
    ("Dyson V15 Detect",                "Dyson",    "Home Appliances", "Vacuum Cleaner",    749.00,  470.00),
    ("Dyson V12 Detect Slim",           "Dyson",    "Home Appliances", "Vacuum Cleaner",    599.00,  375.00),
    ("Rowenta RO9682EA",                "Rowenta",  "Home Appliances", "Vacuum Cleaner",    349.00,  215.00),
    ("Seb DO821800",                    "Seb",      "Home Appliances", "Air Fryer",         149.00,   88.00),
    ("Moulinex EZ602D10",               "Moulinex", "Home Appliances", "Air Fryer",          99.00,   58.00),
    # --- Computing ---
    ("Apple MacBook Air M2 13\"",       "Apple",   "Computing", "Laptop",      1499.00,  980.00),
    ("Apple MacBook Pro M3 14\"",       "Apple",   "Computing", "Laptop",      2199.00, 1440.00),
    ("Dell XPS 15 9530",                "Dell",    "Computing", "Laptop",      1999.00, 1310.00),
    ("HP Spectre x360 14\"",            "HP",      "Computing", "Laptop",      1699.00, 1110.00),
    ("Lenovo ThinkPad X1 Carbon",       "Lenovo",  "Computing", "Laptop",      1799.00, 1175.00),
    ("Asus ZenBook 14X OLED",           "Asus",    "Computing", "Laptop",      1199.00,  780.00),
    ("Acer Swift X 14",                 "Acer",    "Computing", "Laptop",       999.00,  650.00),
    ("MSI Prestige 15",                 "MSI",     "Computing", "Laptop",      1299.00,  845.00),
    ("Samsung Galaxy Book3 Pro",        "Samsung", "Computing", "Laptop",      1599.00, 1045.00),
    ("Apple Mac Mini M2",               "Apple",   "Computing", "Desktop",      699.00,  455.00),
    ("Apple iMac 24\" M3",              "Apple",   "Computing", "Desktop",     1599.00, 1045.00),
    ("Dell OptiPlex 7010",              "Dell",    "Computing", "Desktop",      899.00,  585.00),
    ("HP EliteDesk 800 G9",             "HP",      "Computing", "Desktop",      999.00,  650.00),
    ("Logitech MX Master 3S",           "Logitech","Computing", "Accessories",  109.00,   58.00),
    ("Logitech MX Keys S",              "Logitech","Computing", "Accessories",  129.00,   68.00),
    ("Apple Magic Keyboard",            "Apple",   "Computing", "Accessories",  129.00,   70.00),
    ("Seagate Backup Plus 2TB",         "Seagate", "Computing", "Storage",       79.00,   42.00),
    ("Samsung SSD T7 1TB",              "Samsung", "Computing", "Storage",      129.00,   68.00),
    ("WD My Passport 4TB",              "WD",      "Computing", "Storage",      109.00,   58.00),
    ("HP LaserJet Pro M404n",           "HP",      "Computing", "Printer",      299.00,  185.00),
    ("Epson EcoTank ET-4850",           "Epson",   "Computing", "Printer",      349.00,  215.00),
    # --- Mobile & Connected Devices ---
    ("Apple iPhone 15 Pro 256GB",       "Apple",   "Mobile & Connected Devices", "Smartphone", 1329.00,  870.00),
    ("Apple iPhone 15 128GB",           "Apple",   "Mobile & Connected Devices", "Smartphone", 1029.00,  675.00),
    ("Samsung Galaxy S24 Ultra",        "Samsung", "Mobile & Connected Devices", "Smartphone", 1349.00,  885.00),
    ("Samsung Galaxy S24",              "Samsung", "Mobile & Connected Devices", "Smartphone",  899.00,  590.00),
    ("Google Pixel 8 Pro",              "Google",  "Mobile & Connected Devices", "Smartphone", 1099.00,  720.00),
    ("Google Pixel 8",                  "Google",  "Mobile & Connected Devices", "Smartphone",  799.00,  525.00),
    ("Xiaomi 13T Pro",                  "Xiaomi",  "Mobile & Connected Devices", "Smartphone",  849.00,  555.00),
    ("Xiaomi Redmi Note 13 Pro",        "Xiaomi",  "Mobile & Connected Devices", "Smartphone",  399.00,  250.00),
    ("OnePlus 12",                      "OnePlus", "Mobile & Connected Devices", "Smartphone",  899.00,  590.00),
    ("Apple Watch Series 9",            "Apple",   "Mobile & Connected Devices", "Wearable",    449.00,  295.00),
    ("Apple Watch Ultra 2",             "Apple",   "Mobile & Connected Devices", "Wearable",    899.00,  590.00),
    ("Samsung Galaxy Watch6",           "Samsung", "Mobile & Connected Devices", "Wearable",    299.00,  185.00),
    ("Garmin Fenix 7",                  "Garmin",  "Mobile & Connected Devices", "Wearable",    699.00,  455.00),
    ("Fitbit Sense 2",                  "Fitbit",  "Mobile & Connected Devices", "Wearable",    249.00,  150.00),
    ("Samsung Galaxy Tab S9",           "Samsung", "Mobile & Connected Devices", "Tablet",      849.00,  555.00),
    ("Apple iPad Air 5th Gen",          "Apple",   "Mobile & Connected Devices", "Tablet",      819.00,  535.00),
    ("Apple iPad Pro 12.9\" M2",        "Apple",   "Mobile & Connected Devices", "Tablet",     1219.00,  800.00),
    ("Amazon Echo Dot 5th Gen",         "Amazon",  "Mobile & Connected Devices", "Smart Home",   59.00,   32.00),
    ("Google Nest Hub 2nd Gen",         "Google",  "Mobile & Connected Devices", "Smart Home",   99.00,   55.00),
    ("Philips Hue Starter Kit",         "Philips", "Mobile & Connected Devices", "Smart Home",  149.00,   82.00),
    ("Ring Video Doorbell 4",           "Ring",    "Mobile & Connected Devices", "Smart Home",  199.00,  115.00),
    ("TP-Link Archer AX6000",           "TP-Link", "Mobile & Connected Devices", "Networking",  299.00,  180.00),
    ("Netgear Nighthawk RAX50",         "Netgear", "Mobile & Connected Devices", "Networking",  249.00,  150.00),
]


def generate_dim_product():
    rows = []
    for i, (name, brand, cat, subcat, price, cost) in enumerate(_PRODUCTS_RAW, 1):
        # Quelques produits discontinués (réaliste : ~8% du catalogue)
        status = "discontinued" if random.random() < 0.08 else "active"
        rows.append({
            "product_id":       i,
            "product_name":     name,
            "brand":            brand,
            "category":         cat,
            "subcategory":      subcat,
            "price":            price,
            "cost":             cost,
            "lifecycle_status": status,
        })
    write_csv("dim_product.csv", rows, list(rows[0].keys()))
    return rows


# ---------------------------------------------------------------------------
# DIM_CUSTOMER  (50 000 clients)
# ---------------------------------------------------------------------------

_FIRST_NAMES_M = [
    "Jean","Pierre","Michel","Philippe","Nicolas","Christophe","Julien","Thomas",
    "Alexandre","Olivier","François","Antoine","Stéphane","Laurent","Sébastien",
    "Mathieu","David","Guillaume","Éric","Patrick","Marc","Cédric","Frédéric",
    "Benoît","Xavier","Rémi","Lucas","Hugo","Théo","Nathan","Maxime","Romain",
    "Louis","Clément","Léo","Gabriel","Arthur","Adam","Raphaël","Alexis",
    "Kevin","Florian","Baptiste","Mohamed","Youssef","Karim","Mehdi","Adrien","Quentin",
]
_FIRST_NAMES_F = [
    "Marie","Nathalie","Isabelle","Sophie","Céline","Sandrine","Valérie","Stéphanie",
    "Christine","Florence","Julie","Emilie","Aurélie","Claire","Sarah","Laura",
    "Camille","Emma","Léa","Chloé","Inès","Jade","Manon","Lucie","Alice",
    "Charlotte","Anaïs","Pauline","Marine","Amandine","Margot","Zoé","Océane",
    "Maëlle","Justine","Amélie","Laure","Eva","Yasmine","Fatima","Amira",
    "Nadia","Soraya","Mathilde","Axelle","Elise","Elisa",
]
_LAST_NAMES = [
    "Martin","Bernard","Thomas","Petit","Robert","Richard","Durand","Dubois",
    "Moreau","Laurent","Simon","Michel","Lefebvre","Leroy","Roux","David",
    "Bertrand","Morel","Fournier","Girard","Bonnet","Dupont","Lambert",
    "Fontaine","Rousseau","Vincent","Lefevre","Faure","Andre","Mercier",
    "Blanc","Guerin","Boyer","Garnier","Chevalier","François","Legrand",
    "Gauthier","Garcia","Perrin","Robin","Clement","Morin","Nicolas","Henry",
    "Roussel","Mathieu","Gautier","Masson","Marchand",
    "Benali","Meziane","Boudjema","Rezki","Hamid",
]
_CITIES = [
    ("Paris","Île-de-France"),("Lyon","Auvergne-Rhône-Alpes"),
    ("Marseille","Provence-Alpes-Côte d'Azur"),("Toulouse","Occitanie"),
    ("Bordeaux","Nouvelle-Aquitaine"),("Lille","Hauts-de-France"),
    ("Nantes","Pays de la Loire"),("Strasbourg","Grand Est"),
    ("Montpellier","Occitanie"),("Nice","Provence-Alpes-Côte d'Azur"),
    ("Rennes","Bretagne"),("Grenoble","Auvergne-Rhône-Alpes"),
    ("Rouen","Normandie"),("Toulon","Provence-Alpes-Côte d'Azur"),
    ("Saint-Étienne","Auvergne-Rhône-Alpes"),("Le Havre","Normandie"),
    ("Dijon","Bourgogne-Franche-Comté"),("Angers","Pays de la Loire"),
    ("Reims","Grand Est"),("Brest","Bretagne"),
    ("Clermont-Ferrand","Auvergne-Rhône-Alpes"),("Amiens","Hauts-de-France"),
    ("Perpignan","Occitanie"),("Metz","Grand Est"),
    ("Orléans","Centre-Val de Loire"),("Tours","Centre-Val de Loire"),
    ("Caen","Normandie"),("Besançon","Bourgogne-Franche-Comté"),
]
_EMAIL_DOMAINS = ["gmail.com","yahoo.fr","hotmail.fr","orange.fr","free.fr","sfr.fr","laposte.net"]
_EMAIL_DOMAIN_W = [0.40, 0.18, 0.14, 0.12, 0.08, 0.05, 0.03]
_ACQ_CHANNELS = ["organic_search","paid_search","social_media","email","direct","referral","marketplace","in_store"]
_ACQ_W        = [0.22, 0.18, 0.15, 0.12, 0.15, 0.08, 0.06, 0.04]

_REG_START = date(2019, 1, 1)
_REG_DAYS  = (END_DATE - _REG_START).days


def _normalize(s: str) -> str:
    return (s.lower()
              .replace("é","e").replace("è","e").replace("ê","e").replace("ë","e")
              .replace("à","a").replace("â","a").replace("î","i").replace("ï","i")
              .replace("ô","o").replace("ù","u").replace("û","u").replace("ü","u")
              .replace("ç","c").replace(" ",".").replace("'","."))


def generate_dim_customer(n: int = 50_000):
    all_first = [(fn, "M") for fn in _FIRST_NAMES_M] + [(fn, "F") for fn in _FIRST_NAMES_F]
    rows = []
    for i in range(1, n + 1):
        first, _ = random.choice(all_first)
        last      = random.choice(_LAST_NAMES)
        city, _   = random.choice(_CITIES)
        country   = "France" if random.random() > 0.05 else random.choice(["Belgique","Suisse","Luxembourg","Monaco"])
        r = random.random()
        segment   = "VIP" if r > 0.90 else ("returning" if r > 0.55 else "new")
        reg_date  = (_REG_START + timedelta(days=random.randint(0, _REG_DAYS))).isoformat()
        domain    = random.choices(_EMAIL_DOMAINS, weights=_EMAIL_DOMAIN_W)[0]
        email     = f"{_normalize(first)}.{_normalize(last)}{i}@{domain}"
        acq       = random.choices(_ACQ_CHANNELS, weights=_ACQ_W)[0]
        rows.append({
            "customer_id":        i,
            "first_name":         first,
            "last_name":          last,
            "email":              email,
            "country":            country,
            "city":               city,
            "segment":            segment,
            "acquisition_channel":acq,
            "registration_date":  reg_date,
        })
    write_csv("dim_customer.csv", rows, list(rows[0].keys()))
    return rows


# ---------------------------------------------------------------------------
# SAISONNALITÉ (multiplicateur journalier)
# ---------------------------------------------------------------------------

def _black_friday(year: int) -> date:
    """Dernier vendredi de novembre."""
    d = date(year, 11, 30)
    while d.weekday() != 4:
        d -= timedelta(days=1)
    return d


def get_daily_multiplier(d: date) -> float:
    m, day, dow = d.month, d.day, d.weekday()
    base = {1:0.75, 2:0.65, 3:0.72, 4:0.78,
            5:0.82, 6:0.85, 7:0.80, 8:0.62,
            9:0.90,10:0.88,11:1.40,12:1.85}[m]

    if m == 1 and day <= 15:   base = 1.25   # Soldes d'hiver
    if m == 7 and day <= 15:   base = 1.10   # Soldes d'été
    if m == 8:                  base = 0.62   # Creux estival

    bf = _black_friday(d.year)
    if d == bf:                                base = 4.80   # Black Friday jour J
    elif 0 < (bf - d).days <= 6:              base = 2.10   # Semaine Black Friday

    if m == 12 and day >= 18:  base = 2.90   # Semaine de Noël
    if m == 12 and day >= 26:  base = 1.60   # Après Noël (soldes anticipées)

    if dow >= 5:               base *= 1.15  # Boost week-end

    return base


# ---------------------------------------------------------------------------
# FACT TABLES
# ---------------------------------------------------------------------------

_CHANNEL_IDS = [1, 2, 3, 4]
_CHANNEL_W   = [0.55, 0.35, 0.08, 0.02]
_CHANNEL_NAMES = {1:"online", 2:"in_store", 3:"marketplace", 4:"partner"}

_BASE_DAILY_ORDERS = 185   # ~200K orders/3 ans → ~500K lignes fact_sales

_RETURN_REASONS = ["defective_product","wrong_item","not_as_described",
                   "changed_mind","delivery_issue","compatibility_issue"]
_RETURN_REASON_W = [0.25, 0.10, 0.20, 0.20, 0.15, 0.10]

_ISSUE_TYPES = ["technical_issue","delivery_problem","return_request",
                "billing_issue","product_inquiry","warranty_claim"]
_ISSUE_W     = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

_RESOLUTION_HOURS = [2, 4, 8, 24, 48, 72, 120, 168]
_RESOLUTION_W     = [0.10,0.15,0.20,0.25,0.15,0.08,0.05,0.02]


def generate_fact_tables(date_map, products, stores, n_customers=50_000):
    sales_rows   = []
    orders_rows  = []
    returns_rows = []
    tickets_rows = []

    sale_id   = 1
    return_id = 1
    ticket_id = 1

    instore_ids = [s["store_id"] for s in stores if s["store_type"] != "outlet"]

    # Popularité produit — effet Pareto (20% des refs = 80% des ventes)
    product_weights = []
    for p in products:
        w = {"Mobile & Connected Devices": 2.6, "Computing": 2.4,
             "TV & Displays": 1.8, "Audio & Home Entertainment": 1.5,
             "Home Appliances": 1.0}.get(p["category"], 1.0)
        w *= random.uniform(0.4, 2.2)
        product_weights.append(w)

    prod_list = list(range(len(products)))

    for date_str in sorted(date_map):
        d       = date(int(date_str[:4]), int(date_str[5:7]), int(date_str[8:]))
        date_id = date_map[date_str]
        mult    = get_daily_multiplier(d)
        n_orders = max(1, int(_BASE_DAILY_ORDERS * mult * random.uniform(0.85, 1.15)))

        for _ in range(n_orders):
            order_id   = f"ORD-{date_str.replace('-','')}-{random.randint(10000,99999)}"
            channel_id = random.choices(_CHANNEL_IDS, weights=_CHANNEL_W)[0]
            channel    = _CHANNEL_NAMES[channel_id]
            cust_id    = random.randint(1, n_customers)
            store_id   = random.choice(instore_ids) if channel_id == 2 else None

            n_items   = random.choices([1,2,3,4,5], weights=[0.50,0.25,0.13,0.08,0.04])[0]
            sel_idxs  = random.choices(prod_list, weights=product_weights, k=n_items)

            order_value  = 0.0
            order_items  = []

            for idx in sel_idxs:
                p         = products[idx]
                qty       = random.choices([1,2,3], weights=[0.85,0.12,0.03])[0]
                base_price = float(p["price"])
                cost_price = float(p["cost"])

                if mult > 1.5:
                    disc_pct = random.choices([0,.05,.10,.15,.20,.30],
                                              weights=[0.30,0.20,0.20,0.15,0.10,0.05])[0]
                elif random.random() < 0.22:
                    disc_pct = random.choices([.05,.10,.15], weights=[0.60,0.30,0.10])[0]
                else:
                    disc_pct = 0.0

                unit_rev  = round(base_price * (1 - disc_pct), 2)
                revenue   = round(unit_rev * qty, 2)
                disc_amt  = round(base_price * disc_pct * qty, 2)
                cost_amt  = round(cost_price * qty, 2)
                profit    = round(revenue - cost_amt, 2)
                order_value += revenue

                sales_rows.append({
                    "sale_id":        sale_id,
                    "date_id":        date_id,
                    "product_id":     p["product_id"],
                    "customer_id":    cust_id,
                    "store_id":       store_id,
                    "order_id":       order_id,
                    "quantity":       qty,
                    "revenue":        revenue,
                    "discount_amount":disc_amt,
                    "cost_amount":    cost_amt,
                    "profit_amount":  profit,
                    "channel":        channel,
                })
                sale_id += 1
                order_items.append({
                    "product_id": p["product_id"],
                    "quantity":   qty,
                    "revenue":    revenue,
                    "order_id":   order_id,
                })

            # --- Statut commande ---
            if channel_id == 2:
                delivery_days = 0
                status_flag   = 0   # livré (en magasin = immédiat)
            elif channel_id == 1:
                delivery_days = random.choices([1,2,3,4,5,7,10],
                                               weights=[0.05,0.25,0.30,0.20,0.12,0.06,0.02])[0]
                status_flag   = random.choices([0,1,2], weights=[0.88,0.06,0.06])[0]
            else:
                delivery_days = random.choices([3,5,7,10,14],
                                               weights=[0.15,0.35,0.30,0.15,0.05])[0]
                status_flag   = random.choices([0,1,2], weights=[0.87,0.07,0.06])[0]

            orders_rows.append({
                "order_id":          order_id,
                "date_id":           date_id,
                "customer_id":       cust_id,
                "store_id":          store_id,
                "order_value":       round(order_value, 2),
                "item_count":        n_items,
                "delivery_time_days":delivery_days,
                "order_status_flag": status_flag,
            })

            # --- Retour (status_flag == 2) ---
            if status_flag == 2:
                ret_days = random.randint(3, 30)
                ret_date = d + timedelta(days=ret_days)
                if ret_date > END_DATE:
                    ret_date = END_DATE
                ret_date_id = date_map.get(ret_date.isoformat())
                if ret_date_id:
                    item      = random.choice(order_items)
                    ret_qty   = random.randint(1, item["quantity"])
                    refund    = round((item["revenue"] / item["quantity"]) * ret_qty, 2)
                    reason    = random.choices(_RETURN_REASONS, weights=_RETURN_REASON_W)[0]
                    returns_rows.append({
                        "return_id":       return_id,
                        "date_id":         ret_date_id,
                        "product_id":      item["product_id"],
                        "customer_id":     cust_id,
                        "order_id":        order_id,
                        "return_quantity":  ret_qty,
                        "refund_amount":   refund,
                        "return_rate_flag":1,
                        "return_reason":   reason,
                    })
                    return_id += 1

            # --- Ticket support (~3% des commandes + tous les retours) ---
            if random.random() < 0.03 or status_flag == 2:
                tck_days    = random.randint(0, 14)
                tck_date    = d + timedelta(days=tck_days)
                if tck_date > END_DATE:
                    tck_date = END_DATE
                tck_date_id = date_map.get(tck_date.isoformat())
                if tck_date_id:
                    issue_type   = "return_request" if status_flag == 2 else random.choices(_ISSUE_TYPES, weights=_ISSUE_W)[0]
                    res_hours    = random.choices(_RESOLUTION_HOURS, weights=_RESOLUTION_W)[0]
                    escalation   = 1 if res_hours >= 72 else 0
                    tck_status   = "resolved" if random.random() < 0.85 else random.choice(["pending","in_progress"])
                    tickets_rows.append({
                        "ticket_id":            ticket_id,
                        "date_id":              tck_date_id,
                        "customer_id":          cust_id,
                        "store_id":             store_id,
                        "resolution_time_hours":res_hours,
                        "ticket_count":         1,
                        "escalation_flag":      escalation,
                        "issue_type":           issue_type,
                        "status":               tck_status,
                    })
                    ticket_id += 1

    write_csv("fact_sales.csv",          sales_rows,   list(sales_rows[0].keys()))
    write_csv("fact_orders.csv",         orders_rows,  list(orders_rows[0].keys()))
    write_csv("fact_returns.csv",        returns_rows, list(returns_rows[0].keys()))
    write_csv("fact_support_tickets.csv",tickets_rows, list(tickets_rows[0].keys()))


# ---------------------------------------------------------------------------
# FACT_INVENTORY_SNAPSHOT  (snapshot hebdomadaire — chaque lundi)
# ---------------------------------------------------------------------------

def generate_inventory_snapshot(date_map, products, warehouses):
    rows       = []
    snap_id    = 1
    mondays    = [d for d in sorted(date_map)
                  if date(int(d[:4]),int(d[5:7]),int(d[8:])).weekday() == 0]

    # Stock initial par (product, warehouse)
    stock: dict = {}
    for p in products:
        for w in warehouses:
            base = random.randint(80, 300) if w["warehouse_id"] == 1 else random.randint(30, 150)
            stock[(p["product_id"], w["warehouse_id"])] = base

    for date_str in mondays:
        d       = date(int(date_str[:4]), int(date_str[5:7]), int(date_str[8:]))
        date_id = date_map[date_str]
        mult    = get_daily_multiplier(d)

        for p in products:
            for w in warehouses:
                key     = (p["product_id"], w["warehouse_id"])
                current = stock[key]

                # Consommation hebdomadaire simulée
                consumption = int(10 * mult * random.uniform(0.5, 1.5))

                # Réapprovisionnement si seuil bas
                if current < 25:
                    current += random.randint(60, 220)

                current = max(0, current - consumption)
                stock[key] = current

                reserved  = int(current * random.uniform(0.05, 0.20))
                available = max(0, current - reserved)
                stk_value = round(current * float(p["cost"]), 2)

                rows.append({
                    "snapshot_id":      snap_id,
                    "date_id":          date_id,
                    "product_id":       p["product_id"],
                    "warehouse_id":     w["warehouse_id"],
                    "stock_quantity":   current,
                    "reserved_quantity":reserved,
                    "available_quantity":available,
                    "stock_value":      stk_value,
                })
                snap_id += 1

    write_csv("fact_inventory_snapshot.csv", rows, list(rows[0].keys()))


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import time
    print("=" * 60)
    print(" Patissier - OLAP Mock Data Generator")
    print(" Periode : 2022-01-01 -> 2024-12-31")
    print("=" * 60)
    t0 = time.time()

    print("\n[1/8] dim_date")
    date_map = generate_dim_date()

    print("[2/8] dim_channel")
    channels = generate_dim_channel()

    print("[3/8] dim_warehouse")
    warehouses = generate_dim_warehouse()

    print("[4/8] dim_store")
    stores = generate_dim_store()

    print("[5/8] dim_product")
    products = generate_dim_product()

    print("[6/8] dim_customer  (50 000 clients — ~30s)")
    customers = generate_dim_customer(50_000)

    print("[7/8] fact_sales / fact_orders / fact_returns / fact_support_tickets")
    print("      (3 ans × ~185 ordres/jour avec saisonnalité — quelques minutes)")
    generate_fact_tables(date_map, products, stores, n_customers=50_000)

    print("[8/8] fact_inventory_snapshot  (snapshot hebdomadaire)")
    generate_inventory_snapshot(date_map, products, warehouses)

    elapsed = time.time() - t0
    print(f"\nTermine en {elapsed:.1f}s -- fichiers dans {OUTPUT_DIR}/")
    print("=" * 60)
