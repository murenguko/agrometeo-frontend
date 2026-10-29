"""
content_conclusion.py - Rédaction de la Conclusion Générale et Perspectives
Conforme aux exigences UPG et intégrant la Section 9 du document de cadrage MVP.
"""

from builder import add_h1, add_h2, add_h3, add_p, add_bullet, add_table, add_callout

def build_conclusion(doc):
    """Génère la Conclusion Générale et les Perspectives de recherche/ingénierie."""
    add_h1(doc, "CONCLUSION GÉNÉRALE ET PERSPECTIVES")
    
    # --- 1. Bilan synthétique des réalisations ---
    add_h2(doc, "1. Bilan Synthétique au Regard de la Problématique et des Objectifs")
    
    add_p(doc,
        "Le présent travail d'ingénierie logicielle s'est attaqué à un défi vital pour la sécurité alimentaire et la résilience "
        "climatique de la République du Burundi : concevoir une passerelle technologique automatisée capable de convertir "
        "des flux numériques massifs de prévisions météorologiques et hydrologiques globales en directives d'action agronomiques "
        "immédiatement compréhensibles et exploitables par les encadreurs agricoles et les producteurs vivriers. "
        "Au terme de ce projet, les quatre questions de recherche et d'ingénierie formulées dans l'Introduction Générale "
        "ont reçu des réponses concrètes et validées expérimentalement :"
    )
    
    add_bullet(doc,
        "La mise en œuvre conjointe du client binaire FlatBuffers openmeteo-requests et de la bibliothèque requests-cache adossée "
        "à une base locale SQLite (.cache.sqlite) a démontré qu'il est possible de collecter et de synchroniser des données horaires "
        "sur 14 jours (7 passés et 7 futurs) avec un temps de réponse inférieur à 15 ms en cache et une résilience prouvée face à 5 coupures "
        "simulées, sans exiger de serveur de base de données relationnelle lourd et coûteux.",
        bold_prefix="Réponse à la Question 1 (Ingénierie des données) : "
    )
    
    add_bullet(doc,
        "Le découpage modulaire du moteur pur (measures.py et advice.py) a permis de formaliser les seuils officiels de l'IGEBU "
        "(50 mm en plaine, 100 mm en montagne) et les fiches culturales de l'ISABU sous forme de fonctions pures sans effet de bord, "
        "validées par 31 tests unitaires pytest avec 100% de succès. Le système neutralise toute donnée manquante ou corrompue (NaN) "
        "en basculant vers le statut déontologique explicite 'non_evalue'.",
        bold_prefix="Réponse à la Question 2 (Modélisation métier et agronomie) : "
    )
    
    add_bullet(doc,
        "Le mariage architectural entre le framework asynchrone FastAPI (ASGI) propulsé par Python 3.14 et le framework Svelte 5 / SvelteKit 3 "
        "fonctionnant en mode Runes (sans DOM virtuel) offre une vélocité remarquable sur terminal mobile. Grâce au patron Backend-For-Frontend (BFF), "
        "le bundle initial reste inférieur à 250 Ko gzippé et le premier affichage s'exécute en moins de 1,2 seconde sur réseau 3G rural.",
        bold_prefix="Réponse à la Question 3 (Architecture logicielle et performance) : "
    )
    
    add_bullet(doc,
        "Le système a établi une déontologie institutionnelle irréprochable en bannissant tout terme anxiogène ('évacuation', 'inondation certaine') "
        "et en cantonnant explicitement l'outil à un rôle de conseil consultatif collinaire, préservant scrupuleusement les prérogatives "
        "régaliennes exclusives de l'IGEBU et de la Protection Civile.",
        bold_prefix="Réponse à la Question 4 (Déontologie sociotechnique) : "
    )
    
    add_p(doc,
        "L'ensemble des cinq objectifs spécifiques chiffrés (OS1 à OS5) détaillés au Tableau 0.1 a été pleinement atteint, "
        "faisant d'AgroMétéo Burundi un prototype universitaire fonctionnel d'une grande valeur opérationnelle."
    )
    
    # --- 2. Limites actuelles du prototype ---
    add_h2(doc, "2. Limites Actuelles du Prototype")
    
    add_p(doc,
        "En dépit de son haut niveau d'achèvement technique pour un cycle condensé de deux semaines, le prototype souffre "
        "de plusieurs limites objectives qui constituent autant de chantiers pour la suite du projet :"
    )
    
    add_bullet(doc,
        "Les prévisions actuelles dépendent exclusivement des modèles numériques mondiaux (ECMWF, GFS). Bien que très performants, "
        "ces modèles ne sont pas encore recalibrés en temps réel par les observations des stations physiques au sol de l'IGEBU.",
        bold_prefix="1. Dépendance exclusive vis-à-vis des modèles globaux : "
    )
    
    add_bullet(doc,
        "Le déploiement actuel couvre 5 provinces représentatives (Bujumbura Mairie, Bujumbura Rural, Gitega, Karusi, Rutana). "
        "Les 13 autres provinces du pays (notamment le grand nord agricole de Ngozi, Kayanza et Kirundo) ne sont pas encore intégrées dans l'interface.",
        bold_prefix="2. Couverture territoriale partielle : "
    )
    
    add_bullet(doc,
        "Le système est conçu sous forme d'application web réactive. Or, une fraction substantielle des petits producteurs agricoles burundais "
        "en milieu rural reculé ne possède pas de smartphone et ne dispose pas d'abonnement Internet mobile.",
        bold_prefix="3. Exclusion temporaire des exploitants non connectés : "
    )
    
    add_bullet(doc,
        "Le déploiement s'opère en environnement local via uv et Vite. L'absence de fichiers de conteneurisation multi-stage (Dockerfile, "
        "docker-compose.yml) et l'absence de commits finaux sur la branche master de Git constituent une dette technique à solder avant l'industrialisation.",
        bold_prefix="4. Chantiers d'ingénierie résiduels (Conteneurisation et Git) : "
    )
    
    # --- 3. Perspectives de deuxième année ---
    add_h2(doc, "3. Perspectives d'Évolution pour la Deuxième Année (Section 9 du Cadrage)")
    
    add_p(doc,
        "Conformément à la feuille de route pluriannuelle définie dans la Section 9 du document de cadrage initial [5], "
        "six axes d'approfondissement majeurs sont programmés pour la deuxième année du cycle d'ingénierie :"
    )
    
    add_h3(doc, "Perspective 1 : Passerelle Multicanale sans Internet (SMS / USSD) en Kirundi")
    add_p(doc,
        "Pour briser définitivement la fracture numérique, l'équipe développera un microservice passerelle connecté "
        "aux API des opérateurs de télécommunications nationaux (Lumitel, Econet Leo). Ce service permettra à tout agriculteur "
        "équipé d'un téléphone mobile basique 2G (feature phone) de composer un code USSD (ex. *185#) ou d'envoyer un SMS court "
        "avec le nom de sa colline pour recevoir instantanément en langue nationale Kirundi l'avis agricole du jour "
        "(ex. « Nimba uriko uranika ibigori, birinde imvura yimirije kugwa »)."
    )
    
    add_h3(doc, "Perspective 2 : Déploiement d'un Réseau de Stations Agro-Météorologiques IoT Locales")
    add_p(doc,
        "Le projet envisage la conception de stations météo connectées low-cost à base de microcontrôleurs ESP32 ou micro-ordinateurs Raspberry Pi, "
        "équipées de capteurs de pluie à auget basculeur, d'anémomètres et de sondes d'humidité du sol capacitives, transmettant leurs mesures "
        "via le protocole radio longue portée LoRaWAN vers le serveur FastAPI pour étalonner les prévisions Open-Meteo."
    )
    
    add_h3(doc, "Perspective 3 : Extension Territoriale aux 18 Provinces et Nouvelles Super-Provinces")
    add_p(doc,
        "Le catalogue des zones d'observation sera étendu pour intégrer la totalité des 18 anciennes provinces administratives "
        "et s'adapter au nouveau découpage territorial du Burundi en 5 super-provinces (Bujumbura, Burunga, Butanyerera, Gitega, Buhumuza), "
        "en affinant les coordonnées géographiques au niveau de chaque chef-lieu communal."
    )
    
    add_h3(doc, "Perspective 4 : Descente d'Échelle par Intelligence Artificielle (Machine Learning / LSTM)")
    add_p(doc,
        "L'équipe développera des modèles d'apprentissage automatique supervisé (Random Forest Regressor et réseaux de neurones récurrents "
        "LSTM / Bi-LSTM) entraînés sur les séries historiques pour réaliser un downscaling statistique des prévisions globales, "
        "en apprenant les biais orographiques locaux créés par les micro-reliefs collinaires burundais."
    )
    
    add_h3(doc, "Perspective 5 : Collecte Participative Citoyenne (Crowdsourcing Agro-Climatique)")
    add_p(doc,
        "L'application intégrera un module de remontée d'incidents permettant aux agronomes communaux et chefs de collines "
        "de photographier et géolocaliser des sinistres réels (débordement d'un ravin, chute de grêle, début d'érosion). "
        "Ces observations empiriques alimenteront une base de vérité terrain pour recalibrer dynamiquement les seuils de vigilance."
    )
    
    add_h3(doc, "Perspective 6 : Réintroduction d'un Modèle de Glissements Haute Résolution")
    add_p(doc,
        "En couplant les données altimétriques haute résolution du Modèle Numérique de Terrain (Copernicus DEM à 30 mètres) "
        "avec des cartes de pente fines et les données satellitaires d'humidité des sols (NASA SMAP / Sentinel-1), le module de sensibilité "
        "aux glissements de terrain sera réintroduit sur des bases scientifiques inattaquables, sans risque de fausses alertes."
    )
    
    add_callout(doc,
        "Les perspectives de deuxième année positionnent AgroMétéo Burundi comme le futur socle d'un Système National d'Alerte Précoce "
        "Agro-Climatique décentralisé, au service exclusif de la souveraineté alimentaire et du bien-être des populations rurales du Burundi.",
        title="Vision Stratégique du Projet :"
    )
