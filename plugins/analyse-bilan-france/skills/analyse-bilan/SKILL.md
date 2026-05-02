---
name: analyse-bilan
description: Ce skill doit être utilisé quand l'utilisateur partage un bilan comptable d'une société immobilière ou pose des questions sur la structure bilancielle d'une SCI, foncière, SARL de famille ou société de gestion locative : "analyse mon bilan", "actif immobilisé", "immeubles de placement", "emprunts bancaires", "dépôts de garantie", "fonds propres", "capitaux permanents", "LTV", "loan-to-value", "endettement immobilier", "BFR", "fonds de roulement", "FRNG", "trésorerie nette", "équilibre financier", "SCI", "foncière", "patrimoine immobilier locatif".
version: 2.0.0
allowed-tools: [Read, Glob]
---

# Analyse du bilan d'une société de gestion immobilière locative

## Objectif

Analyser la structure du bilan d'une société dont l'activité consiste à acquérir des biens immobiliers à crédit et à les louer. Calculer les grands équilibres financiers en tenant compte des spécificités du secteur (actif dominé par les immeubles, passif dominé par les emprunts LT, BFR quasi-nul) et formuler un diagnostic sur la solidité patrimoniale et la soutenabilité de l'endettement.

## Spécificités du bilan immobilier locatif

Pour ce type de société, la structure bilancielle est radicalement différente d'une entreprise commerciale :

- **Actif immobilisé très dominant** : les immeubles (valeur brute) représentent l'essentiel de l'actif
- **Actif circulant quasi-nul** : pas de stocks, créances limitées aux loyers en retard et provisions pour charges
- **BFR structurellement faible voire négatif** : les loyers sont encaissés d'avance, les dépôts de garantie sont au passif
- **Endettement bancaire LT massif** : les emprunts immobiliers constituent la majorité du passif
- **Dépôts de garantie locataires** : figurent au passif (dettes envers les locataires), typiquement 1 à 2 mois de loyers

## Processus

### 1. Identifier et structurer les grandes masses du bilan

**ACTIF**

*Actif immobilisé (AI) — masse dominante*
- Immobilisations corporelles : immeubles (valeur brute d'acquisition), travaux et aménagements incorporés
- Cumul des amortissements (à déduire pour obtenir la valeur nette comptable — VNC)
- Immobilisations financières : cautionnements versés, dépôts de garantie versés, parts de sociétés immobilières
- Note : la VNC peut s'éloigner significativement de la valeur de marché — mentionner si une expertise récente est disponible

*Actif circulant (AC) — masse résiduelle*
- Créances locataires (loyers impayés)
- Charges constatées d'avance (assurances, taxes prépayées)
- Disponibilités (compte courant, épargne affectée au remboursement des emprunts)

**PASSIF**

*Ressources propres*
- Capitaux propres (CP) : capital social, réserves, report à nouveau, résultat de l'exercice
- Attention : pour les SCI à l'IR, le résultat est imputé aux associés — le résultat affiché peut être nul ou symbolique

*Dettes financières à long terme (DLT) — masse dominante*
- Emprunts immobiliers bancaires (capital restant dû, partie > 1 an)
- Autres emprunts (familial, associés, obligataire)
- Distinction importante : partie CT des emprunts (échéances < 1 an) à classer en DCT

*Dettes à court terme (DCT)*
- Partie CT des emprunts immobiliers (prochaines échéances)
- Dépôts de garantie locataires (dette envers les locataires, exigible à leur départ)
- Dettes fiscales (taxe foncière à payer) et sociales
- Dettes fournisseurs (syndic, prestataires de maintenance)
- Loyers perçus d'avance (produits constatés d'avance)

### 2. Calculer les indicateurs d'équilibre financier adaptés au secteur

**Fonds de Roulement Net Global (FRNG)**
```
FRNG = Capitaux Permanents - Actif Immobilisé Net
     = (Capitaux Propres + Dettes LT) - Actif Immobilisé Net (VNC)
```
- Pour une société immobilière, le FRNG est souvent **faible ou négatif** : c'est structurellement normal quand l'actif immobilisé est massivement financé par de l'emprunt LT
- FRNG > 0 : les ressources permanentes couvrent les actifs durables — situation confortable
- FRNG légèrement négatif : courant dans le secteur si les emprunts LT couvrent la quasi-totalité des immeubles
- FRNG fortement négatif : risque de déséquilibre si les emprunts CT financent des actifs immobiliers LT

