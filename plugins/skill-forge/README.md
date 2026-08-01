# Plugin Skill Forge

Chaîne de fabrication de skills Claude Code, de l'idée jusqu'à la publication sur GitHub : cadrage, rédaction, évaluation notée avec garde-fou de score, puis publication dans un repo existant via le connecteur GitHub.

## Skill disponible

### `/skill-forge`

Guide la création d'un skill en quatre phases : concevoir & rédiger, évaluer (tests de déclenchement + tests de qualité contre baseline), garde-fou (score sous le seuil configuré ⇒ pas de publication), publier (commit dans le repo cible avec le rapport d'évaluation).

**Ressources embarquées :**
- `scripts/validate_skill.py` — contrôles structurels (frontmatter, kebab-case, secrets, longueur)
- `scripts/score_report.py` — agrégation des notes, garde-fou, rapport Markdown
- `references/evaluation.md` — protocole d'évaluation détaillé
- `references/github-publish.md` — outils MCP GitHub, séquence de publication, mise à jour d'un skill existant
- `assets/config.example.json` — modèle de configuration (repo cible, seuil, pondérations)

## Prérequis

- Connecteur MCP GitHub configuré et autorisé (aucun token en dur — l'authentification passe par le connecteur)
- Python 3 pour les scripts d'évaluation

## Utilisation

```
/skill-forge
```

## Sécurité

La publication est toujours soumise à confirmation explicite de l'utilisateur avant tout commit. Un score sous le seuil configuré bloque la publication sauf validation explicite, tracée dans le message de commit. Aucun jeton n'est jamais demandé ou committé.
