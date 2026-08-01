#!/usr/bin/env python3
"""Agrège les notes d'évaluation d'un skill et applique le garde-fou de publication.

Usage:
    python3 score_report.py <dossier-evals> [--config config.json]
                            [--markdown rapport.md] [--threshold 0.8]

Lit dans <dossier-evals> :
    structure.json  {"score": float, "errors": [...], "warnings": [...]}
    trigger.json    {"queries": [{"query", "should_trigger", "triggered", "runs"}]}
    quality.json    {"evals": [{"name", "prompt",
                                "assertions": [{"text", "passed", "evidence"}],
                                "baseline_assertions": [...]}]}

Écrit <dossier-evals>/score.json et, si demandé, un rapport Markdown.
Code de sortie : 0 si le score global atteint le seuil, 1 sinon.

Le code 1 est le garde-fou : la phase de publication ne doit pas démarrer
tant que ce script ne sort pas 0 (ou que l'utilisateur n'a pas explicitement
demandé à passer outre, ce qui doit être tracé dans le commit).
"""

import argparse
import json
import os
import sys

DEFAULT_WEIGHTS = {"structure": 0.25, "trigger": 0.35, "quality": 0.40}
DEFAULT_THRESHOLD = 0.80


def load(path, default=None):
    if not os.path.isfile(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def score_trigger(data):
    """Exactitude équilibrée : les positifs et les négatifs pèsent autant.

    Sans équilibrage, une description qui déclenche sur tout obtiendrait une
    bonne note dès qu'il y a plus de positifs que de négatifs — or c'est
    exactement le défaut qu'on cherche à détecter.
    """
    if not data:
        return None, {}
    pos, neg, fails = [], [], []
    for q in data.get("queries", []):
        runs = max(1, int(q.get("runs", 1)))
        rate = int(q.get("triggered", 0)) / runs
        # Seuils à 2/3 et 1/3 avec tolérance : sur 3 passages, 2 déclenchements
        # sur une positive est acceptable, 1 seul ne l'est pas.
        if q.get("should_trigger"):
            pos.append(rate)
            if rate < 2 / 3 - 1e-9:
                fails.append(("faux négatif", q.get("query", ""), rate))
        else:
            neg.append(1.0 - rate)
            if rate > 1 / 3 + 1e-9:
                fails.append(("faux positif", q.get("query", ""), rate))
    if not pos and not neg:
        return None, {}
    parts = [sum(g) / len(g) for g in (pos, neg) if g]
    detail = {
        "n_positive": len(pos), "n_negative": len(neg),
        "recall": round(sum(pos) / len(pos), 3) if pos else None,
        "specificity": round(sum(neg) / len(neg), 3) if neg else None,
        "failures": [{"type": t, "query": q, "trigger_rate": round(r, 2)} for t, q, r in fails],
    }
    return sum(parts) / len(parts), detail


def score_quality(data):
    """Taux d'assertions réussies avec le skill, et écart contre le baseline."""
    if not data:
        return None, {}
    total = passed = 0
    b_total = b_passed = 0
    per_eval, failed = [], []
    for ev in data.get("evals", []):
        aa = ev.get("assertions", [])
        p = sum(1 for a in aa if a.get("passed"))
        total += len(aa)
        passed += p
        ba = ev.get("baseline_assertions", [])
        b_total += len(ba)
        b_passed += sum(1 for a in ba if a.get("passed"))
        per_eval.append({
            "name": ev.get("name", "sans-nom"),
            "passed": p, "total": len(aa),
            "rate": round(p / len(aa), 3) if aa else None,
        })
        for a in aa:
            if not a.get("passed"):
                failed.append({"eval": ev.get("name", "sans-nom"),
                               "assertion": a.get("text", ""),
                               "evidence": a.get("evidence", "")})
    if total == 0:
        return None, {}
    rate = passed / total
    detail = {
        "assertions_passed": passed, "assertions_total": total,
        "per_eval": per_eval, "failed_assertions": failed,
    }
    if b_total:
        detail["baseline_rate"] = round(b_passed / b_total, 3)
        detail["delta_vs_baseline"] = round(rate - b_passed / b_total, 3)
    return rate, detail


def build_markdown(res):
    L = []
    verdict = "PUBLICATION AUTORISÉE" if res["passes"] else "PUBLICATION BLOQUÉE"
    L.append(f"# Rapport d'évaluation — {res.get('skill_name', 'skill')}\n")
    # Trois décimales : à deux, un score de 0.797 s'affiche 0.80 et le verdict
    # « bloqué » devient incompréhensible pour qui lit le rapport.
    L.append(f"**Score global : {res['overall']:.3f} / seuil {res['threshold']:.3f} → {verdict}**\n")

    L.append("| Composante | Note | Poids | Contribution |")
    L.append("|---|---|---|---|")
    for k, c in res["components"].items():
        if c["score"] is None:
            L.append(f"| {k} | _non mesuré_ | {c['weight']:.2f} | — |")
        else:
            L.append(f"| {k} | {c['score']:.2f} | {c['weight']:.2f} | "
                     f"{c['score'] * c['weight']:.3f} |")
    L.append("")

    st = res["details"].get("structure", {})
    if st.get("errors"):
        L.append("## Erreurs structurelles bloquantes\n")
        for e in st["errors"]:
            L.append(f"- {e}")
        L.append("")
    if st.get("warnings"):
        L.append("## Avertissements structurels\n")
        for w in st["warnings"]:
            L.append(f"- {w}")
        L.append("")

    tr = res["details"].get("trigger", {})
    if tr:
        L.append("## Déclenchement\n")
        L.append(f"- Rappel (positifs correctement déclenchés) : {tr.get('recall')}")
        L.append(f"- Spécificité (négatifs correctement ignorés) : {tr.get('specificity')}")
        L.append(f"- Jeu de test : {tr.get('n_positive', 0)} positifs / "
                 f"{tr.get('n_negative', 0)} négatifs\n")
        if tr.get("failures"):
            L.append("Requêtes problématiques :\n")
            for f in tr["failures"]:
                L.append(f"- **{f['type']}** (taux {f['trigger_rate']}) — {f['query']}")
            L.append("")

    ql = res["details"].get("quality", {})
    if ql:
        L.append("## Qualité\n")
        L.append(f"- Assertions réussies : {ql.get('assertions_passed')} / "
                 f"{ql.get('assertions_total')}")
        if "baseline_rate" in ql:
            L.append(f"- Baseline sans skill : {ql['baseline_rate']:.2f} "
                     f"(écart {ql['delta_vs_baseline']:+.2f})")
            if ql["delta_vs_baseline"] <= 0:
                L.append("- ⚠️ Le skill ne fait pas mieux que Claude sans skill. "
                         "À traiter avant publication.")
        L.append("")
        if ql.get("per_eval"):
            L.append("| Cas de test | Réussies | Total | Taux |")
            L.append("|---|---|---|---|")
            for e in ql["per_eval"]:
                L.append(f"| {e['name']} | {e['passed']} | {e['total']} | {e['rate']} |")
            L.append("")
        if ql.get("failed_assertions"):
            L.append("### Assertions en échec\n")
            for f in ql["failed_assertions"]:
                L.append(f"- **{f['eval']}** — {f['assertion']}")
                if f.get("evidence"):
                    L.append(f"  - {f['evidence']}")
            L.append("")

    if not res["passes"]:
        L.append("---\n")
        L.append("Le seuil n'est pas atteint. Corrige les points ci-dessus et relance "
                 "l'évaluation dans une nouvelle itération avant de publier. Ne baisse pas "
                 "le seuil pour faire passer le skill.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Agrégation des notes et garde-fou de publication")
    ap.add_argument("evals_dir")
    ap.add_argument("--config")
    ap.add_argument("--markdown")
    ap.add_argument("--threshold", type=float)
    ap.add_argument("--skill-name", default="skill")
    args = ap.parse_args()

    cfg = load(args.config, {}) if args.config else {}
    threshold = args.threshold if args.threshold is not None else cfg.get("threshold", DEFAULT_THRESHOLD)
    weights = {**DEFAULT_WEIGHTS, **cfg.get("weights", {})}

    d = args.evals_dir
    structure = load(os.path.join(d, "structure.json"))
    trigger = load(os.path.join(d, "trigger.json"))
    quality = load(os.path.join(d, "quality.json"))

    s_score = structure.get("score") if structure else None
    t_score, t_detail = score_trigger(trigger)
    q_score, q_detail = score_quality(quality)

    scores = {"structure": s_score, "trigger": t_score, "quality": q_score}
    # Les composantes absentes sont exclues et leur poids redistribué : on ne
    # veut ni les compter comme 0 (injuste) ni comme 1 (complaisant).
    active = {k: weights[k] for k, v in scores.items() if v is not None}
    total_w = sum(active.values())
    overall = sum(scores[k] * w for k, w in active.items()) / total_w if total_w else 0.0

    missing = [k for k, v in scores.items() if v is None]
    # On compare la valeur arrondie, celle qui sera affichée : un verdict qui
    # contredit le nombre imprimé détruit la confiance dans le garde-fou.
    overall = round(overall, 3)
    passes = overall >= threshold and not missing

    result = {
        "skill_name": cfg.get("skill_name", args.skill_name),
        "overall": overall,
        "threshold": threshold,
        "passes": passes,
        "missing_components": missing,
        "components": {k: {"score": (round(v, 3) if v is not None else None),
                           "weight": weights[k]} for k, v in scores.items()},
        "details": {"structure": structure or {}, "trigger": t_detail, "quality": q_detail},
    }

    with open(os.path.join(d, "score.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    md = build_markdown(result)
    if args.markdown:
        os.makedirs(os.path.dirname(os.path.abspath(args.markdown)), exist_ok=True)
        with open(args.markdown, "w", encoding="utf-8") as f:
            f.write(md)

    print(md)
    if missing:
        print(f"Composantes non mesurées : {', '.join(missing)}. "
              "Le garde-fou reste fermé tant qu'elles manquent.", file=sys.stderr)
    return 0 if passes else 1


if __name__ == "__main__":
    sys.exit(main())
