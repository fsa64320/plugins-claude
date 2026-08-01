#!/usr/bin/env python3
"""Contrôles structurels d'un skill avant évaluation et publication.

Usage:
    python3 validate_skill.py <chemin-du-skill> [--json] [-o sortie.json]

Sortie JSON: {"score": 0.0-1.0, "errors": [...], "warnings": [...], "info": {...}}
Code de sortie: 0 si aucune erreur bloquante, 1 sinon.

Toute erreur bloquante met le score à 0 : ce sont des défauts qui cassent
l'installation ou le déclenchement du skill, pas des questions de style.
Les avertissements coûtent 0.1 chacun (plancher 0.3).
"""

import argparse
import ast
import json
import os
import re
import sys

BODY_MAX_LINES = 500
BODY_WARN_LINES = 400
DESC_MIN = 40
DESC_MAX = 1024
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Schémas de secrets. Volontairement conservateurs : on préfère un faux positif
# à un token publié sur GitHub.
SECRET_PATTERNS = [
    (r"gh[pousr]_[A-Za-z0-9]{20,}", "jeton GitHub"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "jeton GitHub (fine-grained)"),
    (r"sk-ant-[A-Za-z0-9\-_]{20,}", "clé API Anthropic"),
    (r"sk-[A-Za-z0-9]{32,}", "clé API de type OpenAI"),
    (r"AKIA[0-9A-Z]{16}", "clé d'accès AWS"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "jeton Slack"),
    (r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----", "clé privée"),
    (r"(?i)\b(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][^'\"\s]{12,}['\"]",
     "identifiant en dur"),
]

TEXT_EXT = {".md", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml", ".txt", ".toml"}


def parse_frontmatter(text):
    """Extrait le frontmatter YAML sans dépendre de PyYAML.

    On ne gère que des paires clé: valeur au premier niveau, éventuellement
    multi-lignes — c'est tout ce qu'un frontmatter de skill contient.
    """
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")
    data, key = {}, None
    for line in raw.split("\n"):
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            data[key] = m.group(2).strip().strip("'\"")
        elif key and line.strip():
            data[key] = (data[key] + " " + line.strip()).strip()
    return data, body


def iter_text_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__", "node_modules"}]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in TEXT_EXT:
                yield os.path.join(dirpath, fn)


def validate(skill_path):
    errors, warnings, info = [], [], {}
    skill_path = os.path.abspath(skill_path.rstrip("/"))
    dirname = os.path.basename(skill_path)
    info["directory"] = dirname

    if not os.path.isdir(skill_path):
        return {"score": 0.0, "errors": [f"Dossier introuvable : {skill_path}"],
                "warnings": [], "info": info}

    md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(md_path):
        return {"score": 0.0, "errors": ["SKILL.md manquant à la racine du skill"],
                "warnings": [], "info": info}

    text = open(md_path, encoding="utf-8").read()
    fm, body = parse_frontmatter(text)

    # --- Frontmatter ---
    if fm is None:
        errors.append("Frontmatter YAML absent ou non fermé (délimiteurs ---)")
        fm = {}

    name = fm.get("name", "")
    if not name:
        errors.append("Champ 'name' absent du frontmatter")
    else:
        info["name"] = name
        if not NAME_RE.match(name):
            errors.append(f"'name' doit être en kebab-case minuscule : '{name}'")
        if name != dirname:
            errors.append(f"'name' ({name}) doit correspondre au nom du dossier ({dirname})")

    desc = fm.get("description", "")
    info["description_length"] = len(desc)
    if not desc:
        errors.append("Champ 'description' absent du frontmatter — le skill ne se déclenchera jamais")
    elif len(desc) < DESC_MIN:
        errors.append(f"'description' trop courte ({len(desc)} car.) : elle doit dire "
                      "ce que fait le skill ET quand l'utiliser")
    elif len(desc) > DESC_MAX:
        warnings.append(f"'description' très longue ({len(desc)} car., max conseillé {DESC_MAX})")
    elif len(desc) < 120:
        warnings.append(f"'description' courte ({len(desc)} car.) : ajoute des formulations "
                        "utilisateur concrètes pour améliorer le déclenchement")

    # --- Corps ---
    body_lines = body.count("\n") + 1 if body.strip() else 0
    info["body_lines"] = body_lines
    if body_lines == 0:
        errors.append("Le corps du SKILL.md est vide")
    elif body_lines > BODY_MAX_LINES:
        warnings.append(f"Corps de {body_lines} lignes (> {BODY_MAX_LINES}) : "
                        "déporte du contenu vers references/")
    elif body_lines > BODY_WARN_LINES:
        warnings.append(f"Corps de {body_lines} lignes, proche de la limite de {BODY_MAX_LINES}")

    caps = len(re.findall(r"\b(ALWAYS|NEVER|MUST|TOUJOURS|JAMAIS)\b", body))
    if caps > 5:
        warnings.append(f"{caps} impératifs en capitales : préfère expliquer le pourquoi, "
                        "un modèle qui comprend l'intention gère mieux les cas non prévus")

    # --- Références relatives ---
    referenced = set(re.findall(r"(?:references|scripts|assets)/[\w./-]+", body))
    missing = [r for r in referenced
               if not os.path.exists(os.path.join(skill_path, r.rstrip(".,;:)")))]
    if missing:
        errors.append("Fichiers référencés dans SKILL.md mais absents : " + ", ".join(sorted(missing)))
    info["referenced_files"] = sorted(referenced)

    # Ressources présentes mais jamais citées : elles ne seront jamais lues.
    for sub in ("references", "assets"):
        d = os.path.join(skill_path, sub)
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.startswith("."):
                    continue
                if f"{sub}/{fn}" not in body:
                    warnings.append(f"{sub}/{fn} n'est cité nulle part dans SKILL.md — "
                                    "il ne sera jamais chargé")

    # --- Scripts Python ---
    scripts_dir = os.path.join(skill_path, "scripts")
    py_count = 0
    if os.path.isdir(scripts_dir):
        for dirpath, _, filenames in os.walk(scripts_dir):
            for fn in filenames:
                if fn.endswith(".py"):
                    py_count += 1
                    p = os.path.join(dirpath, fn)
                    try:
                        ast.parse(open(p, encoding="utf-8").read())
                    except SyntaxError as e:
                        errors.append(f"Erreur de syntaxe dans {os.path.relpath(p, skill_path)} "
                                      f"ligne {e.lineno} : {e.msg}")
    info["python_scripts"] = py_count

    # --- Secrets ---
    for p in iter_text_files(skill_path):
        try:
            content = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, content):
                errors.append(f"Secret potentiel ({label}) dans "
                              f"{os.path.relpath(p, skill_path)} — retire-le avant publication")
                break

    # --- Chemins absolus locaux ---
    for p in iter_text_files(skill_path):
        content = open(p, encoding="utf-8", errors="ignore").read()
        if re.search(r"/(?:Users|home)/[A-Za-z0-9._-]+/", content):
            warnings.append(f"Chemin absolu local dans {os.path.relpath(p, skill_path)} — "
                            "il ne fonctionnera pas chez un autre utilisateur")

    # --- Score ---
    if errors:
        score = 0.0
    else:
        score = max(0.3, 1.0 - 0.1 * len(warnings))

    return {"score": round(score, 3), "errors": errors,
            "warnings": warnings, "info": info}


def main():
    ap = argparse.ArgumentParser(description="Contrôles structurels d'un skill")
    ap.add_argument("skill_path")
    ap.add_argument("--json", action="store_true", help="sortie JSON sur stdout")
    ap.add_argument("-o", "--output", help="écrire le JSON dans ce fichier")
    args = ap.parse_args()

    result = validate(args.skill_path)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Skill : {result['info'].get('name', result['info'].get('directory', '?'))}")
        print(f"Note de structure : {result['score']:.2f}")
        if result["errors"]:
            print(f"\n{len(result['errors'])} erreur(s) bloquante(s) :")
            for e in result["errors"]:
                print(f"  ✗ {e}")
        if result["warnings"]:
            print(f"\n{len(result['warnings'])} avertissement(s) :")
            for w in result["warnings"]:
                print(f"  ! {w}")
        if not result["errors"] and not result["warnings"]:
            print("\nAucun problème détecté.")

    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
