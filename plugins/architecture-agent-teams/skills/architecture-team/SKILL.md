---
name: architecture-team
description: Activez ce skill quand l'utilisateur pose une problématique d'architecture logicielle ou système, demande de "concevoir", "architecturer", "évaluer", "valider" ou "revoir" une solution technique. Exemples déclencheurs : "Conçois une architecture microservices", "Comment sécuriser mon API ?", "Quelle architecture Azure pour mon SaaS ?", "architecture agent teams", "crée une équipe architecture", "expert architecture", "revue d'architecture", "design de système", "choix technologique Azure/AWS", "threat model", "zero trust", "résilience", "scalabilité", "plan de migration cloud", "architecture event-driven", "comment gérer l'authentification", "mise en place d'un système d'emailing".
version: 1.0.0
allowed-tools: [Agent, Read, Glob, Bash, Write, Edit]
---

# Architecture Agent Teams

## Vue d'ensemble

Ce skill orchestre une équipe d'agents spécialisés en architecture logicielle et système pour traiter des problématiques complexes. Chaque agent apporte une expertise distincte ; l'Orchestrateur coordonne leurs contributions.

**Principe fondamental :** Ne créez pas une équipe quand un seul agent peut répondre en un passage. Les équipes ajoutent un overhead de coordination — utilisez-les seulement quand la parallélisation ou la spécialisation apporte une valeur réelle.

**Prérequis — activer les agent teams :**
```json
// .claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## Roster des agents

### Agents permanents (toujours disponibles)

| Agent | Modèle | Type | Rôle | Périmètre |
|-------|--------|------|------|-----------|
| **Orchestrateur** | opus | general-purpose | Planifie, délègue, synthétise. Ne conçoit jamais directement. | Vue globale du problème |
| **Explorateur** | haiku | Explore | Répond aux questions de l'Orchestrateur sur le contexte/codebase. | Ciblé sur ce qui est demandé |
| **Architecte Solution** | sonnet | general-purpose | Patterns architecturaux, décisions de design, trade-offs, ADR. | Architecture transverse |
| **Expert Cybersécurité** | sonnet | general-purpose | Threat modeling, OWASP, Zero Trust, chiffrement, IAM, audit. | Sécurité bout en bout |
| **Expert Azure** | sonnet | general-purpose | Services Azure, ARM/Bicep, AKS, App Service, Entra ID, Azure PaaS. | Périmètre Azure uniquement |
| **Expert AWS** | sonnet | general-purpose | Services AWS, CDK/CloudFormation, EKS, Lambda, IAM, AWS PaaS. | Périmètre AWS uniquement |
| **Relecteur Architecture** | sonnet | code-reviewer | Valide la cohérence, les gaps, les risques non adressés. | Livrables des autres agents |

### Experts à la demande (spawner selon besoin)

| Expert | Modèle | Spécialité | Quand le spawner |
|--------|--------|------------|-----------------|
| **Expert Authentification** | sonnet | OAuth2, OIDC, JWT, SAML, MFA, SSO, Entra ID B2C/B2B, Keycloak | Tout sujet auth/authz/identité |
| **Expert Emailing** | sonnet | SMTP, SendGrid, SES, Mailgun, templates, délivrabilité, SPF/DKIM/DMARC | Système d'envoi d'emails |
| **Expert Base de Données** | sonnet | SQL, NoSQL, NewSQL, migration, sharding, réplication, performance | Modélisation ou choix de BDD |
| **Expert API & Intégration** | sonnet | REST, GraphQL, gRPC, webhooks, API Gateway, contrats, versionning | Design d'API ou intégrations |
| **Expert Performance & Scalabilité** | sonnet | Load balancing, caching (Redis, CDN), observabilité, SLO/SLA | Problèmes de charge ou de latence |
| **Expert DevOps & CI/CD** | sonnet | Pipelines, containers, IaC, GitOps, ArgoCD, Terraform | Déploiement, infra-as-code |
| **Expert Conformité & RGPD** | sonnet | Protection des données, audit trails, chiffrement at-rest, DPA, PCI-DSS | Conformité réglementaire |
| **Expert Event-Driven** | sonnet | Kafka, EventBridge, Azure Service Bus, CQRS, Event Sourcing, Saga | Architecture événementielle |

---

## Modes de communication

### Mode A : Hub-and-Spoke (par défaut)

Toute communication passe par l'Orchestrateur. Aucun agent ne contacte un autre directement.

```
               ┌──────────────┐
               │  Explorateur │
               └──────┬───────┘
                      │
