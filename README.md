# Mes plugins Claude Code

Marketplace personnel de plugins [Claude Code](https://claude.ai/code).

## Ajouter ce marketplace

```bash
claude plugin marketplace add github:fsa64320/plugins-claude
```

## Plugins disponibles

### `declaration-impot-france`

Assistant fiscal pour les contribuables français.

| Skill | Rôle |
|-------|------|
| `analyse-document-fiscal` | Analyse un IFU, relevé SCPI ou attestation fiscale |
| `optimisation-fiscale` | Compare les régimes et identifie les leviers fiscaux |
| `expert-fiscal-qa` | Répond aux questions sur les règles fiscales françaises |
| `guide-declaration` | Guide pas à pas pour remplir la déclaration 2042 |

```bash
claude plugin install declaration-impot-france
```

## Ajouter un nouveau plugin

1. Créer un dossier `plugins/<nom-du-plugin>/`
2. Y ajouter `.claude-plugin/plugin.json` et `skills/<skill>/SKILL.md`
3. Ajouter une entrée dans `.claude-plugin/marketplace.json`
4. `git push`

## Structure du repo

```
plugins-claude/
├── .claude-plugin/
│   └── marketplace.json          ← index de tous les plugins
├── plugins/
│   ├── declaration-impot-france/ ← plugin 1
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/
│   │       ├── analyse-document-fiscal/SKILL.md
│   │       ├── optimisation-fiscale/SKILL.md
│   │       ├── expert-fiscal-qa/SKILL.md
│   │       └── guide-declaration/SKILL.md
│   └── <prochain-plugin>/        ← plugin 2, 3, ...
└── README.md
```

## Avertissement

Les plugins fiscaux sont des outils d'aide informatifs. Ils ne remplacent pas les conseils d'un expert-comptable ou d'un conseiller fiscal agréé.
