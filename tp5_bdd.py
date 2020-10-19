import sqlite3
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Créé la structure des tables dans la BDD
def create_tables():
    # Créé la table "region"
    c.execute("CREATE TABLE IF NOT EXISTS region "
              "(code_region INTEGER PRIMARY KEY, "
              "nom TEXT, "
              "population INTEGER)")

    # Créé la table "departement"
    c.execute("CREATE TABLE IF NOT EXISTS departement "
              "(code_dpt TEXT PRIMARY KEY, "
              "nom TEXT, "
              "code_region INTEGER, "
              "population INTEGER)")

    # Créé la table "commune"
    c.execute("CREATE TABLE IF NOT EXISTS commune "
              "(code_dpt TEXT, "
              "code_commune INTEGER,"
              "nom TEXT, "
              "population INTEGER, "
              "primary key(code_dpt, code_commune))")


# Remplit la BDD à partir des données récupérées dans les fichiers CSV
def insert_lines():
    # Liste des régions
    with open('/home/tom/Téléchargements/TP Python/data/regions.csv', 'r',
              encoding='iso-8859-1') as region_file:  # On ouvre le fichier en lecture, en précisant l'encodage
        lines = region_file.readlines()
        lines = lines[8:]  # On supprime les 8 premières lignes (entêtes du document)
        for line in lines:
            infos = line.split(';')  # On sépare la ligne avec les ;
            c.execute(
                "REPLACE INTO region(code_region, nom) "  # On "replace" (= ajout ou update si clé primaire déjà présente) la région
                "VALUES (?, ?)",
                (infos[0], infos[1]))

    # Liste des départements
    with open('/home/tom/Téléchargements/TP Python/data/departements.csv', 'r', encoding='iso-8859-1') as dpt_file:
        lines = dpt_file.readlines()
        lines = lines[8:]
        for line in lines:
            infos = line.split(';')
            c.execute("REPLACE INTO departement(code_dpt, nom, code_region) "
                      "VALUES (?, ?, ?)",
                      (infos[2], infos[3], infos[0]))

    # Liste des communes
    with open('/home/tom/Téléchargements/TP Python/data/communes.csv', 'r', encoding='iso-8859-1') as communes_files:
        lines = communes_files.readlines()
        lines = lines[8:]
        for line in lines:
            infos = line.split(';')
            c.execute("REPLACE INTO commune(code_dpt, code_commune, nom, population) "
                      "VALUES (?, ?, ?, ?)",
                      (infos[2], infos[5], infos[6], int(infos[9].replace(' ', ''))))  # On supprime les espace dans les nombres pour pouvoir bien les parser


# Calcule les populations de chaque département et région, puis met à jour la BDD
def update_population():
    # Départements
    c.execute("SELECT code_dpt, SUM(population) FROM commune GROUP BY code_dpt")
    for infos in c.fetchall():  # infos = [code_dpt, SUM(population)]
        c.execute("UPDATE departement "
                  "SET population = " + str(infos[1]) + " "
                  "WHERE code_dpt LIKE '" + infos[0] + "'")

    # Régions
    c.execute("SELECT code_region, SUM(population) FROM departement GROUP BY code_region")
    for infos in c.fetchall():  # infos = [code_region, SUM(population)]
        c.execute("UPDATE region "
                  "SET population = " + str(infos[1]) + " "
                  "WHERE code_region == " + str(infos[0]))


# Affiche toutes les communes ayant le même nom, et la liste de tous les départements où elles sont présentes
def get_duplicates_communes():
    # Pour chaque nom de commune (sans les duplicatas)
    c.execute("SELECT DISTINCT nom FROM commune")
    for nom in c.fetchall():
        # On cherche tous les départements où une commune porte le même nom (sans oublier de doubler les apostrophes dans les noms de communes)
        c.execute("SELECT code_dpt FROM commune WHERE nom LIKE '" + nom[0].replace("'", "''") + "'")
        results = c.fetchall()
        # Si le résultat est > 1, on print le nom de la commune avec la liste des départements
        if len(results) > 1:
            liste_dpt = [item for t in results for item in t]  # (formule magique pour transformer une liste de tuples en liste normale)
            print(f'{nom[0]} : {liste_dpt}')


# Sauvegarde la BDD dans un fichier XML
def save_xml():
    data = ET.Element("database")  # data = élément racine du XML

    regions = ET.SubElement(data, "regions")
    departements = ET.SubElement(data, "départements")  # regions, departements et communes = sous-éléments de data
    communes = ET.SubElement(data, "communes")

    # Ajout des régions
    c.execute("SELECT * FROM region")  # On récupère toutes les régions
    rows = c.fetchall()
    for row in rows:  # Pour chaque région
        region = ET.SubElement(regions, "region")  # On créé un sous-élément de 'regions' qu'on nomme 'region'
        region.set("code_region", str(row[0]))  # Et on lui applique des paramètres sous la forme de "clé : valeurs"
        region.set("nom", row[1])
        region.set("population", str(row[2]))

    # Ajout des départements
    c.execute("SELECT * FROM departement")
    rows = c.fetchall()
    for row in rows:
        dpt = ET.SubElement(departements, "departement")
        dpt.set("code_dpt", row[0])
        dpt.set("nom", row[1])
        dpt.set("code_region", str(row[2]))
        dpt.set("population", str(row[3]))

    # Ajout des communes
    c.execute("SELECT * FROM commune")
    rows = c.fetchall()
    for row in rows:
        commune = ET.SubElement(communes, "commune")
        commune.set("code_dpt", row[0])
        commune.set("nom", str(row[1]))
        commune.set("code_commune", row[2])
        commune.set("population", str(row[3]))

    # On transforme tout le contenu de data (la racine) en string (en conservant le bon encodage)
    xml = ET.tostring(data, encoding='iso-8859-1', method='xml')

    # Et on le "prettify" pour avoir des bonnes indentations et pas juste une seule ligne
    pretty_xml = minidom.parseString(xml).toprettyxml(indent="   ")

    # Puis on écrit le fichier
    with open("database.xml", 'w') as f:
        f.write(pretty_xml)


