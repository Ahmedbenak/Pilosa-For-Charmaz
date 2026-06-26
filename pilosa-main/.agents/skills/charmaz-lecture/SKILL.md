---
name: charmaz-lecture
type: skill
scope: corpus_preparation_charmaz
description: Fallback pour pilosa-charmaz-lecture — lecture des entretiens, découpage en segments, attribution des identifiants, alimentation des onglets 00_Corpus_Source et 01_Segments
created: 2026-06-22
updated: 2026-06-22
charmaz_ref: "p. 33 — rich/thick data, conservation du contexte"
---

## Purpose

Lire les entretiens bruts depuis `entretiens/`, les découper en unités de données (segments) en conservant leur contexte (*thick data*, p. 33), attribuer des identifiants traçables, et alimenter les deux premiers onglets du classeur de traçabilité.

## Prerequisites

- `entretiens/` contient au moins un fichier d'entretien (`.txt`, `.md`, `.docx`)
- Le classeur `methodologie/run_<horodatage>/tracabilite.xlsx` existe avec les onglets `00_Corpus_Source` et `01_Segments`
- `methodologie/run_<horodatage>/methodologie.md` existe et définit l'unité de découpage

## Steps

1. Lire `methodologie.md` pour connaître l'unité de découpage retenue (paragraphe / tour de parole / échange interviewer-interviewé).
2. Lister tous les fichiers dans `entretiens/`. Pour chaque fichier :
   - Attribuer un `id_entretien` (`ENT_NNNN`, séquence continue)
   - Extraire les métadonnées non identifiantes (date, durée approximative, nb de pages/mots, format)
   - Écrire une ligne dans `00_Corpus_Source`
3. Pour chaque entretien, découper selon l'unité définie. Pour chaque segment :
   - Attribuer un `id_segment` (`SEG_NNNN`, séquence continue sur l'ensemble du corpus)
   - Conserver le `texte_verbatim` exact (aucune reformulation)
   - Renseigner le `contexte` (tour de parole précédent, position dans l'entretien, locuteur)
   - Renseigner `position_ligne` ou `position_paragraphe`
   - Écrire une ligne dans `01_Segments`
4. Appender une entrée dans `10_Journal_Tracabilite` :
   - `type_operation: preparation_corpus`
   - `sorties` : liste des `id_entretien` et nombre total de `id_segment` créés
5. Appender une ligne dans `logs/session_metrics.tsv`.

## Rules

- **Lecture seule des entretiens.** Ne jamais modifier les fichiers dans `entretiens/`.
- **Conservation du contexte obligatoire.** Charmaz insiste sur les données « riches/épaisses » (p. 33) — un segment sans son contexte (locuteur, moment de l'entretien) n'est pas utilisable.
- **Verbatim exact.** Aucune correction, aucune reformulation du texte d'origine.
- **Aucune interprétation à cette étape.** La préparation ne produit ni code, ni catégorie.
- **Séquence d'identifiants continue.** `SEG_0001` à `SEG_NNNN` sur tout le corpus — pas de numérotation par entretien.
- **Tout output = fichier.** Résultats dans le classeur, journal dans `10_Journal_Tracabilite`. Pas de réponse inline.
- Formats acceptés : `.txt`, `.md`, `.docx` (gère au moins ces trois) — documenter les formats effectivement traités dans `10_Journal_Tracabilite`.

## See also

- `charmaz-codage-initial` — étape suivante : coder chaque segment
- `charmaz-verification` — vérifie que chaque `id_entretien` dans `01_Segments` existe dans `00_Corpus_Source`
- `methodologie.md` — définit l'unité de découpage retenue pour ce corpus
