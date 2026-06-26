---
name: charmaz-checkpoint
type: skill
scope: checkpoint_resume_charmaz
description: Protocole de détection, reprise sur interruption et écriture incrémentale pour la pipeline Charmaz. Lit checkpoint.json au démarrage, décide si démarrage propre ou reprise, et définit le protocole que chaque agent doit suivre pour écrire de façon atomique et mettre à jour le checkpoint après chaque écriture validée.
created: 2026-06-22
updated: 2026-06-22
---

## Purpose

Garantir que la pipeline Charmaz peut être interrompue brutalement à tout moment (limite de consommation atteinte, coupure réseau, etc.) et reprendre exactement là où elle s'était arrêtée au prochain lancement. Aucune duplication, aucune perte, aucune corruption du classeur de traçabilité.

## Prerequisites

- `methodologie/checkpoint.json` existe (ou la pipeline est en démarrage propre)
- `methodologie/tracabilite.xlsx` existe (ou doit être créé)
- `methodologie/gerer_tracabilite.py` est accessible
- L'orchestrateur Charmaz exécute ce protocole avant toute autre action

## Steps — Phase 1 : Détection au démarrage

1. Lire `methodologie/checkpoint.json`.
   - **Si le fichier n'existe pas** → démarrage propre :
     - Appeler `python methodologie/gerer_tracabilite.py --init` pour créer `tracabilite.xlsx`
     - Initialiser `checkpoint.json` avec `statut: a_faire`
     - Continuer avec la pipeline complète depuis l'étape 1

   - **Si `statut: "termine"`** → afficher le résumé final depuis `ETAT_AVANCEMENT.md` et s'arrêter :
     ```
     ANALYSE TERMINÉE. Aucune reprise sans instruction explicite.
     Résumé : methodologie/ETAT_AVANCEMENT.md
     Classeur : methodologie/tracabilite.xlsx
     ```

   - **Si `statut: "en_cours"` ou `"interrompu"`** → afficher le point de reprise et reprendre :
     - Lire et afficher `methodologie/ETAT_AVANCEMENT.md` (section Résumé)
     - Identifier l'étape en cours et le `dernier_id_valide` de chaque étape
     - Appeler `python methodologie/gerer_tracabilite.py --check` pour synchroniser le checkpoint avec le classeur réel (détecte les divergences dues à une interruption brutale)
     - Reprendre à partir du premier id non encore présent dans le classeur

2. Enregistrer le nouveau run dans `checkpoint.json` :
   ```json
   {
     "run_id": "run_AAAAMMJJ_HHMM",
     "debut": "YYYY-MM-DD HH:MM:SS",
     "fin": null,
     "cause_arret": null,
     "nb_ids_ecrits": 0
   }
   ```
   Mettre à jour `dernier_lancement` et `dernier_run_id`.
   Créer le dossier `methodologie/run_<run_id>/` avec un `run_info.json`.

## Steps — Phase 2 : Protocole d'écriture incrémentale (chaque agent)

Chaque agent Charmaz applique ce protocole pour **chaque identifiant** (ou petit lot de 5-10 identifiants) :

```
PROTOCOLE PAR IDENTIFIANT :

1. VÉRIFIER idempotence
   → Appeler lire_derniers_ids(onglet) depuis gerer_tracabilite.py
   → Si l'id existe déjà : SAUTER sans erreur, passer au suivant

2. PRÉPARER les données en mémoire (une ligne ou un petit lot)

3. ÉCRIRE de façon atomique
   → Appeler ecrire_lignes_atomique(onglet, lignes)
   → Cette fonction : write vers tracabilite.xlsx.tmp → rename vers tracabilite.xlsx
   → Si l'écriture échoue : signaler l'erreur, NE PAS mettre à jour le checkpoint

4. METTRE À JOUR le checkpoint IMMÉDIATEMENT après écriture réussie
   → Appeler mettre_a_jour_checkpoint(etape, dernier_id, nb_delta)
   → Mettre à jour corpus.entretiens[i].dernier_segment_valide si applicable
   → Incrémenter runs[-1].nb_ids_ecrits

5. RÉGÉNÉRER ETAT_AVANCEMENT.md
   → Appeler regenerer_etat_avancement() (ou laisser l'orchestrateur le faire
     toutes les N écritures pour limiter les I/O)
```

**Taille recommandée des lots :** 1 identifiant pour les étapes lentes (catégorisation, thématisation), 10-20 pour les étapes rapides (segmentation, codage initial).

## Steps — Phase 3 : Détection de la dernière unité incomplète

Si le checkpoint indique un `dernier_id_valide` mais que le classeur révèle que ce segment n'a pas tous ses codes attendus :

1. Appeler `--check` pour synchroniser
2. Le `dernier_id_valide` reconstruit pointe sur le dernier id **complet** dans le classeur
3. L'agent reprend à partir de l'id suivant
4. Les ids partiellement écrits sont complétés (idempotence : les lignes déjà présentes sont sautées)

## Steps — Phase 4 : Marqueur de fin propre

Seul l'Agent Vérification & Traçabilité, après avoir certifié les 7 contrôles complets, appelle :

```python
from methodologie.gerer_tracabilite import marquer_termine
marquer_termine()
```

Cette fonction écrit `"statut": "termine"` et `certifie_complet: true` dans `checkpoint.json` et régénère `ETAT_AVANCEMENT.md`.

## Rules

- **Checkpoint mis à jour après chaque écriture réussie.** Jamais avant, jamais en batch différé.
- **Écriture atomique sans exception.** `tracabilite.xlsx.tmp` → rename. Jamais écrire directement dans le xlsx.
- **Idempotence garantie.** Avant toute écriture, vérifier que l'id n'existe pas. Un doublon n'est jamais créé.
- **La dernière unité incomplète est retraitée.** Au redémarrage, vérifier la complétude du dernier segment, pas seulement sa présence.
- **Statut par défaut = `interrompu`.** Tout arrêt sans `marquer_termine()` laisse l'analyse reprisable.
- **`termine` = seul l'Agent Vérification peut l'écrire.** Personne d'autre ne touche à ce statut.
- **tracabilite.xlsx.tmp ne doit pas traîner.** Si un `.tmp` existe au démarrage, c'est le signe d'une interruption en plein write atomique → appeler `--check` avant de reprendre.

## Chemins stables

| Fichier | Rôle |
|---|---|
| `methodologie/checkpoint.json` | État machine — mis à jour après chaque écriture |
| `methodologie/tracabilite.xlsx` | Classeur cumulatif — jamais déplacé |
| `methodologie/ETAT_AVANCEMENT.md` | Résumé humain — régénéré automatiquement |
| `methodologie/gerer_tracabilite.py` | Script Python de gestion |
| `methodologie/memos/` | Mémos analytiques cumulatifs |
| `methodologie/run_<id>/` | Logs de session uniquement |

## See also

- `charmaz-lecture`, `charmaz-codage-initial`, etc. — agents qui implémentent ce protocole
- `charmaz-verification` — seul agent qui peut marquer l'analyse comme `termine`
- `methodologie/methodologie.md` §4 — documentation complète du mécanisme
- `methodologie/gerer_tracabilite.py` — implémentation Python des fonctions d'écriture atomique
