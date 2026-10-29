"""
content_chap1.py - Rédaction du Chapitre I : État des Lieux et Diagnostic
Conforme aux normes UPG et intégrant l'analyse de cadrage et la réalité du code.
"""

from builder import add_h1, add_h2, add_h3, add_p, add_bullet, add_table, add_figure, add_callout

def build_chap1(doc):
    """Génère le Chapitre I complet : État des Lieux et Diagnostic."""
    add_h1(doc, "CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC")
    
    # --- 1. Présentation du cadre d'étude et des 5 zones pilotes réelles ---
    add_h2(doc, "1. Présentation du Cadre d'Étude et Périmètre des Zones Pilotes")
    
    add_p(doc,
        "Le document de cadrage initial mentionnait à titre exploratoire trois secteurs géographiques génériques "
        "(la plaine de la Rusizi, des versants occidentaux et un secteur autour de Gitega) [5]. L'investigation rigoureuse "
        "du code source effectif des projets weather-backend et weather-app démontre une avancée majeure d'ingénierie : "
        "l'équipe a matérialisé le déploiement sur cinq zones pilotes territoriales réelles correspondant aux anciennes provinces "
        "administratives du Burundi (Bujumbura Mairie, Bujumbura Rural, Gitega, Karusi, Rutana), en intégrant une distinction "
        "topographique et climatique fondamentale pour Bujumbura Rural, subdivisée entre la plaine de l'Imbo et les contreforts "
        "montagneux de Mumirwa."
    )
    
    figure_1_1 = r"""
                     TOPOGRAPHIE DU BURUNDI ET ZONAGE DES 5 ZONES PILOTES
  Altitude
   (m)
  2600m ──┐                                         /\ (Crête Congo-Nil)
          │                                        /  \
  1800m ──┼───────────────────────┐               /    \       ┌──────────────────┐
          │                       │              /      \      │ Gitega (1750m)   │
  1500m ──┼───────────────────────┼─────────────/        \─────┤ Karusi (1600m)   │
          │                       │   Mumirwa  /          \    │ Rutana (1700m)   │
          │                       │  (> 1350m)/            \   └──────────────────┘
  1000m ──┼────────┐              │  100mm/24h             └── Plateau Central
          │        │ Imbo (<1000m)│  Montagne                  100 mm / 24 h
   773m ──┴────────┴──────────────┴──────────────────────────────────────────────
         Lac      Bujumbura Mairie    Bujumbura Rural            Plateaux de l'Est
      Tanganyika    50 mm / 24 h     (Imbo 50mm / Mumirwa 100mm)   et du Kumoso
    """
    add_figure(doc, figure_1_1, caption="Figure 1.1 — Profil altimétrique schématique du Burundi et découpage des zones d'observation")
    
    add_p(doc,
        "Ce découpage repose sur une analyse agro-écologique fine de la diversité géographique du pays :"
    )
    
    add_bullet(doc,
        "Située sur les berges nord-est du lac Tanganyika à une altitude moyenne de 820 mètres, cette zone urbaine et "
        "périurbaine de plaine alluviale est drainée par plusieurs cours d'eau torrentiels descendant des collines environnantes "
        "(Ntahangwa, Muha, Kanyosha, Mutimbuzi). Les vulnérabilités dominantes résident dans les inondations urbaines éclair, "
        "l'engorgement des sols sablo-limoneux et les montées des eaux lacustres [4]. Cultures prévalentes associées : riz, "
        "maïs, manioc et bananier.",
        bold_prefix="1. Bujumbura Mairie (Plaine de l'Imbo, ~820 m) : "
    )
    
    add_bullet(doc,
        "Cette entité territoriale présente un gradient altitudinal extrême s'étendant de 773 mètres (plaine bordière de l'Imbo) "
        "à plus de 2 600 mètres (contreforts de Mumirwa et crête Congo-Nil). Face à cette hétérogénéité, le système opère une "
        "scission opérationnelle en deux sous-zones bien distinctes :",
        bold_prefix="2. Bujumbura Rural (Zone mixte à fort contraste) : "
    )
    
    add_bullet(doc,
        "Altitude inférieure à 1 000 m. Climat tropical chaud et sec de basse altitude, vulnérable aux crues d'inondation des "
        "rivières Mugere et Karonke et à l'ensablement des périmètres irrigués. Seuil pluviométrique critique fixé à 50 mm / 24 h. "
        "Cultures majeures : riz de bas-fond, maïs de plaine, manioc, bananier.",
        bold_prefix="• Sous-zone Imbo (Basse altitude, < 1 000 m) : "
    )
    
    add_bullet(doc,
        "Altitude supérieure à 1 350 m (station de référence à 1 450 m). Pentes fortes (> 30 %), sols ferrallitiques acides "
        "hautement sensibles à l'érosion pluviale et au glissement de masse. Seuil critique fixé à 100 mm / 24 h. Cultures "
        "majeures : bananeraies d'altitude, maïs, haricot commun, manioc et pomme de terre.",
        bold_prefix="• Sous-zone Mumirwa (Hautes terres escarpées, > 1 350 m) : "
    )
    
    add_bullet(doc,
        "Capitale politique du pays, située au cœur des plateaux centraux burundais à une altitude de 1 650 à 1 850 mètres. "
        "Le relief collinaire ondulé est caractérisé par un réseau dense de marais cultivés en saison sèche et des collines "
        "soumises à un lessivage intense des sols lors des gros orages. Seuil critique de 100 mm / 24 h. Cultures majeures : "
        "maïs, haricot, bananier, riz de marais, patate douce et pomme de terre.",
        bold_prefix="3. Gitega (Plateau central, 1 650–1 850 m) : "
    )
    
    add_bullet(doc,
        "Province du centre-est traversée par le bassin versant majeur de la rivière Ruvubu (affluent du Nil) et ses tributaires "
        "(Gasenyi, Rusheri). Les bas-fonds marécageux y jouent un rôle stratégique pour la survie alimentaire mais sont exposés "
        "à des submersions prolongées, tandis que les collines connaissent des poches de sécheresse intra-saisonnières sévères. "
        "Seuil critique : 100 mm / 24 h. Cultures : maïs, haricot, bananier, manioc et patate douce.",
        bold_prefix="4. Karusi (Bassin de la Ruvubu, 1 500–1 750 m) : "
    )
    
    add_bullet(doc,
        "Région du sud-est marquant la transition entre les escarpements de la crête et les dépressions agro-pastorales chaudes "
        "du Kumoso. Alternance marquée de risques de crues de piémont et de déficits hydriques prolongés en fin de saison A. "
        "Seuil critique : 100 mm / 24 h. Cultures : riz de dépression, maïs, haricot, manioc et bananier.",
        bold_prefix="5. Rutana (Sud-Est et Dépression du Kumoso, 1 600–1 800 m) : "
    )
    
    headers_zones = ["Zone / Localité", "Identifiant Code", "Coordonnées GPS", "Altitude", "Topographie", "Seuil 24h", "Cultures Prévalentes Associées (ISABU)"]
    data_zones = [
        ["Bujumbura Mairie", "bujumbura", "-3.3819° N, 29.3614° E", "~820 m", "Plaine", "50.0 mm", "Riz, Maïs, Manioc, Bananier"],
        ["Buja Rural (Imbo)", "buja_rural_imbo", "-3.4292° N, 29.3165° E", "~850 m", "Plaine", "50.0 mm", "Riz, Maïs, Manioc, Bananier"],
        ["Buja Rural (Mumirwa)", "buja_rural_mumirwa", "-3.4389° N, 29.6944° E", "> 1 350 m", "Montagne", "100.0 mm", "Bananier, Maïs, Haricot, Manioc, Pomme de terre"],
        ["Gitega", "gitega", "-3.4271° N, 29.9246° E", "1 750 m", "Montagne", "100.0 mm", "Maïs, Haricot, Bananier, Riz, Patate douce, Pomme de terre"],
        ["Karusi", "karusi", "-3.1014° N, 30.1628° E", "1 600 m", "Montagne", "100.0 mm", "Maïs, Haricot, Bananier, Manioc, Patate douce"],
        ["Rutana", "rutana", "-3.9279° N, 29.9920° E", "1 700 m", "Montagne", "100.0 mm", "Riz, Maïs, Haricot, Manioc, Bananier"]
    ]
    add_table(doc, headers_zones, data_zones, col_widths=[2.8, 2.5, 3.2, 1.6, 1.8, 1.8, 4.3], caption="Tableau 1.1 — Caractérisation géographique et agro-climatique des zones pilotes d'étude")
    
    add_callout(doc,
        "Dans l'algorithme d'affectation de seuil (app/config.py), si une requête interroge 'buja_rural' sans préciser la sous-zone "
        "('imbo' ou 'mumirwa'), le système se rabat automatiquement sur la classe 'plaine' (seuil bas de 50 mm / 24h au lieu de 100 mm). "
        "Cette règle de précaution maximale garantit qu'un événement pluvieux critique en plaine côtière ne sera jamais minoré "
        "par un seuil de montagne trop tolérant.",
        title="Règle d'Ingénierie Préventive (Principe de Précaution) :"
    )
    
    # --- 2. Expression et analyse du besoin ---
    add_h2(doc, "2. Expression et Analyse du Besoin des Parties Prenantes")
    
    add_p(doc,
        "L'ingénierie des exigences a débuté par une étude minutieuse des attentes exprimées par les différentes strates "
        "d'acteurs intervenant dans la chaîne de valeur agro-climatique burundaise. Quatre grandes catégories d'utilisateurs ont été identifiées :"
    )
    
    headers_besoins = ["Catégorie d'Acteur", "Missions Principales", "Besoins Exprimés en Information", "Impact Attendu de la Solution"]
    data_besoins = [
        [
            "Petits Exploitants Vivriers",
            "Production familiale sur micro-parcelles collinaires (maïs, haricot, tubercules, bananier).",
            "Avis préventifs à 24-72h sur les fortes pluies (pour protéger les récoltes en séchage), le vent violent et les pauses de pluie prolongées.",
            "Réduction drastique des pertes post-récolte (moisissure des grains) et meilleure préservation des buttes culturales."
        ],
        [
            "Coopératives Agricoles (Riz, Café, Maraîchage)",
            "Gestion collective de bas-fonds irrigués, d'aires de séchage communautaires et d'intrants.",
            "Surveillance hydrologique des débits de rivières amont, alertes sur les surélévations de nappes et prévisions de vent pour les hangars.",
            "Coordination anticipée de la main-d'œuvre pour curer les canaux et consolider les diguettes avant l'arrivée des crues."
        ],
        [
            "Moniteurs Agricoles & DPAE (État)",
            "Encadrement technique collinaire, vulgarisation des bonnes pratiques et remontée d'alertes.",
            "Tableaux synthétiques par culture prévalente, traçabilité des indicateurs physiques bruts et des seuils réglementaires IGEBU.",
            "Gain de temps dans la diffusion des conseils techniques lors des tournées et ciblage précis des collines à surveiller."
        ],
        [
            "ONG & Gestionnaires d'Urgence",
            "Programmes de résilience communautaire, veille précoce, assistance humanitaire d'urgence.",
            "Vue comparative multi-zones, indicateurs probabilistes transparents, affichage explicite des limitations méthodologiques.",
            "Optimisation du pré-positionnement des stocks d'urgence (bâches, motopompes, semences de remplacement) avant les sinistres."
        ]
    ]
    add_table(doc, headers_besoins, data_besoins, col_widths=[3.0, 4.0, 5.5, 4.5], caption="Tableau 1.2 — Matrice des besoins exprimés par typologie d'utilisateurs")
    
    # --- 3. Personas et parcours utilisateurs détaillés ---
    add_h2(doc, "3. Modélisation des Personas et Parcours Utilisateurs")
    
    add_p(doc,
        "Afin de guider la conception de l'expérience utilisateur (UX) et des composants interactifs, trois personas représentatifs "
        "ont été élaborés avec leurs scénarios d'usage contextuels :"
    )
    
    add_h3(doc, "Persona 1 : Pierre Nkurunziza — L'Encadreur Agricole de Terrain")
    add_bullet(doc, "38 ans, résidant à Gitega, moniteur agricole communal rattaché à la DPAE.", bold_prefix="Profil : ")
    add_bullet(doc, "Smartphone Android d'entrée de gamme, forfait data mobile limité (recharges de 500 Mo), déplacements quotidiens à moto sur les collines.", bold_prefix="Équipement & Connectivité : ")
    add_bullet(doc, "Consulte l'application chaque matin à 6h30 avant sa tournée pour identifier les collines où les agriculteurs étalent leur maïs ou haricot en plein air et déterminer si un risque de pluie torrentielle justifie d'ordonner le bâchage immédiat.", bold_prefix="Objectif et Scénario : ")
    add_bullet(doc, "Les bulletins météo radio généralistes diffusent des prévisions nationales globales sans ancrage collinaire ni préconisation pour le séchage.", bold_prefix="Frustration majeure : ")
    
    add_h3(doc, "Persona 2 : Chantal Nibigira — La Présidente de Coopérative Rizicole")
    add_bullet(doc, "44 ans, gestionnaire d'une coopérative de 120 exploitants dans la plaine de l'Imbo (Bujumbura Rural).", bold_prefix="Profil : ")
    add_bullet(doc, "Smartphone milieu de gamme, connectivité 3G/4G intermittente.", bold_prefix="Équipement & Connectivité : ")
    add_bullet(doc, "A besoin d'une anticipation hydrologique de 24 à 48 heures lorsque des pluies massives sur les crêtes de Mumirwa menacent de faire gonfler brutalement la rivière Mugere, afin de mobiliser les riziculteurs pour fermer les vannes d'irrigation et consolider les levées de terre entourant les casiers.", bold_prefix="Objectif et Scénario : ")
    add_bullet(doc, "L'arrivée brutale des eaux de crue la nuit emporte régulièrement les diguettes fragiles et ensable les parcelles à quelques semaines de la récolte.", bold_prefix="Frustration majeure : ")
    
    add_h3(doc, "Persona 3 : Dr. Alexis Manirakiza — Le Chargé de Mission Humanitaire et de Veille")
    add_bullet(doc, "41 ans, expert en résilience climatique au sein d'un consortium d'ONG intervenant à Karusi et Rutana.", bold_prefix="Profil : ")
    add_bullet(doc, "Ordinateur portable et tablette tactile 4G professionnelle au bureau et en mission de terrain.", bold_prefix="Équipement & Connectivité : ")
    add_bullet(doc, "Consulte le tableau de bord pour comparer la situation agro-météorologique des différentes provinces et auditer la rigueur scientifique des modèles (vérification des seuils, des percentiles p75 et des sources de données Copernicus/Open-Meteo).", bold_prefix="Objectif et Scénario : ")
    add_bullet(doc, "Méfiance absolue envers les systèmes « boîte noire » qui délivrent des alertes anxiogènes sans en expliciter la chaîne de calcul ni les marges d'erreur.", bold_prefix="Frustration majeure : ")
    
    figure_1_2 = """
                    PARCOURS UTILISATEUR CIBLE — AGROMÉTÉO BURUNDI
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ 1. AUTHENTIFICATION SÉCURISÉE (/login ou /signup)                           │
  │    Saisie identifiant/mot de passe -> Échange OAuth2 Bearer -> Cookie JWT   │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ Redirection automatique si session valide
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ 2. SÉLECTION SPATIALE DE LA ZONE (/ d'accueil)                              │
  │    Carte Leaflet du Burundi (6 marqueurs) ou Grille latérale des 5 provinces │
  │    Choix de la sous-zone le cas échéant (Imbo plaine vs Mumirwa montagne)   │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ Clic marqueur -> Route /region/[slug]
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ 3. TABLEAU DE BORD AGRO-MÉTÉOROLOGIQUE (/region/[slug])                     │
  │    • Synthèse de vigilance (Bannière verte nominale ou ambre avec alerte)  │
  │    • Visualisation interactive svelteplot (T°C, Pluie, Rafales, Probabilité)│
  │    • Indicateurs statistiques automatiques (Min, Max, Moyenne)             │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ Filtrage dynamique
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ 4. CONSULTATION DES AVIS PAR CULTURE PRÉVALENTE (ISABU)                     │
  │    Filtres interactifs (par culture et par sévérité d'alerte)               │
  │    Lecture des messages d'action pragmatiques (« Protégez... », etc.)       │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ Clic « Mesures & limitations »
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ 5. AUDIT SCIENTIFIQUE ET LIMITATIONS DU MODÈLE (Fenêtre Modale)             │
  │    Jauges graphiques valeur/seuil (24h, 72h, vent, crues) + Avertissements │
  └─────────────────────────────────────────────────────────────────────────────┘
    """
    add_figure(doc, figure_1_2, caption="Figure 1.2 — Diagramme de flux du parcours utilisateur complet")
    
    # --- 4. Contraintes globales d'ingénierie ---
    add_h2(doc, "4. Contraintes Globales d'Ingénierie")
    
    add_p(doc,
        "Le projet est assujetti à un ensemble de contraintes sévères qui ont dicté les arbitrages d'architecture logicielle :"
    )
    
    add_bullet(doc,
        "L'application doit fonctionner de manière fluide sur des réseaux cellulaires 2G/3G burundais à fort taux de gigue "
        "et pertes de paquets. Elle doit minimiser la taille des requêtes HTTP et intégrer une politique agressive de mise en cache "
        "côté serveur afin de continuer à servir des bulletins valides en cas de déconnexion momentanée des flux internationaux.",
        bold_prefix="Contrainte de connectivité et de bande passante : "
    )
    
    add_bullet(doc,
        "En tant que prototype universitaire développé sans financement externe, le système doit reposer exclusivement sur "
        "des technologies open-source, des bases de données à palier gratuit sans carte bancaire requise (MongoDB Atlas Tier M0 Sandbox) "
        "et des API météorologiques gratuites sans clé commerciale bloquante (Open-Meteo, GloFAS via Copernicus).",
        bold_prefix="Contrainte d'accessibilité économique et données ouvertes : "
    )
    
    add_bullet(doc,
        "Le calendrier opérationnel du Projet II de l'UPG imposait une livraison de la première version exploitable en dix jours ouvrés "
        "(deux semaines). Ce rythme condensé excluait le développement d'architectures distribuées microservices surdimensionnées "
        "et imposait une focalisation stricte sur le cœur de valeur (BFF SvelteKit, FastAPI, moteur de règles pur).",
        bold_prefix="Contrainte temporelle serrée (délai de 2 semaines) : "
    )
    
    add_bullet(doc,
        "La base logicielle doit être conçue de façon modulaire et extensible, permettant d'accueillir ultérieurement les 18 provinces, "
        "de connecter des stations locales IGEBU et d'intégrer des passerelles de diffusion non-web (SMS/USSD).",
        bold_prefix="Contrainte d'extensibilité et d'évolutivité : "
    )
    
    # --- 5. Étude de faisabilité quadridimensionnelle ---
    add_h2(doc, "5. Étude de Faisabilité Multidimensionnelle")
    
    add_p(doc,
        "Conformément aux normes académiques du canevas Projet II de l'UPG, la viabilité du projet a fait l'objet d'une "
        "analyse d'ingénierie rigoureuse selon quatre dimensions :"
    )
    
    add_bullet(doc,
        "L'interopérabilité des composants logiciels modernes (SvelteKit 3, FastAPI, MongoDB Atlas, client Python openmeteo-requests "
        "et bibliothèque Sveaflet/Leaflet) a été validée expérimentalement. La séparation stricte entre les fonctions de calcul pur "
        "(sans état) et les routeurs d'accès aux données confère au système une testabilité et une robustesse exemplaires.",
        bold_prefix="1. Faisabilité Technique : "
    )
    
    add_bullet(doc,
        "L'ensemble de la pile technologique mise en œuvre est libre de droits de licence (licences MIT, Apache 2.0, BSD). "
        "Les coûts d'infrastructure récurrents pour le MVP sont strictement de zéro dollar ($0.00) grâce à l'exploitation des tiers "
        "gratuits dans le Cloud. Pour les utilisateurs finaux ruraux, le poids extrêmement compact de l'application (bundle < 250 Ko) "
        "engendre une consommation de données mobile insignifiante (inférieure à 1 Mo par consultation complète).",
        bold_prefix="2. Faisabilité Économique : "
    )
    
    add_bullet(doc,
        "L'ergonomie de l'interface a été épurée : navigation tactile immédiate depuis la carte d'accueil, bannières d'alerte aux "
        "codes couleurs univoques (vert / ambre), formulation pragmatique de chaque avis débutant par un verbe d'action de terrain "
        "(« Protégez... », « Surveillez... », « Vérifiez... ») bannissant tout jargon scientifique obscur.",
        bold_prefix="3. Faisabilité Opérationnelle : "
    )
    
    add_bullet(doc,
        "Le projet a résolu avec une rigueur absolue la délicate question de la frontière déontologique avec les services de l'État. "
        "Au Burundi, la délivrance des avis de vigilance officielle et les ordres d'alerte relèvent du monopole exclusif de l'IGEBU "
        "et de la Direction Générale de la Protection Civile. AgroMétéo Burundi se positionne explicitement comme un outil expérimental "
        "d'aide consultative collinaire. Dans l'ensemble du code source, les termes anxiogènes tels que « inondation certaine » ou "
        "« évacuation » sont formellement prohibés et remplacés par des consignes de vigilance ciblée (« vérifier l'état des diguettes »). "
        "De surcroît, le principe d'intégrité déontologique interdit formellement d'assimiler l'absence de données à une situation sans danger : "
        "toute donnée manquante génère le statut explicite 'non_evalue' avec une mise en garde formelle [5].",
        bold_prefix="4. Faisabilité Juridique, Éthique et Déontologique : "
    )
    
    # --- 6. Synthèse du diagnostic ---
    add_h2(doc, "6. Synthèse du Diagnostic")
    
    add_p(doc,
        "Le diagnostic approfondi confirme la pertinence et la faisabilité pleine et entière d'un système de veille agro-climatique "
        "au Burundi. En comblant le fossé entre les prévisions numériques globales et les décisions paysannes concrètes, AgroMétéo Burundi "
        "apporte une réponse logicielle pragmatique, économe en ressources et hautement sécurisée. Les chapitres suivants détaillent "
        "les fondements théoriques, la modélisation conceptuelle, l'implémentation effective et la validation expérimentale de cette solution."
    )
