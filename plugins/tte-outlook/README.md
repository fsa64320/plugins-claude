# Outlook TotalEnergies Plugin

> ⚠️ **Prérequis obligatoire** : ce plugin nécessite le **plugin Playwright** pour fonctionner.  
> Installez-le dans Claude Cowork avant d'utiliser ce plugin.

Plugin Claude Cowork pour interagir avec la messagerie Outlook de TotalEnergies
(`outlook.cloud.microsoft`) via le proxy sécurité MCAS (Microsoft Defender for Cloud Apps).

## Ce que fait ce plugin

- **Se connecter** à Outlook via votre compte TotalEnergies (OAuth Entra ID + MFA + proxy MCAS)
- **Lister** les emails récents de votre boîte de réception
- **Rechercher** des emails par mot-clé, expéditeur ou objet (syntaxe KQL)
- **Lire** le contenu complet d'un email
- **Lister** vos dossiers de messagerie avec compteurs

## Skills

### `outlook-connect`
Gère la connexion complète : proxy MCAS → Microsoft login → Entra ID + MFA → confirmation.

**Exemples d'utilisation :**
- "Connecte-toi à Outlook"
- "Ouvre ma messagerie TotalEnergies"
- "Vérifie si tu es connecté à Outlook"

### `outlook-query`
Interroge l'API Microsoft Graph une fois la session active.

**Exemples d'utilisation :**
- "Montre-moi mes 10 derniers emails"
- "Cherche les emails de jean.dupont@totalenergies.com"
- "Trouve les emails avec 'budget Q2' dans l'objet"
- "Lis l'email sur la réunion de demain"
- "Liste mes dossiers de messagerie"
- "Montre-moi mes emails non lus"

## Workflow typique

1. **(Première fois)** "Connecte-toi à Outlook"
   → Page MCAS → clic automatique → page Microsoft login
   → vous vous authentifiez → MFA → confirmation
2. "Montre mes emails récents" → liste des 20 derniers emails
3. "Cherche les emails sur [sujet]" → résultats de recherche KQL
4. "Lis cet email" → contenu complet structuré

La session reste active plusieurs heures. Pas besoin de se reconnecter à chaque requête.

## Architecture technique

| Élément | Valeur |
|---------|--------|
| URL d'entrée | `https://outlook.cloud.microsoft.mcas.ms/mail/` |
| Proxy sécurité | Microsoft Defender for Cloud Apps (MCAS) |
| URL finale | `https://outlook.cloud.microsoft/mail/` |
| Authentification | OAuth 2.0 PKCE via Entra ID (Microsoft Identity Platform) |
| API principale | Microsoft Graph v1.0 (`https://graph.microsoft.com/v1.0/me/`) |
| API fallback | OWA Service (`https://outlook.cloud.microsoft/owa/service.svc`) |
| Token | MSAL.js dans `sessionStorage` (Bearer) ou cookies de session |
