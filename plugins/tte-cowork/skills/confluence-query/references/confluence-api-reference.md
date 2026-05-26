# Référence API Confluence TDF

## Base URL

```
https://tdf.atlassian.net/wiki/rest/api/
```

## Cloud ID

```
23cadbe4-5ee9-46f7-8a55-f7ac9c44041a
```

## Authentification

Toutes les requêtes passent par `browser_evaluate` avec `credentials: 'include'`.
Aucun header Authorization manuel n'est requis.

---

## Endpoints principaux

### Utilisateur courant
```
GET /user/current
```
Retourne : `accountId`, `displayName`, `email`, `profilePicture`

### Espaces
```
GET /space?limit=50&type=global&status=current
```
Paramètres :
- `type` : `global` (espaces publics) | `personal` (espaces personnels)
- `status` : `current` | `archived`
- `limit` : max 250
- `start` : pagination (offset)

### Recherche CQL
```
GET /content/search?cql=<CQL>&limit=10&expand=space,version
```

Exemples de requêtes CQL :
```
text~"kubernetes"                          -- contient le mot
title="Guide de déploiement"              -- titre exact
space="DP" AND text~"cloud"              -- dans un espace spécifique
type=page AND label="architecture"        -- par label
creator=currentUser()                     -- mes pages
lastmodified >= "2026-01-01"             -- modifiées récemment
space="DP" ORDER BY lastmodified DESC    -- plus récentes d'abord
```

### Pages d'un espace
```
GET /content?spaceKey=<KEY>&type=page&status=current&limit=20&orderby=modified+desc&expand=version
```

### Contenu d'une page
```
GET /content/<pageId>?expand=body.view,version,space,ancestors
```
- `body.view` : HTML rendu (plus lisible que `body.storage`)
- `body.storage` : format wiki brut (Confluence XML)
- `ancestors` : fil d'Ariane hiérarchique

### Recherche par titre exact
```
GET /content/search?cql=title="<titre>" AND type=page&limit=5
```

### Enfants d'une page (sous-pages)
```
GET /content/<pageId>/child/page?limit=50&expand=version
```

### Attachements d'une page
```
GET /content/<pageId>/child/attachment?limit=20
```

---

## Pagination

Toutes les listes sont paginées. La réponse contient :
- `size` : nombre de résultats dans la page courante
- `totalSize` : total (pour `/content/search` seulement)
- `_links.next` : URL de la page suivante (si elle existe)

Pour itérer, utilise le paramètre `start` (offset).

---

## Clés d'espaces TDF connus

| Clé | Nom |
|-----|-----|
| `DP` | Digital Platforms |
| `DI` | Deploy IT |
| `DS2` | Design System 2 |
| `MSNURSERY` | DIT_MS |
| `ESD` | EP SDR DrillX |
| `PA` | Plateau AiO |
| `RCSnR` | RC - Scale and Run |
| `BeMo` | BeMo |
| `SDRGRP` | DIT_GRP |
| `TMP` | DIT - MS |

---

## Limites

- Max 250 résultats par requête (paramètre `limit`)
- Contenu textuel tronqué à 5 000 caractères dans le skill (pour la lisibilité)
- Timeout implicite des cookies de session : plusieurs heures
