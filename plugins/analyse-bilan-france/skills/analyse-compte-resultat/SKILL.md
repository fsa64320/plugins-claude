---
name: analyse-compte-resultat
description: Ce skill doit être utilisé quand l'utilisateur partage un compte de résultat ou pose des questions sur la performance économique d'une société française : "CA", "chiffre d'affaires", "résultat net", "EBE", "excédent brut d'exploitation", "marge", "charges d'exploitation", "résultat d'exploitation", "résultat financier", "résultat exceptionnel", "soldes intermédiaires de gestion", "SIG", "valeur ajoutée", "marge commerciale", "résultat courant", "capacité d'autofinancement", "CAF".
version: 1.0.0
allowed-tools: [Read, Glob]
---

# Analyse du compte de résultat

## Objectif

Calculer les Soldes Intermédiaires de Gestion (SIG) à partir du compte de résultat d'une société française, mesurer les taux de marge, identifier les postes de charges anormaux et formuler un diagnostic sur la performance économique de l'entreprise.

## Processus

### 1. Extraire les données brutes du compte de résultat

Collecter et organiser les éléments suivants depuis le document fourni :

**Produits d'exploitation**
- Ventes de marchandises
- Production vendue (biens et services)
- Production stockée / déstockée
- Production immobilisée
- Subventions d'exploitation
- Reprises sur provisions et transferts de charges
- Autres produits

**Charges d'exploitation**
- Achats de marchandises (± variation de stocks)
- Achats de matières premières et autres approvisionnements (± variation de stocks)
- Autres achats et charges externes (sous-traitance, loyers, honoraires...)
- Impôts, taxes et versements assimilés
- Charges de personnel (salaires + charges sociales)
- Dotations aux amortissements et provisions
- Autres charges

**Résultat financier**
- Produits financiers (intérêts reçus, dividendes, produits de cessions VMP)
- Charges financières (intérêts des emprunts, agios, pertes de change)

**Résultat exceptionnel**
- Produits exceptionnels (cessions d'actifs, subventions d'investissement virées)
- Charges exceptionnelles (pénalités, VNC des actifs cédés, provisions exceptionnelles)

**Participation et impôt**
- Participation des salariés aux résultats
- Impôts sur les bénéfices (IS)

### 2. Calculer les Soldes Intermédiaires de Gestion (SIG)

Appliquer la cascade des SIG dans l'ordre suivant :

**Marge commerciale (MC)**
```
MC = Ventes de marchandises HT - Coût d'achat des marchandises vendues
   = Ventes de marchandises - (Achats de marchandises ± Variation de stocks marchés)
```
- Applicable uniquement aux entreprises ayant une activité de négoce
- Taux de marge commerciale = MC / Ventes de marchandises

**Production de l'exercice**
```
Production = Production vendue + Production stockée + Production immobilisée
```
- Applicable aux entreprises industrielles et de services

**Valeur Ajoutée (VA)**
```
VA = Marge commerciale + Production de l'exercice
   - Consommations en provenance des tiers (achats de matières + autres achats et charges externes)
```
- Mesure la richesse créée par l'entreprise
- Taux de VA = VA / CA HT (indicateur de l'intensité capitalistique)

**Excédent Brut d'Exploitation (EBE)**
```
EBE = VA + Subventions d'exploitation
    - Impôts, taxes et versements assimilés
    - Charges de personnel (salaires + charges sociales)
```
- Principal indicateur de la performance opérationnelle, indépendant de la politique d'amortissement et de financement
- EBE négatif = Insuffisance Brute d'Exploitation (IBE) : signal critique

**Résultat d'Exploitation (RE)**
```
RE = EBE
   + Reprises sur provisions et amortissements d'exploitation + Autres produits d'exploitation
   - Dotations aux amortissements et provisions d'exploitation - Autres charges d'exploitation
```

**Résultat Courant Avant Impôt (RCAI)**
```
RCAI = RE + Résultat financier
     = RE + Produits financiers - Charges financières
```
- Un résultat financier très négatif signale un endettement coûteux

**Résultat Exceptionnel**
```
Résultat exceptionnel = Produits exceptionnels - Charges exceptionnelles
```
- Un résultat exceptionnel récurrent mérite une analyse approfondie

**Résultat Net**
```
Résultat Net = RCAI + Résultat exceptionnel
             - Participation des salariés
             - Impôts sur les bénéfices
```

**Capacité d'Autofinancement (CAF) — méthode additive**
```
CAF = Résultat Net
    + Dotations aux amortissements et provisions (exploitation + financières + exceptionnelles)
    - Reprises sur provisions
    - Plus-values de cession nettes d'impôt (produits de cession - VNC)
```

### 3. Présenter le tableau de synthèse des SIG

| Solde | Montant N (€) | % du CA HT | Montant N-1 (€) | Evolution |
|-------|---------------|------------|-----------------|-----------|
| Chiffre d'affaires HT | X | 100% | X | +/- % |
| Marge commerciale | X | X% | X | +/- % |
| Valeur Ajoutée | X | X% | X | +/- % |
| EBE | X | X% | X | +/- % |
| Résultat d'exploitation | X | X% | X | +/- % |
| Résultat financier | X | X% | X | +/- % |
| RCAI | X | X% | X | +/- % |
| Résultat exceptionnel | X | X% | X | +/- % |
| Résultat net | X | X% | X | +/- % |
| CAF | X | X% | X | +/- % |

### 4. Calculer les taux de marge clés

| Ratio | Formule | Valeur | Appréciation |
|-------|---------|--------|--------------|
| Taux de marge brute | MC / CA HT | X% | |
| Taux de VA | VA / CA HT | X% | |
| Taux de marge EBE | EBE / CA HT | X% | Benchmark : 5-15% selon secteur |
| Taux de marge d'exploitation | RE / CA HT | X% | |
| Taux de marge nette | Résultat Net / CA HT | X% | |
| Taux de CAF | CAF / CA HT | X% | |

### 5. Comparer avec les ratios sectoriels via data.gouv.fr

Si le secteur d'activité de l'entreprise est connu (code NAF/APE), interroger data.gouv.fr pour obtenir les ratios financiers sectoriels de référence (Banque de France / INSEE) et positionner l'entreprise par rapport à la médiane de son secteur.

### 6. Identifier les points de vigilance

Signaler systématiquement les anomalies suivantes si elles sont présentes :
- EBE négatif ou en forte dégradation : l'activité opérationnelle ne génère plus de surplus
- Charges de personnel représentant plus de 70% de la VA : niveau élevé, à contextualiser
- Résultat financier fortement négatif : charges d'intérêts qui pèsent sur la rentabilité
- Résultat exceptionnel significatif et récurrent : masque peut-être la performance réelle
- Résultat net positif uniquement grâce au résultat exceptionnel : fragilité structurelle
- CAF insuffisante pour couvrir les remboursements d'emprunts : risque de capacité de remboursement

## Règles importantes

- Ne jamais inventer un solde si les données sources sont manquantes ou ambiguës : demander la précision
- Bien distinguer CA HT (hors taxes) et CA TTC dans les ratios
- Pour les entreprises avec activités mixtes (négoce + production), calculer les deux marges séparément
- Préciser l'exercice concerné et effectuer la comparaison N / N-1 si les deux exercices sont disponibles
- Rappeler que les SIG constituent une analyse indicative ne remplaçant pas l'avis d'un expert-comptable
