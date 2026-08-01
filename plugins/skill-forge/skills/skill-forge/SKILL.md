---
name: skill-forge
description: Chaîne complète de fabrication d'un skill — concevoir, rédiger, évaluer avec des tests notés, puis publier dans le dossier skills/ d'un repo GitHub existant via le connecteur GitHub. Utilise ce skill dès que l'utilisateur veut "créer un skill", "fabriquer un skill de bout en bout", "tester et publier un skill", "pousser un skill sur GitHub", "ajouter un skill à mon repo", "évaluer mon skill avant de le livrer", ou parle d'un pipeline / d'une usine à skills. Utilise-le aussi quand il demande simplement de transformer un workflow répétitif en skill réutilisable — la publication fait partie du travail, ne t'arrête pas au SKILL.md.
---

# Skill Forge

Chaîne de fabrication d'un skill, de l'idée jusqu'au commit GitHub. Quatre phases, dans cet ordre :

1. **Concevoir & rédiger** — cadrer l'intention, écrire le SKILL.md et ses ressources
2. **Évaluer** — tests de déclenchement + tests de qualité, notés
3. **Garde-fou** — un score sous le seuil bloque la publication
4. **Publier** — commit dans `skills/<nom>/` d'un repo GitHub existant

La discipline importe ici : on publie du code que d'autres vont installer et exécuter. Un skill mal déclenché pollue le contexte de toutes les conversations ; un skill mal rédigé produit des sorties fausses à grande échelle. Le garde-fou n'est pas de la bureaucratie, c'est ce qui rend la publication automatique acceptable.

