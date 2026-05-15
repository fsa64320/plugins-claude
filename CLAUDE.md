# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Présentation

Marketplace personnel de plugins Claude Code. Il regroupe des plugins prêts à l'emploi, chacun composé de skills spécialisés.

**Ajouter ce marketplace dans Claude Code :**
```bash
claude plugin marketplace add github:fsa64320/plugins-claude
```

## Compatibilité

Ce repo est compatible avec **Claude Code** et **GitHub Copilot** simultanément.

| Fichier | Claude Code | GitHub Copilot |
|---|---|---|
| `.claude-plugin/marketplace.json` | ✅ index principal | ignoré |
| `.github/plugin/marketplace.json` | ignoré | ✅ index principal |
| `plugins/*/.claude-plugin/plugin.json` | ✅ métadonnées | ignoré |
| `plugins/*/.mcp.json` | ignoré | ✅ config MCP |
| `plugins/*/skills/*/SKILL.md` | ✅ | ✅ |

## Structure du dépôt

```
.claude-plugin/
  marketplace.json          ← index Claude Code
.github/
  plugin/
    marketplace.json        ← index GitHub Copilot
plugins/
  <nom-plugin>/
    .claude-plugin/
      plugin.json           ← métadonnées Claude Code (nom, version, auteur, MCP servers)
    .mcp.json               ← config MCP pour GitHub Copilot
    skills/
      <nom-skill>/
        SKILL.md            ← description + instructions du skill (compatible les 2 systèmes)
    README.md               ← documentation utilisateur
```

## Ajouter un nouveau plugin

1. Créer `plugins/<nom-plugin>/.claude-plugin/plugin.json`
2. Créer `plugins/<nom-plugin>/.mcp.json` (si MCP servers)
3. Créer au moins un skill dans `plugins/<nom-plugin>/skills/<skill-name>/SKILL.md`
4. Créer `plugins/<nom-plugin>/README.md`
5. Ajouter une entrée dans `.claude-plugin/marketplace.json` (Claude Code)
6. Ajouter une entrée dans `.github/plugin/marketplace.json` (GitHub Copilot)

## Format des fichiers clés

### `plugin.json`

```json
{
  "name": "nom-kebab-case",
  "version": "1.0.0",
  "description": "Description courte affichée dans le marketplace.",
  "author": {
    "name": "Frederick Sales",
    "email": "frederick.sales@gmail.com"
  },
  "mcpServers": {
    "datagouv": {
      "type": "http",
      "url": "https://mcp.data.gouv.fr/mcp"
    }
  }
}
```

### `SKILL.md`

```markdown
---
name: nom-du-skill
description: Phrase(s) décrivant QUAND déclencher ce skill — doit contenir des mots-clés et exemples de phrases utilisateur pour que Claude sache l'activer automatiquement.
version: 1.0.0
allowed-tools: "Read Glob"
---

# Titre du skill

## Objectif
...

## Processus
...

## Règles importantes
...
```

> **Le champ `description` est critique** : c'est lui qui détermine si Claude active ou non le skill. Il doit contenir des exemples de phrases utilisateur, des mots-clés déclencheurs, et couvrir les variations de formulation.

### `.mcp.json` (GitHub Copilot)

```json
{
  "mcpServers": {
    "datagouv": {
      "type": "http",
      "url": "https://mcp.data.gouv.fr/mcp"
    }
  }
}
```

### `marketplace.json` Claude Code (`.claude-plugin/`)

Chaque plugin est déclaré avec `"source": {"source": "git-subdir", "url": "...", "path": "plugins/<nom>", "ref": "main"}`.

### `marketplace.json` GitHub Copilot (`.github/plugin/`)

Chaque plugin liste explicitement les chemins vers ses SKILL.md et son `.mcp.json` :

```json
{
  "name": "nom-plugin",
  "description": "...",
  "version": "1.0.0",
  "source": "plugins/nom-plugin",
  "skills": ["plugins/nom-plugin/skills/nom-skill/SKILL.md"],
  "mcpServers": "plugins/nom-plugin/.mcp.json"
}
```

## Conventions

- Noms de plugins et skills en **kebab-case**
- Tous les contenus en **français**
- Le MCP server `datagouv` (`https://mcp.data.gouv.fr/mcp`) est partagé par tous les plugins de ce repo
- Chaque SKILL.md se termine par une mise en garde rappelant que le skill est indicatif et ne remplace pas un professionnel

## Plugins actuels

| Plugin | Skills |
|--------|--------|
| `declaration-impot-france` | `analyse-document-fiscal`, `optimisation-fiscale`, `expert-fiscal-qa`, `guide-declaration` |
| `immobilier-locatif-france` | `analyse-bilan`, `analyse-compte-resultat`, `ratios-financiers` |
| `particulier-employeur-france` | `guide-embauche-cesu`, `rupture-conventionnelle`, `declarations-cotisations`, `generation-documents` |
| `architecture-agent-teams` | `architecture-team` |
| `gestion-senior-famille-france` | `delegation-administrative`, `finances-ehpad-patrimoine`, `mediation-communication-famille`, `succession-senior-conflit` |
