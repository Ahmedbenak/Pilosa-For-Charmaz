---
type: cartographie
role: etat_initial
created: 2026-06-22
auteur: exploration_§1
---

# État initial du projet Pilosa — Cartographie avant personnalisation Charmaz

## 1. Nature du projet Pilosa

Pilosa est un **moteur de navigation et de recherche dans un corpus documentaire**, piloté par un orchestrateur multi-agents. Il n'est **pas** une pipeline d'analyse qualitative : c'est une infrastructure de recherche/synthèse/vérification sur corpus textuel. La personnalisation Charmaz va **ajouter une couche analytique** par-dessus, en réutilisant les mécanismes de routing, les formats d'agents, et le système de rapports.

---

## 2. Structure des dossiers

```
pilosa-main/
├── AGENTS.md                      Orchestrateur (routage, règles globales) — AUTORITÉ
├── CLAUDE.md                      Mirror généré de AGENTS.md (avec provenance) pour Claude Code
├── .agents/
│   ├── agents/                    7 agents canoniques (.md) — SOURCE DE VÉRITÉ
│   └── skills/                    9 skills portables (sous-dossiers avec SKILL.md)
├── .claude/agents/                Mirror généré pour Claude Code
├── .opencode/agents/              Mirror généré pour OpenCode
├── .codex/agents/                 Mirror généré (TOML) pour Codex
├── system/
│   ├── configuration.md          Profil opérationnel (chemins, politique source, setup_status)
│   ├── context.md                Contexte projet (méthodes, vocabulaire, scope)
│   ├── startup.md                Protocole d'indexation initial (onboarding → maps + dictionary)
│   ├── dictionary.md             Dictionnaire canonique (construit au démarrage)
│   ├── yaml_header_template.md   Schéma YAML frontmatter pour les fichiers raw/
│   └── workspace_index.md        Index maître du workspace
├── raw/                          Corpus actif (copies de travail — NE PAS MODIFIER)
├── entretiens/                   [VIDE — sera le corpus source Charmaz]
├── maps/                         Cartes de navigation Obsidian (wikilinks)
├── agent_reports/                Rapports produits par les agents (numérotés NN_*.md)
├── logs/
│   ├── user_requests.md          Journal des requêtes (orchestrateur)
│   └── session_metrics.tsv       Métriques d'opération par sous-agent
└── .trash/                       Fichiers archivés (jamais supprimés, uniquement déplacés)
```

**Dossiers absents à créer :**
- `methodologie/` — dossier horodaté de traçabilité (pièce centrale de la personnalisation)
- `entretiens/README.md` — documentation du format attendu

---

## 3. Les 7 agents existants

Les agents canoniques vivent dans `.agents/agents/`. Les dossiers `.claude/agents/`, `.opencode/agents/`, `.codex/agents/` sont des **mirrors générés** par `pilosa sync` — ne pas modifier directement.

| Agent | Scope | Rôle | Écrit dans |
|---|---|---|---|
| `pilosa-searcher` | `evidence_retrieval` | Recherche dans maps/ + raw/ + dictionary | `agent_reports/evidence_packet.md` |
| `pilosa-mapper` | `startup_indexing` | Extraction en batch + écriture des cartes Obsidian | `maps/`, `agent_reports/extraction_batch_*.md` |
| `pilosa-analyst` | `project_context` | Analyse contextuelle parallèle au Searcher | `agent_reports/` |
| `pilosa-writer` | `report_synthesis` | Synthèse → rapports numérotés avec dashboard Unicode | `agent_reports/NN_*.md` |
| `pilosa-verifier` | `claim_verification` | Vérification des citations, chemins, claims | `agent_reports/` (corrections in-place) |
| `pilosa-janitor` | `workspace_hygiene` | Hygiène du workspace, archivage proposé | `agent_reports/`, `.trash/` |
| `pilosa-serendippo` | `serendipitous_research` | Découverte de connexions cachées, holistische | `agent_reports/`, `maps/` |

