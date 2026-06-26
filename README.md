================================================================================
                               PILOSA
                Framework de recherche qualitative assisté par IA
================================================================================

Auteur : Tommaso Prinetti
Licence : PolyForm Noncommercial License 1.0.0
Site    : https://github.com/TommasoPrinetti/pilosa

--------------------------------------------------------------------------------
1. DESCRIPTION GÉNÉRALE
--------------------------------------------------------------------------------

Pilosa est un framework open-source conçu pour la recherche qualitative
assistée par intelligence artificielle. Il transforme un dossier de
documents sources (PDF, notes, entretiens, textes, etc.) en une carte de
connaissances interrogeable, indexée par en-têtes et lisible par des agents
LLM (Large Language Models).

L'objectif principal de Pilosa est de permettre aux chercheurs en sciences
humaines et sociales de mener des analyses qualitatives rigoureuses à
l'aide d'agents IA spécialisés, tout en conservant une traçabilité complète
et une séparation stricte entre les données sources et les fichiers de
travail.

Fonctionnalités principales :

- Création d'un espace de travail (workspace) isolé à partir d'un corpus
  source
- Importation de fichiers aux formats multiples (txt, md, csv, json, pdf,
  images via OCR, etc.)
- Indexation automatique et génération de cartes de navigation avec
  wikilinks Obsidian
- Pipeline d'agents spécialisés pour la recherche, l'analyse, la synthèse
  et la vérification d'informations
- Intégration native de la méthodologie de théorisation ancrée (Grounded
  Theory) de Kathy Charmaz
- Dashboard interactif en ligne de commande
- Fonctionne avec Claude Code, Codex, OpenCode et d'autres CLI LLM


--------------------------------------------------------------------------------
2. FONCTIONNEMENT DÉTAILLÉ
--------------------------------------------------------------------------------

2.1. Installation
~~~~~~~~~~~~~~~~~~~

Pilosa s'installe avec une commande unique sans aucune dépendance :

    curl -fsSL https://github.com/TommasoPrinetti/pilosa/releases/.../install.sh | bash

Le framework est livré sous forme d'archive signée avec vérification de
checksum SHA-256. Aucun npm, Python, Go ou Homebrew n'est requis pour
l'installation.

L'installateur crée :
- ~/.pilosa/          : répertoire d'installation (framework + binaires)
- ~/.local/bin/pilosa : point d'entrée CLI
- Binaires optionnels  : Gum (interface interactive), RapidOCR (OCR PDF/image)


2.2. Création d'un espace de travail (Workspace)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La commande `pilosa new /chemin/vers/mes-sources` déclenche le processus
d'onboarding complet :

  1. Sélection du corpus  : pointage vers le dossier source
  2. Création du workspace : un dossier <nom>-pilosa/ est créé
  3. Scan du corpus        : comptage et classification des fichiers par type
  4. Import par lot        : choix interactif des types de fichiers à importer
  5. Traitement PDF        : conversion en Markdown via pdftotext ou OCR
  6. Copie dans raw/       : les fichiers sources sont copiés à l'identique
     dans le dossier raw/ du workspace. Le dossier source original reste
     la référence immuable.
  7. Génération d'un prompt de démarrage copié dans le presse-papiers


2.3. Architecture du workspace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Une fois créé, un workspace Pilosa a la structure suivante :

  workspace/
  ├── AGENTS.md              : Contrat de routage principal
  ├── CLAUDE.md              : Instructions pour les agents LLM
  ├── .bin/                  : Scripts CLI
  ├── .agents/               : Définitions canoniques des agents et skills
  ├── .opencode/             : Miroirs générés pour OpenCode
  ├── .claude/               : Miroirs générés pour Claude Code
  ├── .codex/                : Miroirs générés pour Codex
  ├── system/                : Configuration, contexte, dictionnaire, index
  │   ├── context.md         : Contexte du projet
  │   ├── configuration.md   : Profil de fonctionnement
  │   ├── startup.md         : Protocole de démarrage
  │   ├── dictionary.md      : Vocabulaire partagé
  │   ├── yaml_header_template.md : Schéma des en-têtes YAML
  │   └── workspace_index.md : Index maître du workspace
  ├── raw/                   : Corpus de travail (copies des sources)
  ├── maps/                  : Cartes de navigation (wikilinks Obsidian)
  ├── logs/                  : Journaux des requêtes et sessions
  ├── agent_reports/         : Rapports produits par les agents
  └── .trash/                : Fichiers retirés du corpus


