# Catalogue des experts à la demande

Référence rapide pour l'Orchestrateur : quand spawner quel expert, avec quels signaux dans la demande utilisateur.

---

## Comment utiliser ce catalogue

L'Orchestrateur consulte ce catalogue lors de l'analyse de la problématique (Étape 1 du SKILL.md).
Chaque entrée liste les **signaux déclencheurs** — mots-clés ou contextes dans la demande qui justifient le spawn de cet expert.

---

## Expert Authentification

**Nom d'agent :** `expert-auth`
**Modèle :** sonnet

### Signaux déclencheurs
- Mentions explicites : login, authentification, SSO, MFA, OAuth, OIDC, SAML, JWT, token, session
- Contexte implicite : "les utilisateurs doivent se connecter", "accès sécurisé", "gestion des comptes"
- Cloud spécifique : Entra ID, Azure AD, Cognito, Keycloak, Auth0, Okta, Clerk
- Cas d'usage : application multi-tenant, fédération d'identité, B2B avec SSO client, API sécurisée

### Domaines couverts
- Protocoles : OAuth 2.0, OIDC, SAML 2.0, FIDO2/Passkeys
- Fournisseurs : Microsoft Entra ID (B2B/B2C/External), AWS Cognito, Auth0, Keycloak, Okta
- Flux : Authorization Code + PKCE, Client Credentials, Device Flow
- Sécurité des tokens : durée de vie, refresh strategy, révocation, stockage sécurisé
- MFA : TOTP, SMS (déconseillé), FIDO2, push notification
- SSO : fédération d'identité entreprise, SCIM pour provisioning

### Ne couvre PAS
- IAM infrastructure (→ Expert Azure/AWS pour les rôles de services)
- Autorisation fine (RBAC/ABAC applicatif → Architecte Solution)

---

## Expert Emailing

**Nom d'agent :** `expert-emailing`
**Modèle :** sonnet

### Signaux déclencheurs
- Mentions explicites : email, SMTP, délivrabilité, newsletter, notification par email, SPF, DKIM, DMARC
- Contexte implicite : "envoyer des notifications", "confirmation d'inscription", "reset de mot de passe"
- Prestataires : SendGrid, Amazon SES, Mailgun, Brevo (ex-Sendinblue), Postmark, Mailchimp
- Volume : "X emails par jour/mois", emailing à grande échelle, campagnes marketing

### Domaines couverts
- Prestataires ESP : SendGrid, Amazon SES, Mailgun, Brevo, Postmark (transactionnel), Mailchimp (marketing)
- Délivrabilité : SPF, DKIM (multi-sélecteurs), DMARC (politique p=none/quarantine/reject)
- Architecture d'envoi : synchrone vs asynchrone, queue (SQS, Service Bus, RabbitMQ)
- Gestion des listes : bounces (hard/soft), plaintes, unsubscribes (CAN-SPAM, RGPD)
- Templates : Handlebars, Liquid, MJML, i18n des templates
- Monitoring : taux de livraison, bounce rate, spam score, alertes

### Ne couvre PAS
- Notifications push mobile (→ Architecte Solution)
- SMS/WhatsApp (→ Expert à créer si besoin)

---

## Expert Base de Données

**Nom d'agent :** `expert-bdd`
**Modèle :** sonnet

### Signaux déclencheurs
- Mentions explicites : base de données, SQL, NoSQL, PostgreSQL, MySQL, MongoDB, Redis, migration
- Contexte implicite : "stocker les données", "modèle de données", "performance des requêtes"
- Problèmes : lenteur des requêtes, scaling de la BDD, sharding, réplication, multi-région
- Choix technologique : "quelle BDD choisir pour ce cas ?"

### Domaines couverts
- Relationnel : PostgreSQL, MySQL, Azure SQL, Amazon RDS/Aurora
- NoSQL document : MongoDB, Cosmos DB, DynamoDB
- Cache / In-memory : Redis, Memcached, Azure Cache for Redis, ElastiCache
- NewSQL / distribué : CockroachDB, Spanner, Cassandra
- Modélisation : schéma relationnel, modèle document, gestion des migrations
- Performance : indexation, query optimization, partitioning, sharding, connection pooling
- Réplication et haute disponibilité : read replicas, failover, multi-région

---

## Expert API & Intégration

**Nom d'agent :** `expert-api`
**Modèle :** sonnet

### Signaux déclencheurs
- Mentions explicites : API REST, GraphQL, gRPC, webhook, API Gateway, contrat d'API
- Contexte implicite : "exposer des données", "intégrer un partenaire", "communication entre services"
- Problèmes : versionning d'API, rétrocompatibilité, gestion des contrats, documentation

