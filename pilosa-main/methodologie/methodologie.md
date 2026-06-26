---
type: methodologie_charmaz
role: template_stable
description: |
  Document stable décrivant la méthode, les étapes, les règles de chaque
  agent Charmaz, et le mécanisme de reprise sur interruption.
  Complété au premier lancement, mis à jour si les paramètres changent.
  Les dossiers run_<horodatage>/ pointent vers ce fichier — ils n'en
  contiennent pas de copie.
created: 2026-06-22
updated: 2026-06-22
charmaz_ref: "Charmaz, K. (1996). Grounded Theory. In Smith, Harré & Van Langenhove (Eds.), Rethinking Methods in Psychology (pp. 27-49). Sage."
---

# Méthodologie — Analyse Charmaz du corpus d'entretiens

## 0. Identité du projet

| Champ | Valeur |
|---|---|
| Corpus source | `entretiens/` (lecture seule) |
| Formats acceptés | `.txt`, `.md`, `.docx` |
| Classeur de traçabilité | `methodologie/tracabilite.xlsx` (stable, cumulatif) |
| Fichier d'état | `methodologie/checkpoint.json` (machine) |
| Résumé humain | `methodologie/ETAT_AVANCEMENT.md` |
| Logs de session | `methodologie/run_<AAAAMMJJ_HHMM>/` |
| Mémos analytiques | `methodologie/memos/MEMO_NNNN_*.md` |
| Méthode | Théorie ancrée (Charmaz, 1996) |

---

## 1. Unité de découpage

**Unité retenue :** [À compléter au premier lancement — ex. : tour de parole, paragraphe, échange interviewer-interviewé]

**Conservation du contexte obligatoire** (p. 33) : chaque segment conserve le tour de parole précédent, le locuteur, et la position dans l'entretien. Un segment sans contexte n'est pas utilisable.

**Identifiants :** `SEG_NNNN` — séquence continue sur l'ensemble du corpus (pas par entretien).

---

## 2. Étapes et agents

### Étape 1 — Segmentation (Agent Lecture & Préparation)

- Lit `entretiens/`, découpe selon l'unité définie ci-dessus
- Alimente `00_Corpus_Source` et `01_Segments`
- Checkpoint : met à jour `etapes.segmentation.dernier_id_valide` après chaque `id_segment` validé

### Étape 2 — Codage initial (Agent Codage Initial)

- **L'agent LLM** applique les **deux jeux de questions** Charmaz sur chaque segment en utilisant son intelligence :
  - p. 38 (ancrage descriptif) → codes actifs au gérondif, **émergents du verbatim**
  - p. 39 (émergence des processus) → champ `processus_amorce`
- **Aucune règle regex, aucun code prédéfini.** Les codes émergent de l'analyse LLM du sens
- Alimente `02_Codage_Initial`
- Checkpoint : met à jour `etapes.codage_initial.dernier_id_valide` après chaque `id_code` validé

### Étape 3 — Codage focalisé (Agent Codage Focalisé)

- **L'agent LLM** analyse les codes initiaux, identifie les motifs récurrents et les regroupe par similarité sémantique
- Formule des codes focalisés plus abstraits, toujours actifs au gérondif
- **Aucun dictionnaire de mapping en dur** — les regroupements émergent de l'analyse LLM
- Alimente `03_Codage_Focalise`
- Checkpoint : met à jour `etapes.codage_focalise.dernier_id_valide`

### Étape 4 — Catégorisation (Agent Catégorisation)

- **L'agent LLM** analyse les codes focalisés et les élève au rang de catégories
- Pour chaque catégorie, applique les **4 opérations** (propriétés, conditions, conséquences, relations, p. 41) via un raisonnement LLM
- Distingue les **3 types** (in vivo / théorique / substantif, p. 41)
- Applique les **questions de processus** (p. 39) comme moteur de montée en abstraction
- Vérifie la **contrainte sensitizing concepts** sur chaque catégorie
- **Aucune catégorie prédéfinie** — elles émergent de l'analyse LLM
- Alimente `04_Categories`
- Checkpoint : met à jour `etapes.categorisation.dernier_id_valide`

### Étape 5 — Comparaison constante (Agent Comparaison Constante)

- Applique les **3 types de comparaison** (p. 42) : personnes différentes / même personne dans le temps / catégorie vs catégorie
- Alimente `05_Comparaisons`
- Checkpoint : met à jour `etapes.comparaison_constante.dernier_id_valide`

