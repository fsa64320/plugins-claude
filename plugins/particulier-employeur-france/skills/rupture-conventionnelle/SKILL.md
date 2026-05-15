---
name: rupture-conventionnelle
description: Ce skill doit être utilisé quand le particulier employeur veut "faire une rupture conventionnelle", "se séparer d'un salarié à l'amiable", "mettre fin au contrat d'un commun accord", "remplir le CERFA 14598", "homologation rupture conventionnelle", "délai de rétractation", "indemnité de rupture", "documents de fin de contrat", "solde de tout compte", "certificat de travail", "attestation France Travail".
version: 1.0.0
allowed-tools: "Read Glob"
---

# Rupture conventionnelle — Particulier employeur (CDI)

## Objectif

Guider un particulier employeur dans la procédure complète de rupture conventionnelle d'un CDI avec un salarié à domicile : de l'entretien préalable à la remise des documents de fin de contrat, en passant par le CERFA 14598\*01 et l'homologation DREETS.

## Conditions préalables

La rupture conventionnelle est possible pour un CDI hors période d'essai. Elle n'est **pas possible** si :
- Le salarié est en arrêt maladie lié à un accident du travail ou maladie professionnelle
- Le contexte révèle une pression ou contrainte sur le salarié (risque de requalification)

Elle s'applique aux salariés du particulier employeur comme à tous les CDI de droit privé.

## Procédure étape par étape

### Étape 1 — Entretien préalable

Organiser **au moins un entretien** avec le salarié pour :
- Lui proposer la rupture conventionnelle
- Lui expliquer ses droits (indemnité, allocations chômage)
- S'assurer de son accord libre et éclairé

Aucun formalisme imposé pour la convocation (oral ou écrit), mais une **convocation écrite** est fortement recommandée. Le salarié peut se faire assister d'un représentant du personnel ou d'un conseiller du salarié (liste disponible à la DREETS ou à la mairie).

### Étape 2 — Remplir le formulaire CERFA 14598\*01

Le formulaire officiel est disponible sur : **service-public.fr → "Rupture conventionnelle du contrat de travail à durée indéterminée"**

**Champs à renseigner :**

*Bloc Employeur (particulier)*
- Nom, prénom, adresse complète
- Numéro URSSAF/SIRET (ou numéro de particulier employeur CESU)
- Numéro de téléphone

*Bloc Salarié*
- Nom, prénom, date de naissance
- Adresse, numéro de sécurité sociale
- Emploi occupé et date d'entrée dans l'entreprise

