# Contexte d'authentification — Outlook TotalEnergies

## Instance

| Paramètre | Valeur |
|-----------|--------|
| URL d'entrée | `https://outlook.cloud.microsoft.mcas.ms/mail/` |
| URL finale après auth | `https://outlook.cloud.microsoft/mail/` |
| Proxy sécurité | Microsoft Defender for Cloud Apps (MCAS) |
| IdP | Microsoft Entra ID (`login.microsoftonline.com`) |
| Client ID OAuth | `9199bf20-a13f-4107-85dc-02114787ef48` |
| Scope OAuth | `https://outlook.office.com/.default openid profile offline_access` |
| MFA | Activé (Microsoft Authenticator ou TOTP) |

## Flux de navigation détaillé

```
1. GET https://outlook.cloud.microsoft.mcas.ms/mail/
   → Redirection MCAS vers mcas-proxyweb.mcas.ms/certificate-checker
   
2. Page MCAS : "Notification de redirection"
   → Clic sur "Passer à outlook.cloud.microsoft"
   
3. Redirection OAuth vers login.microsoftonline.com
   → response_type=code, code_challenge (PKCE)
   → Saisie email @totalenergies.com
   → Redirection vers Entra ID TotalEnergies (SSO)
   → MFA (Microsoft Authenticator)
   
4. Retour vers https://outlook.cloud.microsoft/mail/
   → Fragment #access_token=... dans l'URL (MSAL.js)
   → Outlook charge la boîte de réception
```

## Session Playwright

- Le token d'accès est géré par **MSAL.js** (Microsoft Authentication Library) côté client
- Stocké dans `sessionStorage` sous des clés préfixées `msal.` 
- Les cookies de session (`X-OWA-CANARY`, etc.) sont HttpOnly
- La session reste active plusieurs heures (refresh token automatique par MSAL.js)

## Accès à l'API Graph depuis le navigateur

L'API Graph (`https://graph.microsoft.com/v1.0/`) peut être appelée depuis le contexte
Playwright via `fetch()` avec `credentials: 'include'`. Si CORS bloque, utiliser l'API
OWA interne à la place.

### Récupération du token MSAL depuis sessionStorage

```javascript
() => {
  const keys = Object.keys(sessionStorage);
  const tokenKey = keys.find(k => k.includes('accesstoken') && k.includes('graph'));
  if (tokenKey) {
    const item = JSON.parse(sessionStorage.getItem(tokenKey));
    return item.secret; // Bearer token
  }
  return null;
}
```

### API OWA interne (fallback si Graph bloqué)

Base : `https://outlook.cloud.microsoft/owa/service.svc`
Header requis : `action: <OperationName>`, `X-OWA-CANARY: <cookie value>`
