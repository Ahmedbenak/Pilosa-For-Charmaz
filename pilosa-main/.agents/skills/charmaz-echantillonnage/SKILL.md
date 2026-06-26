---
name: charmaz-echantillonnage
type: skill
scope: theoretical_sampling_charmaz
description: Fallback pour pilosa-charmaz-echantillonnage — échantillonnage théorique sur corpus clos (pp. 45-46), réinterrogation analytique des données existantes pour développer et saturer les catégories, signalement explicite des propriétés non saturables comme limites, alimentation de 07_Echantillonnage_Theorique
created: 2026-06-22
updated: 2026-06-22
charmaz_ref: "pp. 45-46 — theoretical sampling (corpus clos)"
---

## Purpose

Affiner les catégories émergentes en identifiant, **à l'intérieur du corpus déjà constitué**, les segments ou entretiens à relire pour développer des propriétés insuffisamment saturées. L'échantillonnage théorique sur corpus clos ne collecte pas de nouvelles données — il réinterroge analytiquement ce qui existe déjà. Les propriétés non saturables faute de données sont signalées comme **limites explicites**, jamais comblées.

> *« Theoretical sampling means seeking pertinent data to develop your emerging theory. »* (Charmaz, p. 45)

**Contrainte absolue sur corpus clos :** aucun retour sur le terrain, aucune nouvelle question posée, aucune donnée extérieure au dossier `entretiens/`.

## Prerequisites

- `04_Categories` contient des catégories avec au moins une propriété insuffisamment documentée
- `06_Memos` contient des pistes d'échantillonnage (champ `questions_ouvertes`)
- `01_Segments` est accessible pour la relecture ciblée

## Steps

1. **Identifier les lacunes** : pour chaque catégorie dans `04_Categories`, repérer les propriétés, conditions ou conséquences insuffisamment documentées (champ vide ou mention `LIMITE_SIGNALEE`).
2. **Formuler la question analytique** : quelle propriété cherche-t-on à développer ou saturer ? (ex. : « Sous quelles conditions ce processus change-t-il de nature ? »)
3. **Désigner les segments à relire** dans le corpus existant :
   - Entretiens provenants de profils différents (variation maximale)
   - Moments différents dans un même entretien (variation temporelle)
   - Segments sur lesquels le codage initial avait noté `processus_amorce` compatible
4. **Relire et ré-exploiter** les segments désignés :
   - Appliquer les questions de codage (p. 38 et p. 39) sur les passages sélectionnés
   - Créer de nouveaux codes dans `02_Codage_Initial` si nécessaire
   - Mettre à jour les propriétés de la catégorie dans `04_Categories`
5. **Tester la saturation** : la propriété est considérée saturée si de nouveaux segments n'apportent plus d'information nouvelle. Sur corpus clos, la saturation peut ne pas être atteignable — le signaler.
6. **Écrire dans `07_Echantillonnage_Theorique`** :
   - `id_categorie` visée
   - `propriete_developpee`
   - `id_segment_relus` — liste des segments ré-exploités
   - `resultat_saturation` : `saturee` / `partiellement_saturee` / `non_saturable_corpus_insuffisant`
   - `limite_signalee` : description de la limite si non saturable
7. Appender une entrée dans `10_Journal_Tracabilite` (type_operation: `echantillonnage_theorique`, violations: aucune ou LIMITE_SIGNALEE).

## Rules

- **Corpus clos — zéro collecte nouvelle.** Seuls les segments existants dans `entretiens/` et `01_Segments` sont utilisés.
- **Propriété non saturable = limite documentée, pas comblée.** La valeur `non_saturable_corpus_insuffisant` dans `07_Echantillonnage_Theorique` est une réponse valide et scientifiquement honnête.
- **L'échantillonnage est guidé par la théorie émergente.** Le choix des segments à relire doit être justifié par une question analytique, pas par la facilité ou la fréquence.
- **Nouveaux codes traçables.** Si la relecture produit de nouveaux codes, ils sont créés dans `02_Codage_Initial` avec leur `id_segment` — jamais en suspension.
- **Report de la revue de littérature.** L'échantillonnage théorique n'implique pas de consulter la littérature — cela vient après l'analyse conceptuelle (p. 47).
- **Tout output = fichier.**

## See also

- `charmaz-categorisation` — fournit les catégories à développer
- `charmaz-memos` — les mémos signalent les pistes d'échantillonnage (`questions_ouvertes`)
- `charmaz-comparaison-constante` — la comparaison guide le choix des segments à relire
- `charmaz-verification` — vérifie que les `id_segment` dans `07_Echantillonnage_Theorique` existent dans `01_Segments`
