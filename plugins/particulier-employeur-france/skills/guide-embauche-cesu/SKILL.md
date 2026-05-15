---
name: guide-embauche-cesu
description: Ce skill doit être utilisé quand le particulier employeur veut "embaucher quelqu'un", "engager un salarié à domicile", "prendre une aide ménagère", "recruter une garde d'enfant", "engager un jardinier", "créer un contrat de travail CDI", "déclarer un salarié sur CESU", "déclarer sur PAJEMPLOI", "connaître les démarches d'embauche", "période d'essai salarié maison", "documents à remettre au salarié".
version: 1.0.0
allowed-tools: "Read Glob"
---

# Guide d'embauche CDI — Particulier employeur (CESU / PAJEMPLOI)

## Objectif

Accompagner un particulier employeur dans toutes les étapes d'embauche d'un salarié à domicile en CDI, depuis le choix du dispositif jusqu'à la remise des documents obligatoires.

## Étape 0 — Choisir le bon dispositif

| Critère | CESU | PAJEMPLOI |
|---------|------|-----------|
| Salarié concerné | Aide ménagère, jardinier, employé de maison, auxiliaire de vie | Assistante maternelle, garde d'enfant à domicile |
| Plateforme | cesu.urssaf.fr | pajemploi.urssaf.fr |
| Aides possibles | CESU préfinancé (employeur / CE) | CMG (Complément Mode de Garde CAF) |

Identifier le type d'activité du salarié pour choisir le bon portail. Un même employeur peut utiliser les deux dispositifs pour des salariés différents.

## Étape 1 — Inscription de l'employeur

1. Se connecter sur **cesu.urssaf.fr** (ou pajemploi.urssaf.fr)
2. Créer un compte employeur (numéro de sécurité sociale + coordonnées bancaires pour le prélèvement des cotisations)
3. Conserver le **numéro d'employeur** attribué — il doit figurer sur le contrat de travail

**Important** : l'inscription en tant qu'employeur vaut déclaration d'activité — il n'y a pas de DPAE séparée à déposer pour les particuliers employeurs utilisant CESU/PAJEMPLOI.

## Étape 2 — Rédiger le contrat de travail CDI

Le contrat de travail écrit est **obligatoire** pour tout CDI à temps partiel (< 35h/semaine) et fortement recommandé même à temps complet.

### Mentions obligatoires

- Identité complète des deux parties (employeur et salarié)
- Nature du contrat (CDI)
- Date de début et durée de la période d'essai
- Lieu(x) de travail
- Description précise des tâches
- Durée hebdomadaire de travail et répartition des horaires
- Salaire brut horaire (≥ SMIC en vigueur) et mensuel
- Convention collective applicable : **Convention Collective Nationale des Salariés du Particulier Employeur (IDCC 2111)**
- Congés payés (2,5 jours ouvrables par mois travaillé)

### Période d'essai

| Type de salarié | Durée maximale |
|-----------------|----------------|
| Employé de maison | 1 mois renouvelable une fois |
| Assistante maternelle | 3 mois (non renouvelable) |

La période d'essai doit être **expressément stipulée** dans le contrat pour être valable.

Pour générer le contrat en PDF automatiquement, utiliser le script `scripts/generate_contrat.py` (voir skill `generation-documents`).

## Étape 3 — Déclarer le salarié sur le portail

### Sur CESU (cesu.urssaf.fr)

1. Se connecter à l'espace employeur
2. Aller dans **"Mes salariés" → "Ajouter un salarié"**
3. Saisir : nom, prénom, date de naissance, numéro de sécurité sociale, date d'embauche
4. **La première déclaration mensuelle vaut déclaration d'embauche** — aucun document séparé à envoyer à l'URSSAF

### Sur PAJEMPLOI (pajemploi.urssaf.fr)

1. Déclarer le salarié dans l'espace "Mon garde d'enfant"
2. Renseigner les informations du salarié et les horaires habituels
3. Pour les assistantes maternelles : joindre l'agrément du Conseil Départemental

## Étape 4 — Documents à remettre au salarié lors de l'embauche

| Document | Obligatoire | Remarque |
|----------|-------------|----------|
| Exemplaire signé du contrat de travail | Oui | Double signature, un exemplaire chacun |
| Bulletin d'adhésion à la mutuelle (si applicable) | Selon accord de branche | La CCN 2111 prévoit une couverture frais de santé obligatoire depuis 2020 |
| Fiche de poste détaillée | Recommandé | Précise les tâches attendues |
| Coordonnées de l'employeur et du portail CESU/PAJEMPLOI | Recommandé | Pour les bulletins de salaire et déclarations |

## Étape 5 — Affiliation à la mutuelle obligatoire

Depuis le **1er janvier 2020**, la CCN des salariés du particulier employeur impose une couverture complémentaire santé collective.

- **Adhésion via Ipsec** (organisme désigné par la branche) : ipsec.fr
- L'employeur participe à hauteur de **50% minimum** de la cotisation
- À effectuer **dès le premier jour de contrat**

## Checklist récapitulative

- [ ] Choix CESU ou PAJEMPLOI selon le type de salarié
- [ ] Inscription sur le portail employeur
- [ ] Contrat de travail CDI rédigé et signé (2 exemplaires)
- [ ] Période d'essai stipulée dans le contrat
- [ ] Salarié déclaré sur le portail
- [ ] Affiliation mutuelle Ipsec effectuée
- [ ] Exemplaire du contrat remis au salarié

## Règles importantes

- La convention collective applicable est la **CCN 2111 (IDCC 2111)** — salariés du particulier employeur — et non le Code du travail standard
- Le salaire minimum est le **SMIC horaire brut** en vigueur (vérifier le montant actualisé sur urssaf.fr)
- En cas de doute sur les obligations, consulter le site **particulier-emploi.fr** (ressource officielle SPF/URSSAF) ou contacter l'URSSAF
- Cette analyse est indicative et ne remplace pas l'avis d'un juriste en droit social