2.4. Pipeline d'agents (Orchestrateur)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le coeur de Pilosa est son orchestrateur. Chaque requête du chercheur est
classifiée puis routée à travers une chaîne d'agents spécialisés :

  1. pilosa-searcher    : Recherche les preuves dans les cartes, fichiers
                          bruts et le dictionnaire
  2. pilosa-mapper      : Lecture par lots et extraction de fragments pour
                          les cartes de navigation
  3. pilosa-serendippo  : Découverte holistique de connexions transversales
  4. pilosa-analyst     : Analyse contextuelle élargie
  5. pilosa-writer      : Synthèse des résultats en rapports structurés
  6. pilosa-verifier    : Vérification des citations, chemins et rapports
  7. pilosa-janitor     : Nettoyage et archivage des fichiers obsolètes

Les classes de requêtes sont :
  - fast_path           : Réponse opérationnelle directe
  - clarify_search      : Traduction de termes avant recherche
  - find_material       : Recherche de contenu existant
  - evidence_answer     : Réponse fondée sur les sources
  - synthesis_report    : Rapport structuré / comparaison / narration
  - verification        : Vérification de citation, chemin ou rapport
  - index_maintenance   : Mise à jour de l'index du workspace
  - cleanup             : Nettoyage du workspace
  - deep_index          : Ré-indexation approfondie du corpus
  - serendipity         : Découverte de connexions cachées
  - charmaz_pipeline    : Pipeline complet d'analyse Charmaz


2.5. Méthodologie Charmaz (Grounded Theory)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pilosa intègre une implémentation complète de la méthodologie de théorisation
ancrée (Grounded Theory) de Kathy Charmaz (1996), divisée en 9 étapes :

  Étape 1  - Segmentation      : Découpage du corpus en unités d'analyse
  Étape 2  - Codage initial    : Codes émergents au gérondif
  Étape 3  - Codage focalisé   : Regroupement sémantique des codes
  Étape 4  - Catégorisation    : Élévation en catégories conceptuelles
  Étape 5  - Comparaison       : Comparaison constante (3 types)
  Étape 6  - Mémos             : Rédaction de mémos analytiques
  Étape 7  - Échantillonnage   : Échantillonnage théorique (corpus clos)
  Étape 8  - Thèmes & Théorie  : Construction des thèmes et théorie finale
  Étape 9  - Vérification      : Traçabilité et certification complète

Les données de traçabilité sont stockées dans :
  - methodologie/checkpoint.json  : État machine (reprise sur interruption)
  - methodologie/tracabilite.xlsx : Classeur de suivi (11 onglets)
  - methodologie/ETAT_AVANCEMENT.md : Résumé humain de la progression
  - methodologie/gerer_tracabilite.py : Script de gestion atomique


2.6. Intégration Obsidian
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les cartes de navigation (maps/) utilisent le format de wikilinks d'Obsidian
([[raw/fichier]]), permettant de visualiser le graphe de connaissances et
les connexions entre les documents sources directement dans Obsidian.


2.7. Modèle de sécurité
~~~~~~~~~~~~~~~~~~~~~~~~~

Pilosa est conçu avec une approche paranoïaque de la chaîne d'approvisionnement
(supply-chain security) :

  - Version épinglée : l'installateur utilise une version stable spécifique,
    pas "latest"
  - Vérification SHA-256 : l'archive du framework et les binaires sont
    vérifiés par checksum
  - Âge minimum des releases : possibilité de rejeter les releases trop
    récentes (prévention zero-day)
  - Mode verify-only : audit d'une installation existante sans réinstallation
  - Zéro dépendances : pas de npm, Python, Java, Go ou Homebrew dans le
    noyau d'installation


--------------------------------------------------------------------------------
3. COMMANDES PRINCIPALES
--------------------------------------------------------------------------------

  pilosa                    : Dashboard interactif
  pilosa new <chemin>       : Créer un nouveau workspace
  pilosa onboard <workspace>: Ré-exécuter l'onboarding
  pilosa update <workspace> : Mettre à jour les fichiers framework
  pilosa check <workspace>  : Valider l'intégrité du workspace
  pilosa sync               : Synchroniser les miroirs d'agents et skills
  pilosa upgrade            : Mettre à jour Pilosa
  pilosa health             : Vérifier la santé du système
  pilosa uninstall          : Désinstaller Pilosa


--------------------------------------------------------------------------------
4. DÉVELOPPEMENT
--------------------------------------------------------------------------------

  git clone https://github.com/TommasoPrinetti/pilosa.git
  cd pilosa

  Branche main : framework stable (releases taguées)
  Branche dev  : développement actif

  Tests : bash tests/test_cli.sh

  Contribution : les modifications du framework vont sur dev ou une branche
  feature. Les scripts .bin/ doivent rester en bash pur, zéro dépendance.


--------------------------------------------------------------------------------
5. LICENCE
--------------------------------------------------------------------------------

PolyForm Noncommercial License 1.0.0 - Voir le fichier LICENSE pour les
détails complets. Usage libre pour la recherche, l'éducation et les
organisations à but non lucratif.
