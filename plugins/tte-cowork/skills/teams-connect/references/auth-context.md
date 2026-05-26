# Contexte d'authentification — Teams TotalEnergies

## Instance

| Paramètre | Valeur |
|-----------|--------|
| URL d'entrée | `https://teams.microsoft.com.mcas.ms/` |
| URL finale après auth | `https://teams.microsoft.com/` |
| Proxy sécurité | Microsoft Defender for Cloud Apps (MCAS) |
| IdP | Microsoft Entra ID (`login.microsoftonline.com`) |
| Scope OAuth | `https://teams.microsoft.com/.default openid profile offline_access` |
| MFA | Activé (Microsoft Authenticator ou TOTP) |

## Flux de navigation détaillé

```
1. GET https://teams.microsoft.com.mcas.ms/
   → Redirection MCAS vers mcas-proxyweb.mcas.ms/certificate-checker

2. Page MCAS : "Notification de redirection"
   → Clic sur "Passer à teams.microsoft.com"

3. Redirection OAuth vers login.microsoftonline.com
   → Saisie email @totalenergies.com
   → Redirection vers Entra ID TotalEnergies (SSO)
   → MFA (Microsoft Authenticator)

4. Retour vers https://teams.microsoft.com/
   → Teams charge l'interface (équipes, canaux, conversations)
```

## Session Playwright

- Le token d'accès est géré par MSAL.js côté client
- Stocké dans `sessionStorage` sous des clés préfixées `msal.`
- Même contrainte que pour Outlook : MCAS bloque les appels `fetch()` vers `graph.microsoft.com`
- Utiliser le scraping DOM comme méthode principale

## Structure DOM de Microsoft Teams Web

Teams Web rend son interface en React. Sélecteurs utiles :

| Élément | Sélecteur |
|---------|-----------|
| Liste des équipes | `[data-tid="team-channel-list"]`, `[role="tree"]` |
| Item d'équipe | `[data-tid="team-channel-list-item"]` |
| Liste des canaux | `[data-tid="channel-list"]` |
| Messages d'un canal | `[data-tid="message-list"]`, `[class*="ts-message-list"]` |
| Item de message | `[data-tid="messageBody"]`, `[class*="message-body"]` |
| Liste des chats | `[data-tid="chat-list"]` |
| Item de chat | `[data-tid="chat-list-item"]` |
| Champ de recherche | `[data-tid="app-bar-search"]`, `input[placeholder*="Rechercher"]` |

## Accès à l'API Graph depuis le navigateur

Même contrainte que pour Outlook : MCAS bloque `fetch()` vers `graph.microsoft.com` via le wrapper JS `inline.cdn.mcas.ms`.

**Méthode principale : scraping DOM**
Teams Web App rend tout en React dans le DOM — messages, équipes, canaux, chats.

**Méthode secondaire : screenshot + analyse visuelle**
Si le DOM est insuffisant, prendre un screenshot et analyser visuellement.
