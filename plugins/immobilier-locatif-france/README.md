# Plugin `analyse-bilan-france`

Assistant d'analyse financière pour les bilans annuels de sociétés françaises. Analyse les états financiers (bilan, compte de résultat, annexes), calcule les ratios financiers clés, diagnostique la santé financière et identifie les points d'attention.

## Installation

```bash
claude plugin install analyse-bilan-france
```

## Skills disponibles

### `/analyse-bilan`

Analyse la structure du bilan comptable (actif/passif) et calcule les grands équilibres financiers.

**Déclenché par :** "analyse mon bilan", "que signifie mon actif immobilisé", "explique le passif", "BFR", "fonds de roulement", "trésorerie nette", "FRNG", "fonds propres", "dettes financières"

**Ce que ça fait :**
- Identifie et structure les grandes masses du bilan (actif immobilisé, actif circulant, capitaux propres, dettes)
- Calcule le Fonds de Roulement Net Global (FRNG = Capitaux Permanents - Actif Immobilisé)
- Calcule le Besoin en Fonds de Roulement (BFR = Stocks + Créances - Dettes d'exploitation)
- Calcule la Trésorerie Nette (TN = FRNG - BFR)
- Présente un tableau de synthèse des grandes masses
- Explique chaque poste en langage simple
- Signale les déséquilibres (FRNG négatif, BFR excessif, trésorerie tendue, capitaux propres insuffisants)

---

### `/analyse-compte-resultat`

Calcule les Soldes Intermédiaires de Gestion (SIG) et mesure la performance économique de l'entreprise.

**Déclenché par :** "analyse mon compte de résultat", "chiffre d'affaires", "résultat net", "EBE", "marge", "SIG", "valeur ajoutée", "résultat d'exploitation", "résultat financier", "CAF"

**Ce que ça fait :**
- Extrait et organise les données du compte de résultat
- Calcule la cascade des SIG : marge commerciale, valeur ajoutée, EBE, résultat d'exploitation, RCAI, résultat net, CAF
- Présente un tableau des SIG avec les % du CA et la comparaison N/N-1
- Calcule les taux de marge clés (marge brute, EBE/CA, marge nette)
- Compare avec les ratios sectoriels via data.gouv.fr si le secteur est connu
- Identifie les postes de charges anormaux et les points de vigilance

---

### `/ratios-financiers`

Calcule l'ensemble des ratios financiers clés et produit un diagnostic financier global avec recommandations.

**Déclenché par :** "ratios financiers", "solvabilité", "liquidité", "rentabilité", "autonomie financière", "capacité de remboursement", "ROE", "ROA", "endettement", "analyse financière complète", "diagnostic financier"

**Ce que ça fait :**
- Calcule les ratios de structure et solvabilité (autonomie financière, taux d'endettement, capacité de remboursement, couverture des intérêts)
- Calcule les ratios de liquidité (liquidité générale, réduite, immédiate)
- Calcule les ratios de rentabilité (ROE, ROA, ROCE, taux de marge nette et EBE)
- Calcule les ratios d'activité (délais clients, fournisseurs, rotation des stocks)
- Présente un tableau récapitulatif avec valeur calculée, benchmark sectoriel indicatif et appréciation
- Compare avec les données sectorielles de data.gouv.fr si le code NAF est disponible
- Formule un diagnostic global en 3 à 5 points et des recommandations concrètes par axe d'amélioration

---

## Exemples d'utilisation

```
Voici le bilan de ma société au 31/12/2024 [joindre le document].
Peux-tu analyser la structure et me dire si l'équilibre financier est sain ?

→ /analyse-bilan
```

```
Mon compte de résultat montre un CA de 2,4 M€ mais un résultat net de seulement 12 000 €.
Où partent les marges ? Calcule les SIG.

→ /analyse-compte-resultat
```

```
Fais une analyse financière complète de mon entreprise avec tous les ratios.
Code NAF : 4711F (grande distribution).

→ /ratios-financiers
```

## Sources de données

Ce plugin est connecté à l'API **data.gouv.fr** (MCP) pour accéder aux données publiques officielles (statistiques sectorielles Banque de France / INSEE) :

```
https://mcp.data.gouv.fr/mcp
```

## Avertissement

Ce plugin est un outil d'aide à l'analyse financière. Il ne remplace pas les conseils d'un expert-comptable, d'un commissaire aux comptes ou d'un conseiller financier agréé. Pour toute situation complexe ou décision stratégique, consultez un professionnel qualifié.
