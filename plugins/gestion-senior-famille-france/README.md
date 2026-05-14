# Plugin gestion-senior-famille-france

Assistant complet pour les familles gérant un proche senior en EHPAD dans un contexte conflictuel ou complexe : délégation administrative, finances et aides, succession anticipée, médiation et communication familiale.

## Installation

```bash
claude plugin marketplace add github:fsa64320/plugins-claude
```

## Skills disponibles

| Skill | Déclenché quand | Ce que ça fait |
|-------|----------------|----------------|
| `delegation-administrative` | "procuration pour ma mère", "habilitation familiale", "tutelle curatelle", "mon proche ne peut plus signer" | Compare les dispositifs légaux (procuration, habilitation, curatelle, tutelle), détaille la procédure, les coûts et les obligations du mandataire |
| `finances-ehpad-patrimoine` | "payer l'EHPAD", "APA", "aide sociale à l'hébergement", "déduction impôt EHPAD", "vendre la maison de mes parents" | Décrypte les tarifs EHPAD, guide sur les aides (APA, APL, ASH), optimise la fiscalité et accompagne la gestion du patrimoine |
| `succession-senior-conflit` | "succession de ma mère", "conflit entre héritiers", "indivision bloquée", "testament", "donation-partage" | Aide à anticiper la succession (donations, testament, fiscalité) et à gérer un conflit entre héritiers (indivision, action en partage) |
| `mediation-communication-famille` | "écrire à mon frère", "lettre à l'EHPAD", "signaler un problème", "réunion de famille conflictuelle", "médiation familiale" | Fournit des outils CNV, des modèles de courriers et une stratégie de médiation pour naviguer les communications difficiles |

## Sources de données

Ce plugin utilise le serveur MCP `datagouv` (`https://mcp.data.gouv.fr/mcp`) pour accéder aux données publiques françaises (législation, formulaires officiels, données des établissements médico-sociaux).

## Exemples d'utilisation

**Délégation administrative :**
> "Mon père a une démence avancée et ne peut plus gérer ses comptes. Que puis-je faire légalement pour le représenter ?"

**Finances EHPAD :**
> "Ma mère entre en EHPAD le mois prochain. Quelles aides peut-elle toucher et comment réduire notre reste à charge ?"

**Succession :**
> "Mes frères et sœurs ne s'entendent pas sur la vente de la maison familiale depuis le décès de papa. Comment débloquer la situation ?"

**Médiation :**
> "Je dois écrire à mon frère qui refuse de signer les actes de succession depuis 6 mois. Aide-moi à rédiger un courrier calme mais ferme."

## Avertissement légal

Ce plugin est un outil d'aide informatif à destination des particuliers. Il ne remplace pas les conseils d'un notaire, d'un avocat spécialisé en droit de la famille, d'un médiateur familial certifié ou d'un travailleur social. Toute décision importante concernant la protection juridique d'un proche, la gestion de son patrimoine ou le règlement d'une succession doit être prise avec l'accompagnement d'un professionnel qualifié.
