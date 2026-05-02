---
name: guide-declaration
description: Ce skill doit être utilisé quand l'utilisateur demande à "remplir ma déclaration d'impôt", "faire ma déclaration", "comment déclarer mes revenus", "guide déclaration 2042", "aide pour ma déclaration", "quelles cases remplir", "déclaration en ligne impots.gouv.fr", "je dois déclarer mes dividendes", "comment reporter mon IFU", "formulaire 2044", "formulaire 2047", "déclaration revenus fonciers".
version: 1.0.0
allowed-tools: [Read, Glob]
---

# Guide déclaration d'impôts — France

## Objectif

Guider pas à pas l'utilisateur dans le remplissage de sa déclaration d'impôts sur impots.gouv.fr, en partant de ses documents fiscaux et en identifiant les cases à remplir.

## Étapes du guide

### Étape 1 — Rassembler les documents

Demander à l'utilisateur quels documents il possède :
- [ ] IFU de la/les banque(s) et courtier(s)
- [ ] Relevé fiscal SCPI
- [ ] Attestation fiscale assurance-vie
- [ ] Justificatifs de revenus locatifs
- [ ] Avis d'imposition N-1 (pour le plafond PER)
- [ ] Justificatifs de charges déductibles (dons, emploi à domicile, frais de garde...)

### Étape 2 — Vérifier les informations pré-remplies

Sur impots.gouv.fr > Déclaration > Vérifier :
- Revenus salariaux (cases 1AJ/1BJ) — pré-remplis par l'employeur
- Revenus de remplacement (pensions, chômage)
- Dividendes et intérêts si déclarés par l'établissement financier

**Important :** Les montants pré-remplis peuvent être incomplets ou erronés. Toujours vérifier avec les IFU reçus.

### Étape 3 — Déclarer les revenus de capitaux mobiliers (Formulaire 2042)

**Onglet "Revenus des valeurs et capitaux mobiliers"**

| Case | Libellé | Source |
|------|---------|--------|
| 2DC | Revenus des actions et parts (dividendes) | IFU |
| 2TR | Intérêts et autres produits de placement | IFU |
| 2BH | Revenus n'ouvrant pas droit à abattement | IFU |
| 2CK | Crédit d'impôt égal au prélèvement forfaitaire non libératoire | IFU |
| 2AB | Crédits d'impôt sur revenus étrangers | IFU |
| 3VG | Plus-values de cession de valeurs mobilières | IFU |
| 3VH | Moins-values de cession de valeurs mobilières | IFU |

**Option barème progressif :** Case 2OP à cocher si elle est avantageuse (TMI ≤ 11%)

### Étape 4 — Déclarer les revenus fonciers

**Si revenus fonciers bruts ≤ 15 000 € → Micro-foncier (Formulaire 2042)**
- Case 4BE : revenus fonciers bruts
- Abattement 30% appliqué automatiquement

**Si revenus fonciers bruts > 15 000 € → Régime réel (Formulaire 2044)**
- Ligne 211 : loyers encaissés
- Lignes 220-240 : charges déductibles (intérêts, taxes, travaux, assurances...)
- Le résultat net est reporté en case 4BA (bénéfice) ou 4BC (déficit)

### Étape 5 — Revenus de source étrangère (Formulaire 2047)

Nécessaire si l'utilisateur a :
- Des dividendes ou intérêts étrangers
- Des revenus SCPI investissant à l'étranger
- Des loyers de biens situés à l'étranger

Les montants sont ensuite reportés sur la 2042.

### Étape 6 — Charges déductibles et réductions

**Charges déductibles du revenu global :**
- Versements PER (case 6NS/6NT/6NU)
- Pensions alimentaires (case 6GI)
- Frais d'accueil de personnes âgées (case 6EU)

**Réductions d'impôt :**
- Dons (case 7UF/7VC)
- Investissements Pinel/Denormandie (case 7QA...)

**Crédits d'impôt :**
- Emploi à domicile (case 7DB)
- Frais de garde enfants < 6 ans (case 7GA)

### Étape 7 — Vérification finale

Avant de valider :
1. Comparer le revenu fiscal de référence avec N-1
2. Vérifier le montant d'impôt calculé (simulation disponible avant validation)
3. Vérifier que tous les crédits d'impôt sont bien pris en compte
4. S'assurer que l'option barème progressif (2OP) est cochée si avantageuse

## Calendrier déclaratif (à titre indicatif)

- Avril : ouverture de la déclaration en ligne
- Mi-mai : date limite zone 1 (départements 01-19)
- Fin mai : date limite zone 2 (départements 20-54)
- Début juin : date limite zone 3 (départements 55-976)

## Ressources utiles

- impots.gouv.fr — espace particulier
- Notice explicative 2042 disponible sur le site des impôts
- Service de renseignement fiscal : 0809 401 401 (gratuit)