*Bloc Convention*
- Date de signature du formulaire (= date d'accord)
- **Date envisagée de rupture** : minimum le lendemain de la fin du délai de rétractation et de l'homologation (voir délais ci-dessous)
- Indemnité spécifique de rupture conventionnelle (montant brut en euros)

Pour générer une version pré-remplie, utiliser le script `scripts/prefill_cerfa_rupture.py` (voir skill `generation-documents`).

### Étape 3 — Délai de rétractation (15 jours calendaires)

À partir du **lendemain de la signature** du CERFA :
- Chacune des parties dispose de **15 jours calendaires** pour se rétracter
- La rétractation s'effectue par lettre recommandée avec accusé de réception ou par lettre remise en main propre contre récépissé
- Si aucune rétractation : envoyer la demande d'homologation à la DREETS

**Exemple de calcul :**
- Signature le 10 du mois → délai de rétractation court du 11 au 25 inclus
- Demande d'homologation possible à partir du 26

### Étape 4 — Demande d'homologation à la DREETS

Après expiration du délai de rétractation :

1. Envoyer le formulaire CERFA 14598\*01 (original signé par les deux parties) à la **DREETS** (Direction Régionale de l'Économie, de l'Emploi, du Travail et des Solidarités) compétente
2. L'envoi se fait en ligne via **rupture-conventionnelle.travail.gouv.fr** (téléprocédure TéléRC) ou par courrier recommandé AR
3. La DREETS dispose de **15 jours ouvrables** pour :
   - Homologuer (silence = homologation tacite)
   - Refuser (notification écrite motivée)

### Étape 5 — Date effective de rupture

La date de rupture ne peut pas être **antérieure au lendemain de l'homologation**.

**Délai total minimum :**
- J0 : signature du CERFA
- J+16 : fin du délai de rétractation (15 jours + 1)
- J+16 : envoi demande homologation
- J+37 : fin du délai d'homologation (15 jours ouvrables ≈ 21 jours calendaires)
- J+38 : date de rupture possible au plus tôt

En pratique, prévoir **6 à 8 semaines** entre la signature et la fin de contrat effective.

## Calcul de l'indemnité spécifique de rupture conventionnelle

L'indemnité est au minimum égale à **l'indemnité légale de licenciement** :

```
Indemnité = (1/4 de mois de salaire brut par année d'ancienneté) pour les 10 premières années
          + (1/3 de mois de salaire brut par année) au-delà de 10 ans
```

- **Salaire de référence** : 1/12 de la rémunération brute des 12 derniers mois, OU 1/3 des 3 derniers mois (prendre le montant le plus favorable au salarié)
- Les fractions d'année sont prises en compte au prorata
- L'indemnité est **exonérée d'IS et de cotisations sociales** dans la limite de 2× le plafond annuel de la SS (montant à vérifier sur urssaf.fr chaque année)

**Exemple :**
- Salarié avec 3 ans et 6 mois d'ancienneté
- Salaire brut mensuel de référence : 1 200 €
- Indemnité = 1 200 × (1/4) × 3,5 = **1 050 €**

## Documents à remettre au salarié à la date de rupture

Les trois documents suivants sont **obligatoires** à remettre le dernier jour de travail :

| Document | Contenu clé | Délai |
|----------|-------------|-------|
| **Certificat de travail** | Dates d'entrée/sortie, emploi occupé, mention "rupture conventionnelle" | Dernier jour |
| **Reçu pour solde de tout compte** | Détail de toutes les sommes versées (dernier salaire, indemnité RC, congés payés non pris) | Dernier jour |
| **Attestation France Travail** (ex-Pôle Emploi) | Permet au salarié d'ouvrir ses droits au chômage | Dernier jour |

Pour générer ces trois documents en PDF, utiliser le script `scripts/generate_fin_contrat.py` (voir skill `generation-documents`).

### Solde de tout compte — éléments à inclure

- Dernier salaire mensuel (prorata si mois incomplet)
- Indemnité de congés payés non pris (10% de la rémunération brute de la période non soldée, ou calcul en jours réels)
- Indemnité spécifique de rupture conventionnelle
- Toute prime contractuelle

Le reçu pour solde de tout compte doit être signé par le salarié. Il dispose de **6 mois** pour le dénoncer par lettre recommandée AR.

### Attestation France Travail

L'attestation France Travail (anciennement "attestation Pôle Emploi") se remplit via le **portail employeur de France Travail** (francetravail.fr → espace employeur) ou par le formulaire cerfa n°14693. Elle permet l'ouverture des droits ARE (Aide au Retour à l'Emploi) pour le salarié.

## Déclaration de fin de contrat sur CESU/PAJEMPLOI

Après la rupture effective :
- Se connecter sur cesu.urssaf.fr ou pajemploi.urssaf.fr
- Dans "Mes salariés", déclarer la **date de fin de contrat** et le motif (rupture conventionnelle)
- Effectuer la dernière déclaration mensuelle de salaire couvrant le dernier mois travaillé

## Règles importantes

- La rupture conventionnelle donne droit aux allocations chômage (ARE) pour le salarié — c'est un avantage différenciant par rapport à la démission
- Ne jamais exercer de pression sur le salarié : cela peut entraîner la requalification en licenciement sans cause réelle et sérieuse
- Conserver une copie de tous les documents signés (CERFA, récépissé d'homologation, reçu pour STC)
- En cas de refus d'homologation par la DREETS, consulter un conseiller en droit du travail avant toute autre démarche
- Cette analyse est indicative et ne remplace pas l'avis d'un juriste en droit social ou d'un expert-comptable
