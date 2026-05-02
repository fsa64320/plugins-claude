---
name: analyse-bilan
description: Ce skill doit être utilisé quand l'utilisateur partage un bilan comptable (actif/passif) ou pose des questions sur la structure bilancielle d'une société française : "analyse mon bilan", "que signifie mon actif immobilisé", "explique le passif", "fonds propres", "dettes financières", "BFR", "besoin en fonds de roulement", "trésorerie nette", "fonds de roulement", "FRNG", "capitaux permanents", "actif circulant", "dettes à court terme", "équilibre financier".
version: 1.0.0
allowed-tools: [Read, Glob]
---

# Analyse du bilan comptable

## Objectif

Analyser la structure du bilan d'une société française, calculer les grands équilibres financiers (FRNG, BFR, Trésorerie Nette) et formuler un diagnostic sur l'équilibre financier de l'entreprise.

## Processus

### 1. Identifier et structurer les grandes masses du bilan

**ACTIF**
- Actif immobilisé (AI) : immobilisations incorporelles, corporelles, financières
- Actif circulant (AC) : stocks, créances clients, autres créances, VMP, disponibilités
- Charges constatées d'avance

**PASSIF**
- Capitaux propres (CP) : capital, réserves, report à nouveau, résultat de l'exercice
- Provisions pour risques et charges
- Dettes financières à long terme (emprunts, dettes auprès des établissements de crédit > 1 an)
- Dettes à court terme (DCT) : dettes fournisseurs, dettes fiscales et sociales, emprunts CT, découverts

### 2. Calculer les trois indicateurs d'équilibre financier

**Fonds de Roulement Net Global (FRNG)**
```
FRNG = Capitaux Permanents - Actif Immobilisé Net
     = (Capitaux Propres + Provisions + Dettes LT) - Actif Immobilisé Net
```
- FRNG > 0 : les ressources stables couvrent les emplois stables — situation saine
- FRNG < 0 : les ressources stables ne couvrent pas l'actif immobilisé — risque de déséquilibre

**Besoin en Fonds de Roulement (BFR)**
```
BFR = (Stocks + Créances clients + Autres créances d'exploitation)
    - (Dettes fournisseurs + Dettes fiscales et sociales + Autres dettes d'exploitation)
```
- BFR > 0 : besoin de financement lié au cycle d'exploitation (courant pour les entreprises industrielles et commerciales)
- BFR < 0 : ressource d'exploitation nette (courant pour la grande distribution)
- BFR très élevé par rapport au CA : signal d'alerte sur la gestion du poste clients ou des stocks

**Trésorerie Nette (TN)**
```
TN = FRNG - BFR
   = (Disponibilités + VMP) - (Découverts bancaires + Concours bancaires courants)
```
- TN > 0 : l'entreprise dispose de liquidités excédentaires
- TN < 0 : l'entreprise est en tension de trésorerie et dépend du financement bancaire court terme

### 3. Présenter le tableau de synthèse des grandes masses

| Indicateur | Montant (€) | Interprétation |
|------------|-------------|----------------|
| Actif Immobilisé Net | X | Emplois stables |
| Capitaux Permanents | X | Ressources stables |
| **FRNG** | **X** | **Excédent / Insuffisance** |
| Actif Circulant d'exploitation | X | |
| Dettes d'exploitation CT | X | |
| **BFR** | **X** | **Besoin / Ressource** |
| **Trésorerie Nette** | **X** | **Saine / Tendue** |

### 4. Expliquer chaque poste en langage simple

Pour chaque grand poste identifié dans le bilan fourni :
- Donner une définition courte et concrète
- Indiquer ce que représente ce montant pour l'activité de l'entreprise
- Signaler si le montant semble cohérent avec la taille/secteur de l'entreprise

### 5. Formuler le diagnostic d'équilibre financier

Analyser les trois situations possibles et formuler un avis clair :

- **Situation équilibrée** : FRNG > 0, BFR maîtrisé, TN positive
- **Situation sous tension** : FRNG insuffisant pour couvrir le BFR, TN négative chronique
- **Situation critique** : FRNG négatif, BFR élevé, recours excessif aux concours bancaires

### 6. Signaler les déséquilibres et points d'attention

- FRNG négatif : les ressources stables ne financent pas l'intégralité des actifs durables
- BFR supérieur à 60 jours de CA : gestion du poste clients ou des stocks à revoir
- Trésorerie nette fortement négative : dépendance aux crédits de trésorerie, risque de liquidité
- Capitaux propres négatifs ou très faibles : capitaux propres inférieurs à la moitié du capital social (obligation de convocation d'une AGE selon l'article L.223-42 / L.225-248 du Code de commerce)
- Dettes financières très supérieures aux capitaux propres : levier excessif

## Règles importantes

- Ne jamais inventer un chiffre : si un poste est absent du document fourni, l'indiquer explicitement et demander la précision
- Distinguer les dettes financières (emprunts bancaires) des dettes d'exploitation (fournisseurs, sociales) dans le calcul du BFR
- Préciser l'exercice concerné (N) et, si disponible, comparer avec N-1
- Rappeler que cette analyse est indicative et ne remplace pas l'avis d'un expert-comptable ou commissaire aux comptes
- Pour les sociétés en difficulté, mentionner les procédures préventives disponibles (mandat ad hoc, conciliation, sauvegarde)
