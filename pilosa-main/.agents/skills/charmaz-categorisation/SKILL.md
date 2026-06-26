---
name: charmaz-categorisation
type: skill
scope: categorisation_charmaz
description: Fallback pour pilosa-charmaz-categorisation — élévation des codes focalisés en catégories avec les 4 opérations obligatoires (propriétés, conditions, conséquences, relations), 3 types (in vivo / théorique / substantif), questions de processus p. 39, contrainte sensitizing concepts, alimentation de 04_Categories
created: 2026-06-22
updated: 2026-06-22
charmaz_ref: "pp. 40-41"
---

## Purpose

Élever les codes focalisés au rang de **catégories analytiques**. Chaque catégorie doit être documentée selon les **4 opérations de Charmaz** (propriétés, conditions, conséquences, relations), typée (in vivo / théorique / substantif), et examinée pour son potentiel de **processus générique**. Aucune catégorie ne peut être importée d'un cadre théorique préexistant sans émergence réelle depuis les données.

> *« As you raise the code to a category, you begin (1) to explicate its properties, (2) to specify conditions under which it arises, is maintained and changes, (3) to describe its consequences and (4) to show how this category relates to other categories. »* (Charmaz, p. 41)

## Prerequisites

- `03_Codage_Focalise` est alimenté
- `02_Codage_Initial` est accessible (pour relire les `processus_amorce`)
- `01_Segments` est accessible (pour relire les verbatims)

## Steps

### A — Regroupement des codes focalisés

Regrouper les codes focalisés ayant des `processus_amorce_synthetise` compatibles. Ce regroupement est la matière première d'une catégorie.

### B — Montée en catégorie avec les questions de processus (p. 39)

Pour chaque cluster candidat à une catégorie, se poser les 5 questions :

| # | Question | Produit pour la catégorie |
|---|---|---|
| 1 | What process is at issue here? | Nom et définition de la catégorie |
| 2 | Under which conditions does this process develop? | `conditions_apparition` |
| 3 | How does the research participant think, feel and act while involved? | `proprietes` et `verbatim_illustratif` |
| 4 | When, why and how does the process change? | `conditions_maintien` et `conditions_changement` |
| 5 | What are the consequences of the process? | `consequences` |

### C — Les 4 opérations obligatoires (p. 41)

Toutes les quatre sans exception :

1. **Propriétés** — caractéristiques et dimensions distinctives de la catégorie
2. **Conditions** — apparition / maintien / changement
3. **Conséquences** — effets en aval, sur les participants ou d'autres processus
4. **Relations** — liens avec d'autres catégories (subsomption, tension, renforcement)

Si une opération est impossible à renseigner faute de données → signaler comme `LIMITE_SIGNALEE` dans `10_Journal_Tracabilite`, pas laisser vide.

### D — Typage (p. 41)

| Type | Critère |
|---|---|
| `in_vivo` | Expression reprise directement du discours des participants |
| `theorique` | Définition théorique du chercheur des actions/événements |
| `substantif` | Réalités substantielles des participants, nommées par le chercheur |
| `sensitizing_concept_non_confirme` | Concept disciplinaire de départ non encore confirmé par les données — déclenche un contrôle Agent Vérification |

### E — Test sensitizing concepts (CONTRAINTE OBLIGATOIRE) (pp. 32, 38)

Pour chaque catégorie, répondre à : « Cette catégorie est-elle issue des données ou d'un cadre préexistant ? »

| Résultat | Valeur `test_sensitizing_concept` | Condition |
|---|---|---|
| Émergée des données | `EMERGE_DES_DONNEES` | ≥ 3 `id_segment` dans `ancrage_empirique` |
| Sensitizing concept converti | `SENSITIZING_CONVERTI` | Codes initiaux réels l'ont validé — documenter lesquels |
| Violation | `VIOLATION_IMPORTATION` | Concept disciplinaire sans codes initiaux réels → entrée immédiate dans `10_Journal_Tracabilite` |

### F — Test processus générique (p. 41)

La catégorie est-elle transversale à plusieurs entretiens, situations, voire applicable au-delà du corpus ? Si oui → `processus_generique: oui` + justification.

### G — Écriture dans `04_Categories`

Colonnes : `id_categorie` (CAT_NNNN), `nom_categorie`, `type`, `liste_id_code_focalise`, `proprietes`, `conditions_apparition`, `conditions_maintien`, `conditions_changement`, `consequences`, `relations_autres_categories`, `processus_generique`, `ancrage_empirique`, `test_sensitizing_concept`, `verbatim_illustratif`.

Appender une entrée dans `10_Journal_Tracabilite` par catégorie (type_operation: `creation_categorie`, violations: aucune ou VIOLATION_IMPORTATION / OPERATION_MANQUANTE).

## Rules

- **4 opérations toutes obligatoires.** Catégorie incomplète = violation signalée.
- **Questions p. 39 comme moteur principal.** Les questions de la p. 38 peuvent être relues sur les verbatims pour affiner les propriétés.
- **Test sensitizing concepts sans exception.** Sur chaque catégorie créée.
- **Ancrage empirique minimum : 3 segments.** `ancrage_empirique` ≠ vide.
- **`VIOLATION_IMPORTATION` n'est pas masquable.** Signaler et laisser l'Agent Vérification décider.
- **Noms de catégories actifs.** Gérondif ou processus (« éviter de… », « gérer le… », « se maintenir en… »).
- **Tout output = fichier.**

## Reprise sur interruption

Avant de commencer, lire `methodologie/checkpoint.json` → `etapes.categorisation.dernier_id_valide`. Reprendre au code focalisé suivant. Vérifier idempotence sur `id_categorie` (1 catégorie à la fois — étape lente). Écriture atomique après chaque catégorie. Voir `charmaz-checkpoint` pour le protocole complet.

## See also

- `charmaz-checkpoint` — protocole de reprise et écriture atomique (obligatoire)
- `charmaz-codage-focalise` — source des codes focalisés
- `charmaz-comparaison-constante` — moteur de vérification et raffinement des catégories
- `charmaz-memos` — documente le raisonnement catégoriel
- `charmaz-verification` — contrôle 4 opérations + test sensitizing concepts
- `methodologie/01_synthese_charmaz.md` §§ 2.4, 2.5 — questions p. 39 et contrainte sensitizing concepts
