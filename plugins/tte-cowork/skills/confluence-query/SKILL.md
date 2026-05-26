---
name: confluence-query
description: >
  Use this skill when the user wants to retrieve data from Confluence TDF:
  list spaces, search pages by keyword, read a specific page, or list recent
  pages in a space. Triggers on phrases like: "liste les espaces confluence",
  "cherche dans confluence", "recherche la page", "lis la page confluence",
  "montre-moi les pages récentes", "pages récentes de l'espace",
  "trouve la documentation sur", "recherche CQL confluence",
  "récupère le contenu de", "quelles sont les pages de l'espace".
  Requires an active Playwright session on tdf.atlassian.net
  (use confluence-connect skill first if not already authenticated).
tools:
  - mcp__plugin_playwright_playwright__browser_evaluate
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_take_screenshot
---

# Skill : Requêtes Confluence TDF

Ce skill interroge l'API REST Confluence de `tdf.atlassian.net` via `browser_evaluate` + `fetch()` depuis le contexte Playwright authentifié. Il couvre 4 opérations.

**Prérequis** : une session Playwright active sur `tdf.atlassian.net`. Si ce n'est pas le cas, lance d'abord le skill `confluence-connect`.

---

## Opération 1 — Lister les espaces

**Déclencheur** : l'utilisateur demande la liste des espaces, espaces disponibles, espaces Confluence.

Exécute via `browser_evaluate` :

```javascript
async () => {
  const resp = await fetch(
    'https://tdf.atlassian.net/wiki/rest/api/space?limit=50&type=global&status=current',
    { credentials: 'include' }
  );
  const data = await resp.json();
  return {
    total: data.size,
    spaces: data.results.map(s => ({
      key: s.key,
      name: s.name,
      url: `https://tdf.atlassian.net/wiki/spaces/${s.key}`
    }))
  };
}
```

Présente le résultat sous forme de tableau markdown avec colonnes **Clé**, **Nom**, **Lien**.

---

## Opération 2 — Rechercher des pages par mot-clé (CQL)

**Déclencheur** : l'utilisateur veut chercher une page, trouver de la documentation, rechercher un terme.

Extrais le mot-clé ou la requête CQL de la demande. Si l'utilisateur mentionne un espace, ajoute `AND space="CLÉ"` à la requête CQL.

```javascript
async (keyword, spaceKey) => {
  const cql = spaceKey
    ? `text~"${keyword}" AND space="${spaceKey}" ORDER BY lastmodified DESC`
    : `text~"${keyword}" ORDER BY lastmodified DESC`;
  const url = `https://tdf.atlassian.net/wiki/rest/api/content/search?cql=${encodeURIComponent(cql)}&limit=10&expand=space,version`;
  const resp = await fetch(url, { credentials: 'include' });
  const data = await resp.json();
  return {
    total: data.totalSize,
    results: data.results.map(p => ({
      id: p.id,
      title: p.title,
      space: p.space?.name,
      spaceKey: p.space?.key,
      lastModified: p.version?.when,
      url: `https://tdf.atlassian.net/wiki/spaces/${p.space?.key}/pages/${p.id}`
    }))
  };
}
```

Construis la fonction JavaScript avec les valeurs du mot-clé et de l'espace (si précisé), puis exécute-la via `browser_evaluate`.

Présente les résultats en liste numérotée avec titre, espace et date de modification.

---

## Opération 3 — Lire le contenu d'une page

**Déclencheur** : l'utilisateur veut lire, afficher ou résumer une page précise.

Si l'utilisateur donne un titre, commence par une recherche CQL (`title="<titre exact>"`) pour récupérer l'ID. Si l'utilisateur donne directement un ID ou une URL, extrais l'ID.

```javascript
async (pageId) => {
  const resp = await fetch(
    `https://tdf.atlassian.net/wiki/rest/api/content/${pageId}?expand=body.view,version,space,ancestors`,
    { credentials: 'include' }
  );
  const page = await resp.json();

  // Extraire le texte brut du HTML
  const html = page.body?.view?.value || '';
  const text = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();

  return {
    id: page.id,
    title: page.title,
    space: page.space?.name,
    spaceKey: page.space?.key,
    lastModified: page.version?.when,
    modifiedBy: page.version?.by?.displayName,
    url: `https://tdf.atlassian.net/wiki${page._links?.webui}`,
    contentText: text.substring(0, 5000) // limité à 5000 chars pour la lisibilité
  };
}
```

Construis la fonction avec l'ID de page et exécute-la via `browser_evaluate`.

Présente le contenu extrait de façon structurée : titre, métadonnées, puis le texte de la page. Si le contenu est long, propose un résumé.

---

## Opération 4 — Pages récentes d'un espace

**Déclencheur** : l'utilisateur demande les pages récentes, dernières modifications, activité récente d'un espace.

Demande la clé d'espace si elle n'est pas fournie (propose de lister les espaces si l'utilisateur ne connaît pas la clé).

```javascript
async (spaceKey, limit) => {
  const url = `https://tdf.atlassian.net/wiki/rest/api/content?spaceKey=${spaceKey}&type=page&status=current&limit=${limit || 20}&orderby=modified+desc&expand=version,ancestors`;
  const resp = await fetch(url, { credentials: 'include' });
  const data = await resp.json();
  return {
    space: spaceKey,
    total: data.size,
    pages: data.results.map(p => ({
      id: p.id,
      title: p.title,
      lastModified: p.version?.when,
      modifiedBy: p.version?.by?.displayName,
      url: `https://tdf.atlassian.net/wiki/spaces/${spaceKey}/pages/${p.id}`
    }))
  };
}
```

Construis la fonction avec la clé d'espace et la limite souhaitée, puis exécute-la via `browser_evaluate`.

Présente les pages sous forme de liste chronologique (du plus récent au plus ancien).

---

## Gestion des erreurs

Si `resp.ok` est `false` ou si l'API retourne une erreur :

- **401 / 403** : la session a expiré. Indique à l'utilisateur de relancer `confluence-connect` pour se réauthentifier.
- **404** : page ou espace introuvable. Propose une recherche alternative.
- **Autre** : affiche le code d'erreur et le message retourné par l'API.

## Références

- Voir `references/confluence-api-reference.md` pour la liste complète des endpoints et des paramètres CQL.
