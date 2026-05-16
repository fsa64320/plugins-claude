---
name: recuperer-donnees-cesu
description: Utiliser ce skill pour récupérer les données de salaire et cotisations depuis le portail CESU URSSAF. Phrases déclencheurs : "récupère mes données CESU", "scrape URSSAF", "récupère mes salaires URSSAF", "cotisations CESU", "données CESU", "bulletins URSSAF".
version: 2.0.0
allowed-tools: "Bash"
---

# Récupération des données CESU URSSAF

## Objectif

Extraire les données de salaire et cotisations depuis le portail cesu.urssaf.fr en rejouant un appel API copié depuis le navigateur de l'utilisateur. Produit un tableau Markdown structuré.

## Processus

### Étape 1 — Guider l'utilisateur pour capturer la requête API

Expliquer à l'utilisateur ce qu'il doit faire dans son navigateur :

> **Comment récupérer la requête API depuis votre navigateur :**
>
> 1. Ouvrez **cesu.urssaf.fr** dans Chrome/Safari/Firefox
> 2. Connectez-vous à votre espace
> 3. Ouvrez les **DevTools** (F12 ou Cmd+Option+I sur Mac)
> 4. Cliquez sur l'onglet **Network** (Réseau)
> 5. Cochez **XHR/Fetch** pour filtrer
> 6. Naviguez vers **"Mes déclarations"** ou **"Mes bulletins de salaire"**
> 7. Repérez la requête qui contient les données (réponse JSON avec des montants)
> 8. Clic droit sur cette requête → **"Copy as cURL"** (Copier comme cURL)
> 9. Collez le résultat ici

Si l'utilisateur ne sait pas quelle requête choisir, lui dire de chercher :
- Les requêtes dont la réponse (onglet Preview/Response) contient des montants, noms d'employés, ou dates
- Les URLs contenant "declaration", "bulletin", "salaire", "cotisation"
- La plus grosse réponse JSON (en taille)

### Étape 2 — Localiser et exécuter le script

```bash
SCRIPT=$(find ~/.claude/plugins -name "scrape_cesu.py" 2>/dev/null | head -1)
echo $SCRIPT
```

### Étape 3a — Mode curl (recommandé)

Une fois la commande curl récupérée, l'exécuter :

```bash
python3 "$SCRIPT" --curl '<COMMANDE_CURL_COPIÉE>'
```

**Important** : Encadrer la commande curl avec des guillemets simples externes pour éviter les problèmes d'échappement.

### Étape 3b — Mode fichier JSON (alternative)

Si l'utilisateur préfère sauvegarder la réponse JSON depuis DevTools (onglet Response → copier) :

```bash
python3 "$SCRIPT" --fichier /chemin/vers/reponse.json
```

### Étape 3c — Mode cookie + URL (alternative)

Si l'utilisateur fournit séparément le cookie et l'URL :

```bash
python3 "$SCRIPT" --cookie "JSESSIONID=abc123;autreC=val" --url "https://www.cesu.urssaf.fr/..."
```

### Étape 4 — Interpréter les résultats

**Cas 1 : Tableau Markdown rempli** → Présenter les résultats directement et proposer :
- Export vers Excel
- Intégration au pipeline fiscal
- Analyse par employé ou par période

**Cas 2 : "Aucune déclaration structurée extraite"** + JSON brut affiché → Le script n'a pas reconnu la structure. Analyser le JSON brut affiché et :
1. Identifier les champs contenant salaires/cotisations
2. Proposer à l'utilisateur d'adapter le parsing ou de copier une autre requête API

**Cas 3 : Erreur HTTP 401/403** → Le cookie a expiré. Demander à l'utilisateur de se reconnecter et recopier un curl frais.

## Dépendances

- `httpx` (déjà installé dans le venv du projet IFU). Sinon : `pip3 install httpx`
- Pas de Playwright, pas de navigateur automatisé

## Format de sortie

```markdown
## Données CESU URSSAF

| Employé | Période | Salaire brut | Salaire net | Cotis. patronales | Cotis. salariales | Coût employeur |
|---------|---------|:---:|:---:|:---:|:---:|:---:|
| Prénom Nom | Janvier 2025 | 1 234,56 € | 987,65 € | 432,10 € | 246,91 € | 1 666,66 € |
| **TOTAL** | — | **X €** | **Y €** | **Z €** | **W €** | **T €** |
```

## Règles importantes

- Ne jamais afficher les cookies/tokens de l'utilisateur dans la réponse
- Si le JSON brut contient des données personnelles sensibles (NIR, adresse), les masquer
- Informer l'utilisateur que la session expire (typiquement 20-30 min) — il devra recopier un curl si ça échoue
- Proposer d'itérer si la première requête copiée n'est pas la bonne
