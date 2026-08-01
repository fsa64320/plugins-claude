# Publication sur GitHub

Publication du skill validé dans `skills/<nom>/` d'un repo existant, via le connecteur MCP GitHub. Pas de `git` local, pas de token manipulé en clair.

## Avant tout : trouver les outils

Les outils MCP GitHub sont souvent différés (leur schéma n'est pas chargé au démarrage). Charge-les d'un coup :

```
ToolSearch { query: "+github", max_results: 30 }
```

Puis repère les capacités dont tu as besoin — les noms exacts varient selon le serveur MCP installé, ne les devine pas :

| Besoin | Outil typique |
|---|---|
| Vérifier l'accès au repo | `get_repository`, `search_repositories` |
| Lister / lire un fichier existant | `get_file_contents` |
| Créer une branche | `create_branch` |
| Écrire un ou plusieurs fichiers | `create_or_update_file`, `push_files` |
| Ouvrir une pull request | `create_pull_request` |

Si `ToolSearch` ne renvoie rien, le connecteur GitHub n'est pas connecté ou pas autorisé. Dis-le à l'utilisateur et indique-lui de l'autoriser dans ses réglages de connecteurs — tu ne peux pas lancer le flux OAuth depuis une session non interactive. N'essaie pas de contourner par `curl`, `git` en shell, ou une bibliothèque HTTP : c'est explicitement hors périmètre, et le sandbox n'a de toute façon pas les identifiants.

Fais cette vérification en **phase 0**, pas au moment de publier. Un connecteur manquant découvert après l'évaluation fait perdre tout le travail de la session.

---

## Séquence

### 1. Reconnaissance du repo

Lis le repo cible pour connaître sa branche par défaut, puis vérifie si `skills/<nom>/SKILL.md` existe déjà.

- **Absent** → création classique.
- **Présent** → c'est une mise à jour. Récupère le `sha` de chaque fichier que tu vas écraser : la plupart des outils MCP le réclament pour modifier un fichier existant, et l'omettre provoque une erreur de conflit. Signale aussi à l'utilisateur qu'il s'agit d'un remplacement, avec un aperçu de ce qui change.

Si le repo contient un `.claude-plugin/marketplace.json` ou un index des skills, il faudra probablement y ajouter une entrée. Regarde comment les skills existants y sont déclarés et suis la même convention plutôt que d'inventer un format.

### 2. Branche dédiée

Crée `skill/<nom>` (ou `skill/<nom>-update` pour une mise à jour) depuis la branche par défaut. Ne travaille jamais directement sur `main`, même en mode `direct_commit` — une branche coûte peu et rend le retour en arrière trivial.

### 3. Confirmation — étape obligatoire

Avant d'écrire quoi que ce soit, présente à l'utilisateur :

- le repo et la branche cibles
- la liste complète des fichiers qui seront committés, avec leur taille
- le score global d'évaluation et le verdict du garde-fou
- s'il s'agit d'un remplacement, ce qui sera écrasé

Attends un accord clair. Un accord vaut pour cette publication, pas pour les suivantes : si l'utilisateur enchaîne sur un deuxième skill, redemande.

### 4. Commit

Contenu à committer :

```
skills/<nom>/SKILL.md
skills/<nom>/scripts/…
skills/<nom>/references/…
skills/<nom>/assets/…
skills/<nom>/EVALUATION.md      ← rapport.md renommé
skills/<nom>/evaluation.json    ← score.json
```

Joindre le rapport d'évaluation au commit n'est pas de la décoration : c'est ce qui permet à quelqu'un d'autre — ou à toi dans six mois — de savoir sur quoi ce skill a été validé et avec quel jeu de test.

Si un outil de type `push_files` permet d'écrire plusieurs fichiers en un seul commit, préfère-le : un commit atomique laisse un historique lisible, alors que fichier par fichier produit une dizaine de commits sans intérêt.

Message de commit :

```
feat(skills): ajoute <nom> — score d'évaluation 0.87

<une phrase sur ce que fait le skill>

Évaluation : structure 0.90 · déclenchement 0.85 · qualité 0.87
Baseline sans skill : 0.41 (écart +0.46)
```

Si l'utilisateur a demandé à publier malgré un score insuffisant, écris-le dans le message — `score 0.72 sous le seuil de 0.80, publié sur décision explicite`. La trace doit vivre dans le dépôt, pas seulement dans la conversation.

### À ne jamais committer

- jetons, clés, identifiants sous quelque forme que ce soit
- chemins absolus de la machine de l'utilisateur (`/Users/…`)
- transcriptions d'évaluation contenant des données personnelles ou professionnelles réelles — anonymise ou exclus
- fichiers volumineux (plus de quelques centaines de Ko) sans prévenir l'utilisateur

`validate_skill.py` détecte les deux premiers, mais il ne lit pas les transcriptions et n'a pas de jugement sur ce qui est confidentiel. Cette responsabilité reste la tienne.

### 5. Pull request

En mode `pull_request` (recommandé), ouvre la PR de `skill/<nom>` vers la branche par défaut. Corps de la PR :

```markdown
## <nom du skill>

<ce que fait le skill, deux ou trois phrases>

### Évaluation — score 0.87 / seuil 0.80 ✅

| Composante | Note |
|---|---|
| Structure | 0.90 |
| Déclenchement | 0.85 |
| Qualité | 0.87 |

Baseline sans skill : 0.41 · écart +0.46
Jeu de test : 20 requêtes de déclenchement, 4 cas de qualité

<points d'attention connus, limites, ce qui reste à améliorer>

Rapport complet : `skills/<nom>/EVALUATION.md`
```

Donne l'URL de la PR à l'utilisateur. Ne la merge pas toi-même : la relecture est précisément l'intérêt d'une PR.

En mode `direct_commit`, la branche est quand même créée puis fusionnée — mais annonce-le clairement et redemande confirmation, parce que le résultat atterrit sans relecture sur la branche principale.

---

## Dépannage

**« Not Found » sur le repo** — soit le nom est faux, soit le connecteur n'a pas la portée nécessaire. Fais vérifier à l'utilisateur les permissions du connecteur GitHub. Le message ne distingue pas les deux cas, par conception de l'API.

**Conflit sur un fichier existant** — le `sha` fourni est périmé ou absent. Relis le fichier pour obtenir le `sha` courant et réessaie.

**Branche déjà existante** — un skill du même nom a déjà été publié depuis une session précédente. Demande à l'utilisateur s'il veut réutiliser la branche, en ouvrir une avec un suffixe, ou abandonner.

**Protection de branche** — si la branche par défaut exige des vérifications ou des approbations, le mode `direct_commit` échouera. Bascule en `pull_request`, c'est de toute façon le comportement souhaitable.

**Le connecteur répond mais les écritures échouent** — le connecteur est probablement en lecture seule. C'est un réglage côté connecteur, l'utilisateur doit l'ajuster ; n'essaie pas d'autre voie d'écriture.
