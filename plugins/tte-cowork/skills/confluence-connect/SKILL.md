---
name: confluence-connect
description: >
  Use this skill when the user wants to connect to or authenticate on Confluence TDF
  (tdf.atlassian.net). Triggers on phrases like: "connecte-toi à confluence",
  "ouvre confluence", "authentifie-toi sur confluence", "lance confluence",
  "démarre la session confluence", "vérifie si tu es connecté à confluence".
  Also use this skill as the first step before any confluence-query operation
  if the Playwright session is not yet open.
tools:
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_take_screenshot
  - mcp__plugin_playwright_playwright__browser_evaluate
  - mcp__plugin_playwright_playwright__browser_wait_for
  - mcp__plugin_playwright_playwright__browser_snapshot
---

# Skill : Connexion à Confluence TDF

Ce skill ouvre une session Playwright sur `https://tdf.atlassian.net/wiki/home` et vérifie que l'utilisateur est bien authentifié via OAuth Entra ID.

## Étape 1 — Naviguer vers Confluence

Appelle `browser_navigate` avec l'URL `https://tdf.atlassian.net/wiki/home`.

## Étape 2 — Détecter l'état d'authentification

Après la navigation, prends un screenshot (`browser_take_screenshot`) et analyse l'état :

- **Déjà connecté** : la page affiche le tableau de bord Confluence (sidebar avec "Pour vous", "Espaces", avatar utilisateur). → Passe directement à l'étape 4.
- **Page de connexion Atlassian** : la page affiche "Log in with Atlassian account" ou un champ email. → Continue à l'étape 3.
- **Redirection Microsoft Entra ID** : la page affiche une interface Microsoft (login.microsoftonline.com). → Continue à l'étape 3.

## Étape 3 — Authentification par l'utilisateur

Informe l'utilisateur en langage clair :

> "Le navigateur est ouvert sur la page de connexion Confluence / Microsoft. **Merci de vous authentifier** (email TotalEnergies + MFA Entra ID). Dites-moi quand vous avez terminé."

Attends la confirmation de l'utilisateur avec `browser_wait_for` (text: "Pour vous", time: 120).

Si le délai expire, prends un nouveau screenshot et redemande confirmation.

## Étape 4 — Vérification finale

Une fois la page Confluence chargée, exécute ce JavaScript pour confirmer la connexion :

```javascript
async () => {
  const resp = await fetch('https://tdf.atlassian.net/wiki/rest/api/user/current', {
    credentials: 'include'
  });
  const user = await resp.json();
  return {
    connected: resp.ok,
    displayName: user.displayName,
    accountId: user.accountId,
    email: user.email
  };
}
```

Utilise `browser_evaluate` pour exécuter ce code et retourner le résultat à l'utilisateur.

## Étape 5 — Rapport à l'utilisateur

Confirme la connexion avec un message du type :

> "✅ Connecté à Confluence TDF en tant que **[Prénom Nom]**. La session est active et prête pour les requêtes."

Si la connexion a échoué (resp.ok === false), explique l'erreur et propose de réessayer.

## Références

- Voir `references/auth-context.md` pour les détails techniques de l'instance TDF
