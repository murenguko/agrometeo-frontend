"""
content_intro.py - Rédaction de l'Introduction Générale
Conforme aux exigences UPG et aux consignes sans pages liminaires.
"""

from builder import add_h1, add_h2, add_h3, add_p, add_bullet, add_table, add_callout

def build_intro(doc):
    """Génère le chapitre complet de l'Introduction Générale."""
    add_h1(doc, "INTRODUCTION GÉNÉRALE")
    
    # --- 1. Contexte général et justification ---
    add_h2(doc, "1. Contexte Général et Justification")
    
    add_p(doc, 
        "La République du Burundi, pays enclavé d'Afrique centrale et orientale couvrant une superficie de 27 834 km², "
        "se caractérise par une topographie particulièrement escarpée et contrastée. S'étageant depuis les rives du lac "
        "Tanganyika à 773 mètres d'altitude jusqu'aux sommets abrupts de la crête Congo-Nil culminant à plus de 2 670 mètres, "
        "le relief burundais façonne une multitude de microclimats locaux soumis à un régime pluviométrique bimodal rythmé "
        "par les saisons culturales A (septembre à janvier) et B (février à juin), complétées dans les bas-fonds marécageux "
        "par la saison maraîchère de contre-saison C (juillet à septembre) [1]. L'agriculture représente le socle vital de la "
        "société et de l'économie nationale : elle emploie entre 85 % et 90 % de la population active, génère près de 40 % "
        "du Produit Intérieur Brut (PIB) et assure la quasi-totalité de l'apport calorique des ménages ruraux [2]."
    )
    
    add_p(doc,
        "Néanmoins, le secteur agricole burundais demeure très majoritairement pluvial, ce qui le rend dramatiquement "
        "vulnérable aux aléas hydrométéorologiques extrêmes amplifiés par le changement climatique global [3]. Au cours de "
        "la dernière décennie, la fréquence et l'intensité des événements perturbateurs ont atteint des niveaux critiques : "
        "les précipitations torrentielles soudaines provoquent des crues fluviales dévastatrices dans la plaine alluviale "
        "de la Rusizi et sur le littoral de Bujumbura (avec les inondations récurrentes du quartier de Gatumba et des berges "
        "des rivières Ntahangwa, Muha et Mutimbuzi), tandis que les fortes pentes dénudées des versants de Mumirwa et de la "
        "crête subissent une érosion régressive majeure, un ravinement généralisé et des glissements de terrain mortels [4]. "
        "À l'inverse, des retards de début de saison pluvieuse ou des pauses pluviométriques inopinées de plus de cinq à sept "
        "jours durant les phases critiques de floraison entraînent des chutes drastiques de rendement pour le maïs, le haricot "
        "et les tubercules, plongeant des milliers de familles rurales dans l'insécurité alimentaire immédiate."
    )
    
    add_p(doc,
        "Face à ces défis pressants, la disponibilité d'une information agro-météorologique locale, fiable et anticipée "
        "constitue un levier d'adaptation indispensable pour sécuriser les pratiques culturales paysannes : choix opportun "
        "des semis, protection des récoltes sur les aires de séchage en plein air, drainage préventif des parcelles et "
        "consolidation des diguettes de bas-fonds rizicoles. Le présent projet d'ingénierie logicielle s'inscrit précisément "
        "dans cette dynamique de résilience climatique."
    )
    
    # --- 2. Problématique détaillée ---
    add_h2(doc, "2. Problématique de Recherche et d'Ingénierie")
    
    add_p(doc,
        "En dépit de l'essor remarquable des technologies de l'information et de la télédétection spatiale globale, "
        "un fossé opérationnel et technologique profond subsiste entre les données climatiques satellitaires mondiales et "
        "les réalités quotidiennes des producteurs agricoles burundais. Cette situation découle d'un quadruple verrou "
        "structurel :"
    )
    
    add_bullet(doc,
        "Le réseau d'observation météorologique terrestre géré par l'Institut Géographique du Burundi (IGEBU) fait face "
        "à des contraintes matérielles, financières et énergétiques sévères. Avec un nombre réduit de stations synoptiques "
        "et agro-climatologiques automatiques opérationnelles à l'échelle nationale, de vastes étendues collinaires et de "
        "bassins versants échappent à un suivi continu en temps réel, créant d'importantes zones d'ombre d'observation.",
        bold_prefix="1. Insuffisance et dispersion du réseau d'observation au sol : "
    )
    
    add_bullet(doc,
        "Les modèles de prévision numérique du temps à haute résolution (Copernicus, ECMWF, GFS, Open-Meteo) et les "
        "systèmes mondiaux de surveillance des inondations (GloFAS) produisent des flux massifs de données brutes. "
        "Cependant, ces données sont distribuées via des API complexes, encodées dans des formats binaires spécialisés "
        "(GRIB2, NetCDF, FlatBuffers) et exprimées en unités physiques pures (m³/s, kg/m², flux radiatif) hermétiques aux "
        "moniteurs agricoles communaux, aux directeurs de coopératives et aux agronomes de terrain.",
        bold_prefix="2. Complexité et technicité excessive des flux de données globaux : "
    )
    
    add_bullet(doc,
        "Une prévision physique brute annonçant par exemple « 35 mm de précipitations sur 24 heures » ou un débit fluvial "
        "de « 18 m³/s » ne constitue pas en soi une information décisionnelle exploitable. Le technicien agronome et "
        "le paysan ont besoin de savoir quelles sont les conséquences directes pour leurs cultures spécifiques : faut-il "
        "rentrer d'urgence le maïs étalé sur les claies de séchage ? Le riz de bas-fond court-il un risque d'asphyxie par "
        "rupture des levées de terre ? Le bananier risque-t-il le déracinement face à des rafales de vent de 45 km/h ? "
        "Il existe une absence patente de passerelle algorithmique automatisée traduisant les grandeurs physiques en "
        "directives agronomiques pragmatiques, conformes aux fiches techniques de l'Institut des Sciences Agronomiques "
        "du Burundi (ISABU).",
        bold_prefix="3. Absence de passerelle décisionnelle agronomique contextualisée : "
    )
    
    add_bullet(doc,
        "Les canaux historiques de dissémination (bulletins décadaires sur support papier, synthèses radiodiffusées "
        "hebdomadaires) souffrent d'une latence temporelle incompatible avec la gestion des aléas d'urgence. Par ailleurs, "
        "l'infrastructure numérique locale (terminaux mobiles d'entrée de gamme, réseaux 2G/3G instables, coût élevé de la "
        "bande passante data) rend inopérantes les applications web lourdes ou nécessitant des transferts volumineux.",
        bold_prefix="4. Latence de diffusion et contraintes d'infrastructure locale : "
    )
    
    # --- 3. Questions spécifiques de recherche ---
    add_h2(doc, "3. Questions Spécifiques de Recherche et d'Ingénierie")
    
    add_p(doc,
        "Afin d'apporter une solution logicielle pérenne, robuste et adaptée au contexte burundais, le présent travail "
        "d'ingénierie articule sa démarche méthodologique autour de quatre questions directrices fondamentales :"
    )
    
    add_bullet(doc,
        "Comment collecter, normaliser, synchroniser et mettre en cache en temps quasi-réel des séries temporelles hétérogènes "
        "de prévisions météorologiques horaires (Open-Meteo) et de débits hydrologiques mondiaux (GloFAS), sans imposer une "
        "infrastructure serveur matérielle locale lourde et coûteuse ?",
        bold_prefix="Question 1 (Ingénierie des données) : "
    )
    
    add_bullet(doc,
        "Quels modèles mathématiques, quelles règles logiques formelles et quels seuils quantitatifs permettent de convertir "
        "des séries continues d'altération physique (précipitations 24h/72h, rafales de vent, percentiles de débit fluvial p75) "
        "en conseils agricoles d'action immédiate par culture, tout en préservant une stricte neutralité fonctionnelle sans effet de bord ?",
        bold_prefix="Question 2 (Modélisation métier et agronomie) : "
    )
    
    add_bullet(doc,
        "Quelle architecture logicielle moderne (paradigme client-serveur, patron Backend-For-Frontend, réactivité par compilation "
        "Svelte 5 sans DOM virtuel, API asynchrone ASGI FastAPI) permet de garantir une fluidité d'affichage optimale, une consommation "
        "de bande passante minimale et une haute résilience aux coupures réseau intermittentes sur terminaux mobiles au Burundi ?",
        bold_prefix="Question 3 (Architecture logicielle et performance) : "
    )
    
    add_bullet(doc,
        "Comment concilier une aide proactive à la décision agricole collinaire avec les impératifs déontologiques et juridiques "
        "nationaux, de manière à soutenir les communautés sans empiéter sur le monopole institutionnel régalien des alertes "
        "officielles dévolu à l'IGEBU et à la Protection Civile ?",
        bold_prefix="Question 4 (Déontologie et responsabilité sociotechnique) : "
    )
    
    # --- 4. Objectif général ---
    add_h2(doc, "4. Objectif Général du Projet")
    
    add_p(doc,
        "L'objectif général du projet consiste à concevoir, développer, tester et évaluer un prototype complet de "
        "Système de Veille Météorologique et Climatique pour le Burundi (baptisé AgroMétéo Burundi). Ce système "
        "s'articule autour d'une interface cartographique web réactive et ergonomique (SvelteKit / Sveaflet / Tailwind CSS) "
        "et d'un serveur d'agrégation décisionnel asynchrone (FastAPI / Python 3.14 / MongoDB / Cache SQLite), capable de "
        "fournir aux encadreurs agricoles, coopératives et décideurs des visualisations horaires fluides et des avis "
        "agro-climatiques contextualisés par zone géographique et par culture vivrière."
    )
    
    # --- 5. Objectifs spécifiques SMART ---
    add_h2(doc, "5. Objectifs Spécifiques et Indicateurs Mesurables de Succès (SMART)")
    
    add_p(doc,
        "Pour assurer une évaluation objective et rigoureuse de la réalisation, l'objectif général est décliné en cinq "
        "objectifs spécifiques conformes aux critères SMART (Spécifique, Mesurable, Atteignable, Réaliste, Temporellement défini) :"
    )
    
    headers_smart = ["Code", "Objectif Spécifique (OS)", "Description Technique Détaillée", "Indicateur Chiffré de Succès (SMART)"]
    data_smart = [
        [
            "OS1",
            "Collecte & Ingestion multi-sources résiliente",
            "Développer un service asynchrone d'interrogation, normalisation et mise en cache des prévisions météorologiques horaires (Open-Meteo) et hydrologiques (GloFAS).",
            "Taux de disponibilité des données ≥ 99% ; temps de réponse du cache SQLite < 50 ms ; résilience prouvée à 5 coupures simulées avec retry automatique (backoff 0.2s)."
        ],
        [
            "OS2",
            "Moteur de règles métier fonctionnel pur",
            "Implémenter un moteur algorithmique découplé appliquant les seuils officiels IGEBU (50/100 mm) et les règles ISABU pour 7 cultures vivrières sans effet de bord.",
            "Taux de couverture de tests unitaires de 100% sur la logique décisionnelle (31/31 tests passés avec succès sous pytest) ; aucun crash en présence de données manquantes (NaN/None)."
        ],
        [
            "OS3",
            "Architecture de sécurité et d'authentification",
            "Intégrer un système complet de gestion des utilisateurs et sécurisation des routes météo via tokens JWT HS256 et cryptographie Argon2id.",
            "Temps de réponse serveur constant lors des échecs d'authentification grâce à un dummy hash (neutralisation totale de l'énumération par canal auxiliaire) ; expiration stricte à 30 min."
        ],
        [
            "OS4",
            "Interface cartographique interactive et légère",
            "Concevoir une interface monopage avec carte Leaflet tuilée OSM (Sveaflet) et graphiques vectoriels interactifs (svelteplot) adaptée aux faibles bandes passantes.",
            "Poids total du bundle JavaScript initial compilé < 250 Ko ; temps de premier rendu utile (FCP) < 1,5 seconde sur connexion 3G simulée ; 100% responsive sur mobile et desktop."
        ],
        [
            "OS5",
            "Contextualisation territoriale et agronomique",
            "Modéliser 5 zones pilotes provinciales avec distinction fine des altitudes (plaine <1000m vs montagne >1350m) et association dynamique aux cultures prévalentes régionales.",
            "100% des requêtes sur Bujumbura Rural appliquent le seuil exact de leur sous-zone (Imbo 50 mm vs Mumirwa 100 mm) avec repli de précaution automatique vers 50 mm en cas d'ambiguïté."
        ]
    ]
    add_table(doc, headers_smart, data_smart, col_widths=[1.5, 3.5, 5.5, 5.0], caption="Tableau 0.1 — Objectifs Spécifiques et Indicateurs Mesurables de Succès (SMART)")
    
    # --- 6. Structure globale du rapport ---
    add_h2(doc, "6. Structure Globale du Rapport")
    
    add_p(doc,
        "Le présent rapport académique est rédigé dans le respect scrupuleux des normes méthodologiques de la Faculté des "
        "TIC de l'Université Polytechnique de Gitega (UPG). Conformément aux directives validées pour ce projet de fin de cycle, "
        "le document s'ouvre directement sur cette Introduction Générale et s'organise en cinq chapitres substantiels, "
        "suivis d'une Conclusion Générale et d'Annexes techniques approfondies :"
    )
    
    add_bullet(doc,
        "Présente le cadre d'étude géographique, caractérise en détail les 5 zones pilotes burundaises (Bujumbura Mairie, "
        "Bujumbura Rural scindée en Imbo et Mumirwa, Gitega, Karusi, Rutana), modélise les besoins des usagers à travers "
        "trois personas types, définit les contraintes opérationnelles et expose l'étude de faisabilité multidimensionnelle.",
        bold_prefix="Chapitre I — État des lieux et diagnostic : "
    )
    
    add_bullet(doc,
        "Établit l'assise conceptuelle du travail par une confrontation comparative rigoureuse des technologies logicielles "
        "contemporaines : architectures client-serveur et patron BFF, frameworks front-end (SvelteKit vs React/Vue/Angular), "
        "frameworks back-end (FastAPI vs Django/Node/Spring), bases de données (MongoDB Atlas et SQLite vs PostgreSQL relationnel), "
        "protocoles d'échange d'API, sécurité cryptographique (Argon2id, OAuth2, JWT) et accessibilité numérique (WCAG 2.1).",
        bold_prefix="Chapitre II — Étude théorique et état de l'art : "
    )
    
    add_bullet(doc,
        "Formalise l'ensemble des spécifications fonctionnelles (EF-01 à EF-20) et non fonctionnelles (ENF-01 à ENF-10), "
        "détaille l'architecture applicative globale, présente la modélisation UML complète (cas d'utilisation, classes, composants, "
        "séquences, états-transitions, déploiement physique), décrit le schéma des données, formalise mathématiquement les règles "
        "métier agro-climatiques et expose le calendrier Agile Scrum sur deux semaines.",
        bold_prefix="Chapitre III — Conception de la solution cible : "
    )
    
    add_bullet(doc,
        "Décrit la matérialisation technique de la solution au sein des dépôts weather-backend et weather-app : outillage moderne "
        "(Python 3.14, uv, Vite, Svelte 5 en mode Runes), implémentation des routeurs d'authentification et de météo, services "
        "de collecte et de calcul pur, composants cartographiques Leaflet et graphiques svelteplot, gestion des cookies sécurisés et "
        "politique de gestion des versions Git.",
        bold_prefix="Chapitre IV — Implémentation et réalisation : "
    )
    
    add_bullet(doc,
        "Expose le protocole d'assurance qualité et les résultats expérimentaux des tests (31 tests unitaires pytest validés à 100%, "
        "compilation de production Vite sans erreur, tests de responsive design et de charge). Ce chapitre intègre la pièce "
        "maîtresse de notre étude : une comparaison détaillée, critique et argumentée entre le Document de Cadrage MVP initial "
        "et l'Implémentation Réelle, justifiant scientifiquement chaque divergence (zonage territorial, substitution de PostgreSQL par "
        "MongoDB, sécurisation avancée Argon2id, retrait du modèle LHASA et cartographie dynamique des cultures ISABU).",
        bold_prefix="Chapitre V — Tests, validation et évaluation : "
    )
    
    add_bullet(doc,
        "Dresse le bilan synthétique des réalisations au regard des questions de recherche posées, explicite les limites actuelles "
        "du prototype et trace les perspectives technologiques majeures pour la deuxième année du projet (diffusion multicanale "
        "USSD/SMS pour téléphones basiques, réseau de stations IoT locales, modèles d'intelligence artificielle de descente d'échelle, "
        "multilinguisme en langue nationale Kirundi).",
        bold_prefix="Conclusion générale et perspectives : "
    )
    
    add_bullet(doc,
        "Fournissent les diagrammes UML détaillés (Annexe A), le schéma d'architecture physique de la base de données (Annexe B), "
        "le manuel complet d'installation et d'exploitation pas à pas (Annexe D), ainsi que l'arborescence du code et les métriques de "
        "qualité logicielle (Annexe F), complétés par les références bibliographiques normalisées au format IEEE.",
        bold_prefix="Annexes et Références : "
    )
    
    add_callout(doc,
        "Afin de respecter strictement la réglementation nationale sur les services météorologiques au Burundi, l'ensemble "
        "des messages produits par AgroMétéo Burundi se définit comme une aide consultative collinaire et ne se substitue "
        "en aucun cas aux avis et vigilances officielles émis par l'IGEBU ni aux ordres de sécurité civile de l'État.",
        title="Mention Déontologique Préliminaire :"
    )
