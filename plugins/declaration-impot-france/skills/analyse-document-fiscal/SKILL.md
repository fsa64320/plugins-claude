---
name: analyse-document-fiscal
description: Ce skill doit être utilisé quand l'utilisateur partage ou mentionne un document fiscal à analyser : "analyse mon IFU", "lis mon relevé fiscal SCPI", "que signifie cette case", "j'ai reçu un document de ma banque", "IFU Boursorama", "relevé Linxea", "attestation fiscale", "document Amundi", "relevé de situation". Extrait les montants, identifie les cases 2042 concernées et explique chaque ligne.
version: 1.0.0
allowed-tools: [Read, Glob]
---

# Analyse de document fiscal

## Objectif

Extraire et expliquer les informations fiscales d'un document fourni par l'utilisateur (IFU, relevé SCPI, attestation fiscale, relevé de portefeuille, etc.) et identifier les cases à reporter dans la déclaration 2042.

## Processus

1. **Identifier le type de document**
   - IFU (Imprimé Fiscal Unique) : émis par les banques/courtiers pour les valeurs mobilières
   - Relevé fiscal SCPI : émis par les sociétés de gestion pour les revenus fonciers et étrangers
   - Attestation fiscale assurance-vie
   - Relevé de situation PEA / PEA-PME

2. **Extraire les montants clés selon le type**

   Pour un **IFU** :
   - Case 2DC : dividendes d'actions françaises et européennes
   - Case 2TR : intérêts et produits de placement à revenu fixe
   - Case 2BH : revenus de valeurs mobilières (autres)
   - Case 2CK : crédit d'impôt égal au prélèvement forfaitaire non libératoire
   - Case 2CA : pertes nettes sur cessions de valeurs mobilières
   - Case 2VV : plus-values nettes sur cessions de valeurs mobilières
   - Case 2AB : crédits d'impôt sur valeurs étrangères
   - Case 3VG / 3VH : plus-values / moins-values sur cessions de valeurs mobilières (PFU)

   Pour un **relevé SCPI** :
   - Revenus fonciers français → case 4BA (formulaire 2044)
   - Revenus de source étrangère → formulaire 2047
   - Quote-part de charges déductibles
   - Prélèvements sociaux déjà effectués

3. **Présenter un tableau de synthèse**

   | Case | Libellé | Montant | Formulaire |
   |------|---------|---------|------------|
   | 2DC  | Dividendes | X,XX € | 2042 |
   | ...  | ...     | ...     | ...  |

4. **Expliquer chaque ligne en langage simple**
   - Ce que représente le revenu
   - Pourquoi il est imposable (ou non)
   - Le régime fiscal applicable (PFU 30% ou barème progressif)

5. **Signaler les points d'attention**
   - Revenus étrangers nécessitant le formulaire 2047
   - Crédit d'impôt à ne pas oublier (case 2AB)
   - Option barème progressif si potentiellement avantageuse

## Règles importantes

- Ne jamais inventer un montant : si une case n'est pas visible dans le document, l'indiquer explicitement
- Distinguer PFU (30%) vs barème progressif et expliquer la différence
- Pour les SCPI étrangères, rappeler que la convention fiscale avec le pays concerné s'applique
- Toujours rappeler que cette analyse est indicative et ne remplace pas un expert-comptable
