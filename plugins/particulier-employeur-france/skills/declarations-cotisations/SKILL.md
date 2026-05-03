---
name: declarations-cotisations
description: Ce skill doit être utilisé quand le particulier employeur veut "faire sa déclaration mensuelle", "déclarer le salaire sur CESU", "déclarer sur PAJEMPLOI", "calculer les cotisations URSSAF", "calculer le salaire brut en net", "connaître le taux de cotisations", "payer l'URSSAF", "calendrier des échéances URSSAF", "date limite déclaration CESU", "cotisations sociales employé à domicile", "bulletins de paie CESU".
version: 1.0.0
allowed-tools: [Read, Glob]
---

# Déclarations mensuelles et cotisations — Particulier employeur (CESU / PAJEMPLOI)

## Objectif

Accompagner le particulier employeur dans ses déclarations mensuelles de salaire, le calcul des cotisations sociales et le respect du calendrier déclaratif URSSAF.

## Fonctionnement général

Le particulier employeur déclare chaque mois le salaire versé à son salarié sur le portail CESU ou PAJEMPLOI. L'URSSAF calcule automatiquement les cotisations et prélève le montant sur le compte bancaire de l'employeur.

Le portail édite ensuite un **bulletin de salaire simplifié** (volet social) transmis directement au salarié via son espace en ligne.

## Comment déclarer sur CESU (cesu.urssaf.fr)

1. Se connecter à l'espace employeur
2. Aller dans **"Déclarer une activité"**
3. Sélectionner le salarié concerné
4. Saisir pour le mois concerné :
   - Nombre d'heures travaillées
   - Salaire net horaire ou salaire net total versé
5. Valider la déclaration
6. L'URSSAF calcule les cotisations et prélève le tout (net versé au salarié + cotisations)

**Important** : déclarer le salaire **net** sur CESU. Le portail recalcule le brut et les cotisations automatiquement. Ne pas saisir le brut.

## Comment déclarer sur PAJEMPLOI (pajemploi.urssaf.fr)

1. Se connecter à l'espace "Mon garde d'enfant"
2. Saisir pour le mois :
   - Nombre d'heures de garde
   - Salaire net versé
   - Jours d'absence éventuels
3. Valider et confirmer le montant prélevé
4. La CAF complète avec le CMG (Complément Mode de Garde) si éligible

## Calcul du salaire brut → net

### Taux de cotisations 2024 (CESU — employé de maison)

| Cotisation | Part employeur | Part salariale | Base |
|------------|---------------|----------------|------|
| Assurance maladie | 7,00% | 0,75% | Brut |
| Vieillesse plafonnée | 8,55% | 6,90% | Brut ≤ plafond SS |
| Vieillesse déplafonnée | 1,90% | 0,40% | Brut total |
| Allocations familiales | 3,45% | — | Brut |
| Accident du travail | 2,30% | — | Brut |
| Chômage | 4,05% | 2,40% | Brut |
| Retraite complémentaire | 4,72% | 3,15% | Brut |
| Prévoyance (CCN 2111) | 0,95% | 0,45% | Brut |
| **Total approximatif** | **~33%** | **~14%** | |

> Ces taux sont indicatifs. Le portail CESU applique les taux exacts en vigueur. Consulter urssaf.fr pour les taux actualisés.

### Formule de calcul

```
Salaire brut = Salaire net / (1 - taux de cotisations salariales)
             ≈ Salaire net / 0,86

Cotisations patronales ≈ Salaire brut × 0,33
Coût total employeur = Salaire brut + Cotisations patronales
                     ≈ Salaire brut × 1,33
                     ≈ Salaire net × 1,55
```

**Exemple :**
- Salaire net versé : 1 000 €
- Salaire brut ≈ 1 000 / 0,86 ≈ 1 163 €
- Cotisations patronales ≈ 1 163 × 0,33 ≈ 384 €
- Coût total employeur ≈ **1 163 + 384 = 1 547 €**

### Cotisations réduites via CESU

Les particuliers employeurs bénéficient d'une **exonération partielle** sur les cotisations patronales :
- **Exonération de droit commun** : réduction de cotisations patronales pour les particuliers employeurs (montant calculé automatiquement par le portail)
- **Abattement pour les +70 ans ou bénéficiaires d'APA/PCH** : exonération totale des cotisations patronales

## Calendrier des échéances

### CESU — déclaration mensuelle

| Période | Délai de déclaration | Prélèvement bancaire |
|---------|---------------------|---------------------|
| Salaire du mois M | Jusqu'au **5 du mois M+1** (ou dernier jour ouvré si férié) | Vers le **15 du mois M+1** |

**Exemple** : salaire de janvier → déclarer avant le 5 février → prélèvement vers le 15 février.

### PAJEMPLOI — déclaration mensuelle

| Période | Délai de déclaration | Prélèvement bancaire |
|---------|---------------------|---------------------|
| Salaire du mois M | Jusqu'au **10 du mois M+1** | Vers le **25 du mois M+1** |

### Régularisation annuelle

En janvier de chaque année, l'URSSAF effectue une **régularisation** basée sur les revenus réels de l'année écoulée. Un éventuel complément ou remboursement de cotisations peut intervenir.

## Retard ou oubli de déclaration

- Déclaration en retard : possible sur le portail jusqu'à **3 mois** après la période concernée (au-delà, contacter l'URSSAF)
- Majoration de retard : 5% des cotisations dues + 0,2% par mois de retard
- En cas d'oubli prolongé, régulariser rapidement pour éviter une mise en demeure

## Congés payés

- Le particulier employeur doit verser **10% de la rémunération brute totale** au titre des congés payés (ou laisser le salarié prendre ses congés en nature — 2,5 jours ouvrables par mois de travail)
- Sur CESU : une case dédiée permet de déclarer et payer les congés payés en même temps que le salaire mensuel
- **Recommandation** : verser l'indemnité de CP chaque mois plutôt qu'en une fois pour faciliter la gestion de trésorerie

## Chèques CESU préfinancés

Si l'employeur (entreprise du conjoint, CE, collectivité) fournit des **chèques CESU préfinancés** :
- Leur valeur couvre uniquement le **salaire net** du salarié (pas les cotisations)
- Les cotisations restent à la charge du particulier employeur et sont prélevées séparément
- Saisir les chèques CESU reçus dans l'espace "Titres CESU" du portail

## Règles importantes

- Ne pas confondre salaire net (ce que reçoit le salarié) et coût total employeur (salaire net + cotisations)
- Conserver tous les relevés de prélèvement URSSAF (accessibles dans l'espace en ligne) — durée de conservation recommandée : 5 ans
- En cas de litige sur le calcul des cotisations, contacter directement l'URSSAF CESU : **3960** (service CESU particulier employeur)
- Cette analyse est indicative et ne remplace pas l'avis d'un expert-comptable ou d'un conseiller URSSAF