### Domaines couverts
- Styles : REST, GraphQL, gRPC, WebSocket, webhooks
- Gateway : Azure APIM, AWS API Gateway, Kong, Traefik
- Contrats : OpenAPI 3.x, Protobuf, schema-first vs code-first
- Versionning : URL versioning, header versioning, deprecation strategy
- Sécurité API : rate limiting, OAuth scopes, API keys, mTLS
- Intégration : patterns d'intégration (Strangler Fig, Anti-Corruption Layer)

---

## Expert Performance & Scalabilité

**Nom d'agent :** `expert-perf`
**Modèle :** sonnet

### Signaux déclencheurs
- Mentions explicites : performance, latence, scalabilité, charge, SLO, SLA, cache, CDN
- Contexte implicite : "X utilisateurs simultanés", "pics de trafic", "réduire la latence"
- Problèmes : goulots d'étranglement, timeout, OOM, coûts liés à la sur-scalabilité

### Domaines couverts
- Caching : stratégies (cache-aside, write-through, write-behind), Redis, CDN (Azure Front Door, CloudFront)
- Load balancing : L4 vs L7, sticky sessions, health checks, circuit breaker
- Scalabilité horizontale vs verticale, auto-scaling
- Observabilité : métriques (Prometheus/Grafana, Azure Monitor, CloudWatch), tracing distribué (Jaeger, X-Ray), logs centralisés
- SLO/SLA : définition des indicateurs, error budgets, alerting

---

## Expert DevOps & CI/CD

**Nom d'agent :** `expert-devops`
**Modèle :** sonnet

### Signaux déclencheurs
- Mentions explicites : CI/CD, pipeline, déploiement, Terraform, Bicep, container, Docker, Kubernetes
- Contexte implicite : "automatiser les déploiements", "infrastructure as code", "GitOps"
- Problèmes : temps de déploiement, rollback, environnements multiples, secrets management

### Domaines couverts
- CI/CD : GitHub Actions, Azure DevOps Pipelines, GitLab CI, Jenkins
- IaC : Terraform (multi-cloud), Bicep/ARM (Azure), CDK (AWS), Pulumi
- Containers : Docker, Kubernetes (AKS, EKS, GKE), Helm, Kustomize
- GitOps : ArgoCD, Flux, stratégie de branches (trunk-based, GitFlow)
- Secrets management : Azure Key Vault, AWS Secrets Manager, HashiCorp Vault
- Environnements : dev/staging/prod, feature flags, blue/green, canary

---

## Expert Conformité & RGPD

**Nom d'agent :** `expert-conformite`
**Modèle :** sonnet

### Signaux déclencheurs
- Mentions explicites : RGPD, GDPR, PCI-DSS, HDS, ISO 27001, audit, conformité
- Contexte implicite : "données personnelles", "données de santé", "paiement en ligne"
- Obligations : droit à l'oubli, portabilité des données, consentement, DPA

### Domaines couverts
- RGPD : cartographie des données, bases légales, registre des traitements, DPA, breach notification
- PCI-DSS : scope de conformité, tokenisation, segmentation réseau, audit logs
- HDS : hébergement de données de santé, certification, contraintes techniques
- Chiffrement : at-rest (clés gérées client vs provider), in-transit (TLS 1.3)
- Audit trails : logging des accès, intégrité des logs, durée de conservation

---

## Expert Event-Driven

**Nom d'agent :** `expert-event-driven`
**Modèle :** sonnet

### Signaux déclencheurs
- Mentions explicites : Kafka, EventBridge, Service Bus, CQRS, Event Sourcing, Saga, messaging
- Contexte implicite : "découpler les services", "traitement asynchrone", "audit complet des actions"
- Problèmes : couplage fort entre services, traitement par lots, cohérence éventuelle

### Domaines couverts
- Brokers : Apache Kafka (Confluent), Azure Service Bus / Event Hubs, AWS SQS / SNS / EventBridge, RabbitMQ
- Patterns : CQRS (Command Query Responsibility Segregation), Event Sourcing, Outbox Pattern
- Orchestration vs Chorégraphie, Saga Pattern (orchestrée vs chorégraphiée)
- Idempotence, ordering, at-least-once vs exactly-once delivery
- Schema registry : Confluent Schema Registry, AWS Glue Schema Registry
- Monitoring : lag consumer, dead letter queues, alertes

---

## Grille de décision rapide

```
La demande mentionne...              Spawner...
────────────────────────────────────────────────────────────
login / auth / SSO / token           expert-auth
email / notification / SMTP          expert-emailing
base de données / schéma / SQL       expert-bdd
API / REST / GraphQL / webhook       expert-api
performance / latence / cache        expert-perf
CI/CD / Terraform / pipeline         expert-devops
RGPD / conformité / audit            expert-conformite
Kafka / messaging / CQRS / events    expert-event-driven
```

Plusieurs signaux = plusieurs experts. Vérifier la cohérence entre leurs recommandations via le Relecteur Architecture.
