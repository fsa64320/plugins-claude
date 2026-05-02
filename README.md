# Plugin Fiscal France — Claude Code

Plugin Claude Code pour l'aide à la déclaration d'impôts en France.

## Skills disponibles

| Skill | Déclencheur |
|-------|-------------|
| `analyse-document-fiscal` | Analyser un IFU, relevé SCPI, attestation fiscale |
| `optimisation-fiscale` | Optimiser sa fiscalité, comparer PFU vs barème |
| `expert-fiscal-qa` | Questions sur les règles fiscales françaises |
| `guide-declaration` | Guide pas à pas pour remplir la déclaration 2042 |

## Installation

```bash
claude plugin add github:fredericksales/plugin-fiscal-france
```

## Structure

```
plugins/
└── declaration-impot-france/
    ├── .claude-plugin/
    │   └── plugin.json
    └── skills/
        ├── analyse-document-fiscal/SKILL.md
        ├── optimisation-fiscale/SKILL.md
        ├── expert-fiscal-qa/SKILL.md
        └── guide-declaration/SKILL.md
```

## Avertissement

Ce plugin est un outil d'aide informatif. Il ne remplace pas les conseils d'un expert-comptable ou d'un conseiller fiscal agréé.
