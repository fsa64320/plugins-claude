---
name: analyse-document-fiscal
description: Ce skill doit être utilisé quand l'utilisateur partage ou mentionne un document fiscal à analyser : "analyse mon IFU", "lis mon relevé fiscal SCPI", "que signifie cette case", "j'ai reçu un document de ma banque", "IFU Boursorama", "relevé Linxea", "attestation fiscale", "document Amundi", "relevé de situation". Extrait les montants, identifie les cases 2042 concernées et explique chaque ligne.
version: 1.1.1
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

- Ne jamais inventer un montant : si une case n'est pas visible dans le document, l'inscrire `— Non concerné`, ne jamais l'omettre
- Distinguer PFU (30%) vs barème progressif et expliquer la différence
- Pour les SCPI étrangères, rappeler que la convention fiscale avec le pays concerné s'applique
- Produire les **9 blocs** du Format de réponse dans l'ordre indiqué, sans exception
- Les blocs 2044, 2047 et 2074 ne sont inclus que si le document les rend nécessaires ; sinon écrire explicitement : *« Formulaire X non applicable à ce document. »*
- Montants toujours formatés `X XXX,XX €` (espace milliers, virgule décimale)
- Le bloc Synthèse fiscale estimée est omis si les données sont trop partielles pour un calcul
- Toujours rappeler que cette analyse est indicative et ne remplace pas un expert-comptable

## Format de réponse

Produire **systématiquement** la sortie suivante, dans cet ordre et avec cette mise en forme exacte.

---

### 📄 Document analysé
| Champ | Valeur |
|-------|--------|
| Type | IFU / Relevé SCPI / Attestation AV / Relevé PEA / Autre |
| Émetteur | Nom de l'établissement |
| Année fiscale | AAAA |
| Date d'émission | JJ/MM/AAAA (si disponible) |
| Formulaires concernés | 2042 / 2044 / 2047 / 2074 (cocher les applicables) |

---

### 📊 Formulaire 2042 — Déclaration principale

| Case | Libellé | Montant | Statut |
|------|---------|---------|--------|
| 2DC | Dividendes d'actions françaises/européennes | 0,00 € | — Non concerné |
| 2TR | Intérêts et produits de placement | 0,00 € | — Non concerné |
| 2BH | Revenus de valeurs mobilières (autres) | 0,00 € | — Non concerné |
| 2CK | Crédit d'impôt prélèvement forfaitaire | 0,00 € | — Non concerné |
| 2AB | Crédits d'impôt sur valeurs étrangères | 0,00 € | — Non concerné |
| 2CA | Pertes nettes sur cessions | 0,00 € | — Non concerné |
| 3VG | Plus-values nettes sur cessions (PFU) | 0,00 € | — Non concerné |
| 3VH | Moins-values nettes sur cessions (PFU) | 0,00 € | — Non concerné |

> Toutes les cases pertinentes au type de document sont listées. Statut : `✅ À reporter` ou `— Non concerné`.

---

### 🏠 Formulaire 2044 — Revenus fonciers (régime réel)

> *(Bloc présent uniquement si le document contient des revenus fonciers en régime réel — SCPI, immobilier locatif direct. Sinon : « Formulaire 2044 non applicable à ce document. »)*

| Ligne | Libellé | Montant |
|-------|---------|---------|
| 110 | Revenus bruts (A) | 0,00 € |
| 112 | Frais et charges (B) | 0,00 € |
| 113 | Intérêts d'emprunt (C) | 0,00 € |
| 114 | Bénéfice (+) / Déficit (–) (D) | 0,00 € |

Report en 2042 :
| Case 2042 | Libellé | Montant |
|-----------|---------|---------|
| 4BA | Revenus fonciers nets | 0,00 € |
| 4BC | Déficit foncier imputable | 0,00 € |

> Si micro-foncier (revenus < 15 000 €) : déclarer directement case **4BE** en 2042, sans remplir 2044.

---

### 🌍 Formulaire 2047 — Revenus de source étrangère

> *(Bloc présent uniquement si le document contient des revenus de source étrangère. Sinon : « Formulaire 2047 non applicable à ce document. »)*

