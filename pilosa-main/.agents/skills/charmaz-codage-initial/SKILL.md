---
name: charmaz-codage-initial
type: skill
scope: initial_coding_charmaz
description: Fallback pour pilosa-charmaz-codage-initial — codage ligne par ligne avec les deux jeux de questions Charmaz (p. 38 ancrage descriptif ; p. 39 émergence des processus), codes actifs au gérondif, codes in vivo, alimentation de 02_Codage_Initial
created: 2026-06-22
updated: 2026-06-22
charmaz_ref: "pp. 37-39"
---

## Purpose

Coder chaque segment du corpus ligne par ligne : codes actifs au gérondif, proches des données. Appliquer les deux jeux de questions de Charmaz — le premier (p. 38) ancre le code dans l'observable ; le second (p. 39) cherche le processus sous-jacent. Les deux jeux sont obligatoires sur chaque segment.

## Prerequisites

- `01_Segments` est alimenté (au moins un `id_segment`)
- `00_Corpus_Source` est alimenté
- `methodologie.md` est lisible

## Steps

### Étape A — Premier jeu : ancrage descriptif (p. 38)

Pour chaque segment, se poser les 5 questions descriptives et produire 1 à 4 codes :

| # | Question | Ce qu'elle produit |
|---|---|---|
| 1 | What is going on? | Code sur l'action ou l'état général |
| 2 | What are people doing? | Code sur l'action concrète des personnes |
| 3 | What is the person saying? | Code sur l'énonciation, la prise de position |
| 4 | What do these actions and statements take for granted? | Code sur les implicites, l'inexprimé |
| 5 | How do structure and context serve to support, maintain, impede or change these actions and statements? | Code sur le rôle du contexte structurel |

Règles de codage :
- Chaque code est formulé **au gérondif** : *évitant de divulguer*, *anticipant le rejet*, *revendiquant une normalité*, *gérant l'incertitude*…
- Court (2-5 mots), proche du verbatim — pas d'abstraction encore
- Si le participant emploie un terme qui capture parfaitement l'action → code **in vivo**, marquer `in_vivo: oui`
- Renseigner `question_p38_mobilisee` avec le numéro de la question (1-5)

### Étape B — Second jeu : détection du processus (p. 39)

Après les questions de la p. 38, se poser les 5 questions de processus sur le même segment :

| # | Question | Ce qu'elle fait émerger |
|---|---|---|
| 1 | What process is at issue here? | Nom du processus sous-jacent |
| 2 | Under which conditions does this process develop? | Conditions d'apparition |
| 3 | How does the research participant think, feel and act while involved in this process? | Dimension vécue du processus |
| 4 | When, why and how does the process change? | Dynamique et variation |
| 5 | What are the consequences of the process? | Effets en aval |

Si un processus est entrevu, renseigner `processus_amorce` avec une formulation courte. Sinon : `non_encore_visible`. Ce champ servira à l'Agent Catégorisation — ne pas le laisser vide sans justification.

**Ces questions ne produisent pas de nouveaux codes — elles alimentent uniquement `processus_amorce`.**

### Étape C — Vérification avant écriture

- [ ] `id_segment` existe dans `01_Segments`
- [ ] `texte_code` au gérondif
- [ ] `question_p38_mobilisee` renseigné
- [ ] `question_p39_mobilisee` renseigné (ou `non_encore_visible` justifié)
- [ ] Aucun terme théorique importé sans ancrage dans le verbatim

### Étape D — Écriture dans `02_Codage_Initial`

Colonnes : `id_code` (CODE_NNNN), `id_segment`, `texte_code`, `in_vivo`, `question_p38_mobilisee`, `question_p39_mobilisee`, `processus_amorce`, `note_analytique`.

Appender une entrée dans `10_Journal_Tracabilite` (type_operation: `codage_initial`, entrees: liste id_segment, sorties: liste id_code, violations: aucune ou description).

## Rules

- **Gérondif sans exception.** Un code nominal ou statique est refusé.
- **Deux jeux obligatoires.** Les 5 questions de la p. 38 ET les 5 de la p. 39 sur chaque segment.
- **In vivo signalé.** Mot ou expression du participant repris tel quel → `in_vivo: oui`.
- **Aucun cadre théorique plaqué.** Les sensitizing concepts restent en arrière-plan — ils ne deviennent pas des codes sans ancrage dans le verbatim.
- **Un code = un segment.** Jamais de code sans `id_segment` rattaché.
- **Violations immédiatement journalisées** dans `10_Journal_Tracabilite`.
- **Tout output = fichier.**

## Reprise sur interruption

Avant de commencer, lire `methodologie/checkpoint.json` → `etapes.codage_initial.dernier_id_valide`. Reprendre à partir du segment suivant. Vérifier idempotence sur `id_code` avant chaque écriture. Écriture atomique après chaque lot. Voir `charmaz-checkpoint` pour le protocole complet.

## See also

- `charmaz-checkpoint` — protocole de reprise et écriture atomique (obligatoire)
- `charmaz-codage-focalise` — étape suivante : sélection des codes récurrents
- `charmaz-categorisation` — utilise `processus_amorce` pour la montée en catégorie
- `charmaz-verification` — vérifie le format gérondif et le chaînage `id_segment`
- `methodologie/01_synthese_charmaz.md` §§ 2.3 et 2.4 — distinction des deux jeux de questions
