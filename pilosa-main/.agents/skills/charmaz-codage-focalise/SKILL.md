---
name: charmaz-codage-focalise
type: skill
scope: focused_coding_charmaz
description: Fallback pour pilosa-charmaz-codage-focalise — sélection des codes initiaux les plus récurrents et signifiants, regroupement, application à de larges portions de corpus, alimentation de 03_Codage_Focalise
created: 2026-06-22
updated: 2026-06-22
charmaz_ref: "p. 40 — focused coding"
---

## Purpose

Identifier, parmi les codes initiaux (`02_Codage_Initial`), ceux qui sont les plus **récurrents** et les plus **signifiants analytiquement**. Ces codes focalisés sont plus conceptuels et sélectifs que les codes initiaux. Les appliquer ensuite à de larges portions du corpus pour vérifier leur portée. Alimenter `03_Codage_Focalise`.

> *« Focused codes are more selective, abstract and conceptual than line-by-line codes. »* (Charmaz, p. 40)

## Prerequisites

- `02_Codage_Initial` est alimenté avec au moins 50 codes
- `01_Segments` est accessible pour relire les contextes si nécessaire

## Steps

1. Lire `02_Codage_Initial` dans son intégralité.
2. **Compter la fréquence** de chaque code (ou de codes textuellement proches) sur l'ensemble du corpus.
3. **Identifier les codes focalisés candidats** :
   - Codes apparaissant dans 3+ segments différents
   - Codes couvrant des actions ou processus fondamentaux pour comprendre ce qui se passe dans le corpus
   - Codes dont le `processus_amorce` est renseigné et récurrent
4. **Formuler le code focalisé** : plus abstrait et conceptuel que le code initial, mais toujours actif (gérondif ou processus). Pas nécessairement la reprise verbatim du code initial le plus fréquent — peut synthétiser un regroupement.
5. Pour chaque code focalisé, renseigner :
   - `id_code_focalise` (`FCO_NNNN`)
   - `intitule_focalise` — formulation active du code focalisé
   - `liste_id_code` — tous les codes initiaux regroupés sous ce code focalisé
   - `frequence` — nombre de segments couverts
   - `portee_corpus` — proportion du corpus concernée (calculée ou estimée)
   - `processus_amorce_synthetise` — synthèse des `processus_amorce` des codes initiaux regroupés
6. **Test de portée** : relire un échantillon de segments non couverts et vérifier que le code focalisé s'y applique ou non (confirmer sa délimitation).
7. Écrire dans `03_Codage_Focalise`.
8. Appender une entrée dans `10_Journal_Tracabilite` (type_operation: `codage_focalise`, justification: critères de sélection appliqués).

## Rules

- **Les codes focalisés ne remplacent pas les codes initiaux** — ils les subsument. La relation est conservée dans `liste_id_code`.
- **Toujours actifs.** Les codes focalisés restent formulés comme des processus ou au gérondif.
- **Aucune perte de traçabilité.** Tout `id_code` regroupé dans `liste_id_code` doit exister dans `02_Codage_Initial`.
- **Pas de seuil numérique rigide.** La fréquence est un signal, pas un critère exclusif — un code peu fréquent mais analytiquement central peut devenir code focalisé avec justification.
- **Signaler les codes initiaux non regroupés** : les codes présents dans `02_Codage_Initial` mais non repris dans un code focalisé doivent être listés comme `non_retenus` avec raison.
- **Tout output = fichier.**

## See also

- `charmaz-codage-initial` — source des codes initiaux
- `charmaz-categorisation` — élève les codes focalisés en catégories
- `charmaz-verification` — vérifie que chaque `id_code` dans `liste_id_code` existe dans `02_Codage_Initial`
