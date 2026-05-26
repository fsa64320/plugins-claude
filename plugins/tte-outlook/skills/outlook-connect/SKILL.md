---
name: outlook-connect
description: >
  Use this skill when the user wants to connect to or authenticate on Outlook TotalEnergies.
  Triggers on phrases like: "connecte-toi à Outlook", "ouvre Outlook", "authentifie-toi sur Outlook",
  "lance Outlook", "démarre la session Outlook", "vérifie si tu es connecté à Outlook",
  "ouvre ma messagerie", "accède à mes emails TotalEnergies".
  Also use as the first step before any outlook-query operation if the Playwright session
  is not yet open on outlook.cloud.microsoft.
tools:
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_take_screenshot
  - mcp__plugin_playwright_playwright__browser_click
  - mcp__plugin_playwright_playwright__browser_evaluate
  - mcp__plugin_playwright_playwright__browser_wait_for
  - mcp__plugin_playwright_playwright__browser_snapshot
---

# Skill : Connexion à Outlook TotalEnergies

Ce skill ouvre une session Playwright sur Outlook TotalEnergies en gérant le proxy MCAS
et l'authentification OAuth Entra ID.

## Étape 1 — Naviguer vers Outlook

Appelle `browser_navigate` avec l'URL `https://outlook.cloud.microsoft.mcas.ms/mail/`.

## Étape 2 — Gérer la page MCAS (proxy Microsoft Defender)

Prends un screenshot (`browser_take_screenshot`) et analyse la page :

- **Page "Notification de redirection"** (MCAS) : titre "Notification de redirection",
  bouton "Passer à outlook.cloud.microsoft".
  → Clique sur ce lien avec `browser_click` (target: `a:has-text("Passer à outlook.cloud.microsoft")`).
- **Page de connexion Microsoft** (`login.microsoftonline.com`) : champ email Microsoft.
  → Continue à l'étape 3.
- **Outlook déjà chargé** (`outlook.cloud.microsoft/mail/`) : boîte de réception visible.
  → Passe directement à l'étape 4.

## Étape 3 — Authentification par l'utilisateur

Informe l'utilisateur en langage clair :

> "Le navigateur est ouvert sur la page de connexion Microsoft. **Merci de vous authentifier**
> avec votre adresse TotalEnergies (ex: prenom.nom@totalenergies.com) et de valider le MFA Entra ID.
> Dites-moi quand vous avez terminé."

Attends la confirmation de l'utilisateur avec `browser_wait_for` (text: "Boîte de réception", time: 120).

Si le délai expire, prends un nouveau screenshot et redemande confirmation.

## Étape 4 — Vérification finale

Une fois Outlook chargé, vérifie la connexion via l'API Graph :

```javascript
async () => {
  const resp = await fetch('https://graph.microsoft.com/v1.0/me', {
    credentials: 'include'
  });
  if (!resp.ok) {
    // Fallback : chercher les infos dans le DOM Outlook
    const name = document.querySelector('[aria-label*="Photo de profil"]')?.getAttribute('aria-label')
      || document.title;
    return { connected: true, displayName: name, source: 'dom' };
  }
  const me = await resp.json();
  return {
    connected: true,
    displayName: me.displayName,
    email: me.mail || me.userPrincipalName,
    source: 'graph'
  };
}
```

Exécute ce code via `browser_evaluate`. Si l'API Graph répond, affiche les infos de l'utilisateur.
Si elle ne répond pas (CORS ou MCAS), confirme simplement via le DOM que la boîte mail est chargée.

## Étape 5 — Rapport à l'utilisateur

Confirme la connexion avec un message du type :

> "✅ Connecté à Outlook TotalEnergies en tant que **[Prénom Nom]** ([email]).
> La session est active et prête pour les requêtes."

## Références

- Voir `references/auth-context.md` pour les détails techniques du flux MCAS + Entra ID
