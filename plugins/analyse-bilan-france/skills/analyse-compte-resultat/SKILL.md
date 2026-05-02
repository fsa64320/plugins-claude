---
name: analyse-compte-resultat
description: Ce skill doit être utilisé quand l'utilisateur partage un compte de résultat d'une société immobilière locative ou pose des questions sur les revenus et charges d'une SCI, foncière, SARL de famille ou société de gestion locative : "loyers", "revenus locatifs", "charges d'exploitation", "intérêts d'emprunt", "taxe foncière", "amortissements", "résultat net", "cash-flow locatif", "cash-flow net", "capacité d'autofinancement", "CAF", "rendement", "résultat d'exploitation", "charges financières", "remboursement d'emprunt", "annuités", "résultat foncier".
version: 2.0.0
allowed-tools: [Read, Glob]
---

# Analyse du compte de résultat d'une société de gestion immobilière locative

## Objectif

Analyser la performance économique d'une société dont les revenus proviennent exclusivement ou principalement de loyers. Calculer les soldes clés adaptés au secteur immobilier (EBE locatif, résultat d'exploitation, cash-flow locatif, cash-flow après service de la dette), mesurer la rentabilité et la capacité à couvrir les charges financières liées aux emprunts immobiliers.

## Spécificités du compte de résultat immobilier locatif

La cascade des SIG standard (marge commerciale → production → VA → EBE) est partiellement inadaptée :
- **Pas de ventes de marchandises ni de production vendue** : le chiffre d'affaires = loyers perçus (hors charges locatives refacturées)
- **Charges d'exploitation dominées par les amortissements et les charges financières** : ces deux postes peuvent dépasser les loyers bruts dans les premières années
- **La distinction charges décaissables / non-décaissables est essentielle** : les amortissements réduisent le résultat comptable mais ne sont pas des sorties de trésorerie
- **Le cash-flow après service de la dette** (loyers - charges décaissables - annuités capital+intérêts) est l'indicateur de gestion le plus important pour l'investisseur

## Processus

### 1. Extraire et structurer les données du compte de résultat

**Produits d'exploitation — revenus locatifs**
- Loyers bruts perçus (hors charges locatives récupérables)
- Charges locatives refacturées aux locataires (provisions pour charges de copropriété)
- Indemnités d'assurance loyers impayés encaissées
- Produits accessoires (parking, cave, antenne)
- Reprises sur provisions pour dépréciation de créances locataires

**Charges d'exploitation**

*Charges décaissables (sorties de trésorerie réelles)*
- Charges de copropriété non récupérables sur locataires
- Taxe foncière (sur les propriétés bâties)
- Primes d'assurance (multirisque immeuble, loyers impayés)
- Honoraires de gestion locative (agence ou administrateur de biens)
- Frais d'entretien courant et petites réparations
- Frais de remise en état entre deux locataires
- Frais comptables, juridiques, d'assemblée générale

*Charges non-décaissables (réductions comptables sans sortie de trésorerie)*
- Dotations aux amortissements des immeubles (linéaire sur 25-50 ans selon composants)
- Dotations aux amortissements des travaux incorporés
- Dotations aux provisions pour créances douteuses (loyers impayés)

**Résultat financier**
- Charges financières : intérêts des emprunts immobiliers, frais de dossier étalés, assurance emprunteur (quote-part intérêts)
- Produits financiers : intérêts sur comptes d'épargne, sur dépôts de garantie placés (si applicable)
- Note : les intérêts d'emprunt constituent souvent la charge financière la plus lourde, surtout en début de crédit

**Résultat exceptionnel**
- Plus ou moins-values de cession d'immeuble (produit de cession - VNC)
- Remboursements d'assurance exceptionnels
- Pénalités reçues ou versées

**Impôts**
- IS (si société soumise à l'IS : SARL, SAS, SCI à l'IS)
- Pour les SCI à l'IR : pas d'IS au niveau société, le résultat est imposé directement chez les associés au titre des revenus fonciers — le compte de résultat affiche un résultat avant impôt des associés

### 2. Calculer les soldes clés adaptés au secteur immobilier

**Revenus locatifs nets de charges récupérables**
```
Revenus locatifs nets = Loyers bruts - Charges locatives non récupérées sur locataires
```
- C'est la base de calcul des rendements

**Excédent Brut d'Exploitation locatif (EBE locatif)**
```
EBE locatif = Loyers bruts
            - Charges décaissables d'exploitation
              (copropriété non récupérable + taxe foncière + assurances + gestion + entretien + frais divers)
```
- Mesure la performance opérationnelle hors politique d'amortissement et hors financement
- EBE locatif négatif = les charges courantes dépassent les loyers — situation critique

**Résultat d'Exploitation (RE)**
```
RE = EBE locatif
   - Dotations aux amortissements des immeubles et travaux
   - Dotations aux provisions pour loyers douteux
   + Reprises sur provisions
```
- Fréquemment négatif pour un immeuble récemment acquis : les amortissements sont élevés par rapport aux loyers
- Un RE négatif n'est pas nécessairement alarmant si le cash-flow est positif

