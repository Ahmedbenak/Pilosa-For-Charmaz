---
name: charmaz-verification
type: skill
scope: tracabilite_verification_charmaz
description: Fallback pour pilosa-charmaz-verification — gardien de la traçabilité sans orphelin (chaînage complet des id), codes actifs au gérondif, 4 opérations sur chaque catégorie, contrainte sensitizing concepts, aucun verbatim hors corpus, alimentation de 10_Journal_Tracabilite
created: 2026-06-22
updated: 2026-06-22
charmaz_ref: "pp. 32, 38, 41 — principe de traçabilité"
---

## Purpose

Vérifier à chaque étape la rigueur méthodologique et la traçabilité sans orphelin. Deux responsabilités cardinales : (1) tout `id` référencé en aval doit exister en amont ; (2) chaque règle Charmaz (codes actifs, 4 opérations, sensitizing concepts) est contrôlée. Ne crée aucune donnée. Ne corrige pas. Signale et bloque ou certifie.

## Prerequisites

- Le classeur `methodologie/run_<horodatage>/tracabilite.xlsx` est accessible avec les onglets concernés

## Steps — 7 contrôles

### Contrôle 1 — Chaînage des identifiants (aucun orphelin)

| Référence | Doit exister dans |
|---|---|
| `id_entretien` dans `01_Segments` | `00_Corpus_Source` |
| `id_segment` dans `02_Codage_Initial` | `01_Segments` |
| `id_code` dans `03_Codage_Focalise` (`liste_id_code`) | `02_Codage_Initial` |
| `id_code_focalise` dans `04_Categories` (`liste_id_code_focalise`) | `03_Codage_Focalise` |
| `id_categorie` dans `05_Comparaisons` | `04_Categories` |
| `id_categorie` et `id_segment` dans `06_Memos` | `04_Categories` et `01_Segments` |
| `id_categorie` et `id_segment` dans `07_Echantillonnage_Theorique` | `04_Categories` et `01_Segments` |
| `id_categorie` dans `08_Construction_Themes` (`id_categorie_sources`) | `04_Categories` |
| `id_theme` dans `09_Theorie_Finale` (`id_theme_sources`) | `08_Construction_Themes` |

**Tout `id` orphelin = VIOLATION + blocage de la progression.**

### Contrôle 2 — Aucun verbatim hors corpus

Tout verbatim cité dans `06_Memos` ou `09_Theorie_Finale` doit être retrouvable dans `texte_verbatim` de `01_Segments`. Un verbatim non retrouvable = **VIOLATION : verbatim hors corpus**.

### Contrôle 3 — Codes actifs au gérondif

Dans `02_Codage_Initial`, chaque `texte_code` répond à « qu'est-ce qui se passe ici ? » par une action ou un processus observable dans le verbatim. Un code nominal théorique non ancré = **VIOLATION : code non actif**.

### Contrôle 4 — 4 opérations sur chaque catégorie (p. 41)

Dans `04_Categories` : `proprietes`, `conditions_*`, `consequences`, `relations_autres_categories` tous renseignés (≠ vide). Champ vide = **VIOLATION : operation_manquante** (préciser laquelle).

### Contrôle 5 — Contrainte sensitizing concepts (CRITIQUE) (pp. 32, 38)

Dans `04_Categories`, vérifier `test_sensitizing_concept` :

| Valeur | Action de vérification |
|---|---|
| `EMERGE_DES_DONNEES` | `ancrage_empirique` contient ≥ 3 `id_segment` existants → CERTIFIE si ok |
| `SENSITIZING_CONVERTI` | Les codes initiaux de l'`ancrage_empirique` existent dans `02_Codage_Initial` → CERTIFIE si ok |
| `VIOLATION_IMPORTATION` | Confirmer + bloquer progression vers `08_Construction_Themes` |
| `sensitizing_concept_non_confirme` | Si `ancrage_empirique` vide → VIOLATION_IMPORTATION ; si renseigné → reclassifier et certifier |
| Absent / vide | VIOLATION : test_sensitizing_concept_absent |

**Aucune catégorie avec `VIOLATION_IMPORTATION` non résolue ne peut alimenter `08_Construction_Themes`.**

### Contrôle 6 — Cheminement de thématisation tracé

Dans `08_Construction_Themes` : `regle_regroupement` renseignée, `id_categorie_sources` existants dans `04_Categories`, `justification_regroupement` référençant un `id_comparaison` ou `id_memo`. Thème sans règle documentée = **VIOLATION : thematisation_non_tracee**.

### Contrôle 7 — Cohérence de la théorie finale

Dans `09_Theorie_Finale` : chaque `id_enonce` référence des `id_theme` existants et est traceable jusqu'à des verbatims dans `01_Segments`. Énoncé sans ancrage = **VIOLATION : theorie_non_tracee**.

## Output

Pour chaque contrôle, écrire dans `10_Journal_Tracabilite` :

| Champ | Valeur |
|---|---|
| `id_decision` | `DEC_NNNN` |
| `agent` | `pilosa-charmaz-verification` |
| `horodatage` | timestamp ISO |
| `type_controle` | `orphelin` / `verbatim_hors_corpus` / `code_non_actif` / `operation_manquante` / `sensitizing_concepts` / `thematisation` / `theorie` |
| `id_element_verifie` | `id_code`, `id_categorie`, etc. |
| `resultat` | `CERTIFIE` / `VIOLATION` / `LIMITE_SIGNALEE` |
| `details` | Description précise |
| `action_requise` | Ce que l'agent amont doit corriger, ou `aucune` |

Rapport de vérification → `agent_reports/verification_charmaz_<horodatage>.md`.

## Rules

- **Ne jamais cacher une violation.** Chaque anomalie = entrée dans `10_Journal_Tracabilite`.
- **Ne jamais corriger à la place de l'agent amont.** Signaler, pas réécrire.
- **Ne jamais inventer de données de remplacement.** `id_segment` manquant = violation signalée telle quelle.
- **Bloquer sur violation non résolue.** Aucun onglet aval alimenté si orphelin ou VIOLATION_IMPORTATION existe en amont.
- **`LIMITE_SIGNALEE` pour les lacunes du corpus.** Propriété non saturable faute de données = limite documentée, pas violation.
- **Vérification à chaque étape, pas seulement à la fin.**
- **Tout output = fichier.**

## Reprise sur interruption et marqueur de fin

Avant de commencer, lire `checkpoint.json` → `etapes.verification.dernier_id_valide`. Reprendre au contrôle suivant. Vérifier idempotence sur `id_decision`.

**Seul cet agent peut marquer l'analyse comme `termine`.** Après certification des 7 contrôles, appeler `marquer_termine()` depuis `methodologie/gerer_tracabilite.py`. Si des violations non résolues subsistent, NE PAS appeler `marquer_termine()` — laisser `interrompu`.

Voir `charmaz-checkpoint` pour le protocole complet.

## See also

- `charmaz-checkpoint` — protocole de reprise, écriture atomique, marqueur de fin (obligatoire)
- Tous les agents Charmaz — cet agent est appelé après chaque onglet complété
- `charmaz-categorisation` — source principale des violations sensitizing concepts
- `charmaz-construction-themes` — conditionnée par les certifications de cet agent
