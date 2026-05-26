---
name: teams-query
description: >
  Use this skill when the user wants to retrieve data from Microsoft Teams TotalEnergies:
  list teams, list channels, read channel messages, read direct messages (chats), or search messages.
  Triggers on phrases like: "liste mes équipes Teams", "montre-moi mes conversations Teams",
  "lis les messages du canal", "cherche dans Teams", "qu'est-ce qu'il y a dans le canal",
  "montre-moi les messages de [personne] sur Teams", "lis mes chats Teams",
  "cherche le message sur [sujet] dans Teams", "quels sont les derniers messages dans [canal]",
  "liste les canaux de [équipe]", "accède à Teams", "ouvre le canal [nom]".
  Requires an active Playwright session on teams.microsoft.com
  (use teams-connect skill first if not already authenticated).
tools:
  - mcp__plugin_playwright_playwright__browser_evaluate
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_take_screenshot
  - mcp__plugin_playwright_playwright__browser_click
  - mcp__plugin_playwright_playwright__browser_wait_for
  - mcp__plugin_playwright_playwright__browser_snapshot
---

# Skill : Requêtes Microsoft Teams TotalEnergies

Ce skill interroge Teams via scraping DOM depuis le contexte Playwright authentifié.
Il couvre 4 opérations.

**Prérequis** : une session Playwright active sur `teams.microsoft.com`.
Si ce n'est pas le cas, lance d'abord le skill `teams-connect`.

---

## Contrainte MCAS

> ⚠️ Comme pour Outlook, le proxy MCAS bloque les appels `fetch()` vers `graph.microsoft.com`.
> **Méthode principale : scraping DOM** — Teams Web App rend tout son contenu en React dans le DOM.
> **Méthode secondaire : screenshot** — si le DOM est insuffisant, analyse visuelle.

---

## Opération 1 — Lister les équipes et canaux

**Déclencheur** : l'utilisateur veut voir ses équipes, ses canaux.

### 1a. Naviguer vers Teams si nécessaire

Vérifie d'abord l'URL courante. Si l'on n'est pas sur Teams, navigue vers `https://teams.microsoft.com/`.

### 1b. Extraire les équipes du DOM

```javascript
() => {
  // Équipes dans la barre latérale
  const teamItems = document.querySelectorAll(
    '[data-tid="team-channel-list-item"], [class*="teamItem"], [role="treeitem"]'
  );
  const teams = [];
  teamItems.forEach((el, i) => {
    if (i >= 30) return;
    const text = el.innerText?.replace(/\n+/g, ' | ').substring(0, 150) || '';
    if (!text.trim()) return;
    // Canaux enfants de cette équipe
    const channels = [];
    el.querySelectorAll('[data-tid*="channel"], [class*="channel"]').forEach(ch => {
      const chText = ch.innerText?.trim();
      if (chText) channels.push(chText.substring(0, 80));
    });
    teams.push({ index: i + 1, text, channels });
  });

  // Fallback : lire tout le panneau latéral
  const sidebar = document.querySelector('[data-tid="app-layout-left-rail"], nav[aria-label]');
  const sidebarText = sidebar ? sidebar.innerText.substring(0, 3000) : '';

  return { count: teamItems.length, teams, sidebarText };
}
```

Si le DOM ne retourne rien, prends un screenshot pour analyser visuellement la liste des équipes.

Formate en tableau markdown : **Équipe**, **Canaux disponibles**.

---

## Opération 2 — Lire les messages d'un canal

**Déclencheur** : l'utilisateur veut lire les messages d'un canal précis.

### 2a. Naviguer vers le canal

Si l'utilisateur donne un nom d'équipe et de canal :
1. Clique sur l'équipe dans la barre latérale (target: texte de l'équipe)
2. Attends l'affichage des canaux
3. Clique sur le canal cible

Si l'utilisateur donne une URL Teams directe (`teams.microsoft.com/l/channel/...`), navigue directement.

### 2b. Extraire les messages du DOM

```javascript
() => {
  // Messages dans le fil du canal
  const messageEls = document.querySelectorAll(
    '[data-tid="messageBody"], [class*="message-body"], [class*="messageBody"], ' +
    '[class*="ts-message"], [data-scroll-id]'
  );
  const messages = [];

  messageEls.forEach((el, i) => {
    if (i >= 30) return;
    const text = el.innerText?.replace(/\n+/g, ' | ').trim() || '';
    if (!text || text.length < 5) return;

    // Chercher l'auteur et la date dans les éléments parents/frères
    const container = el.closest('[class*="message"]') || el.parentElement;
    const authorEl = container?.querySelector('[class*="author"], [data-tid*="author"], [class*="displayName"]');
    const timeEl = container?.querySelector('time, [class*="timestamp"], [datetime]');

    messages.push({
      index: i + 1,
      author: authorEl?.innerText?.trim() || '?',
      time: timeEl?.getAttribute('datetime') || timeEl?.innerText?.trim() || '',
      text: text.substring(0, 400)
    });
  });

  // Fallback : texte brut de la zone de messages
  const threadEl = document.querySelector(
    '[data-tid="message-list"], [class*="threadSection"], [class*="channel-thread"]'
  );
  const rawText = threadEl ? threadEl.innerText.substring(0, 5000) : '';

  return { count: messageEls.length, messages, rawText };
}
```

