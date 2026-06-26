---
name: charmaz-memos
type: skill
scope: memo_writing_charmaz
description: Fallback pour pilosa-charmaz-memos — rédaction des mémos analytiques (pp. 42-44), définition des catégories, intégration des verbatims justificatifs, mise en relation des idées, alimentation de 06_Memos et fichiers .md de mémos
created: 2026-06-22
updated: 2026-06-22
charmaz_ref: "pp. 42-44 — memo writing"
---

## Purpose

Rédiger les **mémos analytiques** — l'étape de réflexion et d'écriture intermédiaire qui accélère la montée en théorie. Un mémo définit une catégorie, l'explore, intègre des verbatims justificatifs, compare avec d'autres catégories, et esquisse des relations conceptuelles. Les mémos sont la mémoire analytique du chercheur.

> *« Memos are the theorizing write-up of ideas about codes and their relationships as they strike the analyst while coding. »* (Charmaz, p. 42)

## Prerequisites

- `04_Categories` contient des catégories documentées
- `05_Comparaisons` contient des comparaisons (ou est en cours d'alimentation)
- Les segments (`01_Segments`) sont accessibles pour les verbatims

## Steps

1. **Choisir une catégorie ou une relation entre catégories** à approfondir.
2. **Rédiger le mémo** dans un fichier `.md` à part entière dans `methodologie/run_<horodatage>/memos/` :
   - `MEMO_NNNN_<nom-categorie>.md`
   - Structure suggérée :
     - **Titre et date**
     - **Catégorie(s) traitées** (avec `id_categorie`)
     - **Ce que la catégorie capture** — définition provisoire en ses propres mots
     - **Propriétés observées** — avec verbatims justificatifs (`id_segment` + citation)
     - **Conditions d'apparition, maintien, changement** — illustrées par des verbatims
     - **Conséquences** — effets visibles dans le corpus
     - **Relations avec d'autres catégories** — hypothèses de connexion
     - **Questions ouvertes** — ce que le corpus ne permet pas encore de trancher
     - **Idées pour l'échantillonnage théorique** — quels segments relire pour développer cette catégorie
3. **Enregistrer dans `06_Memos`** une ligne de registre :
   - `id_memo` (`MEMO_NNNN`)
   - `titre`
   - `id_categorie_principale` et `id_categories_secondaires`
   - `id_segments_cites` — tous les segments dont le verbatim est cité dans le mémo
   - `fichier_memo` — chemin vers le fichier `.md`
   - `questions_ouvertes` — court résumé des incertitudes identifiées
4. Appender une entrée dans `10_Journal_Tracabilite` (type_operation: `redaction_memo`).

## Rules

- **Verbatims traçables.** Tout verbatim cité dans un mémo doit référencer son `id_segment` et le texte doit être identique au `texte_verbatim` de `01_Segments`. Pas de paraphrase sans indication.
- **Un mémo = un fichier `.md`.** Le contenu ne va pas dans le classeur, seulement dans le registre `06_Memos`.
- **Pas de théorie prématurée.** Les mémos explorent et interrogent — ils ne proclament pas. Les hypothèses sont formulées comme telles.
- **Les mémos alimentent la thématisation.** Les regroupements dans `08_Construction_Themes` doivent être justifiés par des `id_memo` ou `id_comparaison`.
- **Questions ouvertes signalées.** Ce que le corpus ne permet pas de résoudre est documenté ici — pas éludé.
- **Tout output = fichier.**

## See also

- `charmaz-categorisation` — catégories source des mémos
- `charmaz-comparaison-constante` — les comparaisons alimentent les mémos
- `charmaz-echantillonnage` — les mémos génèrent des pistes pour l'échantillonnage théorique
- `charmaz-construction-themes` — les mémos justifient les regroupements thématiques
- `charmaz-verification` — vérifie que les verbatims cités dans `06_Memos` existent dans `01_Segments`