┌─────────────┐  ┌────┴──────────────┐  ┌──────────────┐
│ Architecte  ├──┤  ORCHESTRATEUR    ├──┤ Cybersécurité│
│ Solution    │  │     (opus)        │  │              │
└─────────────┘  │                   │  └──────────────┘
                 │  Tous les msgs    │
┌─────────────┐  │  passent ici      │  ┌──────────────┐
│   Azure     ├──┤                   ├──┤     AWS      │
└─────────────┘  │                   │  └──────────────┘
                 │                   │
┌─────────────┐  │                   │  ┌──────────────┐
│ Expert à la ├──┤                   ├──┤  Relecteur   │
│ demande     │  └──────────────────┘  │  Architecture│
└─────────────┘                        └──────────────┘
```

**Utiliser pour :** Conception, évaluation, plan de migration, tout travail où les agents produisent des livrables distincts.

### Mode B : Discussion (débat d'architecture)

Les agents débattent directement entre eux. L'Orchestrateur est modérateur. Tous les échanges sont loggés dans `temp/discussions/`.

**Utiliser pour :** Choix entre plusieurs approches concurrentes, décisions avec trade-offs significatifs, revue critique d'une architecture existante.

#### Détecter le besoin de discussion

| Signal dans la demande | Exemple |
|------------------------|---------|
| Comparaison d'approches | "Microservices vs monolithe pour ce cas ?" |
| Décision avec trade-offs | "Quelle solution de messaging choisir ?" |
| Revue critique | "Quels sont les points faibles de cette architecture ?" |
| Hypothèses concurrentes | "Pourquoi notre système est-il lent ?" |

Si détecté, proposer les deux modes à l'utilisateur :
```
Ce sujet se prête à deux approches :

1. Hub-and-spoke (standard) — Chaque expert produit son analyse,
   l'Orchestrateur synthétise. Résultat rapide et structuré.
2. Mode discussion — Les experts débattent directement leurs positions.
   Produit des conclusions plus robustes mais coûte plus de tokens.

Quelle approche préférez-vous ?
```

---

## Étape 1 : Analyser la problématique

Avant de composer l'équipe, extraire ces dimensions :

### 1a. Identifier les dimensions du problème

- Quels domaines sont touchés (sécurité, cloud, data, API, auth…) ?
- Y a-t-il des contraintes cloud (Azure only, AWS, multi-cloud, on-prem) ?
- Y a-t-il un existant à analyser ou part-on de zéro ?
- Faut-il un livrable précis (ADR, schéma, checklist, plan de migration) ?

### 1b. Correspondance problème → agents

```
Domaine identifié...                     → Agent à spawner
───────────────────────────────────────────────────────────
Questions sur le contexte/codebase       → Explorateur (toujours)
Patterns, design global, trade-offs      → Architecte Solution
Sécurité, menaces, IAM, compliance       → Cybersécurité
Services Azure, hébergement Microsoft    → Expert Azure
Services AWS, hébergement Amazon         → Expert AWS
Identité, login, tokens, SSO             → Expert Authentification (demande)
Emails transactionnels/marketing         → Expert Emailing (demande)
Modélisation données, choix BDD          → Expert Base de Données (demande)
Design API, contrats, intégrations       → Expert API & Intégration (demande)
Performance, cache, scalabilité          → Expert Performance (demande)
CI/CD, Terraform, containers             → Expert DevOps (demande)
RGPD, PCI-DSS, audit                     → Expert Conformité (demande)
Messaging, CQRS, Event Sourcing          → Expert Event-Driven (demande)
Validation finale des livrables          → Relecteur Architecture (toujours pour implem)
```

### 1c. Correspondances types de demande → équipes

| Type de demande | Agents spawnés | Mode |
|-----------------|---------------|------|
| Nouvelle architecture système | Explorateur + Architecte Solution + Cybersécurité + Relecteur | Hub-and-spoke |
| Architecture SaaS sur Azure | Explorateur + Architecte Solution + Azure + Cybersécurité + Relecteur | Hub-and-spoke |
| Migration vers AWS | Explorateur + Architecte Solution + AWS + DevOps + Relecteur | Hub-and-spoke |
| Système d'authentification | Explorateur + Architecte Solution + Auth + Cybersécurité + Relecteur | Hub-and-spoke |
| Système de notification email | Explorateur + Architecte Solution + Emailing + Cybersécurité + Relecteur | Hub-and-spoke |
| Revue architecture existante | Explorateur + 3-4 panélistes experts | **Proposer discussion** |
| Choix entre 2+ approches | Explorateur + panélistes | **Proposer discussion** |
| Threat modeling | Explorateur + Cybersécurité + Architecte Solution + Relecteur | Hub-and-spoke |
| Architecture event-driven | Explorateur + Architecte Solution + Event-Driven + Cybersécurité + Relecteur | Hub-and-spoke |

### 1d. Présenter la recommandation à l'utilisateur

Avant d'exécuter, toujours présenter :

```
Analyse de votre problématique :
- Dimensions identifiées : [liste]
- [X] peuvent être traitées en parallèle, [Y] sont séquentielles
- Approche recommandée : [équipe / agent unique / discussion]

