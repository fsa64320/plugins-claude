---
name: teams-connect
description: >
  Use this skill when the user wants to connect to or authenticate on Microsoft Teams TotalEnergies.
  Triggers on phrases like: "connecte-toi à Teams", "ouvre Teams", "authentifie-toi sur Teams",
  "lance Teams", "démarre la session Teams", "vérifie si tu es connecté à Teams",
  "ouvre Microsoft Teams", "accède à Teams TotalEnergies", "ouvre mes conversations Teams".
  Also use as the first step before any teams-query operation if the Playwright session
  is not yet open on teams.microsoft.com.
tools:
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_take_screenshot
  - mcp__plugin_playwright_playwright__browser_click
  - mcp__plugin_playwright_playwright__browser_evaluate
  - mcp__plugin_playwright_playwright__browser_wait_for
  - mcp__plugin_playwright_playwright__browser_snapshot
---

# Skill : Connexion à Microsoft Teams TotalEnergies

Ce skill ouvre une session Playwright sur Microsoft Teams TotalEnergies en gérant le proxy MCAS
et l'authentification OAuth Entra ID. Le flux est identique à Outlook — même proxy, même IdP.

## Étape 1 — Naviguer vers Teams

Appelle `browser_navigate` avec l'URL `https://teams.microsoft.com.mcas.ms/`.

> Si la navigation échoue ou redirige immédiatement, essaie directement `https://teams.microsoft.com/`.

## Étape 2 — Gérer la page MCAS (proxy Microsoft Defender)

Prends un screenshot (`browser_take_screenshot`) et analyse la page :

- **Page "Notification de redirection"** (MCAS) : bouton "Passer à teams.microsoft.com".
  → Clique avec `browser_click` (target: `a:has-text("Passer à teams.microsoft.com")`).
- **Page de connexion Microsoft** (`login.microsoftonline.com`) : champ email.
  → Continue à l'étape 3.
- **Teams déjà chargé** (`teams.microsoft.com`) : interface Teams visible.
  → Passe directement à l'étape 4.

## Étape 3 — Authentification par l'utilisateur

Informe l'utilisateur en langage clair :

> "Le navigateur est ouvert sur la page de connexion Microsoft Teams. **Merci de vous authentifier**
> avec votre adresse TotalEnergies (ex: prenom.nom@totalenergies.com) et de valider le MFA.
> Dites-moi quand vous avez terminé."

Attends la confirmation de l'utilisateur. Prends un screenshot pour vérifier que Teams est chargé.

## Étape 4 — Vérification finale

Une fois Teams chargé, vérifie la connexion :

```javascript
async () => {
  // Tentative via Graph API
  const resp = await fetch('https://graph.microsoft.com/v1.0/me', {
    credentials: 'include'
  });
  if (resp.ok) {
    const me = await resp.json();
    return { connected: true, displayName: me.displayName, email: me.mail || me.userPrincipalName, source: 'graph' };
  }

  // Fallback : lecture du DOM Teams
  const nameEl = document.querySelector('[data-tid="me-control-avatar"]')
    || document.querySelector('[aria-label*="photo de profil"]')
    || document.querySelector('[class*="userDisplayName"]');
  const name = nameEl?.getAttribute('aria-label') || nameEl?.innerText || document.title;
  return { connected: true, displayName: name, source: 'dom' };
}
```

Exécute via `browser_evaluate`. Confirme la connexion avec le nom affiché.

## Étape 5 — Rapport à l'utilisateur

> "✅ Connecté à Microsoft Teams TotalEnergies en tant que **[Prénom Nom]**.
> La session est active et prête pour les requêtes."

## Références

- Voir `references/auth-context.md` pour les détails techniques du flux MCAS + Entra ID