# Charge un fichier XML pour mettre à jour la BDD
def load_xml():
    # On récupère le fichier XML
    tree = ET.parse("database.xml")

    # Puis sa racine (cf. save_xml)
    data = tree.getroot()

    # Ajout des régions
    regions = data[0]  # On récupère l'éléments 'regions'
    for region in regions:  # Pour chaque sous-élément de 'regions'
        infos = region.attrib  # On récupère ses attributs (ensembles clé-valeurs)
        c.execute("REPLACE INTO region(code_region, nom, population) "  # Et on ajoute ça à la BDD
                  "VALUES (?, ?, ?)",
                  (infos["code_region"], infos["nom"], infos["population"]))

    # Ajout des départements
    departements = data[1]
    for dpt in departements:
        infos = dpt.attrib
        c.execute("REPLACE INTO departement(code_dpt, nom, code_region, population) "
                  "VALUES (?, ?, ?, ?)",
                  (infos["code_dpt"], infos["nom"], infos["code_region"], infos["population"]))

    # Ajout des communes
    communes = data[2]
    for commune in communes:
        infos = commune.attrib
        c.execute("REPLACE INTO commune(code_dpt, code_commune, nom, population) "
                  "VALUES (?, ?, ?, ?)",
                  (infos["code_dpt"], infos["code_commune"], infos["nom"], infos["population"]))


# Change la structure de la BDD pour intégrer les nouvelles régions
def add_new_regions():
    # Créé la table "nouvellesregions"
    c.execute("CREATE TABLE IF NOT EXISTS nouvellesregions "
              "(code_region INTEGER PRIMARY KEY, "
              "nom TEXT, "
              "population INTEGER)")

    # On remplit la table "nouvellesregions"
    with open('/home/tom/Téléchargements/TP Python/data/zones-2016.csv', 'r', encoding='iso-8859-1') as region_file:
        lines = region_file.readlines()
        lines = lines[-18:]  # On garde juste les 18 dernières lignes (les régions)
        for line in lines:
            infos = line.split(';')
            c.execute(
                "REPLACE INTO nouvellesregions(code_region, nom) "
                "VALUES (?, ?)",
                (infos[1], infos[2]))

    # Ajout un champ "code_nouvelle_region" à la table "departement"
    # [!] SQLite ne supporte pas la clause "IF NOT EXISTS" pour la fonction ALTER TABLE,
    # [!] c'est pourquoi on utilise les exceptions pour gérer le cas où la colonne existerait déjà
    try:
        c.execute("ALTER TABLE departement "
                  "ADD code_nouvelle_region INTEGER")
    except sqlite3.OperationalError:
        pass

    # On met à jour le champ "code_nouvelle_region" pour les départements
    with open("/home/tom/Téléchargements/TP Python/data/communes-2016.csv", 'r', encoding='iso-8859-1') as communes_file:
        lines = communes_file.readlines()
        lines = lines[7:]
        updated_dpt = []  # Liste des départements mis à jour
        for line in lines:
            infos = line.split(';')
            # Si le département n'a pas déjà été mis à jour
            if not infos[2] in updated_dpt:
                c.execute("UPDATE departement "
                          "SET code_nouvelle_region = " + str(infos[3]) + " "
                          "WHERE code_dpt LIKE '" + infos[2] + "'")
                updated_dpt.append(infos[2])  # On met à jour la liste des départements mis à jour

    # On calcule la population des nouvelles régions avec la population des communes
    c.execute("SELECT code_region FROM nouvellesregions")
    for code_region in c.fetchall():  # Pour chaque code_region
        population = 0
        c.execute(
            "SELECT commune.population FROM commune, departement "  # On récupère les populations de toutes les communes
            "WHERE commune.code_dpt == departement.code_dpt "  # dans les départements de la région "code_region"
            "AND departement.code_nouvelle_region == " + str(code_region[0]))
        for pop_commune in c.fetchall():
            population += pop_commune[0]
        c.execute("UPDATE nouvellesregions "  # Puis on met à jour la population de la nouvelle région
                  "SET population = " + str(population) + " "
                  "WHERE code_region ==" + str(code_region[0]))


# -------------- MAIN ---------------#
conn = sqlite3.connect('database.db', timeout=5)
c = conn.cursor()

# create_tables()
# insert_lines()

# update_population()
# get_duplicates_communes()

# save_xml()
# load_xml()

# add_new_regions()

conn.commit()
conn.close()
