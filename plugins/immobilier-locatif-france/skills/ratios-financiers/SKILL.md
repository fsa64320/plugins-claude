---
name: ratios-financiers
description: Ce skill doit être utilisé quand l'utilisateur demande des ratios financiers pour une société immobilière locative ou pose des questions sur la rentabilité et la santé financière d'une SCI, foncière, SARL de famille : "LTV", "loan-to-value", "DSCR", "debt service coverage ratio", "rendement locatif", "rendement brut", "rendement net", "taux de vacance", "effet de levier immobilier", "levier financier", "taux d'endettement", "autonomie financière", "capacité de remboursement", "ratios immobiliers", "solvabilité", "rentabilité immobilière".
version: 2.0.0
allowed-tools: [Read, Glob]
---

# Ratios financiers d'une société de gestion immobilière locative

## Objectif

Calculer et interpréter les ratios financiers adaptés aux sociétés dont l'activité est la détention d'actifs immobiliers financés à crédit et la génération de revenus locatifs. Ces ratios permettent d'évaluer la solidité patrimoniale, la soutenabilité de l'endettement, la performance locative et l'exposition aux risques spécifiques du secteur.

## Organisation des ratios

Les ratios sont organisés en quatre familles selon les décisions de gestion qu'ils informent :

1. **Ratios de structure de financement** — comment l'actif est financé
2. **Ratios de performance locative** — ce que rapportent les biens
3. **Ratios de soutenabilité de la dette** — capacité à rembourser
4. **Ratios de solvabilité et risque** — résistance aux chocs

---

## Famille 1 — Structure de financement

### Loan-to-Value (LTV)

```
LTV = Encours total des emprunts immobiliers / Valeur des actifs immobiliers
```

| LTV | Appréciation |
|-----|--------------|
| < 50% | Très faible endettement — sécurité élevée |
| 50–70% | Niveau courant pour un investissement prudent |
| 70–80% | Niveau standard dans l'immobilier locatif |
| 80–90% | Exposition élevée — faible marge en cas de dépréciation |
| > 90% | Critique — risque de valeur nette négative |

- Si la valeur de marché n'est pas disponible, utiliser la VNC comptable comme proxy en précisant la limite (VNC peut sous-estimer la valeur réelle sur des biens anciens)
- Recommander une expertise immobilière si la VNC et la valeur de marché semblent diverger significativement

### Taux d'autonomie financière immobilière

```
Taux d'autonomie = Capitaux propres / Total passif
```

| Ratio | Appréciation |
|-------|--------------|
| > 30% | Solide — les fonds propres couvrent un tiers du financement |
| 15–30% | Courant dans l'immobilier locatif à crédit |
| 5–15% | Faible — forte dépendance bancaire |
| < 5% | Très faible — vulnérable aux aléas |

### Ratio dettes financières / Capitaux propres (gearing)

```
Gearing = Dettes financières totales / Capitaux propres
```

- Gearing < 3 : endettement maîtrisé
- Gearing 3–7 : niveau élevé mais courant dans l'immobilier patrimonial
- Gearing > 10 : très fortement endetté — structure fragile
- Gearing négatif (CP négatifs) : situation de surendettement comptable

---

## Famille 2 — Performance locative

### Rendement locatif brut

```
Rendement brut = Loyers annuels bruts / Valeur d'acquisition des biens (ou valeur de marché)
```

