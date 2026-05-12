# Architecture Agent Teams

Plugin Claude Code pour résoudre des problématiques d'architecture logicielle et système grâce à une équipe d'agents spécialisés.

## Présentation

Ce plugin orchestre une équipe d'agents experts pour traiter des sujets d'architecture complexes : conception de systèmes, threat modeling, choix cloud (Azure/AWS), sécurité, et bien plus. Chaque agent apporte une expertise pointue ; un Orchestrateur coordonne leurs contributions pour produire des livrables cohérents et actionnables.

## Installation

```bash
claude plugin marketplace add github:fsa64320/plugins-claude
```

**Prérequis — activer les agent teams :**
```json
// .claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Utilisation

Décrivez simplement votre problématique d'architecture. Le skill se déclenche automatiquement sur des phrases comme :

- "Conçois une architecture microservices pour mon SaaS"
- "Comment sécuriser mon API exposée sur Azure ?"
- "Quelle architecture AWS pour un système événementiel haute disponibilité ?"
- "Fais un threat modeling de mon application"
- "Aide-moi à concevoir le système d'authentification SSO pour mes clients B2B"
- "Revue d'architecture de mon système existant"
- "Comment gérer l'envoi d'emails transactionnels à grande échelle ?"

## Agents disponibles

### Équipe permanente

| Agent | Modèle | Rôle |
|-------|--------|------|
| **Orchestrateur** | claude-opus | Coordonne l'équipe, synthétise les livrables |
| **Explorateur** | claude-haiku | Cartographie le contexte et le codebase |
| **Architecte Solution** | claude-sonnet | Patterns, ADR, décisions de design, trade-offs |
| **Expert Cybersécurité** | claude-sonnet | Threat modeling, OWASP, Zero Trust, IAM |
| **Expert Azure** | claude-sonnet | Services Azure, AKS, Entra ID, Bicep/ARM |
| **Expert AWS** | claude-sonnet | Services AWS, EKS, Cognito, CDK/Terraform |
| **Relecteur Architecture** | claude-sonnet | Valide la cohérence et les gaps |

### Experts à la demande

Spawnés automatiquement selon les besoins détectés dans votre demande :

| Expert | Déclenché par |
|--------|--------------|
| **Authentification** | auth, SSO, OAuth, OIDC, login, JWT, MFA |
| **Emailing** | email, SMTP, notifications, délivrabilité, SendGrid, SES |
| **Base de Données** | BDD, SQL, NoSQL, modèle de données, migration, performance |
| **API & Intégration** | REST, GraphQL, gRPC, webhook, API Gateway |
| **Performance & Scalabilité** | latence, charge, cache, CDN, SLO/SLA |
| **DevOps & CI/CD** | pipeline, Terraform, containers, IaC, GitOps |
| **Conformité & RGPD** | RGPD, PCI-DSS, HDS, audit, données personnelles |
| **Event-Driven** | Kafka, CQRS, Event Sourcing, Saga, messaging |

## Modes de travail

### Hub-and-spoke (défaut)
Chaque expert produit son analyse en parallèle, l'Orchestrateur coordonne et synthétise. Optimal pour la conception et la planification.

### Mode discussion
Les experts débattent directement entre eux pour des sujets avec des trade-offs importants (choix entre deux approches, revue critique, root cause). Un log de discussion est produit dans `temp/discussions/`.

## Livrables produits

Selon votre demande, l'équipe peut produire :

- **Schémas d'architecture** (ASCII / Mermaid C4)
- **ADR** (Architecture Decision Records)
- **Threat model** avec matrice STRIDE et recommandations
- **Plan de migration** avec phases, dépendances et stratégie de rollback
- **Comparatifs technologiques** avec justification
- **Configurations recommandées** (IAM, réseau, DNS, CI/CD)
- **Estimations de coût** cloud
- **Checklists** de conformité

## Exemple de session

```
Vous : Conçois l'architecture d'un SaaS B2B multi-tenant sur Azure.
       Les clients doivent pouvoir se connecter avec leur propre Entra ID.
       Environ 500 clients, 50 000 utilisateurs actifs.

→ L'Orchestrateur analyse la demande
→ Spawn : Architecte Solution + Expert Azure + Expert Cybersécurité + Expert Auth
→ Chaque expert produit son analyse en parallèle
→ Relecteur Architecture valide la cohérence
→ Livrable synthétisé : architecture complète avec schéma, services Azure, flux OIDC,
  recommandations IAM, points de vigilance sécurité
```

---

> **Avertissement :** Les recommandations produites par ce plugin sont indicatives et constituent un point de départ de réflexion architecturale. Elles ne remplacent pas l'évaluation d'un architecte solution ou d'un expert certifié pour des décisions en production. Validez toujours les choix architecturaux au regard des contraintes spécifiques de votre contexte (équipe, budget, exigences métier, conformité).
