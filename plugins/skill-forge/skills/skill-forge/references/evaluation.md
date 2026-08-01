# Protocole d'évaluation

Trois composantes notées, agrégées par `scripts/score_report.py`. Chacune produit un fichier JSON dans le dossier `evals/iteration-N/`. Tant qu'une composante manque, le garde-fou reste fermé — une évaluation partielle donne une confiance factice.

## Arborescence

```
<workspace>/<nom-du-skill>/
├── config.json
├── skill/                     le skill en cours de fabrication
└── evals/
    ├── iteration-1/
    │   ├── structure.json
    │   ├── trigger.json
    │   ├── trigger_queries.json
    │   ├── quality.json
    │   ├── score.json
    │   ├── rapport.md
    │   └── runs/              transcriptions et sorties des cas de test
    └── iteration-2/
```

---

## 1. Structure

```bash
python3 scripts/validate_skill.py <workspace>/skill --json -o evals/iteration-N/structure.json
```

Le script vérifie le frontmatter, la cohérence nom/dossier, la longueur exploitable de la description, la taille du corps, la résolution des références relatives, la syntaxe des scripts Python, l'absence de secrets et de chemins absolus locaux.

Une erreur bloquante met la note à 0 : ces défauts cassent l'installation ou le déclenchement, ils ne se négocient pas. Les avertissements coûtent 0.1 chacun avec un plancher à 0.3.

Lis quand même le SKILL.md toi-même. Le script attrape les défauts mécaniques ; il ne voit pas qu'une instruction est ambiguë ou qu'un script fait autre chose que ce que le skill annonce.

---

## 2. Déclenchement

### Construire le jeu de requêtes

20 requêtes, environ 10 positives et 10 négatives, dans `trigger_queries.json` :

```json
[
  {"query": "...", "should_trigger": true},
  {"query": "...", "should_trigger": false}
]
```

Ce qui fait la valeur du jeu, c'est le réalisme et la difficulté.

**Positives (8-10)** — des façons différentes de demander la même chose : formelle, familière, avec fautes, en abrégé. Inclus des cas où l'utilisateur ne nomme jamais le skill ni son domaine mais en a manifestement besoin. Inclus au moins un cas où un autre skill pourrait se déclencher mais où celui-ci doit gagner.

**Négatives (8-10)** — la valeur est dans les quasi-collisions : domaine voisin, formulation ambiguë qu'un simple appariement de mots-clés ferait déclencher à tort, cas où le skill touche au sujet mais où un autre outil est plus adapté. Une négative évidente ne teste rien : « écris une fonction fibonacci » comme négative d'un skill PDF ne mesure aucune frontière.

Écris des requêtes concrètes et situées — chemins de fichiers, noms d'entreprise, noms de colonnes, un peu de contexte personnel. Trop court et abstrait, ça ne ressemble pas à ce que les gens tapent.

Mauvais : `"Formate ces données"`
Bon : `"bon alors ma responsable vient de m'envoyer un xlsx (dans mes téléchargements, un truc genre 'CA Q4 final FINAL v2.xlsx') et elle veut une colonne avec la marge en pourcentage. Le CA est en colonne C et les coûts en D je crois"`

**Fais valider le jeu à l'utilisateur avant de lancer.** Un mauvais jeu de test produit une mauvaise description, et la description est le seul mécanisme de déclenchement.

### Mesurer

Chaque requête est passée 3 fois pour lisser le bruit — le déclenchement n'est pas déterministe. Pour chaque passage, on note si le skill a été consulté.

```json
{
  "queries": [
    {"query": "...", "should_trigger": true, "runs": 3, "triggered": 3},
    {"query": "...", "should_trigger": false, "runs": 3, "triggered": 0}
  ]
}
```

La note est une exactitude équilibrée : moyenne du rappel (positifs déclenchés) et de la spécificité (négatifs ignorés), à poids égaux. Sans équilibrage, une description qui déclenche sur tout obtiendrait une bonne note — c'est justement le défaut à détecter.

Une requête positive sous 67 % de déclenchement, ou négative au-dessus de 33 %, est signalée nommément dans le rapport.

### Corriger

Un mauvais déclenchement se corrige presque toujours dans la description, pas dans le corps.

- Faux négatifs → la description manque des formulations de l'utilisateur réel. Ajoute-les, et sois plus insistant ("utilise ce skill dès que…"). Claude sous-déclenche par défaut.
- Faux positifs → la description est trop large. Nomme explicitement ce qui ne relève pas du skill et vers quoi rediriger.

