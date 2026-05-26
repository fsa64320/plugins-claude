# TTE Cowork Plugin

> ⚠️ **Prérequis obligatoire** : ce plugin nécessite le **plugin Playwright** pour fonctionner.  
> Installez-le dans Claude Cowork avant d'utiliser ce plugin.

Plugin Claude Cowork pour interagir avec les outils TotalEnergies :
- **Confluence TDF** (`tdf.atlassian.net`) — base documentaire
- **Outlook TotalEnergies** (`outlook.cloud.microsoft`) — messagerie
- **Microsoft Teams TotalEnergies** (`teams.microsoft.com`) — messagerie instantanée et canaux

Les trois services utilisent l'authentification OAuth 2.0 via Entra ID (Microsoft Identity Platform), avec proxy MCAS pour Outlook et Teams.

---

## Skills Confluence

### `confluence-connect`
Gère la connexion à Confluence TDF via Playwright + OAuth Entra ID.

**Exemples d'utilisation :**
- "Connecte-toi à Confluence"
- "Ouvre Confluence TDF"
- "Vérifie si tu es connecté à Confluence"
- "Authentifie-toi sur tdf.atlassian.net"

### `confluence-query`
Interroge l'API REST Confluence une fois la session active.

**Exemples d'utilisation :**
- "Liste les espaces Confluence"
- "Cherche les pages sur [sujet]"
- "Lis la page [titre]"
- "Montre les pages récentes de l'espace [clé]"
- "Recherche dans Confluence : [mot-clé]"

---

## Skills Outlook

### `outlook-connect`
Gère la connexion complète : proxy MCAS → Microsoft login → Entra ID + MFA → confirmation.

**Exemples d'utilisation :**
- "Connecte-toi à Outlook"
- "Ouvre ma messagerie TotalEnergies"
- "Vérifie si tu es connecté à Outlook"

### `outlook-query`
Interroge la boîte mail Outlook une fois la session active (scraping DOM).

**Exemples d'utilisation :**
- "Montre-moi mes 10 derniers emails"
- "Cherche les emails de jean.dupont@totalenergies.com"
- "Trouve les emails avec 'budget Q2' dans l'objet"
- "Lis l'email sur la réunion de demain"
- "Liste mes dossiers de messagerie"
- "Montre-moi mes emails non lus"

---

## Workflows typiques

### Confluence
1. "Connecte-toi à Confluence"
   → Page Atlassian → OAuth Entra ID → MFA → confirmation
2. "Liste les espaces Confluence" → liste des espaces disponibles
3. "Cherche les pages sur [sujet]" → résultats CQL
4. "Lis cette page" → contenu complet structuré

### Outlook
1. **(Première fois)** "Connecte-toi à Outlook"
   → Page MCAS → clic automatique → page Microsoft login
   → vous vous authentifiez → MFA → confirmation
2. "Montre mes emails récents" → liste des 20 derniers emails
3. "Cherche les emails de [nom]" → résultats de recherche
4. "Lis cet email" → contenu complet structuré

La session reste active plusieurs heures. Pas besoin de se reconnecter à chaque requête.

---

## Skills Teams

### `teams-connect`
Gère la connexion complète : proxy MCAS → Microsoft login → Entra ID + MFA → confirmation.

**Exemples d'utilisation :**
- "Connecte-toi à Teams"
- "Ouvre Microsoft Teams"
- "Vérifie si tu es connecté à Teams"

### `teams-query`
Interroge Teams via scraping DOM une fois la session active.

**Exemples d'utilisation :**
- "Liste mes équipes Teams"
- "Montre-moi les canaux de [équipe]"
- "Lis les messages du canal [nom]"
- "Montre-moi mes conversations directes"
- "Cherche [mot-clé] dans Teams"
- "Qu'est-ce qu'il y a dans le canal [nom] ?"

---

## Workflow Teams

1. **(Première fois)** "Connecte-toi à Teams"
   → Page MCAS → clic automatique → page Microsoft login
   → vous vous authentifiez → MFA → confirmation
2. "Liste mes équipes" → liste des équipes et canaux
3. "Lis les messages du canal [nom]" → fil de messages
4. "Montre mes conversations directes" → liste des DMs
5. "Cherche [sujet] dans Teams" → résultats de recherche

---

## Architecture technique

### Confluence TDF

| Élément | Valeur |
|---------|--------|
| URL | `https://tdf.atlassian.net/wiki` |
| Cloud ID | `23cadbe4-5ee9-46f7-8a55-f7ac9c44041a` |
| Authentification | OAuth 2.0 via Entra ID (SSO TotalEnergies) |
| API | Confluence REST API v1 |
| Accès token | Cookies de session (`fetch` avec `credentials: 'include'`) |

### Outlook TotalEnergies

| Élément | Valeur |
|---------|--------|
| URL d'entrée | `https://outlook.cloud.microsoft.mcas.ms/mail/` |
| Proxy sécurité | Microsoft Defender for Cloud Apps (MCAS) |
| URL finale | `https://outlook.cloud.microsoft/mail/` |
| Authentification | OAuth 2.0 PKCE via Entra ID |
| Données | Scraping DOM (Graph API bloqué par MCAS) |

### Microsoft Teams TotalEnergies

| Élément | Valeur |
|---------|--------|
| URL d'entrée | `https://teams.microsoft.com.mcas.ms/` |
| Proxy sécurité | Microsoft Defender for Cloud Apps (MCAS) |
| URL finale | `https://teams.microsoft.com/` |
| Authentification | OAuth 2.0 PKCE via Entra ID |
| Données | Scraping DOM (Graph API bloqué par MCAS) |
