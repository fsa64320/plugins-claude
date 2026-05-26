---
name: outlook-query
description: >
  Use this skill when the user wants to retrieve data from their Outlook TotalEnergies mailbox:
  list emails, search emails by keyword or sender, read an email, or list mail folders.
  Triggers on phrases like: "lis mes emails", "montre-moi mes emails récents",
  "cherche les emails de", "recherche dans ma boîte mail", "lis cet email",
  "quels sont mes derniers messages", "liste mes dossiers", "emails non lus",
  "trouve l'email de", "montre-moi les emails sur", "vérifie ma boîte de réception".
  Requires an active Playwright session on outlook.cloud.microsoft
  (use outlook-connect skill first if not already authenticated).
tools:
  - mcp__plugin_playwright_playwright__browser_evaluate
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_take_screenshot
---

# Skill : Requêtes Outlook TotalEnergies

Ce skill interroge la messagerie Outlook via l'API Microsoft Graph ou l'API OWA interne,
depuis le contexte Playwright authentifié. Il couvre 4 opérations.

**Prérequis** : une session Playwright active sur `outlook.cloud.microsoft`.
Si ce n'est pas le cas, lance d'abord le skill `outlook-connect`.

---

## Stratégie d'accès API

Avant toute requête, détermine la méthode disponible via `browser_evaluate` :

```javascript
async () => {
  // Essai 1 : token MSAL dans sessionStorage → Graph API
  const keys = Object.keys(sessionStorage);
  const tokenKey = keys.find(k =>
    k.includes('accesstoken') &&
    (k.includes('graph') || k.includes('outlook'))
  );
  if (tokenKey) {
    const item = JSON.parse(sessionStorage.getItem(tokenKey));
    if (item?.secret && new Date(item.expiresOn * 1000) > new Date()) {
      return { method: 'graph-bearer', token: item.secret };
    }
  }
  // Essai 2 : fetch avec credentials (cookies de session)
  const test = await fetch('https://graph.microsoft.com/v1.0/me', { credentials: 'include' });
  if (test.ok) return { method: 'graph-cookie' };
  // Fallback : API OWA
  return { method: 'owa' };
}
```

Selon le résultat, utilise la méthode correspondante dans les opérations ci-dessous.

---

## Opération 1 — Lister les emails récents

**Déclencheur** : l'utilisateur veut voir ses emails récents, sa boîte de réception.

### Avec Graph API (méthode `graph-bearer` ou `graph-cookie`)

```javascript
async (bearerToken) => {
  const headers = bearerToken
    ? { Authorization: `Bearer ${bearerToken}` }
    : {};
  const resp = await fetch(
    'https://graph.microsoft.com/v1.0/me/messages' +
    '?$top=20&$orderby=receivedDateTime desc' +
    '&$select=id,subject,from,receivedDateTime,isRead,bodyPreview',
    { credentials: 'include', headers }
  );
  const data = await resp.json();
  return {
    total: data.value?.length,
    emails: data.value?.map(m => ({
      id: m.id,
      subject: m.subject,
      from: m.from?.emailAddress?.address,
      fromName: m.from?.emailAddress?.name,
      received: m.receivedDateTime,
      isRead: m.isRead,
      preview: m.bodyPreview?.substring(0, 100)
    }))
  };
}
```

Construis la fonction avec le token si disponible, puis exécute via `browser_evaluate`.

Présente les résultats en liste avec : expéditeur, objet, date, statut lu/non-lu, aperçu.

---

## Opération 2 — Rechercher des emails

**Déclencheur** : l'utilisateur cherche des emails par mot-clé, expéditeur, objet.

Extrais le terme de recherche et la cible (expéditeur / objet / corps) de la demande.

