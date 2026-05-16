---
name: recuperer-donnees-cesu
description: Utiliser ce skill pour récupérer les données de salaire et cotisations depuis le portail CESU URSSAF. Phrases déclencheurs : "récupère mes données CESU", "scrape URSSAF", "récupère mes salaires URSSAF", "récupère mes cotisations CESU", "télécharge mes bulletins de salaire URSSAF", "extraire données URSSAF".
version: 1.0.0
allowed-tools: "Bash"
---

# Récupération des données CESU URSSAF

## Objectif

Ouvrir automatiquement le portail cesu.urssaf.fr dans un navigateur, attendre que l'utilisateur se connecte manuellement, puis extraire les données de salaire et cotisations pour tous les employés sur la période demandée. Produire un tableau Markdown structuré exploitable par d'autres skills.

## Processus

### Étape 1 — Demander la période

Avant toute action, demander à l'utilisateur :

> Quelle période souhaitez-vous extraire ?
> - Année (ex : 2025)
> - Mois de début (ex : 1 pour janvier)
> - Mois de fin (ex : 12 pour décembre)
>
> Exemple : *"2025, janvier à décembre"* ou *"2024, toute l'année"*

Mémoriser les valeurs : `ANNEE`, `MOIS_DEBUT`, `MOIS_FIN`.

### Étape 2 — Vérifier et installer Playwright

Vérifier si Playwright est disponible :

```bash
python3 -c "import playwright" 2>/dev/null && echo "OK" || echo "ABSENT"
```

Si absent, l'installer :

```bash
pip3 install playwright && python3 -m playwright install chromium
```

Informer l'utilisateur du résultat (installation réussie ou déjà présent).

### Étape 3 — Localiser le script

Le script se trouve dans le dossier `scripts/` du plugin. Trouver son chemin absolu :

```bash
find ~/.claude/plugins -name "scrape_cesu.py" 2>/dev/null | head -1
```

### Étape 4 — Lancer le script

Exécuter le script avec les paramètres de période. Le script ouvrira un navigateur Chromium visible — l'utilisateur devra s'y connecter manuellement.

```bash
python3 <CHEMIN_SCRIPT> --annee <ANNEE> --mois-debut <MOIS_DEBUT> --mois-fin <MOIS_FIN>
```

Informer l'utilisateur avant le lancement :

> Un navigateur Chromium va s'ouvrir sur cesu.urssaf.fr.
> Connectez-vous avec vos identifiants habituels.
> Une fois sur le tableau de bord, revenez dans le terminal et appuyez sur Entrée.

**Note** : Le script est interactif (il attend une saisie clavier). La commande Bash doit être exécutée avec un timeout suffisant (5 minutes minimum).

### Étape 5 — Présenter les résultats

Récupérer la sortie stdout du script et la présenter telle quelle. Elle contient un tableau Markdown avec :

| Employé | Mois | Salaire brut | Salaire net | Cotis. patronales | Cotis. salariales | Coût total employeur |
|---------|------|-------------|------------|------------------|------------------|--------------------|
| ...     | ...  | ...         | ...        | ...              | ...              | ...                |
| **TOTAL** | — | X € | Y € | Z € | W € | T € |

Puis proposer à l'utilisateur les actions suivantes :
- Exporter ces données vers Excel (via le skill `xlsx`)
- Les intégrer au pipeline fiscal IFU existant
- Les analyser par employé ou par période

## Gestion des erreurs

- **Playwright introuvable après installation** : demander à l'utilisateur de relancer Claude Code
- **Navigateur qui ne s'ouvre pas** : vérifier que `playwright install chromium` a bien téléchargé les binaires
- **Script non trouvé** : demander à l'utilisateur de vérifier que le plugin est bien à jour (`~/.claude/plugins/marketplaces/plugins-claude/`)
- **Données vides** : vérifier que l'utilisateur est bien connecté et sur le tableau de bord CESU avant d'appuyer sur Entrée

## Règles importantes

- Ne jamais stocker ni afficher les identifiants URSSAF de l'utilisateur
- Ne lancer le script qu'après confirmation de la période par l'utilisateur
- Si le script retourne une erreur, l'afficher intégralement pour faciliter le diagnostic
- Montants toujours en euros, formatés `X XXX,XX €`