### Étape 6 — Mémos (Agent Mémos)

- Rédige les mémos analytiques dans `methodologie/memos/MEMO_NNNN_*.md`
- Registre dans `06_Memos`
- Checkpoint : met à jour `etapes.memos.dernier_id_valide`

### Étape 7 — Échantillonnage théorique (Agent Échantillonnage Théorique)

- Identifie les lacunes des catégories et désigne des segments existants à relire
- **Corpus clos** : aucune collecte nouvelle — réexploitation analytique uniquement
- Propriétés non saturables signalées comme `LIMITE_SIGNALEE`
- Alimente `07_Echantillonnage_Theorique`
- Checkpoint : met à jour `etapes.echantillonnage_theorique.dernier_id_valide`

### Étape 8 — Construction thèmes & théorie (Agent Construction Thèmes & Théorie)

- Agrège catégories → sous-thèmes → grands thèmes avec règles de regroupement tracées
- Identifie les processus génériques
- Formule les énoncés théoriques avec ancrage jusqu'au verbatim
- Alimente `08_Construction_Themes` et `09_Theorie_Finale`
- Checkpoint : met à jour `etapes.construction_themes.dernier_id_valide` puis `etapes.theorie_finale.dernier_id_valide`

### Étape 9 — Vérification & Traçabilité (Agent Vérification)

- Vérifie le chaînage complet (aucun orphelin), les codes actifs, les 4 opérations, les sensitizing concepts
- Alimente `10_Journal_Tracabilite`
- **Seul cet agent peut passer `statut` à `"termine"` dans `checkpoint.json`**, après certification complète

---

## 3. Règles transversales

- **Analyse par agents LLM uniquement** — aucun script Python ne contient de règles de codage, de dictionnaires de mapping ou de catégories prédéfinies. Les scripts sont limités à l'infrastructure (I/O Excel, checkpoint).
- **Émergence réelle** — les codes, codes focalisés et catégories doivent varier selon le contenu des verbatims. La répétition mécanique des mêmes libellés est un signal d'alerte.
- **Codes actifs au gérondif sans exception** — pas de code statique ou nominal
- **In vivo signalé** (`in_vivo: oui`) quand le terme vient du participant
- **Sensitizing concepts comme points de départ** (Charmaz, p. 32 n.2 ; Glaser, p. 38) — jamais plaqués comme cadre
- **Comparaison constante transversale** — moteur de tout l'analyse
- **Revue de littérature reportée** après l'analyse conceptuelle (p. 47)
- **Aucune donnée inventée** — tout énoncé remonte jusqu'à un `id_segment` réel
- **Tout output = fichier** — aucune réponse inline

---

## 4. Reprise et persistance

### 4.1 Architecture des chemins

| Rôle | Chemin | Nature |
|---|---|---|
| Classeur de traçabilité | `methodologie/tracabilite.xlsx` | Stable, cumulatif — ne pas déplacer |
| Checkpoint machine | `methodologie/checkpoint.json` | Stable, mis à jour après chaque écriture |
| Résumé humain | `methodologie/ETAT_AVANCEMENT.md` | Stable, régénéré à chaque lancement |
| Mémos analytiques | `methodologie/memos/` | Stable, fichiers ajoutés au fil de l'analyse |
| Logs de session | `methodologie/run_<AAAAMMJJ_HHMM>/` | Par session — pointe vers les fichiers stables |

Les dossiers `run_<horodatage>/` contiennent uniquement :
- `run_info.json` — métadonnées de la session (horodatage démarrage, agent, cause_arret)
- `session_log.md` — log textuel de la session (non critique)

### 4.2 Comportement au lancement

L'orchestrateur Charmaz lit `methodologie/checkpoint.json` en premier :

| Cas | Comportement |
|---|---|
| Fichier inexistant | Démarrage propre — initialiser checkpoint, créer tracabilite.xlsx |
| `statut: "a_faire"` | Démarrage propre |
| `statut: "termine"` | Afficher le résumé final, ne rien relancer sans instruction explicite |
| `statut: "en_cours"` ou `"interrompu"` | Afficher le résumé ETAT_AVANCEMENT.md, reprendre au `dernier_id_valide` de chaque étape |

**Comportement par défaut : `interrompu`.** Tout lancement qui n'atteint pas le marqueur explicite de fin de l'Agent Vérification laisse le statut à `interrompu` au prochain lancement.

