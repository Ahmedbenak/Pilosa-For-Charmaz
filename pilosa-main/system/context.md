---
type: context
role: startup
scope: project_context
status: active
description: Read by Writer for synthesis; updated by startup during indexing.
created: 2026-05-26
updated: 2026-06-05
setup_status: not_started
connects_to:
  - AGENTS.md
  - system/configuration.md
  - system/startup.md
  - logs/user_requests.md
---
# Context

## Project
- Title: Analyse d'entretiens sociologiques — IA et imaginaires numériques
- Description: Projet d'analyse qualitative d'un corpus de 13 entretiens semi-directifs portant sur les représentations, usages et imaginaires liés à l'intelligence artificielle et aux algorithmes. Les entretiens explorent les perceptions des participant·e·s face à l'IA, leurs pratiques numériques, leurs craintes et attentes.

## Project Artifacts
- Corpus source : `entretiens/` (13 fichiers .md, lecture directe par l'agent Lecture)
- Référence méthodologique : `Charmaz_1996 (1).pdf` — *The Search for Meanings — Grounded Theory*

## Sources
- Source location: `entretiens/`
- Main source types: entretiens semi-directifs (.md)
- Expected incoming sources: corpus clos — aucune collecte nouvelle

## Research Vocabulary
- Key actors / institutions / places: participant·e·s (personnes interrogées), chercheur·se·s, concepteur·trice·s d'IA
- Key concepts: imaginaire technique, perception de l'IA, confiance algorithmique, autonomie numérique, biais perçus
- Sensitizing concepts, not evidence: à émerger des données selon le protocole Charmaz (pp. 32, 38)
- Theoretical frames, not forced labels: aucun cadre théorique préimposé — la théorie émerge par codage itératif

## Method And Evidence
- Methods: **Théorisation ancrée (Grounded Theory) selon Kathy Charmaz (1996)**
  - Segmentation du corpus avec conservation du contexte (thick data, p. 33)
  - Codage initial ligne par ligne avec deux jeux de questions (pp. 38-39)
  - Codage focalisé : sélection des codes les plus récurrents/signifiants (p. 40)
  - Catégorisation avec 4 opérations obligatoires (p. 41)
  - Comparaison constante en 3 types (p. 42)
  - Mémos analytiques (pp. 42-44)
  - Échantillonnage théorique sur corpus clos (pp. 45-46)
  - Construction de thèmes et théorie finale ancrée (pp. 41, 47-48)
  - Vérification continue de la traçabilité et de l'ancrage empirique
- Claims require source paths.
- L2 clues require Verifier checking before reporting.
- External sources must stay labeled external unless moved into `raw/`.
- External source policy: no

## Outputs
- Analyse qualitative complète dans `methodologie/tracabilite.xlsx` (11 onglets)
- Mémos analytiques dans `methodologie/memos/`
- Rapports de vérification dans `agent_reports/`
- État d'avancement dans `methodologie/ETAT_AVANCEMENT.md`
- Checkpoint machine dans `methodologie/checkpoint.json`

## Blind Spots
Limites identifiables a priori :
- Corpus clos de 13 entretiens — saturation théorique peut ne pas être atteignable
- Pas de collecte longitudinale — comparaison temporelle limitée
- Biais de sélection propre au recrutement des participant·e·s

## Researcher Preferences
[To be filled by researcher]

## Preferred LLM CLI
pilosa
