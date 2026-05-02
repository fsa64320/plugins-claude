---
name: ratios-financiers
description: Ce skill doit être utilisé quand l'utilisateur demande une analyse par ratios financiers ou pose des questions sur la solidité financière d'une société française : "ratios financiers", "solvabilité", "liquidité", "rentabilité", "autonomie financière", "capacité de remboursement", "levier financier", "ROE", "ROA", "endettement", "analyse financière complète", "taux d'endettement", "liquidité générale", "liquidité réduite", "diagnostic financier", "santé financière".
version: 1.0.0
allowed-tools: [Read, Glob]
---

# Calcul et analyse des ratios financiers

## Objectif

Calculer l'ensemble des ratios financiers clés d'une société française à partir de son bilan et de son compte de résultat, comparer ces ratios aux benchmarks sectoriels et formuler un diagnostic financier global avec des recommandations concrètes.

## Prérequis

Avant de calculer les ratios, s'assurer de disposer des données suivantes :

**Du bilan :**
- Total actif
- Actif circulant (stocks + créances clients + disponibilités + VMP)
- Créances clients + disponibilités + VMP (sans les stocks)
- Capitaux propres
- Dettes financières totales (LT + CT, hors dettes d'exploitation)
- Dettes à court terme (dettes fournisseurs + dettes fiscales et sociales + concours bancaires + part CT des emprunts)

**Du compte de résultat :**
- Chiffre d'affaires HT
- EBE (Excédent Brut d'Exploitation)
- Résultat d'exploitation
- Résultat net
- CAF (Capacité d'Autofinancement)

Si des données sont manquantes, les indiquer et proposer de calculer les ratios disponibles.

## Processus

### 1. Ratios de structure et de solvabilité

Ces ratios mesurent la solidité financière à long terme et l'indépendance vis-à-vis des créanciers.

**Autonomie financière**
```
Autonomie financière = Capitaux propres / Total passif × 100
```
| Valeur | Appréciation |
|--------|--------------|
| > 40% | Bon |
| 30% - 40% | Acceptable |
| < 30% | Vigilance |

**Taux d'endettement (gearing)**
```
Taux d'endettement = Dettes financières nettes / Capitaux propres
                   (Dettes financières nettes = Dettes financières brutes - Disponibilités - VMP)
```
| Valeur | Appréciation |
|--------|--------------|
| < 0,5 | Bon |
| 0,5 - 1 | Acceptable |
| > 1 | Vigilance |

**Capacité de remboursement**
```
Capacité de remboursement = Dettes financières nettes / CAF  (en années)
```
| Valeur | Appréciation |
|--------|--------------|
| < 2 ans | Bon |
| 2 - 3 ans | Acceptable |
| > 3 ans | Vigilance (seuil bancaire généralement fixé à 3-4 ans) |

**Couverture des intérêts (Interest Coverage)**
```
Couverture des intérêts = EBE / Charges financières nettes
```
| Valeur | Appréciation |
|--------|--------------|
| > 5 | Bon |
| 2 - 5 | Acceptable |
| < 2 | Vigilance |

### 2. Ratios de liquidité

Ces ratios mesurent la capacité de l'entreprise à honorer ses obligations à court terme.

**Liquidité générale (Current Ratio)**
```
Liquidité générale = Actif circulant total / Dettes à court terme
```
| Valeur | Appréciation |
|--------|--------------|
| > 1,5 | Bon |
| 1 - 1,5 | Acceptable |
| < 1 | Vigilance (l'actif circulant ne couvre pas les dettes CT) |

**Liquidité réduite (Quick Ratio)**
```
Liquidité réduite = (Créances clients + Disponibilités + VMP) / Dettes à court terme
```
| Valeur | Appréciation |
|--------|--------------|
| > 1 | Bon |
| 0,7 - 1 | Acceptable |
| < 0,7 | Vigilance |

**Liquidité immédiate (Cash Ratio)**
```
Liquidité immédiate = (Disponibilités + VMP) / Dettes à court terme
```
| Valeur | Appréciation |
|--------|--------------|
| > 0,3 | Bon |
| 0,1 - 0,3 | Acceptable |
| < 0,1 | Vigilance |

### 3. Ratios de rentabilité

Ces ratios mesurent l'efficacité de l'entreprise à générer du profit.

**ROE — Return on Equity (Rentabilité des capitaux propres)**
```
ROE = Résultat net / Capitaux propres × 100
```
| Valeur | Appréciation |
|--------|--------------|
| > 15% | Bon |
| 8% - 15% | Acceptable |
| < 8% | Faible (inférieur au coût du capital moyen) |

**ROA — Return on Assets (Rentabilité économique)**
```
ROA = Résultat net / Total actif × 100
  ou
ROA = Résultat d'exploitation × (1 - taux IS) / Total actif × 100  (vision économique)
```
| Valeur | Appréciation |
|--------|--------------|
| > 8% | Bon |
| 4% - 8% | Acceptable |
| < 4% | Faible |

**Rentabilité opérationnelle (ROCE)**
```
ROCE = Résultat d'exploitation / (Capitaux propres + Dettes financières nettes) × 100
```

**Taux de marge nette**
```
Taux de marge nette = Résultat net / CA HT × 100
```

**Taux de marge EBE**
```
Taux de marge EBE = EBE / CA HT × 100
```
| Secteur indicatif | Benchmark EBE/CA |
|-------------------|-----------------|
| Distribution / Négoce | 2% - 5% |
| Services | 8% - 20% |
| Industrie | 6% - 15% |
| BTP | 3% - 8% |

### 4. Ratios d'activité (gestion du cycle d'exploitation)

**Délai de rotation des stocks (DRS)**
```
DRS = Stocks / (Achats HT + Variation de stocks) × 360  (en jours)
```

**Délai de crédit clients (DCC)**
```
DCC = Créances clients TTC / CA TTC × 360  (en jours)
```
Benchmark : < 45 jours (norme légale de paiement en France : 60 jours fin de mois)

**Délai de crédit fournisseurs (DCF)**
```
DCF = Dettes fournisseurs TTC / Achats TTC × 360  (en jours)
```
Benchmark : 30 - 60 jours

### 5. Présenter le tableau récapitulatif complet

| Catégorie | Ratio | Valeur calculée | Benchmark indicatif | Appréciation |
|-----------|-------|-----------------|--------------------|-|
| Structure | Autonomie financière | X% | > 30% | Bon / Acceptable / Vigilance |
| Structure | Taux d'endettement | X | < 1 | Bon / Acceptable / Vigilance |
| Structure | Capacité de remboursement | X ans | < 3 ans | Bon / Acceptable / Vigilance |
| Structure | Couverture des intérêts | X | > 5 | Bon / Acceptable / Vigilance |
| Liquidité | Liquidité générale | X | > 1,5 | Bon / Acceptable / Vigilance |
| Liquidité | Liquidité réduite | X | > 0,7 | Bon / Acceptable / Vigilance |
| Liquidité | Liquidité immédiate | X | > 0,3 | Bon / Acceptable / Vigilance |
| Rentabilité | ROE | X% | > 10% | Bon / Acceptable / Vigilance |
| Rentabilité | ROA | X% | > 5% | Bon / Acceptable / Vigilance |
| Rentabilité | Taux de marge nette | X% | Selon secteur | Bon / Acceptable / Vigilance |
| Rentabilité | Taux de marge EBE | X% | Selon secteur | Bon / Acceptable / Vigilance |
| Activité | Délai clients | X jours | < 45 j | Bon / Acceptable / Vigilance |
| Activité | Délai fournisseurs | X jours | 30-60 j | Bon / Acceptable / Vigilance |
| Activité | Rotation des stocks | X jours | Selon secteur | Bon / Acceptable / Vigilance |

Légende des appréciations :
- **Bon** : ratio dans la zone optimale
- **Acceptable** : ratio dans la norme, mais à surveiller
- **Vigilance** : ratio dégradé, action recommandée

### 6. Comparer avec les benchmarks sectoriels via data.gouv.fr

Si le code NAF/APE de l'entreprise est connu, interroger data.gouv.fr pour obtenir les statistiques sectorielles de la Banque de France ou de l'INSEE et positionner l'entreprise (quartile supérieur / médiane / quartile inférieur) par rapport à ses pairs.

### 7. Formuler le diagnostic global

Synthétiser l'analyse en 3 à 5 points structurés :

**Structure du diagnostic :**
1. **Point fort principal** : identifier le ou les ratios qui se distinguent positivement
2. **Point de vigilance principal** : identifier le ou les ratios les plus préoccupants
3. **Tendance** : si les données N et N-1 sont disponibles, indiquer si la situation s'améliore ou se dégrade
4. **Profil de risque global** : faible / modéré / élevé, avec justification
5. **Positionnement sectoriel** : si les données sectorielles sont disponibles

### 8. Formuler des recommandations concrètes

Pour chaque ratio en zone "Vigilance", proposer un axe d'amélioration actionnable :

| Ratio dégradé | Axe d'amélioration |
|---------------|-------------------|
| Autonomie financière faible | Augmentation de capital, mise en réserve du résultat, réduction des distributions |
| Endettement élevé | Remboursement anticipé, renégociation de la structure de dette, cession d'actifs non stratégiques |
| Capacité de remboursement > 3 ans | Amélioration de la CAF (hausse des marges, réduction des charges fixes), report des investissements |
| Liquidité tendue | Optimisation du BFR (réduction des délais clients, gestion des stocks), ouverture d'une ligne de crédit confirmée |
| Délais clients élevés | Mise en place d'une politique de relance, affacturage, conditions de paiement contractuelles |
| ROE faible | Amélioration des marges opérationnelles, révision de la structure de coûts, optimisation fiscale |

## Règles importantes

- Toujours calculer les ratios à partir des données fournies sans extrapolation
- Préciser les données manquantes qui empêchent le calcul d'un ratio
- Contextualiser les benchmarks : un ratio "mauvais" dans un secteur peut être normal dans un autre
- Ne pas conclure à une situation de défaillance sur la base des seuls ratios — ils sont des indicateurs, pas des certitudes
- Rappeler que cette analyse est indicative et ne remplace pas l'avis d'un expert-comptable, d'un commissaire aux comptes ou d'un conseiller financier
- Pour les entreprises en difficulté avérée, mentionner les dispositifs d'accompagnement : CODEFI, médiateur du crédit aux entreprises, procédures amiables (mandat ad hoc, conciliation)
