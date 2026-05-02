# Plugin `declaration-impot-france`

Assistant fiscal complet pour les contribuables français. Analyse les documents fiscaux, guide la déclaration de revenus et identifie les leviers d'optimisation.

## Installation

```bash
claude plugin install declaration-impot-france
```

## Skills disponibles

### `/analyse-document-fiscal`

Analyse un document fiscal fourni (IFU, relevé SCPI, attestation fiscale) et extrait les montants à reporter dans la déclaration.

**Déclenché par :** "analyse mon IFU", "lis mon relevé SCPI", "que signifie cette case", "document Boursorama / Linxea / Amundi"

**Ce que ça fait :**
- Identifie le type de document (IFU, SCPI, assurance-vie, PEA)
- Extrait les montants case par case (2DC, 2TR, 3VG, 4BA…)
- Présente un tableau de synthèse prêt à reporter sur la 2042
- Signale les points d'attention (revenus étrangers, option barème, crédits d'impôt)

---

### `/expert-fiscal-qa`

Répond aux questions fiscales françaises avec la rigueur d'un expert-comptable.

**Déclenché par :** "comment fonctionne le LMNP", "qu'est-ce que le PFU", "comment déclarer mes dividendes étrangers", "SCI à l'IS ou à l'IR"

**Domaines couverts :**
- Impôt sur le revenu : tranches, TMI, quotient familial
- Revenus du capital : PFU, dividendes, plus-values mobilières, PEA
- Revenus fonciers : micro-foncier, régime réel, déficit foncier, SCPI, LMNP
- Immobilier : plus-values, IFI, travaux déductibles
- Structures : SCI, holding patrimoniale
- International : conventions fiscales, double imposition, résidence fiscale

---

### `/guide-declaration`

Guide pas à pas pour remplir la déclaration sur impots.gouv.fr.

**Déclenché par :** "faire ma déclaration", "quelles cases remplir", "comment reporter mon IFU", "formulaire 2044 / 2047"

**Étapes couvertes :**
1. Rassembler les documents (IFU, relevés SCPI, attestations…)
2. Vérifier les informations pré-remplies
3. Déclarer les revenus de capitaux mobiliers (formulaire 2042)
4. Déclarer les revenus fonciers (micro-foncier ou régime réel 2044)
5. Déclarer les revenus de source étrangère (formulaire 2047)
6. Charges déductibles, réductions et crédits d'impôt
7. Vérification finale avant validation

---

### `/optimisation-fiscale`

Compare les régimes fiscaux et identifie les leviers d'économie d'impôt.

**Déclenché par :** "optimiser ma fiscalité", "PFU ou barème progressif", "est-ce intéressant d'investir dans un PER", "LMNP réel ou micro", "déficit foncier"

**Leviers analysés :**
| Levier | Économie potentielle |
|--------|----------------------|
| Option barème progressif (case 2OP) | Si TMI ≤ 11% |
| Déficit foncier | Jusqu'à 10 700 € / an sur revenu global |
| PER — épargne retraite | Plafond 35 194 € (2025), déductible du revenu |
| PEA | Exonération IR après 5 ans |
| LMNP régime réel | Amortissement du bien |
| Dons | Réduction 66% à 75% |
| Emploi à domicile | Crédit 50%, plafond 12 000 € |

## Sources de données

Ce plugin est connecté à l'API **data.gouv.fr** (MCP) pour accéder aux données fiscales publiques officielles :

```
https://mcp.data.gouv.fr/mcp
```

## Exemples d'utilisation

```
Analyse mon IFU Boursorama, voici le fichier : [glisser le PDF]

→ /analyse-document-fiscal
```

```
Est-ce que je devrais opter pour le barème progressif ?
Ma TMI est à 11%, j'ai 3 000 € de dividendes.

→ /optimisation-fiscale
```

```
Comment déclarer mes revenus SCPI qui investissent en Allemagne ?

→ /expert-fiscal-qa
```

```
Guide-moi pour remplir ma déclaration, j'ai un IFU et des revenus fonciers.

→ /guide-declaration
```

## Avertissement

Ce plugin est un outil d'aide informatif. Il ne remplace pas les conseils d'un expert-comptable ou d'un conseiller fiscal agréé. Pour toute situation complexe, consultez un professionnel ou le service des impôts : **0809 401 401** (gratuit).
