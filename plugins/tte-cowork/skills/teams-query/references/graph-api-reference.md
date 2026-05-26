# Référence API — Microsoft Teams TotalEnergies

## Microsoft Graph API v1.0 (fallback si MCAS non bloquant)

Base URL : `https://graph.microsoft.com/v1.0/`

> ⚠️ En contexte TotalEnergies, MCAS bloque généralement les appels `fetch()` vers Graph.
> Utiliser en priorité le scraping DOM (voir SKILL.md).
> Ces endpoints restent utiles si les restrictions MCAS évoluent.

---

## Endpoints Teams

### Lister les équipes rejointes
```
GET /me/joinedTeams
  ?$select=id,displayName,description
```

### Lister les canaux d'une équipe
```
GET /teams/{teamId}/channels
  ?$select=id,displayName,description,membershipType
```

### Lire les messages d'un canal
```
GET /teams/{teamId}/channels/{channelId}/messages
  ?$top=20
  &$orderby=createdDateTime desc
```

### Lire un message spécifique
```
GET /teams/{teamId}/channels/{channelId}/messages/{messageId}
```

### Réponses à un message (thread)
```
GET /teams/{teamId}/channels/{channelId}/messages/{messageId}/replies
```

---

## Endpoints Chats (messages directs)

### Lister les conversations directes
```
GET /me/chats
  ?$top=20
  &$expand=members
  &$select=id,topic,chatType,lastUpdatedDateTime
```

### Lire les messages d'un chat
```
GET /me/chats/{chatId}/messages
  ?$top=30
  &$orderby=createdDateTime desc
```

---

## Recherche dans Teams

### Recherche de messages via Graph Search
```javascript
async (searchQuery) => {
  const resp = await fetch('https://graph.microsoft.com/v1.0/search/query', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      requests: [{
        entityTypes: ['chatMessage'],
        query: { queryString: searchQuery },
        from: 0,
        size: 15
      }]
    })
  });
  return resp.json();
}
```

---

## Récupération du token MSAL (même méthode que Outlook)

```javascript
() => {
  const allKeys = Object.keys(sessionStorage);
  const results = [];
  allKeys.forEach(k => {
    try {
      const item = JSON.parse(sessionStorage.getItem(k));
      if (item?.credentialType === 'AccessToken' && item?.secret) {
        results.push({
          key: k,
          token: item.secret,
          expires: new Date(item.expiresOn * 1000).toISOString(),
          scopes: item.target
        });
      }
    } catch(e) {}
  });
  return results;
}
```

---

## IDs utiles

### Types de canaux (`membershipType`)
| Type | Description |
|------|-------------|
| `standard` | Canal standard (tous les membres) |
| `private` | Canal privé (membres sélectionnés) |
| `shared` | Canal partagé entre équipes |

### Types de chats (`chatType`)
| Type | Description |
|------|-------------|
| `oneOnOne` | Conversation 1:1 |
| `group` | Conversation de groupe |
| `meeting` | Chat de réunion |

---

## Structure d'un message Graph Teams

```json
{
  "id": "...",
  "createdDateTime": "2026-05-19T14:30:00Z",
  "from": {
    "user": {
      "displayName": "François VALLET",
      "id": "..."
    }
  },
  "body": {
    "contentType": "html",
    "content": "<p>Bonjour...</p>"
  },
  "attachments": [],
  "mentions": [],
  "reactions": []
}
```

---

## URLs de navigation Teams Web

| Vue | URL |
|-----|-----|
| Canal d'équipe | `https://teams.microsoft.com/l/channel/{channelId}/{channelName}?groupId={teamId}` |
| Chat 1:1 | `https://teams.microsoft.com/l/chat/{chatId}/0` |
| Réunion | `https://teams.microsoft.com/l/meetup-join/{...}` |
| Recherche | `https://teams.microsoft.com/_#/search` |