Si le skill `skill-creator` est disponible, appuie-toi sur lui pour la phase 1 (rédaction, patterns d'écriture, optimisation de description) et reviens ici pour les phases 2 à 4. Ne réinvente pas ce qu'il fait déjà.

---

## Phase 0 — Configuration

Avant de commencer, il faut savoir où publier et à quel niveau d'exigence. Lis `config.json` à la racine du workspace de travail s'il existe ; sinon demande à l'utilisateur et écris-le (modèle dans `assets/config.example.json`) :

```json
{
  "repo": "owner/nom-du-repo",
  "branch": "main",
  "skills_dir": "skills",
  "publish_mode": "pull_request",
  "threshold": 0.80,
  "weights": { "structure": 0.25, "trigger": 0.35, "quality": 0.40 }
}
```

- `publish_mode` : `pull_request` (recommandé, l'utilisateur relit avant merge) ou `direct_commit`
- `threshold` : score global minimal pour autoriser la publication, entre 0 et 1
- Ne demande pas de token GitHub. L'authentification passe par le connecteur MCP GitHub déjà configuré. Si l'utilisateur propose de coller un token, refuse et explique que la connexion se fait dans ses réglages de connecteurs.

Vérifie tout de suite que les outils GitHub MCP répondent (voir `references/github-publish.md`). Si le connecteur n'est pas connecté, dis-le maintenant plutôt qu'après trois heures de travail : l'utilisateur peut l'autoriser pendant que tu construis.

Espace de travail : `<workspace>/skill-forge/<nom-du-skill>/` avec le skill dans `skill/` et les résultats d'éval dans `evals/iteration-N/`.

---

## Phase 1 — Concevoir et rédiger

### Cadrer

Quatre questions à trancher avec l'utilisateur avant d'écrire une ligne :

1. Que doit permettre ce skill, concrètement, qu'un Claude sans skill ferait mal ?
2. Sur quelles formulations doit-il se déclencher — et sur lesquelles surtout pas ?
3. Quel format de sortie attendu ?
4. Quelles ressources embarquées : scripts, gabarits, documentation de référence ?

La question 2 est celle qu'on bâcle le plus souvent et celle qui coûte le plus cher. Fais nommer à l'utilisateur au moins deux cas voisins où le skill ne doit **pas** se déclencher — ils deviendront des cas de test négatifs en phase 2.

### Structure

```
<nom-du-skill>/
├── SKILL.md          requis — frontmatter YAML (name, description) + instructions
├── scripts/          code exécutable pour les tâches déterministes et répétées
├── references/       documentation chargée à la demande
└── assets/           fichiers utilisés dans la sortie (gabarits, icônes)
```

Le chargement est progressif : le couple nom + description est toujours en contexte, le corps du SKILL.md seulement quand le skill se déclenche, les ressources seulement quand elles sont lues. Vise moins de 500 lignes dans le corps ; au-delà, déporte vers `references/` avec des pointeurs explicites indiquant quand aller lire quoi.

### Rédiger

- **description** : c'est le mécanisme de déclenchement. Elle doit dire ce que fait le skill *et* dans quels contextes l'employer, avec des formulations proches de celles d'un vrai utilisateur. Claude a tendance à sous-déclencher les skills — sois un peu insistant ("utilise ce skill dès que…"). Toute l'information "quand l'utiliser" va dans la description, pas dans le corps.
- **corps** : impératif, et surtout explique le *pourquoi* de chaque consigne. Un modèle qui comprend l'intention gère les cas non prévus ; un modèle qui suit des MUST en capitales échoue dès qu'il sort du script. Si tu écris ALWAYS ou JAMAIS en majuscules, c'est le signal de reformuler en expliquant l'enjeu.
- **scripts** : dès qu'une opération est déterministe et se répète, écris-la une fois en script plutôt que de la faire reconstruire à chaque invocation.
- **sécurité** : un skill ne doit rien contenir de surprenant pour qui lit sa description. Pas de code d'exfiltration, pas de secrets en dur, pas d'accès non annoncé. `validate_skill.py` cherche les schémas de secrets, mais il ne remplace pas ta lecture.

---

## Phase 2 — Évaluer

Trois notes, agrégées en un score global. Le protocole détaillé est dans `references/evaluation.md` — lis-le maintenant, avant de lancer quoi que ce soit.

### 2a. Structure (automatique)

```bash
python3 scripts/validate_skill.py <chemin-du-skill> --json > evals/structure.json
```

Frontmatter valide, nom en kebab-case cohérent avec le dossier, description de longueur exploitable, corps sous la limite, références relatives résolues, scripts syntaxiquement corrects, absence de secrets. Toute erreur bloquante met la note de structure à 0 — ce sont des défauts qui cassent l'installation, pas des questions de goût.

### 2b. Déclenchement

20 requêtes réalistes, moitié devant déclencher le skill, moitié non. Les négatives doivent être des quasi-collisions : requêtes du domaine voisin, formulations ambiguës, cas où un autre outil est plus adapté. Une négative évidente ne teste rien.

Fais valider le jeu de test à l'utilisateur avant de le lancer — un mauvais jeu produit une mauvaise description. Puis mesure le taux de déclenchement correct (3 passages par requête pour lisser le bruit).

### 2c. Qualité

3 à 5 tâches réelles, exécutées avec le skill et sans le skill (baseline). Pour chacune, des assertions objectivement vérifiables, avec des noms qui se lisent seuls dans le rapport. Privilégie les assertions scriptables aux jugements à l'œil.

Le baseline n'est pas décoratif : si le skill ne bat pas le Claude nu, il ne mérite pas d'exister et il faut le dire à l'utilisateur plutôt que de le publier.

### 2d. Note globale et rapport

```bash
python3 scripts/score_report.py evals/ --config config.json --markdown evals/rapport.md
```

Le script agrège les trois notes selon les poids configurés, écrit `evals/score.json` et un rapport lisible, et sort en code 1 si le score est sous le seuil. Montre le rapport à l'utilisateur avant toute publication.

---

## Phase 3 — Garde-fou

Le contrat est simple : **score global < seuil ⇒ pas de publication.**

Quand le seuil n'est pas atteint :

1. Présente le rapport en nommant les points faibles précisément — quelle assertion a échoué, quelles requêtes ont mal déclenché.
2. Propose les corrections. Généralise à partir des échecs plutôt que de rustiner le cas précis : on optimise un skill qui servira des milliers de fois, pas trois cas de test.
3. Relance l'évaluation dans `iteration-N+1/`. Boucle jusqu'au seuil.

L'utilisateur peut vouloir passer outre. C'est sa décision, mais elle doit être explicite : demande-lui de confirmer qu'il veut publier malgré le score, et inscris le score obtenu et le fait qu'il a été outrepassé dans le message de commit. Ne baisse jamais le seuil dans `config.json` pour faire passer un skill — le seuil est un engagement, pas une variable d'ajustement.

Vérifie aussi, avant de publier, que tu n'as pas fait passer le score en affaiblissant les tests. Si les assertions ont changé entre deux itérations, dis-le explicitement dans le rapport.

---

## Phase 4 — Publier sur GitHub

Seuil franchi et rapport validé par l'utilisateur : on publie. La procédure complète, y compris la découverte des outils MCP et la gestion des mises à jour de skills existants, est dans `references/github-publish.md`.

Séquence :

1. Lire le repo cible et vérifier que `skills/<nom>/` n'existe pas déjà (s'il existe, c'est une mise à jour — récupère les SHA des fichiers, ils sont requis pour écraser)
2. Créer une branche `skill/<nom>` depuis la branche par défaut
3. Committer tous les fichiers du skill, `evals/rapport.md` et `evals/score.json`
4. Ouvrir une pull request dont la description contient le score et le résumé d'évaluation
5. Donner l'URL de la PR à l'utilisateur

**Demande confirmation explicite avant l'étape 3.** Écrire dans un repo est une action publique et irréversible en pratique : annonce le repo, la branche, la liste des fichiers et le score, et attends un accord clair. Un accord donné pour une publication ne vaut pas pour la suivante.

Ne committe jamais : jetons ou clés, chemins absolus de la machine de l'utilisateur, transcriptions d'évaluation contenant des données personnelles, fichiers de plus de quelques centaines de Ko sans en parler.

---

## Rappel du cycle

Concevoir → rédiger → valider la structure → tester le déclenchement → tester la qualité contre baseline → noter → corriger et reboucler tant que le seuil n'est pas franchi → confirmer → publier en PR.

La boucle d'itération est le cœur du travail, pas une formalité de fin. Un skill qui passe du premier coup signifie généralement que les tests sont trop faciles.

## Fichiers de référence

- `references/evaluation.md` — protocole d'évaluation détaillé, format des fichiers de résultats, rédaction des assertions
- `references/github-publish.md` — outils MCP GitHub, séquence de publication, mise à jour d'un skill existant, dépannage
- `scripts/validate_skill.py` — contrôles structurels, sortie JSON
- `scripts/score_report.py` — agrégation des notes, garde-fou, rapport Markdown
- `assets/config.example.json` — modèle de configuration