| Section | Pays | Nature du revenu | Montant brut | Retenue à la source | Crédit d'impôt FR |
|---------|------|-----------------|-------------|--------------------|--------------------|
| 1 | Ex : Allemagne | Dividendes | 0,00 € | 0,00 € | 0,00 € |
| 3 | Ex : Luxembourg | Intérêts | 0,00 € | 0,00 € | 0,00 € |
| 6 | Ex : Espagne | Revenus fonciers | 0,00 € | 0,00 € | 0,00 € |

Reports en 2042 :
| Case 2042 | Libellé | Montant |
|-----------|---------|---------|
| 2AB | Crédit d'impôt égal à la retenue étrangère | 0,00 € |
| 4BA | Revenus fonciers étrangers nets (si convention taux effectif) | 0,00 € |

> Vérifier la convention fiscale applicable entre la France et le pays source — le traitement varie selon les conventions.

---

### 📈 Formulaire 2074 — Plus-values mobilières (régime dérogatoire)

> *(Bloc présent uniquement si le document mentionne des cessions hors PFU : reports de moins-values antérieures à 2018, abattements pour durée de détention, BSPCE, stock-options. Sinon : « Formulaire 2074 non applicable à ce document. »)*

| Ligne | Libellé | Montant |
|-------|---------|---------|
| 001 | Prix de cession total | 0,00 € |
| 020 | Prix d'acquisition | 0,00 € |
| 021 | Frais d'acquisition | 0,00 € |
| 040 | Plus-value / Moins-value brute | 0,00 € |
| 060 | Abattement pour durée de détention | 0,00 € |
| 070 | Plus-value / Moins-value nette imposable | 0,00 € |

Reports en 2042 C :
| Case 2042 C | Libellé | Montant |
|-------------|---------|---------|
| 3VG | Plus-value nette imposable | 0,00 € |
| 3VH | Moins-value nette reportable | 0,00 € |
| 3UA | Plus-value avec abattement renforcé | 0,00 € |

> Le formulaire 2074 est obligatoire dès lors qu'une compensation entre plus et moins-values ou un abattement s'applique, même si le résultat net est nul.

---

### 💬 Explication des lignes renseignées

Pour chaque case ou ligne avec un montant > 0, produire un paragraphe :

**Case 2DC — Dividendes d'actions**
Revenus versés par des sociétés françaises ou européennes cotées. Soumis au PFU de 30 % (12,8 % IR + 17,2 % PS) ou, sur option globale via la case 2OP, au barème progressif avec abattement de 40 %.

*(Répéter pour chaque case ou ligne concernée)*

---

### ⚠️ Points d'attention

- [ ] Revenus de source étrangère détectés → compléter le formulaire **2047**
- [ ] Crédit d'impôt étranger (case **2AB**) → ne pas omettre, il réduit l'impôt dû
- [ ] Revenus fonciers en régime réel → remplir le formulaire **2044** avant la 2042
- [ ] Plus-values avec abattement ou report de moins-values → formulaire **2074** requis
- [ ] Option barème progressif (case **2OP**) → avantageuse si TMI < 30 %
- [ ] Prélèvements sociaux déjà prélevés à la source → ne pas les redéclarer

*(Lister uniquement les points réellement applicables au document analysé)*

---

### 🧮 Synthèse fiscale estimée

| Régime | Base imposable | Impôt estimé |
|--------|---------------|-------------|
| PFU 30 % (par défaut) | X XXX,XX € | XXX,XX € |
| Barème progressif (option 2OP) | X XXX,XX € | À calculer selon TMI |

> Estimation indicative sur la base des éléments du document uniquement. Le calcul exact dépend de l'ensemble de la déclaration du foyer fiscal.

---

### ⚖️ Mise en garde

*Cette analyse est produite à titre informatif et pédagogique à partir des éléments fournis. Elle ne constitue pas un conseil fiscal et ne remplace pas l'intervention d'un expert-comptable ou d'un conseiller fiscal agréé. En cas de doute, consultez un professionnel ou le service des impôts.*
