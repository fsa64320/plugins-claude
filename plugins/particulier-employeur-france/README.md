# particulier-employeur-france

Plugin Claude Code pour les particuliers employeurs français qui emploient un salarié à domicile via le CESU ou PAJEMPLOI (aide ménagère, garde d'enfant, jardinier, auxiliaire de vie).

## Ce que fait ce plugin

| Skill | Déclenché quand vous dites... |
|-------|-------------------------------|
| `guide-embauche-cesu` | "je veux embaucher quelqu'un", "comment créer un contrat CDI", "démarches pour prendre une aide ménagère" |
| `rupture-conventionnelle` | "je veux me séparer de mon salarié à l'amiable", "remplir le CERFA 14598", "indemnité de rupture conventionnelle" |
| `declarations-cotisations` | "faire ma déclaration mensuelle CESU", "calculer les cotisations URSSAF", "convertir brut en net" |
| `generation-documents` | "générer le contrat de travail en PDF", "créer le solde de tout compte", "pré-remplir le formulaire de rupture" |

## Prérequis pour la génération de documents

Le skill `generation-documents` utilise des scripts Python présents dans `scripts/`. Assurez-vous d'avoir Python 3 installé ainsi que les dépendances nécessaires à l'exécution des scripts.

## Installation

```bash
claude plugin install particulier-employeur-france
```

Ou depuis le marketplace :

```bash
claude plugin marketplace add github:fsa64320/plugins-claude
claude plugin install particulier-employeur-france
```

## Avertissement

Ce plugin est un outil d'aide et d'information. Il ne remplace pas les conseils d'un expert en droit du travail ou d'un gestionnaire de paie. En cas de doute, consultez un professionnel ou contactez l'URSSAF / le CESU directement.