### Format obligatoire des agents (frontmatter YAML)

```yaml
---
name: pilosa-xxx
type: agent
scope: xxx
description: |
  [description multi-lignes]
created: YYYY-MM-DD
updated: YYYY-MM-DD
permissions:
  read: allow
  grep: allow
  glob: allow
  write:
    - agent_reports/
    - logs/session_metrics.tsv
---
```

---

## 4. Les 9 skills existantes (Pilosa d'origine)

Situées dans `.agents/skills/<nom>/SKILL.md` :

| Skill | Usage |
|---|---|
| `orchestrator-dispatch` | Classification des requêtes et sélection des séquences |
| `evidence-search` | Recherche d'évidence dans raw/ |
| `context-analysis` | Analyse contextuelle parallèle au Searcher |
| `report-writing` | Format des rapports, references, verbatim-format.md |
| `claim-verification` | Vérification des claims, citations et chemins |
| `source-intake` | Enregistrement de nouvelles sources dans le workspace |
| `mapper-fallback` | Fallback pour pilosa-mapper (extraction + cartes Obsidian) |
| `serendippo-fallback` | Fallback pour pilosa-serendippo (connexions cachées) |
| `workspace-cleanup` | Audit d'hygiène et archivage des fichiers obsolètes |

**Note de correction :** La cartographie initiale mentionnait à tort des skills `coding`, `evaluation`, `sorting`, `workflow` et `map-writing`. Ces skills n'existent pas dans le projet réel. Seules les 9 skills ci-dessus sont présentes dans `.agents/skills/`.

**Après personnalisation Charmaz :** 9 skills Charmaz ont été ajoutées (voir § 9), portant le total à 18 skills.

Les skills servent de **fallback** si le spawn natif d'un agent échoue : l'orchestrateur lit le `SKILL.md` et injecte son contenu dans son propre prompt.

---

## 5. L'orchestrateur : classes de routes existantes

`AGENTS.md` / `CLAUDE.md` définissent 10 classes de routes :

| Classe | Quand | Séquence par défaut |
|---|---|---|
| `fast_path` | Réponse opérationnelle directe | (aucune) |
| `clarify_search` | Traduction de termes avant recherche | skip ou searcher |
| `find_material` | Ce qui existe / où chercher | searcher → verifier |
| `evidence_answer` | Réponse ancrée dans les sources | searcher + analyst → writer → verifier |
| `synthesis_report` | Rapport structuré | searcher×N + analyst → writer → verifier |
| `verification` | Vérifier un claim, citation, chemin | verifier |
| `index_maintenance` | Fix / nettoyer l'index | searcher → verifier |
| `cleanup` | Audit + archivage | janitor |
| `deep_index` | Ré-indexation profonde | mapper → verifier |
| `serendipity` | Connexions cachées cross-corpus | serendippo |

---

## 6. Flux de données dans Pilosa standard

```
Corpus source (externe)
    ↓ [CLI onboarding : pilosa new]
raw/                    ← copies actives, immuables pendant l'analyse
    ↓ [startup : pilosa-mapper en batch]
maps/                   ← cartes de navigation Obsidian (wikilinks)
system/dictionary.md    ← dictionnaire canonique
    ↓ [requête utilisateur → orchestrateur]
agent_reports/          ← rapports de sous-agents (evidence_packet, rapports numérotés)
logs/                   ← métriques + journal de requêtes
```

### Règle globale inviolable
> **All output must be reports.** Tout agent écrit dans des fichiers, jamais en réponse inline. Les fichiers de process (evidence_packet.md, extraction_batch_*.md) sont déplacés dans `.trash/` après finalisation.

---

## 7. État du setup au moment de l'exploration