Équipe proposée :
- [agent] — [pourquoi]
- [agent] — [pourquoi]

Experts à la demande recommandés :
- [expert] — [pourquoi]

Ordre d'exécution :
1. Explorateur cartographie le contexte
2. [tâche] (parallèle avec 3)
3. [tâche] (parallèle avec 2)
4. Relecteur valide les livrables
```

---

## Étape 2 : Choisir l'approche

### Agent unique
**Quand :** Question pointue sur un seul domaine, réponse en un passage suffisante.

### Agents parallèles
**Quand :** 2-3 domaines indépendants, pas d'état partagé, résultats indépendants.

### Équipe complète
**Quand :**
- 3+ domaines nécessitant coordination ou handoffs
- Architecture transverse (sécurité + cloud + data + API)
- Travail long avec échanges de résultats entre agents
- Livrables interdépendants (ex. : schéma d'auth qui influence l'architecture API)

**Ne PAS créer d'équipe quand :**
- Un seul sonnet peut répondre en un passage
- Les tâches sont séquentielles et couplées
- L'overhead dépasse le bénéfice

---

## Étape 3 : Sélection des modèles

| Signal | Modèle | Raison |
|--------|--------|--------|
| Recherche dans le contexte, patterns | **haiku** | Mécanique, pas de raisonnement profond |
| Analyse de services, rédaction de plans | **sonnet** | Bon raisonnement + génération |
| Décisions architecturales complexes, trade-offs multiples | **sonnet** | Jugement dans un périmètre défini |
| Coordination de 4+ agents, orchestration complexe | **opus** | Raisonnement profond + gestion de l'ambiguïté |
| Architecture ouverte, exigences floues | **opus** | Doit arbitrer, pas juste appliquer |

**Pyramide de coût :** Explorateur (haiku) collecte → Experts (sonnet) conçoivent → Orchestrateur (opus) coordonne.

---

## Étape 4 : Composer et exécuter

### Cycle de vie

1. **Créer l'équipe** — `TeamCreate` avec un nom descriptif (ex. `arch-saas-azure`)
2. **Spawner l'Explorateur** — toujours en premier pour cartographier le contexte
3. **Créer les tâches** — `TaskCreate` avec périmètre, contraintes, dépendances (`addBlockedBy`)
4. **Spawner les agents** — uniquement ceux nécessaires, avec leur liste de fichiers/contexte
5. **Assigner les tâches** — `TaskUpdate` avec `owner`
6. **Coordonner** — `SendMessage` type `message` uniquement. Pas de broadcast.
7. **Valider** — Relecteur Architecture valide tous les livrables avant conclusion
8. **Arrêter** — `SendMessage` type `shutdown_request` à chaque agent
9. **Nettoyer** — `TeamDelete` après confirmation d'arrêt de tous les agents

### Workflow de l'Orchestrateur

```
1. Recevoir la problématique de l'utilisateur
2. Spawner Explorateur → poser des questions ciblées sur le contexte
3. Sur la base des résultats, déterminer quels agents spawner
4. Créer les tâches avec périmètre explicite et contraintes
5. Spawner les agents, assigner les tâches
6. Attendre les livrables. Relayer le contexte entre agents si nécessaire.
7. Spawner le Relecteur une fois les livrables produits
8. Si le Relecteur identifie des gaps → renvoyer aux agents concernés
9. Synthétiser et présenter les résultats à l'utilisateur
10. Arrêter tous les agents → TeamDelete
```

---

## Livrables attendus par type de demande

| Demande | Livrables produits |
|---------|-------------------|
| Conception architecture | Schéma C4 (texte), ADR, liste des services, risques |
| Threat modeling | STRIDE par composant, matrice de risques, recommandations |
| Architecture cloud | Services recommandés, topologie réseau, IAM, coût estimé |
| Système auth | Flux OIDC/OAuth2, choix de solution, configuration recommandée |
| Système emailing | Choix de prestataire, topologie, configuration SPF/DKIM/DMARC |
| Plan de migration | Phases, dépendances, risques, rollback strategy |
| Revue architecture | Points forts, gaps, vulnérabilités, recommandations priorisées |

---

## Règles d'optimisation des tokens

### Tous les agents

| Règle | Application |
|-------|-------------|
| **Penser en silence** | Tout le raisonnement dans l'extended thinking. Output = résultats uniquement. |
| **Recherche ciblée** | Chercher uniquement dans les fichiers/contexte assignés. |
| **Output minimal** | Format : livrable produit, décisions prises, blocages. Pas de résumé de lecture. |
| **Bloquer = remonter** | Si bloqué, message à l'Orchestrateur avec le blocage précis, pas un status général. |

### Orchestrateur

| Règle | Application |
|-------|-------------|
| **Ne jamais chercher directement** | Déléguer toute recherche à l'Explorateur. Tokens opus = précieux. |
| **Fournir le contexte upfront** | Avant d'assigner, utiliser l'Explorateur pour identifier le contexte exact. |
| **Grouper les questions Explorateur** | Poser plusieurs questions en un seul message. |

---

## Erreurs courantes

| Erreur | Correction |
|--------|-----------|
| Agents réfléchissant à voix haute | Imposer "tout raisonnement en extended thinking" dans chaque prompt |
| Orchestrateur cherchant lui-même | Toujours déléguer à l'Explorateur |
| Créer une équipe pour une question simple | Utiliser un seul `Task` sonnet |
| Spawner Azure ET AWS sans besoin clair | Vérifier le contexte cloud avec l'utilisateur avant |
| Oublier le Relecteur | Le Relecteur est toujours présent pour valider les livrables finaux |
| Experts à la demande non spawnés | Analyser la demande complète — l'auth et l'emailing sont souvent des sous-sujets implicites |
| Mode discussion sans log | Le Modérateur crée le fichier log AVANT de spawner les panélistes |

---

## Signaux d'alerte

**Surconstruction :** équipe de 6+ agents, plusieurs agents opus, dépendances circulaires.

**Sous-construction :** un seul agent traitant 5+ domaines séquentiellement, travail parallelisable en série.

**Gaspillage de tokens :** agents outputtant leur raisonnement, Orchestrateur faisant des grep lui-même, agents lisant des répertoires entiers.

---

> **Avertissement :** Ce skill est un guide méthodologique pour l'orchestration d'agents IA spécialisés en architecture. Les recommandations produites sont indicatives et constituent un point de départ de réflexion. Elles ne remplacent pas une évaluation par un architecte solution ou un expert certifié pour des décisions en production. Validez toujours les choix architecturaux avec les équipes et contraintes spécifiques de votre contexte.

Voir [agent-prompt-template.md](agent-prompt-template.md) pour les templates de prompts par rôle et [expertise-catalogue.md](expertise-catalogue.md) pour le détail des experts à la demande.
