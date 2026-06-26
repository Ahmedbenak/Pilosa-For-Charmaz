---
name: charmaz-comparaison-constante
type: skill
scope: constant_comparison_charmaz
description: Fallback pour pilosa-charmaz-comparaison-constante — 3 types de comparaison (personnes différentes / même personne dans le temps / catégorie vs catégorie, p. 42), moteur transversal de la catégorisation et de la thématisation, alimentation de 05_Comparaisons
created: 2026-06-22
updated: 2026-06-22
charmaz_ref: "p. 42 — constant comparison"
---

## Purpose

Appliquer la **comparaison constante** comme moteur transversal de l'analyse. La comparaison n'est pas une étape séparée : elle alimente la catégorisation, affine les propriétés, identifie les variations, et prépare la thématisation. Trois types de comparaison sont définis par Charmaz (p. 42). Alimenter `05_Comparaisons`.

> *« Grounded theorists use constant comparative methods throughout the research process. »* (Charmaz, p. 42)

## Prerequisites

- `04_Categories` contient au moins 3 catégories documentées
- `01_Segments` est accessible pour les verbatims
- `02_Codage_Initial` et `03_Codage_Focalise` sont accessibles

## Steps

### Les 3 types de comparaison (p. 42)

**Type 1 — Comparaison entre personnes différentes**

Comparer comment différents participants (entretiens distincts) vivent ou expriment un même processus ou une même catégorie :
- Sélectionner une catégorie (`id_categorie`)
- Identifier tous les segments (`id_segment`) qui s'y rattachent, sur des entretiens distincts
- Comparer : mêmes propriétés ? conditions différentes ? conséquences différentes ?
- Résultat : confirmation / variation / infirmation des propriétés de la catégorie

**Type 2 — Comparaison de la même personne à des moments différents**

Si un participant apparaît à plusieurs moments du corpus (ou si le corpus contient des données longitudinales) :
- Identifier les segments du même `id_entretien` à des positions différentes
- Comparer les processus exprimés : évolution, contradiction, stabilité
- Résultat : propriétés de changement et de maintien pour la catégorie

**Type 3 — Comparaison de catégorie à catégorie**

Mettre en relation deux catégories ou plus pour identifier :
- Lesquelles se subsument (l'une est un cas particulier de l'autre)
- Lesquelles sont en tension ou se contradisent
- Lesquelles se renforcent ou co-apparaissent systématiquement
- Résultat : `relations_autres_categories` dans `04_Categories` + fondement de la thématisation

### Écriture dans `05_Comparaisons`

Pour chaque comparaison effectuée, écrire une ligne :

| Champ | Contenu |
|---|---|
| `id_comparaison` | `CMP_NNNN` |
| `type_comparaison` | `type1_personnes` / `type2_temps` / `type3_categories` |
| `elements_compares` | Références des éléments (`id_categorie`, `id_segment`, `id_entretien`) |
| `question_posee` | La question analytique ayant motivé la comparaison |
| `resultat` | Ce que la comparaison a révélé (confirmation / variation / infirmation) |
| `impact_sur_categorie` | Modification des propriétés, conditions, conséquences ou relations d'une catégorie |
| `refs_id_categorie_modifiees` | Liste des catégories modifiées suite à cette comparaison |

Appender une entrée dans `10_Journal_Tracabilite` (type_operation: `comparaison_constante`).

## Rules

- **Trois types mobilisés.** Une analyse qui n'utilise que le type 3 est incomplète — les types 1 et 2 ancrent la comparaison dans les données individuelles.
- **Toute modification de catégorie est tracée.** Si une comparaison modifie `proprietes`, `conditions` ou `relations` dans `04_Categories`, la référence à `id_comparaison` y est ajoutée.
- **Corpus clos.** Sur ce projet, seuls les entretiens existants dans `entretiens/` sont comparés — aucune collecte nouvelle.
- **La comparaison est un outil, pas une fin.** Elle sert à affiner les catégories et à préparer la thématisation, pas à produire un inventaire exhaustif de différences.
- **Tout output = fichier.**

## See also

- `charmaz-categorisation` — catégories source des comparaisons
- `charmaz-memos` — la comparaison alimente les mémos analytiques
- `charmaz-construction-themes` — les comparaisons justifient les regroupements thématiques
- `charmaz-verification` — vérifie que les `id_categorie` et `id_segment` référencés existent
