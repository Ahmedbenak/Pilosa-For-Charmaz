---
name: charmaz-construction-themes
type: skill
scope: theme_theory_construction_charmaz
description: Fallback pour pilosa-charmaz-construction-themes — agrégation des catégories en sous-thèmes et grands thèmes selon des règles de regroupement tracées, identification des processus génériques, formulation de la théorie finale ancrée, alimentation de 08_Construction_Themes et 09_Theorie_Finale
created: 2026-06-22
updated: 2026-06-22
charmaz_ref: "pp. 41, 47-48 — generic processes, theory formulation"
---

## Purpose

Agréger les catégories en **sous-thèmes**, puis en **grands thèmes**, selon des règles de regroupement explicitement tracées. Identifier les **processus génériques** — transversaux à plusieurs situations, potentiellement applicables au-delà du corpus. Formuler la **théorie finale ancrée** sous forme d'énoncés liés à leur chaîne de traçabilité. Le raisonnement de regroupement doit être visible, pas seulement le résultat.

> *« Generic processes are basic and fundamental in social life. »* (Charmaz, p. 41)

## Prerequisites

- `04_Categories` est alimenté, catégories avec 4 opérations documentées
- `05_Comparaisons` et `06_Memos` sont alimentés (servent à justifier les regroupements)
- `07_Echantillonnage_Theorique` est alimenté (saturation des propriétés vérifiée)
- Aucune `VIOLATION_IMPORTATION` non résolue dans `04_Categories` (vérifiée par Agent Vérification)

## Steps

### A — Construction des sous-thèmes (onglet `08_Construction_Themes`)

1. Pour chaque groupe de catégories, identifier la **règle de regroupement** :
   - `theme_englobant` : une catégorie subsume les autres (relation d'inclusion)
   - `theme_conteneur` : création d'un thème nouveau qui réunit des catégories de même registre
   - `processus_generique` : le regroupement exprime un processus transversal à plusieurs domaines ou entretiens (au sens Charmaz, p. 41)
2. Pour chaque sous-thème et grand thème, renseigner :
   - `id_sous_theme` ou `id_theme` (`STHM_NNNN` / `THM_NNNN`)
   - `intitule_theme`
   - `regle_regroupement` — `theme_englobant` / `theme_conteneur` / `processus_generique`
   - `id_categorie_sources` — liste des catégories regroupées
   - `justification_regroupement` — ancrée dans `id_comparaison` ou `id_memo` (pas abstraite)
   - `processus_generique` : `oui` / `non` + justification si oui (quels entretiens, quelle transversalité)
3. Vérifier que chaque `id_categorie_sources` existe dans `04_Categories`.

### B — Formulation de la théorie finale (onglet `09_Theorie_Finale`)

1. Formuler les **énoncés théoriques** : propositions sur les processus génériques identifiés, ancrées dans les catégories.
2. Pour chaque énoncé :
   - `id_enonce` (`ENO_NNNN`)
   - `texte_enonce` — la proposition théorique
   - `id_theme_sources` — thèmes qui fondent l'énoncé
   - `processus_generique_exprime` — le ou les processus génériques formulés
   - `ancrage_ultimate` — remontée jusqu'à 3 `id_segment` illustratifs (traçabilité jusqu'au verbatim)
3. Vérifier que chaque `id_theme_sources` existe dans `08_Construction_Themes`.
4. Vérifier que les `id_segment` dans `ancrage_ultimate` existent dans `01_Segments`.

### C — Report de la revue de littérature (p. 47)

La littérature disciplinaire n'est mobilisée qu'après la formulation conceptuelle — et seulement pour situer la théorie émergente, jamais pour l'orienter rétrospectivement. Signaler dans `10_Journal_Tracabilite` si des références théoriques ont été consultées à cette étape.

### D — Journalisation

Appender une entrée dans `10_Journal_Tracabilite` pour chaque thème et chaque énoncé théorique (type_operation: `construction_theme` / `formulation_theorie`).

## Rules

- **Raisonnement de regroupement visible.** La question « comment ce thème a-t-il été obtenu ? » doit trouver réponse dans `regle_regroupement` + `justification_regroupement`.
- **Aucun thème sans catégorie réelle.** Tout `id_categorie_sources` doit exister dans `04_Categories`.
- **Aucun énoncé sans thème réel.** Tout `id_theme_sources` doit exister dans `08_Construction_Themes`.
- **Ancrage ultimate obligatoire.** Chaque énoncé théorique doit être traçable jusqu'au verbatim source.
- **Processus génériques identifiés explicitement.** Ce sont la visée de la méthode — ne pas s'arrêter à des thèmes purement descriptifs.
- **Report de la littérature respecté.** Pas de consultation de la littérature avant cette étape (p. 47).
- **Aucune `VIOLATION_IMPORTATION` non résolue ne monte dans les thèmes** — Agent Vérification doit avoir certifié `04_Categories` avant.
- **Tout output = fichier.**

## See also

- `charmaz-categorisation` — fournit les catégories sources
- `charmaz-comparaison-constante` et `charmaz-memos` — justifient les regroupements
- `charmaz-verification` — contrôle le cheminement de thématisation et la cohérence de la théorie finale
- `methodologie/01_synthese_charmaz.md` §§ 7, 8, 9 — processus génériques et théorie ancrée
