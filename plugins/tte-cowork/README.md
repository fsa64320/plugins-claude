# Confluence TDF Plugin

> ⚠️ **Prérequis obligatoire** : ce plugin nécessite le **plugin Playwright** pour fonctionner.  
> Installez-le dans Claude Cowork avant d'utiliser ce plugin.

Plugin Claude Cowork pour interagir avec l'instance Confluence de TotalEnergies Digital Factory (`tdf.atlassian.net`).

## Ce que fait ce plugin

- **Se connecter** à Confluence via votre compte TotalEnergies (OAuth Entra ID + MFA)
- **Lister** tous les espaces Confluence accessibles
- **Rechercher** des pages par mot-clé ou requête CQL
- **Lire** le contenu textuel d'une page
- **Lister** les pages récemment modifiées dans un espace

## Prérequis

Ce plugin nécessite le **plugin Playwright** installé dans Claude Cowork.  
Le plugin Playwright fournit les outils `mcp__plugin_playwright_playwright__*` utilisés pour piloter le navigateur.

## Skills

### `confluence-connect`
Ouvre une session Playwright sur Confluence et gère l'authentification OAuth.

**Exemples d'utilisation :**
- "Connecte-toi à Confluence"
- "Ouvre Confluence TDF"
- "Vérifie si tu es connecté à Confluence"

### `confluence-query`
Interroge l'API Confluence une fois la session active.

**Exemples d'utilisation :**
- "Liste les espaces Confluence"
- "Cherche les pages sur Kubernetes dans l'espace Digital Platforms"
- "Lis la page intitulée Guide de déploiement"
- "Montre-moi les 20 dernières pages modifiées dans l'espace DP"
- "Trouve la documentation sur l'architecture Cloud"

## Workflow typique

1. **(Première fois)** "Connecte-toi à Confluence" → le navigateur s'ouvre → vous vous authentifiez → confirmation
2. "Liste les espaces" → tableau des espaces disponibles
3. "Cherche les pages sur [sujet]" → liste de résultats cliquables
4. "Lis la page [titre]" → contenu textuel extrait

La session reste active plusieurs heures. Pas besoin de se reconnecter à chaque requête.

## Architecture technique

- **Authentification** : cookies HttpOnly via session Playwright (pas de token à stocker)
- **API** : Confluence REST v1 (`/wiki/rest/api/`)
- **Cloud ID** : `23cadbe4-5ee9-46f7-8a55-f7ac9c44041a`
- **Instance** : `https://tdf.atlassian.net`