**Résultat Courant Avant Impôt (RCAI)**
```
RCAI = RE + Résultat financier
     = RE - Charges financières (intérêts) + Produits financiers
```
- Très souvent négatif en début d'investissement (amortissements élevés + intérêts élevés)
- Peut générer un déficit foncier imputable sur le revenu global des associés (dans le cadre d'une SCI à l'IR)

**Résultat Net**
```
Résultat Net = RCAI + Résultat exceptionnel - IS (si applicable)
```

**Capacité d'Autofinancement (CAF) — méthode additive**
```
CAF = Résultat Net
    + Dotations aux amortissements (immeubles + travaux)
    + Dotations aux provisions nettes de reprises
    - Plus-values de cession nettes d'impôt
```
- La CAF représente les ressources internes générées — elle doit couvrir a minima les remboursements en capital des emprunts

**Cash-flow locatif brut (indicateur de gestion)**
```
Cash-flow locatif brut = Loyers bruts perçus - Charges décaissables d'exploitation
                       = EBE locatif
```

**Cash-flow locatif net (après financement)**
```
Cash-flow locatif net = EBE locatif - Annuités totales d'emprunt (capital + intérêts)
```
- C'est l'indicateur le plus important pour l'investisseur : mesure ce que génère le bien après paiement de l'emprunt
- Positif : le bien s'autofinance et dégage un surplus
- Légèrement négatif : effort d'épargne mensuel nécessaire — courant en début d'investissement dans les marchés tendus
- Fortement négatif : le bien consomme de la trésorerie de façon structurelle — à surveiller

**Taux de couverture du service de la dette (DSCR — preview)**
```
DSCR = EBE locatif / Annuités totales d'emprunt (capital + intérêts)
```
- DSCR > 1,2 : confortable — les loyers couvrent le remboursement avec une marge de 20%
- DSCR 1,0–1,2 : tendu — peu de marge face à une vacance ou une hausse des charges
- DSCR < 1,0 : insuffisant — les loyers ne couvrent pas les remboursements, effort de trésorerie personnel

### 3. Présenter le tableau de synthèse

| Solde | Montant N (€) | % des loyers bruts | Montant N-1 (€) | Evolution |
|-------|---------------|-------------------|-----------------|-----------|
| Loyers bruts perçus | X | 100% | X | +/- % |
| Charges décaissables d'exploitation | X | X% | X | +/- % |
| **EBE locatif (cash-flow brut)** | **X** | **X%** | X | **+/- %** |
| Dotations aux amortissements | X | X% | X | +/- % |
| Résultat d'exploitation | X | X% | X | +/- % |
| Charges financières (intérêts) | X | X% | X | +/- % |
| RCAI | X | X% | X | +/- % |
| Résultat exceptionnel | X | X% | X | +/- % |
| Résultat net | X | X% | X | +/- % |
| **CAF** | **X** | **X%** | X | **+/- %** |
| Annuités totales (capital + intérêts) | X | X% | X | +/- % |
| **Cash-flow net après financement** | **X** | **X%** | X | **+/- %** |
| **DSCR** | **X,X** | | X,X | |

### 4. Comparer avec les données sectorielles via data.gouv.fr

Si le code NAF/APE de la société est connu (68.20A, 68.20B pour location immobilière), interroger data.gouv.fr pour obtenir les ratios sectoriels de référence (Banque de France / INSEE) :
- Rentabilité moyenne du secteur location immobilière
- Ratio charges financières / EBE sectoriel
- Taux d'endettement médian

### 5. Identifier les points de vigilance spécifiques au locatif

- **EBE locatif < 50% des loyers bruts** : charges d'exploitation anormalement élevées — analyser poste par poste
- **Charges financières > EBE locatif** : les intérêts seuls dépassent le surplus d'exploitation — DSCR < 1, situation non soutenable sans apports extérieurs
- **CAF < remboursements en capital** : la société ne génère pas assez de ressources internes pour rembourser son emprunt — dépendance aux loyers pour couvrir le capital remboursé
- **Résultat net très négatif** : peut être normal (amortissements + intérêts élevés) mais génère un report à nouveau négatif cumulatif — surveiller les capitaux propres
- **Vacance locative implicite** (loyers perçus < loyers théoriques) : à quantifier si possible
- **Taxe foncière > 10% des loyers** : niveau élevé, à vérifier selon la localisation
- **Dépendance à un seul locataire** : risque de concentration — à mentionner si une seule ligne de loyer est visible

## Règles importantes

- Ne jamais inventer un solde si les données sources sont manquantes — demander la précision
- Distinguer systématiquement les charges décaissables (impact trésorerie) des charges non-décaissables (amortissements, provisions)
- Pour les SCI à l'IR, préciser que le résultat net affiché est avant imposition des associés — le cash-flow effectif peut être très différent de la charge fiscale réelle des associés
- Préciser l'exercice concerné et effectuer la comparaison N / N-1 si disponible
- Rappeler que cette analyse est indicative et ne remplace pas l'avis d'un expert-comptable ou d'un gestionnaire de patrimoine