| Rendement brut | Appréciation (ordre de grandeur France 2024) |
|----------------|----------------------------------------------|
| < 3% | Faible — marchés très tendus (Paris centre, Côte d'Azur) |
| 3–5% | Moyen — grandes métropoles régionales |
| 5–8% | Bon — villes moyennes, immobilier ancien |
| > 8% | Élevé — à vérifier : risque de vacance ou de dégradation élevé ? |

### Rendement locatif net de charges (avant financement)

```
Rendement net = EBE locatif / Valeur d'acquisition des biens
              = (Loyers bruts - Charges décaissables d'exploitation) / Valeur des actifs
```

- Mesure la vraie performance économique hors financement
- Écart brut/net élevé (> 2 points) : charges d'exploitation excessives ou mal maîtrisées

### Rendement locatif net après financement (cash-on-cash return)

```
Rendement net après financement = Cash-flow net annuel / Apport personnel (fonds propres investis)
                                = Cash-flow locatif net / Capitaux propres
```

- Mesure le retour sur l'investissement en fonds propres
- Peut être négatif (effort d'épargne) ou très élevé grâce à l'effet de levier

### Taux de vacance locative

```
Taux de vacance = Jours/mois de vacance dans l'année / 365 (ou 12)
```
Ou, si on dispose des montants :
```
Taux de vacance financier = (Loyers théoriques - Loyers perçus) / Loyers théoriques
```

| Taux de vacance | Appréciation |
|-----------------|--------------|
| < 3% | Excellent — très bonne occupation |
| 3–7% | Normal — correspond à 1 mois de vacance sur l'année |
| 7–15% | Élevé — à investiguer (localisation, état du bien, prix) |
| > 15% | Critique — risque structurel sur la rentabilité |

---

## Famille 3 — Soutenabilité de la dette

### Debt Service Coverage Ratio (DSCR)

```
DSCR = EBE locatif / Annuités totales d'emprunt (capital remboursé + intérêts)
```

| DSCR | Appréciation |
|------|--------------|
| > 1,5 | Très confortable — large marge de sécurité |
| 1,2–1,5 | Confortable — niveau attendu par les banques |
| 1,0–1,2 | Tendu — peu de marge face à la vacance |
| < 1,0 | Insuffisant — les loyers ne couvrent pas le remboursement |

- DSCR minimum bancaire généralement exigé à l'octroi : 1,1 à 1,25 selon les établissements
- Calculer le DSCR en scénario de stress : que se passe-t-il avec 15% de vacance ou +1% de taux variable ?

### Capacité de remboursement

```
Capacité de remboursement = Dettes financières totales / CAF annuelle
```

- < 5 ans : excellent
- 5–10 ans : correct
- 10–15 ans : acceptable pour l'immobilier (actifs de très longue durée de vie)
- > 15 ans : élevé — la CAF ne rembourse l'encours qu'en très longue durée

### Couverture des intérêts

```
Couverture des intérêts = EBE locatif / Charges financières (intérêts seuls)
```

- > 2 : charges financières bien couvertes
- 1,5–2 : niveau acceptable
- 1,0–1,5 : fragile — une légère baisse des loyers rend les intérêts non couverts
- < 1 : les intérêts seuls ne sont pas couverts par l'EBE — situation non soutenable

### Ratio loyers / charges financières

```
Ratio loyers/intérêts = Loyers bruts annuels / Intérêts d'emprunt annuels
```

- Indicateur simple et rapide : les loyers doivent couvrir a minima 2× les intérêts pour laisser de la marge aux charges d'exploitation et au remboursement du capital

---

## Famille 4 — Solvabilité et risque

### Effet de levier immobilier

```
Effet de levier = Rendement des actifs (ROA) - Coût de la dette (taux d'intérêt moyen)
ROA = EBE locatif / Valeur totale des actifs immobiliers
Coût de la dette = Charges financières (intérêts) / Encours moyen des emprunts
```

- Effet de levier positif (ROA > coût de la dette) : l'endettement amplifie la rentabilité des fonds propres — le crédit est rentable
- Effet de levier nul : le crédit ne crée pas de valeur
- Effet de levier négatif (ROA < coût de la dette) : l'endettement détruit de la rentabilité — situation fréquente en période de taux élevés sur des biens à faible rendement

### Solvabilité globale (ratio de couverture des dettes)

```
Solvabilité = Total actif net (VNC) / Total des dettes
```

- > 1,5 : bonne solvabilité
- 1,0–1,5 : acceptable
- < 1,0 : actifs insuffisants pour couvrir les dettes en valeur comptable (à pondérer par la valeur de marché)

### Analyse de sensibilité (stress tests)

Calculer l'impact sur le cash-flow net et le DSCR selon trois scénarios :

| Scénario | Hypothèse | Impact sur EBE | DSCR résultant |
|----------|-----------|----------------|----------------|
| Base | Situation actuelle | - | X,X |
| Vacance +15% | 15% des loyers perdus | -15% EBE | X,X |
| Taux variable +2% | Si emprunt à taux variable | Intérêts +X€ | X,X |
| Charges +20% | Hausse copropriété/taxe foncière | -X% EBE | X,X |

---

## Présentation synthétique

| Ratio | Valeur calculée | Benchmark secteur | Appréciation |
|-------|----------------|-------------------|--------------|
| LTV | X% | 70–80% | Faible / Normal / Élevé |
| Autonomie financière | X% | 15–25% | Faible / Correct / Solide |
| Gearing | X | 3–7× | Maîtrisé / Élevé / Excessif |
| Rendement brut | X% | 3–8% selon localisation | Faible / Moyen / Bon |
| Rendement net (avant financement) | X% | 2–6% | Faible / Moyen / Bon |
| Taux de vacance | X% | < 7% | Excellent / Normal / Élevé |
| DSCR | X,X | > 1,2 | Confortable / Tendu / Insuffisant |
| Couverture des intérêts | X,X | > 1,5 | Solide / Fragile / Critique |
| Capacité de remboursement | X ans | 10–15 ans | Bon / Acceptable / Long |
| Effet de levier | +/- X pts | Positif souhaité | Favorable / Neutre / Défavorable |

## Règles importantes

- Ne jamais calculer un ratio sans préciser si la valeur utilisée est la VNC comptable ou la valeur de marché
- Pour les sociétés SCI à l'IR, signaler que la capacité de remboursement des emprunts peut s'appuyer sur des ressources extérieures (revenus personnels des associés) non visibles dans les comptes sociaux
- Préciser l'exercice concerné et, si N-1 est disponible, présenter l'évolution
- Pour les emprunts in fine, adapter le calcul du DSCR : seuls les intérêts sont annuités — le capital est remboursé en une fois à l'échéance (risque de refinancement)
- Rappeler que cette analyse est indicative et ne remplace pas l'avis d'un expert-comptable, d'un gestionnaire de patrimoine ou d'un conseiller en gestion de fortune
