---
name: generation-documents
description: Ce skill doit être utilisé quand le particulier employeur veut "générer un contrat de travail", "créer un contrat CDI en PDF", "remplir le formulaire de rupture conventionnelle", "générer les documents de fin de contrat", "créer le solde de tout compte", "générer le certificat de travail", "pré-remplir le CERFA 14598", "utiliser les scripts de génération", "créer des documents PDF".
version: 1.0.0
allowed-tools: [Read, Glob, Bash]
---

# Génération automatique de documents — Particulier employeur

## Objectif

Générer automatiquement les documents officiels du particulier employeur en PDF à partir des données saisies : contrat de travail CDI, documents de fin de contrat (solde de tout compte, certificat de travail), et pré-remplissage du formulaire de rupture conventionnelle.

## Prérequis

Installer les dépendances Python nécessaires :

```bash
pip install reportlab pypdf
```

Les scripts sont situés dans `scripts/` à la racine du plugin.

## Script 1 — Contrat de travail CDI (`generate_contrat.py`)

Génère un contrat de travail CDI complet et conforme à la CCN 2111 (salariés du particulier employeur).

**Utilisation :**

```bash
python scripts/generate_contrat.py
```

Le script demande interactivement les informations suivantes :

| Champ | Exemple |
|-------|---------|
| Nom et prénom de l'employeur | Dupont Jean |
| Adresse de l'employeur | 12 rue des Lilas, 75001 Paris |
| Numéro CESU employeur | 123456789 |
| Nom et prénom du salarié | Martin Sophie |
| Date de naissance du salarié | 15/03/1985 |
| Adresse du salarié | 5 allée des Roses, 75002 Paris |
| Date d'entrée en CDI | 01/06/2024 |
| Durée de la période d'essai | 1 mois |
| Description des tâches | Aide ménagère, repassage, courses |
| Lieu(x) de travail | 12 rue des Lilas, 75001 Paris |
| Nombre d'heures par semaine | 20h |
| Répartition horaire | Lundi, mercredi, vendredi 8h-12h |
| Salaire brut horaire | 12,50 € |

**Fichier généré :** `contrat_CDI_[nom_salarie]_[date].pdf`

## Script 2 — Documents de fin de contrat (`generate_fin_contrat.py`)

Génère les trois documents obligatoires à remettre au salarié lors de la rupture conventionnelle.

**Utilisation :**

```bash
python scripts/generate_fin_contrat.py
```

Le script génère dans le même PDF (ou des fichiers séparés selon le choix) :

1. **Certificat de travail** — Mentionne les dates d'entrée/sortie, l'emploi occupé et le motif de rupture
2. **Reçu pour solde de tout compte** — Détaille toutes les sommes versées avec calcul automatique
3. **Attestation France Travail** — Format conforme au cerfa n°14693 (à compléter via francetravail.fr)

| Champ requis | Pour les 3 documents |
|-------------|---------------------|
| Informations employeur | Identité, adresse, n° CESU |
| Informations salarié | Identité, adresse, n° SS |
| Date d'entrée | Pour ancienneté |
| Date de rupture effective | Date du dernier jour |
| Salaire brut mensuel de référence | Calcul indemnité et STC |
| Heures de congés payés non soldées | Pour le STC |
| Montant indemnité rupture conv. | Pour le STC |

**Fichiers générés :**
- `certificat_travail_[nom]_[date].pdf`
- `solde_tout_compte_[nom]_[date].pdf`
- `attestation_ft_[nom]_[date].pdf`

## Script 3 — Pré-remplissage CERFA rupture conventionnelle (`prefill_cerfa_rupture.py`)

Génère un document PDF pré-rempli reprenant la structure du CERFA 14598\*01 (formulaire de rupture conventionnelle homologuée).

**Utilisation :**

```bash
python scripts/prefill_cerfa_rupture.py
```

Le script génère un document à imprimer et faire signer par les deux parties.

**Important** : le document généré est un **formulaire de substitution** mis en forme avec les données saisies. Pour la procédure d'homologation officielle via TéléRC, utiliser le portail : **rupture-conventionnelle.travail.gouv.fr**

| Champ CERFA | Emplacement dans le formulaire |
|------------|-------------------------------|
| N° de SIRET / N° particulier employeur | Bloc "Employeur" |
| Code NAF / secteur d'activité | Bloc "Employeur" (laisser vide pour particulier) |
| Effectif de l'entreprise | 1 (particulier employeur) |
| Date de conclusion de la convention | Date de signature |
| Date envisagée de rupture | Calculée automatiquement (J+38 min.) |
| Indemnité spécifique brute | Montant calculé selon ancienneté |

## Workflow complet pour une rupture conventionnelle

```
1. Exécuter prefill_cerfa_rupture.py  →  document à signer
2. Signer le CERFA avec le salarié
3. Attendre 15 jours calendaires (délai rétractation)
4. Soumettre via rupture-conventionnelle.travail.gouv.fr
5. Attendre 15 jours ouvrables (homologation)
6. Exécuter generate_fin_contrat.py  →  STC + certificat + attestation FT
7. Remettre les 3 documents le dernier jour de travail
```

## Personnalisation des documents

Les documents générés utilisent la **mise en forme officielle URSSAF/France Travail** avec :
- Entête avec coordonnées des parties
- Corps structuré avec les mentions légales obligatoires
- Espace pour signature et date

Pour modifier les templates, éditer les fonctions de mise en page dans chaque script (section `# TEMPLATE` en début de fichier).

## Règles importantes

- Les documents générés ont une **valeur juridique** dès lors qu'ils sont signés par les deux parties — les conserver soigneusement
- L'attestation France Travail doit impérativement être **télédéclarée** sur francetravail.fr (espace employeur) — le PDF généré sert de brouillon de préparation
- Vérifier la conformité des montants (indemnité, congés payés) avec un expert-comptable en cas de doute
- Ces scripts sont fournis à titre indicatif et ne remplacent pas un logiciel de paie certifié
