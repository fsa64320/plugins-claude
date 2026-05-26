# Contexte d'authentification — Confluence TDF

## Instance

| Paramètre | Valeur |
|-----------|--------|
| URL | `https://tdf.atlassian.net/wiki` |
| Cloud ID | `23cadbe4-5ee9-46f7-8a55-f7ac9c44041a` |
| Organisation | TotalEnergies Digital Factory |
| IdP | Microsoft Entra ID (SSO via `login.microsoftonline.com`) |
| MFA | Activé (TOTP ou Authenticator Microsoft) |

## Flux OAuth

1. Atlassian redirige vers `id.atlassian.com`
2. Atlassian détecte le domaine `@totalenergies.com` → redirige vers Entra ID
3. L'utilisateur s'authentifie avec ses credentials TotalEnergies
4. MFA requis (TOTP ou Microsoft Authenticator)
5. Retour vers Atlassian → session cookie `cloud.session.token` (HttpOnly)

## Session Playwright

- Les cookies sont **HttpOnly** : non accessibles via `document.cookie`
- L'API Confluence REST accepte les cookies de session automatiquement via `fetch()` avec `credentials: 'include'`
- La session dure plusieurs heures (pas de timeout court)
- En cas de session expirée, Atlassian redirige vers `id.atlassian.com/login`

## API REST utilisée

Base URL : `https://tdf.atlassian.net/wiki/rest/api/`

Toutes les requêtes se font via `browser_evaluate` en injectant un `fetch()` dans le contexte du navigateur Playwright, ce qui inclut automatiquement les cookies de session.

```javascript
// Patron de requête
async () => {
  const resp = await fetch('https://tdf.atlassian.net/wiki/rest/api/<endpoint>', {
    credentials: 'include'
  });
  return await resp.json();
}
```
