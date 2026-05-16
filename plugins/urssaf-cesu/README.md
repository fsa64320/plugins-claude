# Plugin URSSAF CESU

Récupère automatiquement les données de salaire et cotisations depuis le portail [cesu.urssaf.fr](https://www.cesu.urssaf.fr) pour les particuliers employeurs.

## Skill disponible

### `/recuperer-donnees-cesu`

Ouvre un navigateur Chromium sur le portail CESU, attend votre connexion manuelle, puis extrait les déclarations pour tous vos employés sur la période choisie.

**Données extraites :**
- Salaire brut déclaré
- Salaire net versé
- Cotisations patronales
- Cotisations salariales
- Coût total employeur

**Sortie :** tableau Markdown consommable par d'autres skills (pipeline fiscal IFU, export Excel, etc.)

## Prérequis

- Python 3.9+
- Playwright : `pip3 install playwright && python3 -m playwright install chromium`

Le skill vérifie et installe Playwright automatiquement si absent.

## Utilisation

```
/recuperer-donnees-cesu
```

Le skill vous demandera la période souhaitée, ouvrira le navigateur, et vous guidera pour la connexion manuelle.

## Sécurité

Aucun identifiant n'est stocké. La connexion est toujours effectuée manuellement par l'utilisateur dans le navigateur.