À noter : Claude ne consulte un skill que pour ce qu'il ne sait pas faire seul. Une requête triviale ne déclenchera aucun skill même avec une description parfaite — ce sont de mauvais cas de test, pas des échecs de description.

---

## 3. Qualité

### Cas de test

3 à 5 tâches réelles, du type de ce que le skill servira à faire. Chacune est exécutée deux fois : **avec le skill** et **sans le skill** (baseline). Lance les deux séries dans le même tour si tu disposes de sous-agents, pour qu'elles finissent ensemble.

Le baseline n'est pas décoratif. Si le skill ne fait pas mieux qu'un Claude nu, il ne mérite pas d'être publié, et c'est une information à donner à l'utilisateur plutôt qu'à masquer. Pour une mise à jour de skill existant, le baseline est la version précédente.

### Assertions

Pour chaque cas, des assertions objectivement vérifiables, avec un intitulé qui se lit seul dans le rapport — quelqu'un qui parcourt les résultats doit comprendre ce qui est contrôlé sans lire le cas de test.

Bon : `"Le fichier de sortie contient une colonne 'marge_pct' avec des valeurs entre 0 et 100"`
Mauvais : `"La sortie est correcte"`

Quand une assertion peut être vérifiée par un script, écris le script : c'est plus rapide, plus fiable et réutilisable d'une itération à l'autre.

Certains skills ont des sorties subjectives — style d'écriture, choix graphiques. Ne force pas des assertions sur ce qui relève du jugement humain : réduis le poids de la composante qualité dans `config.json` et appuie-toi sur la relecture de l'utilisateur.

```json
{
  "evals": [
    {
      "name": "extraction-marge-xlsx",
      "prompt": "...",
      "assertions": [
        {"text": "Le fichier produit est un .xlsx ouvrable", "passed": true, "evidence": "openpyxl l'a ouvert, 3 feuilles"},
        {"text": "La colonne marge_pct existe et est numérique", "passed": false, "evidence": "colonne absente"}
      ],
      "baseline_assertions": [
        {"text": "Le fichier produit est un .xlsx ouvrable", "passed": true, "evidence": "..."},
        {"text": "La colonne marge_pct existe et est numérique", "passed": false, "evidence": "..."}
      ]
    }
  ]
}
```

Les mêmes assertions doivent être appliquées aux deux configurations, sinon la comparaison ne veut rien dire.

---

## 4. Agrégation

```bash
python3 scripts/score_report.py evals/iteration-N \
  --config config.json --markdown evals/iteration-N/rapport.md
```

Score global = moyenne pondérée des trois notes (poids par défaut : structure 0.25, déclenchement 0.35, qualité 0.40). Une composante absente est exclue du calcul et son poids redistribué, mais le garde-fou reste fermé tant qu'elle manque — on ne publie pas sur une évaluation partielle.

Le script sort en code 1 si le seuil n'est pas atteint. C'est le signal de bouclage : ne lance pas la phase de publication tant qu'il ne sort pas 0.

---

## 5. Itérer

Présente le rapport à l'utilisateur, puis corrige. Trois réflexes utiles :

**Généralise.** Le skill servira des milliers de fois sur des prompts qu'on ne verra jamais. Si tu rustines le cas de test précis qui a échoué, tu obtiens un skill qui passe les tests et rate le reste. Face à un défaut tenace, essaie plutôt une autre formulation, une autre métaphore, une autre façon d'organiser le travail — c'est peu coûteux à tester.

**Allège.** Retire ce qui ne sert pas. Lis les transcriptions, pas seulement les sorties : si le skill fait perdre du temps sur des détours inutiles, supprime la consigne responsable et remesure.

**Explique le pourquoi.** Un modèle qui comprend l'enjeu gère les cas non prévus ; un modèle qui suit des règles rigides échoue dès qu'il en sort. Si tu te surprends à empiler des impératifs en capitales, reformule en expliquant ce qui est en jeu.

**Repère le travail répété.** Si les trois cas de test ont chacun conduit à réécrire le même script utilitaire, ce script doit être dans `scripts/`. Écris-le une fois, référence-le depuis le SKILL.md.

Nouvelle itération dans `iteration-N+1/`, jeu de test identique (sinon les scores ne se comparent pas). Si tu modifies des assertions, dis-le explicitement dans le rapport : un score qui monte parce que les tests ont été assouplis n'est pas un progrès.

Continue jusqu'à ce que le seuil soit franchi et que l'utilisateur soit satisfait. Un skill qui passe du premier coup signale généralement des tests trop faciles.