| Élément | État |
|---|---|
| `system/configuration.md` | `setup_status: not_started` — `source_location: [filled by CLI]` |
| `system/context.md` | `setup_status: not_started` — tous champs vides / placeholders |
| `entretiens/` | Dossier vide (aucun entretien chargé) |
| `raw/` | `.gitkeep` uniquement |
| `maps/` | `.gitkeep` + `AGENTS.md` + `map_template.md` |
| `agent_reports/` | 2 rapports existants (`01_*.md`, `02_*.md`), `AGENTS.md` |
| `logs/` | `.gitkeep` + `session_metrics.tsv` vide + `user_requests.md` |
| `methodologie/` | **INEXISTANT** |

---

## 8. Points d'extension — où brancher les agents Charmaz

| Point d'extension | Comment | Ce que ça permet |
|---|---|---|
| `.agents/agents/` | Créer un `.md` par agent Charmaz (même frontmatter) | Disponibilité dans tous les vendors après `pilosa sync` |
| `AGENTS.md` | Ajouter des classes de route Charmaz + séquences | Orchestrer la pipeline Charmaz comme les autres routes |
| `system/configuration.md` | Modifier `active_corpus_path` → `entretiens/` | Pointer le corpus vers les entretiens |
| `system/context.md` | Décrire le projet sociologique, méthode Charmaz | Contextualiser les agents analytiques |
| `.agents/skills/` | Créer des skills Charmaz (codage, catégorisation...) | Fallback et portabilité entre LLM CLI |
| `methodologie/` | **NOUVEAU** — dossier horodaté + classeur xlsx | Traçabilité de bout en bout (priorité §2) |

---

## 9. Ce qui existe vs. ce qui sera créé / adapté

### À réutiliser sans modification
- Format des agents (frontmatter YAML) ✓
- Mécanisme de routing orchestrateur (classes → séquences) ✓
- Système de reports numérotés dans `agent_reports/` ✓
- `logs/session_metrics.tsv` (métriques) ✓
- Dossier `entretiens/` (existe, vide) ✓

### À adapter
- `AGENTS.md` : ajouter les routes Charmaz (`charmaz_initial_coding`, `charmaz_focused_coding`, etc.)
- `system/context.md` : décrire le projet d'entretiens sociologiques
- `system/configuration.md` : pointer `entretiens/` comme corpus source, `methodologie/` comme sortie
- `pilosa-verifier` : étendre ou spécialiser en Agent Vérification & Traçabilité Charmaz

### À créer from scratch
- 9 agents Charmaz dans `.agents/agents/` (Lecture, Codage Initial, Codage Focalisé, Catégorisation, Comparaison Constante, Mémos, Échantillonnage Théorique, Construction Thèmes & Théorie, Vérification & Traçabilité)
- Orchestrateur Charmaz (nouvelles routes dans `AGENTS.md`)
- Dossier `methodologie/run_<horodatage>/` avec générateur automatique
- `methodologie/run_.../methodologie.md` (description reproductible de chaque étape)
- Gabarit `methodologie/run_.../tracabilite.xlsx` (11 onglets, chaînage des id)
- Validateur de traçabilité (agent ou script)
- `entretiens/README.md` (format attendu des entretiens)
- `methodologie/RECAP_PERSONNALISATION.md` (livrable final §7)
- `methodologie/_exemple_demo/` (mini-jeu fictif pour tester le validateur)

---

## 10. Contraintes techniques à respecter

- **Ne jamais modifier `raw/`** (corpus actif, lecture seule)
- **`entretiens/` = corpus source Charmaz** : les agents lisent, ne modifient pas
- **Mirrors** : tout nouvel agent dans `.agents/agents/` doit être synchronisé via `pilosa sync` (reconstruit `.claude/agents/`, `.opencode/agents/`, `.codex/agents/`)
- **Toute sortie = fichier** : les agents Charmaz n'écrivent pas en inline — ils produisent des fichiers dans `methodologie/run_<horodatage>/`
- **Métriques** : chaque agent Charmaz doit appender à `logs/session_metrics.tsv`
- **Traçabilité** (priorité §2) : tout identifiant (`id_segment`, `id_code`, etc.) référencé dans un onglet aval doit exister dans l'onglet amont — aucun orphelin toléré