### 4.3 Protocole d'écriture incrémentale

Chaque agent applique ce protocole pour chaque lot d'identifiants :

```
1. Vérifier que l'id à écrire n'existe pas déjà dans le classeur
   (idempotence — comparer avec les id déjà présents dans l'onglet cible)
2. Préparer la ou les lignes dans un buffer en mémoire
3. Écrire dans tracabilite.xlsx.tmp (copie temporaire du xlsx courant + nouvelles lignes)
4. Si l'écriture réussit → remplacer tracabilite.xlsx par tracabilite.xlsx.tmp (atomique)
5. Supprimer tracabilite.xlsx.tmp
6. Mettre à jour checkpoint.json :
   - dernier_heartbeat ← maintenant
   - etapes.<etape>.dernier_id_valide ← dernier id écrit
   - etapes.<etape>.nb_valides ← incrémenter
   - Pour les segments : corpus.entretiens[i].dernier_segment_valide ← dernier SEG écrit
7. Régénérer ETAT_AVANCEMENT.md depuis checkpoint.json
```

**Si le processus est tué entre les étapes 4 et 6 :** le classeur est à jour mais le checkpoint est périmé. Au redémarrage, l'agent relit le classeur pour reconstruire le dernier id réellement présent, puis met à jour le checkpoint.

### 4.4 Idempotence des identifiants

Les identifiants sont **déterministes** : le même segment source (même `id_entretien` + même `position_ligne`) produit toujours le même `id_segment`. Algorithme recommandé :

```
SEG_NNNN où NNNN = numéro de séquence global calculé lors du premier parcours du corpus
          et conservé dans checkpoint.json
```

Avant toute écriture, chaque agent vérifie si l'identifiant cible existe déjà dans l'onglet correspondant du classeur. Si oui → saut sans erreur (comportement idempotent). Si non → écriture.

### 4.5 Détection de la dernière unité incomplète

Si le processus est interrompu en plein milieu du traitement d'un segment :
- Le segment peut être partiellement écrit dans le classeur (1 code sur 3 écrits)
- Au redémarrage, l'agent relit le classeur et identifie le dernier `id_segment` traité
- Si ce segment n'a pas tous ses codes attendus → il est retraité depuis le début (les codes déjà présents sont sautés par idempotence)
- Si le segment est complet → l'agent passe au suivant

### 4.6 Marqueur de fin propre

Seul l'Agent Vérification & Traçabilité peut écrire `"statut": "termine"` dans checkpoint.json, et seulement après :
- Avoir certifié l'intégralité des 7 contrôles
- Avoir vérifié le chaînage de bout en bout (segment → code → catégorie → thème → théorie)
- Avoir écrit le rapport final dans `agent_reports/verification_charmaz_<horodatage>.md`

### 4.7 Script de gestion du classeur

Le script `methodologie/gerer_tracabilite.py` fournit les fonctions et commandes CLI pour les agents :

**Fonctions Python :**
- `creer_classeur()` — crée `tracabilite.xlsx` avec les 11 onglets vides si absent
- `lire_derniers_ids(onglet)` — retourne l'ensemble des ids déjà présents dans un onglet
- `ecrire_lignes_atomique(onglet, lignes)` — écriture .tmp → replace atomique
- `reconstruire_checkpoint()` — relit le classeur et met à jour checkpoint.json en cas de divergence

**Commandes CLI (utilisées par les agents LLM) :**
- `--read-sheet NAME` — lit un onglet et affiche en JSON
- `--write-sheet NAME --data '{}'` — écrit une ligne depuis un dictionnaire JSON
- `--get-ids NAME` — liste les IDs d'un onglet
- `--next-id NAME` — calcule le prochain ID disponible
- `--list-sheets` — liste les onglets avec leur nombre de lignes
- `--status` — affiche l'état du checkpoint

---

## 5. Fichier script de gestion (`gerer_tracabilite.py`)

Voir `methodologie/gerer_tracabilite.py` — module Python autonome, dépendances : `openpyxl`.

```
pip install openpyxl
python methodologie/gerer_tracabilite.py --init       # Créer le classeur vide
python methodologie/gerer_tracabilite.py --check      # Reconstruire checkpoint depuis le classeur
python methodologie/gerer_tracabilite.py --status     # Afficher l'état courant
```