**Besoin en Fonds de Roulement (BFR)**
```
BFR = Créances locataires - (Dettes fournisseurs + Dettes fiscales/sociales + Loyers d'avance)
```
- Pour une société locative, le BFR est **quasi-nul ou légèrement négatif** : normal et sain
- BFR négatif : les locataires paient d'avance et les dépôts de garantie constituent une ressource d'exploitation
- BFR positif et significatif : signal d'alerte — impayés locataires élevés à investiguer

**Trésorerie Nette (TN)**
```
TN = FRNG - BFR = Disponibilités - Découverts bancaires
```
- TN > 0 : capacité à faire face aux appels de charges et aux échéances d'emprunt
- TN négative chronique : risque de liquidité si les loyers perçus ne couvrent pas les annuités

**Loan-to-Value (LTV) — ratio clé du secteur**
```
LTV = Total des emprunts immobiliers / Valeur de marché des actifs immobiliers
```
- Si la valeur de marché n'est pas disponible, utiliser la VNC comme proxy (en précisant la limite)
- LTV < 60% : situation confortable, marge de manœuvre importante
- LTV 60-80% : niveau courant pour un investissement immobilier locatif
- LTV > 80% : exposition élevée, sensible aux corrections de marché
- LTV > 100% : capitaux propres négatifs en valeur de marché — situation critique

### 3. Présenter le tableau de synthèse des grandes masses

| Indicateur | Montant (€) | % du total actif | Interprétation |
|------------|-------------|-----------------|----------------|
| Actif Immobilisé Net (VNC immeubles) | X | X% | Emplois stables |
| Capitaux Permanents | X | X% | Ressources stables |
| **FRNG** | **X** | | **Excédent / Insuffisance** |
| Actif Circulant | X | X% | |
| Dettes CT (hors emprunts) | X | | |
| **BFR** | **X** | | **Besoin / Ressource** |
| **Trésorerie Nette** | **X** | | **Saine / Tendue** |
| **LTV (si valeur marché disponible)** | **X%** | | **Soutenable / Élevé / Critique** |

### 4. Expliquer les postes clés en langage simple

Pour chaque grand poste identifié :
- Donner sa définition concrète dans le contexte immobilier
- Indiquer ce que le montant représente pour la gestion locative
- Signaler si le ratio (par rapport à la valeur des actifs ou aux loyers annuels) est cohérent

### 5. Formuler le diagnostic patrimonial et financier

**Axe 1 — Structure du bilan**
- Ratio fonds propres / total passif : < 20% courant dans l'immobilier à crédit, < 10% fragile
- Capacité des capitaux propres à absorber une dépréciation des actifs

**Axe 2 — Soutenabilité de l'endettement**
- Ratio dettes financières LT / VNC des immeubles (proxy LTV comptable)
- Durée résiduelle moyenne des emprunts vs. durée résiduelle économique des biens

**Axe 3 — Liquidité**
- Trésorerie disponible vs. prochaines échéances d'emprunt (12 mois)
- Existence d'une réserve pour gros travaux ou vacance locative

### 6. Signaler les déséquilibres et points d'attention spécifiques

- **LTV > 80%** : surexposition à la dette, risque en cas de baisse de valeur des actifs
- **Capitaux propres négatifs** : fonds propres inférieurs à la moitié du capital social → obligation légale de convocation d'AGE (art. L.223-42 / L.225-248 C.com.) ; pour une SCI, risque personnel des associés selon les statuts
- **Dépôts de garantie non provisionnés** : dette réelle envers les locataires, à distinguer de la trésorerie disponible
- **VNC très éloignée de la valeur de marché** : fréquent sur des biens anciens très amortis — la LTV comptable sous-estime la solidité réelle ; recommander une expertise immobilière
- **Emprunts in fine** : le capital n'est pas amorti progressivement, le risque de refinancement à l'échéance doit être identifié
- **Trésorerie nette insuffisante pour 3 mois d'annuités** : tension de liquidité préoccupante

## Règles importantes

- Ne jamais inventer un chiffre : si un poste est absent, l'indiquer et demander la précision
- Distinguer systématiquement la valeur brute des immeubles et la VNC (valeur nette après amortissements)
- Pour les SCI à l'IR, signaler que les résultats sont fiscalement transparents — l'imposition réelle est chez les associés
- Préciser l'exercice (N) et comparer avec N-1 si disponible
- Rappeler que cette analyse est indicative et ne remplace pas l'avis d'un expert-comptable ou d'un évaluateur immobilier agréé