```javascript
async (searchQuery, bearerToken) => {
  // searchQuery ex: "réunion projet", "from:jean.dupont@totalenergies.com"
  const headers = bearerToken ? { Authorization: `Bearer ${bearerToken}` } : {};
  const encoded = encodeURIComponent(`"${searchQuery}"`);
  const resp = await fetch(
    `https://graph.microsoft.com/v1.0/me/messages?$search=${encoded}` +
    `&$top=15&$select=id,subject,from,receivedDateTime,isRead,bodyPreview`,
    { credentials: 'include', headers }
  );
  const data = await resp.json();
  return {
    query: searchQuery,
    total: data.value?.length,
    emails: data.value?.map(m => ({
      id: m.id,
      subject: m.subject,
      from: m.from?.emailAddress?.address,
      fromName: m.from?.emailAddress?.name,
      received: m.receivedDateTime,
      isRead: m.isRead,
      preview: m.bodyPreview?.substring(0, 150)
    }))
  };
}
```

**Syntaxe de recherche KQL supportée** :
- Mot-clé libre : `budget Q2`
- Par expéditeur : `from:prenom.nom@totalenergies.com`
- Par objet : `subject:compte-rendu`
- Combiné : `from:jean subject:réunion`

Construis la fonction avec la requête, exécute via `browser_evaluate`, présente les résultats.

---

## Opération 3 — Lire le contenu d'un email

**Déclencheur** : l'utilisateur veut lire un email précis (après une recherche ou par ID).

Si l'utilisateur ne donne pas d'ID, effectue d'abord une recherche (opération 2) pour
identifier l'email, puis lis son contenu.

```javascript
async (messageId, bearerToken) => {
  const headers = bearerToken ? { Authorization: `Bearer ${bearerToken}` } : {};
  const resp = await fetch(
    `https://graph.microsoft.com/v1.0/me/messages/${messageId}` +
    `?$select=id,subject,from,toRecipients,ccRecipients,receivedDateTime,body,attachments`,
    { credentials: 'include', headers }
  );
  const msg = await resp.json();

  // Extraire le texte brut du HTML
  const html = msg.body?.content || '';
  const text = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();

  return {
    id: msg.id,
    subject: msg.subject,
    from: msg.from?.emailAddress?.address,
    fromName: msg.from?.emailAddress?.name,
    to: msg.toRecipients?.map(r => r.emailAddress?.address).join(', '),
    cc: msg.ccRecipients?.map(r => r.emailAddress?.address).join(', '),
    received: msg.receivedDateTime,
    bodyText: text.substring(0, 6000)
  };
}
```

Construis la fonction avec l'ID de message, exécute via `browser_evaluate`.
Présente l'email structuré : en-têtes (De, À, CC, Date, Objet), puis corps du message.
Si le contenu est long, propose un résumé.

---

## Opération 4 — Lister les dossiers

**Déclencheur** : l'utilisateur demande la liste des dossiers, boîtes mail, catégories.

```javascript
async (bearerToken) => {
  const headers = bearerToken ? { Authorization: `Bearer ${bearerToken}` } : {};
  const resp = await fetch(
    'https://graph.microsoft.com/v1.0/me/mailFolders' +
    '?$top=50&$select=id,displayName,totalItemCount,unreadItemCount',
    { credentials: 'include', headers }
  );
  const data = await resp.json();
  return {
    folders: data.value?.map(f => ({
      id: f.id,
      name: f.displayName,
      total: f.totalItemCount,
      unread: f.unreadItemCount
    }))
  };
}
```

Présente les dossiers en tableau avec nom, total, non-lus. Propose ensuite de lister
les emails d'un dossier spécifique en ajoutant `&$filter=parentFolderId eq '<id>'`
à la requête des messages.

---

## Gestion des erreurs

- **401** : token expiré → relance `outlook-connect` pour se réauthentifier
- **403** : permission insuffisante (scope Graph manquant) → affiche le message d'erreur
- **CORS bloqué** : l'API Graph n'est pas accessible depuis ce contexte →
  tente l'API OWA interne (voir `references/graph-api-reference.md`, section "API OWA fallback")
- **Autre** : affiche le code d'erreur et `error.message` retournés par l'API

## Références

- Voir `references/graph-api-reference.md` pour la liste complète des endpoints Graph
  et l'API OWA de fallback
