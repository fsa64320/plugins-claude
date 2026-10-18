# Mes plugins Claude Code

Marketplace personnel de plugins [Claude Code](https://claude.ai/code).

## Ajouter ce marketplace

```bash
claude plugin marketplace add github:fsa64320/plugins-claude
```

## Plugins disponibles

Le plugin `declaration-impot-france` a déménagé dans la marketplace [`sales-marketplace`](https://github.com/fsa64320/marketplace) :

```bash
claude plugin marketplace add fsa64320/marketplace
claude plugin install declaration-impot-france@sales-marketplace
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
│   └── <nom-du-plugin>/
│       ├── .claude-plugin/plugin.json
│       └── skills/<skill>/SKILL.md
└── README.md
```

## Avertissement

Les plugins fiscaux sont des outils d'aide informatifs. Ils ne remplacent pas les conseils d'un expert-comptable ou d'un conseiller fiscal agréé.
