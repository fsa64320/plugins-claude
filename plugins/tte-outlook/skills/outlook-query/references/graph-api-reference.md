# Référence API — Outlook TotalEnergies

## Microsoft Graph API v1.0

Base URL : `https://graph.microsoft.com/v1.0/me/`

Toutes les requêtes se font via `browser_evaluate` avec `credentials: 'include'`
ou avec un `Bearer` token extrait du `sessionStorage` MSAL.

---

## Endpoints Messages

### Lister les messages
```
GET /messages
  ?$top=20
  &$orderby=receivedDateTime desc
  &$select=id,subject,from,receivedDateTime,isRead,bodyPreview
```

### Lire un message
```
GET /messages/{id}
  ?$select=id,subject,from,toRecipients,ccRecipients,receivedDateTime,body
```

### Rechercher (KQL)
```
GET /messages?$search="<query>"&$top=15
```

Syntaxe KQL supportée :
| Filtre | Exemple |
|--------|---------|
| Mot-clé libre | `"compte rendu"` |
| Expéditeur | `"from:jean.dupont@totalenergies.com"` |
| Objet | `"subject:réunion"` |
| Corps | `"body:budget"` |
| Non-lus | `"isRead:false"` |
| Date | `"received>=2026-05-01"` |

### Messages non lus seulement
```
GET /messages?$filter=isRead eq false&$top=20&$orderby=receivedDateTime desc
```

### Messages d'un dossier spécifique
```
GET /mailFolders/{folderId}/messages?$top=20&$orderby=receivedDateTime desc
```

### Pièces jointes d'un message
```
GET /messages/{id}/attachments
  ?$select=id,name,contentType,size
```

---

## Endpoints Dossiers

### Lister les dossiers
```
GET /mailFolders?$top=50&$select=id,displayName,totalItemCount,unreadItemCount
```

### Sous-dossiers
```
GET /mailFolders/{id}/childFolders
```

### IDs des dossiers standards
| Dossier | Alias |
|---------|-------|
| Boîte de réception | `inbox` |
| Éléments envoyés | `sentitems` |
| Brouillons | `drafts` |
| Éléments supprimés | `deleteditems` |
| Courrier indésirable | `junkemail` |

Utilisation : `GET /mailFolders/inbox/messages`

---

## Récupération du token MSAL

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

## API OWA Interne (fallback si Graph bloqué par CORS/MCAS)

Si `graph.microsoft.com` est inaccessible depuis le contexte Playwright,
utiliser l'API OWA interne d'Outlook Web App.

Base URL : `https://outlook.cloud.microsoft/owa/service.svc`

### Récupérer le canary token (obligatoire)
```javascript
() => document.cookie
  .split('; ')
  .find(c => c.startsWith('X-OWA-CANARY='))
  ?.split('=')[1]
```

### Exemple de requête OWA (FindItem)
```javascript
async (canaryToken) => {
  const resp = await fetch('https://outlook.cloud.microsoft/owa/service.svc', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json; charset=UTF-8',
      'Action': 'FindItem',
      'X-OWA-CANARY': canaryToken,
      'X-Req-Source': 'Mail'
    },
    body: JSON.stringify({
      __type: 'FindItemRequest:#Exchange',
      ItemShape: { __type: 'ItemResponseShape:#Exchange', BaseShape: 'IdOnly',
        AdditionalProperties: [
          { __type: 'PropertyUri:#Exchange', FieldURI: 'Subject' },
          { __type: 'PropertyUri:#Exchange', FieldURI: 'DateTimeReceived' },
          { __type: 'PropertyUri:#Exchange', FieldURI: 'From' },
          { __type: 'PropertyUri:#Exchange', FieldURI: 'IsRead' }
        ]
      },
      ParentFolderIds: [{ __type: 'DistinguishedFolderId:#Exchange', Id: 'inbox' }],
      Traversal: 'Shallow',
      Paging: { __type: 'IndexedPageView:#Exchange', BasePoint: 'Beginning',
        Offset: 0, MaxEntriesReturned: 20 }
    })
  });
  return resp.json();
}
```

---

## Pagination Graph API

Toutes les listes supportent `$top` (max 1000) et `$skip` pour paginer.
La réponse contient `@odata.nextLink` si d'autres résultats existent.

```javascript
// Exemple de pagination
let url = 'https://graph.microsoft.com/v1.0/me/messages?$top=50';
const allMessages = [];
while (url) {
  const resp = await fetch(url, { credentials: 'include' });
  const data = await resp.json();
  allMessages.push(...(data.value || []));
  url = data['@odata.nextLink'];
}
```