Formate en tableau markdown : **Auteur**, **Heure**, **Message** (tronqué à 200 car.).
Si rawText est plus riche que messages, utilise rawText pour présenter les échanges.

---

## Opération 3 — Lire les conversations directes (Chats)

**Déclencheur** : l'utilisateur veut voir ses DMs, ses chats, ses messages directs.

### 3a. Naviguer vers la section Chats

Clique sur l'icône "Chat" dans la barre de navigation gauche :
```javascript
() => {
  // Bouton Chat dans la nav latérale
  const chatBtn = document.querySelector(
    '[data-tid="app-bar-chat"], [aria-label*="Chat"], [aria-label*="Conversation"]'
  );
  if (chatBtn) { chatBtn.click(); return 'clicked'; }
  return 'not-found';
}
```

Si le JS ne fonctionne pas, utilise `browser_click` avec target: `[aria-label="Chat"]` ou `[data-tid="app-bar-chat"]`.

### 3b. Extraire la liste des chats

```javascript
() => {
  // Liste des conversations dans le panneau gauche
  const chatItems = document.querySelectorAll(
    '[data-tid="chat-list-item"], [class*="chatListItem"], [class*="chat-list-item"]'
  );
  const chats = [];

  chatItems.forEach((el, i) => {
    if (i >= 25) return;
    const fullText = el.innerText?.replace(/\n+/g, ' | ').trim() || '';
    if (!fullText) return;
    const isUnread = el.getAttribute('aria-label')?.includes('non lu')
      || el.querySelector('[class*="unread"], [class*="badge"]') !== null;
    chats.push({
      index: i + 1,
      text: fullText.substring(0, 200),
      isUnread
    });
  });

  const listEl = document.querySelector('[data-tid="chat-list"], [aria-label*="liste"]');
  const rawList = listEl ? listEl.innerText.substring(0, 3000) : '';

  return { count: chatItems.length, chats, rawList };
}
```

Formate en tableau markdown : **Interlocuteur(s)**, **Dernier message**, **Date**, 🔵 si non lu.

### 3c. Lire les messages d'un chat spécifique

Si l'utilisateur veut lire un chat particulier, clique dessus puis applique le même extracteur que l'Opération 2.

---

## Opération 4 — Rechercher dans Teams

**Déclencheur** : l'utilisateur cherche un message, une conversation, un fichier par mot-clé.

### 4a. Ouvrir la recherche

```javascript
() => {
  const searchBtn = document.querySelector(
    '[data-tid="app-bar-search"], [aria-label*="Rechercher"], input[placeholder*="Rechercher"]'
  );
  if (searchBtn) { searchBtn.click(); return 'clicked'; }
  return 'not-found';
}
```

### 4b. Taper le terme de recherche

Utilise `browser_click` sur le champ de recherche puis `browser_type` pour saisir le terme.
Attends les résultats avec `browser_wait_for` (quelques secondes).

### 4c. Extraire les résultats

```javascript
() => {
  // Résultats de recherche
  const results = document.querySelectorAll(
    '[data-tid="search-result-item"], [class*="searchResult"], [class*="search-result"]'
  );
  const items = [];

  results.forEach((el, i) => {
    if (i >= 20) return;
    const text = el.innerText?.replace(/\n+/g, ' | ').trim() || '';
    if (!text) return;
    items.push({ index: i + 1, text: text.substring(0, 300) });
  });

  // Fallback : lire la zone de résultats complète
  const resultsZone = document.querySelector(
    '[data-tid="search-results"], [class*="searchResults"], [aria-label*="résultats"]'
  );
  const rawResults = resultsZone ? resultsZone.innerText.substring(0, 4000) : '';

  return { count: results.length, items, rawResults };
}
```

Présente les résultats groupés par type (Messages, Personnes, Fichiers) si distinguables.

---

## Gestion des erreurs

- **DOM vide / sélecteurs non trouvés** : Teams peut changer sa structure HTML. Prends un screenshot
  et analyse visuellement. Essaie des sélecteurs alternatifs (`[role="listitem"]`, `[role="article"]`).
- **Page de chargement** : attends que Teams soit pleinement chargé avant d'extraire (icône de chargement absente).
- **MCAS bloque la navigation** : utilise `browser_click` sur le bouton "Passer à teams.microsoft.com".
- **Session expirée** : page de login visible → relance `teams-connect`.

## Références

- Voir `references/graph-api-reference.md` pour les endpoints Graph Teams (fallback si MCAS lève la restriction)
