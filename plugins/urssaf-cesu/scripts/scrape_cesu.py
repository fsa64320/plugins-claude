#!/usr/bin/env python3
"""
Extracteur CESU URSSAF — via replay de requêtes API

Deux modes d'utilisation :
  1. --curl "curl 'https://...' -H ..."   → replay une commande curl copiée depuis DevTools
  2. --cookie "JSESSIONID=..." --url "..." → appel direct avec cookie

Usage:
    python3 scrape_cesu.py --curl "$(pbpaste)"
    python3 scrape_cesu.py --cookie "JSESSIONID=abc123" --url "https://www.cesu.urssaf.fr/..."
    python3 scrape_cesu.py --fichier reponse.json
"""

import argparse
import json
import re
import sys
from datetime import datetime

try:
    import httpx
except ImportError:
    print("Erreur : httpx n'est pas installé.", file=sys.stderr)
    print("Installez-le avec : pip3 install httpx", file=sys.stderr)
    sys.exit(1)


MOIS_FR = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
    5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
    9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre",
}


# --- Parsing d'une commande curl ---


def parse_curl(curl_cmd: str) -> dict:
    """
    Parse une commande curl copiée depuis Chrome/Firefox DevTools.
    Retourne un dict {url, method, headers, cookies, data}.
    """
    result = {"url": "", "method": "GET", "headers": {}, "cookies": {}, "data": None}

    # Extraire l'URL (entre quotes simples ou doubles, ou sans quotes)
    url_match = re.search(r"curl\s+['\"]?(https?://[^\s'\"]+)['\"]?", curl_cmd)
    if url_match:
        result["url"] = url_match.group(1)

    # Extraire les headers (-H 'Key: Value' ou --header 'Key: Value')
    headers = re.findall(r"(?:-H|--header)\s+['\"]([^'\"]+)['\"]", curl_cmd)
    for h in headers:
        if ":" in h:
            key, val = h.split(":", 1)
            key = key.strip()
            val = val.strip()
            if key.lower() == "cookie":
                # Parser les cookies
                for cookie_pair in val.split(";"):
                    if "=" in cookie_pair:
                        ck, cv = cookie_pair.strip().split("=", 1)
                        result["cookies"][ck.strip()] = cv.strip()
            else:
                result["headers"][key] = val

    # Extraire --cookie ou -b
    cookie_match = re.search(r"(?:-b|--cookie)\s+['\"]([^'\"]+)['\"]", curl_cmd)
    if cookie_match:
        for cookie_pair in cookie_match.group(1).split(";"):
            if "=" in cookie_pair:
                ck, cv = cookie_pair.strip().split("=", 1)
                result["cookies"][ck.strip()] = cv.strip()

    # Extraire les données POST (-d ou --data)
    data_match = re.search(r"(?:-d|--data|--data-raw)\s+['\"]([^'\"]*)['\"]", curl_cmd)
    if data_match:
        result["data"] = data_match.group(1)
        result["method"] = "POST"

    # Extraire la méthode (-X)
    method_match = re.search(r"-X\s+(\w+)", curl_cmd)
    if method_match:
        result["method"] = method_match.group(1).upper()

    return result


# --- Requête HTTP ---


def executer_requete(parsed: dict) -> dict:
    """Exécute la requête et retourne le JSON de réponse."""
    if not parsed["url"]:
        print("Erreur : aucune URL trouvée dans la commande curl.", file=sys.stderr)
        sys.exit(1)

    print(f"  Appel : {parsed['method']} {parsed['url'][:80]}...", file=sys.stderr)

    with httpx.Client(follow_redirects=True, timeout=30.0) as client:
        response = client.request(
            method=parsed["method"],
            url=parsed["url"],
            headers=parsed["headers"],
            cookies=parsed["cookies"],
            content=parsed["data"],
        )

    if response.status_code != 200:
        print(f"  Erreur HTTP {response.status_code}", file=sys.stderr)
        print(f"  Corps : {response.text[:500]}", file=sys.stderr)
        sys.exit(1)

    try:
        return response.json()
    except json.JSONDecodeError:
        # Peut-être du HTML — afficher un aperçu
        print("  Réponse non-JSON reçue. Aperçu :", file=sys.stderr)
        print(f"  {response.text[:300]}", file=sys.stderr)
        sys.exit(1)


# --- Extraction des données ---


def extraire_declarations(data) -> list:
    """
    Extrait les données de déclaration depuis la réponse JSON.
    S'adapte à plusieurs structures possibles de l'API CESU.
    """
    resultats = []

    # La réponse peut être un dict ou une liste
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        # Chercher une clé contenant les déclarations
        for key in ["declarations", "bulletins", "lignes", "data", "content", "items",
                    "listDeclarations", "listBulletins", "voletSocial", "results"]:
            if key in data and isinstance(data[key], list):
                items = data[key]
                break
        if not items:
            # Peut-être que la réponse elle-même est une seule déclaration
            items = [data]

    for item in items:
        if not isinstance(item, dict):
            continue

        record = {
            "employe": "",
            "mois": "",
            "mois_num": 0,
            "annee": 0,
            "brut": 0.0,
            "net": 0.0,
            "cotis_pat": 0.0,
            "cotis_sal": 0.0,
        }

        # Extraction adaptative — chercher les champs par patterns de noms
        for k, v in item.items():
            kl = k.lower()

            # Nom de l'employé
            if any(mot in kl for mot in ["salarie", "employe", "nom", "prenom", "identite"]):
                if isinstance(v, str) and v.strip():
                    if record["employe"]:
                        record["employe"] += " " + v.strip()
                    else:
                        record["employe"] = v.strip()
                elif isinstance(v, dict):
                    # Objet employé avec nom/prenom
                    nom = v.get("nom", v.get("nomFamille", ""))
                    prenom = v.get("prenom", "")
                    record["employe"] = f"{prenom} {nom}".strip()

            # Période / mois
            if any(mot in kl for mot in ["periode", "mois", "date", "month"]):
                if isinstance(v, str):
                    # Format "01/2025" ou "2025-01" ou "Janvier 2025"
                    m = re.search(r"(\d{1,2})[/\-](\d{4})", str(v))
                    if m:
                        record["mois_num"] = int(m.group(1))
                        record["annee"] = int(m.group(2))
                    else:
                        m = re.search(r"(\d{4})[/\-](\d{1,2})", str(v))
                        if m:
                            record["annee"] = int(m.group(1))
                            record["mois_num"] = int(m.group(2))
                elif isinstance(v, int):
                    if 1 <= v <= 12 and "mois" in kl:
                        record["mois_num"] = v
                    elif v > 2000:
                        record["annee"] = v

            if "annee" in kl or "year" in kl or "exercice" in kl:
                if isinstance(v, int) and v > 2000:
                    record["annee"] = v

            # Montants
            montant = None
            if isinstance(v, (int, float)):
                montant = float(v)
            elif isinstance(v, str):
                # "1 234,56" ou "1234.56"
                cleaned = v.replace("\xa0", "").replace(" ", "").replace("€", "").replace(",", ".")
                try:
                    montant = float(cleaned)
                except ValueError:
                    pass

            if montant is not None:
                if any(mot in kl for mot in ["brut", "salaireBrut", "remuneration_brute"]):
                    record["brut"] = montant
                elif any(mot in kl for mot in ["net", "salaireNet", "remuneration_nette", "netApayer"]):
                    record["net"] = montant
                elif any(mot in kl for mot in ["cotisPatron", "patronal", "partEmployeur", "cotisation_employeur"]):
                    record["cotis_pat"] = montant
                elif any(mot in kl for mot in ["cotisSalari", "salarial", "partSalari", "cotisation_salarie"]):
                    record["cotis_sal"] = montant
                elif "cotis" in kl or "contribution" in kl:
                    # Cotisation générique — attribuer à patronale par défaut
                    if record["cotis_pat"] == 0:
                        record["cotis_pat"] = montant

        # Ne garder que les enregistrements avec au moins un montant
        if record["brut"] > 0 or record["net"] > 0 or record["cotis_pat"] > 0:
            if record["mois_num"] > 0:
                record["mois"] = MOIS_FR.get(record["mois_num"], str(record["mois_num"]))
            resultats.append(record)

    return resultats


# --- Formatage Markdown ---


def formater_montant(v: float) -> str:
    """Formate un float en '1 234,56 €'."""
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")
    return f"{s} €"


def generer_markdown(resultats: list, raw_data=None) -> str:
    """Génère le tableau Markdown de sortie."""
    lignes = []

    if not resultats:
        lignes.append("## Données CESU URSSAF\n")
        lignes.append("_Aucune déclaration structurée extraite._\n")
        if raw_data:
            lignes.append("### Données brutes JSON\n")
            lignes.append("```json")
            lignes.append(json.dumps(raw_data, indent=2, ensure_ascii=False)[:3000])
            lignes.append("```\n")
            lignes.append("_Partagez ce JSON avec Claude pour qu'il puisse adapter le parsing._")
        return "\n".join(lignes)

    # Trier par employé puis mois
    resultats_tries = sorted(resultats, key=lambda r: (r["employe"], r.get("annee", 0), r["mois_num"]))

    lignes.append("## Données CESU URSSAF\n")
    lignes.append(
        "| Employé | Période | Salaire brut | Salaire net | Cotis. patronales | Cotis. salariales | Coût employeur |"
    )
    lignes.append(
        "|---------|---------|:------------:|:-----------:|:-----------------:|:-----------------:|:--------------:|"
    )

    tot_brut = tot_net = tot_pat = tot_sal = 0.0

    for r in resultats_tries:
        brut = r["brut"]
        net = r["net"]
        pat = r["cotis_pat"]
        sal = r["cotis_sal"]
        cout = brut + pat

        tot_brut += brut
        tot_net += net
        tot_pat += pat
        tot_sal += sal

        periode = f"{r['mois']} {r['annee']}" if r["mois"] else "—"
        lignes.append(
            f"| {r['employe'] or '—'} | {periode} "
            f"| {formater_montant(brut)} "
            f"| {formater_montant(net)} "
            f"| {formater_montant(pat)} "
            f"| {formater_montant(sal)} "
            f"| {formater_montant(cout)} |"
        )

    tot_cout = tot_brut + tot_pat
    lignes.append(
        f"| **TOTAL** | — "
        f"| **{formater_montant(tot_brut)}** "
        f"| **{formater_montant(tot_net)}** "
        f"| **{formater_montant(tot_pat)}** "
        f"| **{formater_montant(tot_sal)}** "
        f"| **{formater_montant(tot_cout)}** |"
    )

    lignes.append("")
    lignes.append(
        f"_Extrait le {datetime.now().strftime('%d/%m/%Y à %H:%M')} "
        f"— {len(resultats)} déclaration(s)_"
    )

    return "\n".join(lignes)


# --- Mode fichier JSON local ---


def lire_fichier_json(chemin: str) -> dict:
    """Lit un fichier JSON local."""
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur : fichier non trouvé : {chemin}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Erreur : JSON invalide dans {chemin} : {e}", file=sys.stderr)
        sys.exit(1)


# --- Point d'entrée ---


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extracteur CESU URSSAF — récupère salaires et cotisations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  # Replay d'une commande curl copiée depuis DevTools
  python3 scrape_cesu.py --curl "$(pbpaste)"

  # Appel direct avec cookie
  python3 scrape_cesu.py --cookie "JSESSIONID=abc" --url "https://..."

  # Parser un fichier JSON déjà téléchargé
  python3 scrape_cesu.py --fichier response.json
        """,
    )
    parser.add_argument("--curl", type=str, help="Commande curl complète (entre guillemets)")
    parser.add_argument("--cookie", type=str, help="Cookie de session (JSESSIONID=...)")
    parser.add_argument("--url", type=str, help="URL de l'API à appeler")
    parser.add_argument("--fichier", type=str, help="Fichier JSON local à parser")
    parser.add_argument("--raw", action="store_true", help="Afficher aussi le JSON brut")
    return parser.parse_args()


def main():
    args = parse_args()

    data = None

    if args.fichier:
        # Mode fichier local
        print(f"  Lecture de {args.fichier}...", file=sys.stderr)
        data = lire_fichier_json(args.fichier)

    elif args.curl:
        # Mode replay curl
        parsed = parse_curl(args.curl)
        if not parsed["url"]:
            print("Erreur : impossible d'extraire l'URL de la commande curl.", file=sys.stderr)
            print("Assurez-vous de copier la commande complète depuis DevTools.", file=sys.stderr)
            sys.exit(1)
        data = executer_requete(parsed)

    elif args.cookie and args.url:
        # Mode cookie + URL direct
        cookies = {}
        for pair in args.cookie.split(";"):
            if "=" in pair:
                k, v = pair.strip().split("=", 1)
                cookies[k.strip()] = v.strip()
        parsed = {
            "url": args.url,
            "method": "GET",
            "headers": {
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            },
            "cookies": cookies,
            "data": None,
        }
        data = executer_requete(parsed)

    else:
        print("Erreur : spécifiez --curl, --fichier, ou --cookie + --url", file=sys.stderr)
        print("Utilisez --help pour voir les exemples.", file=sys.stderr)
        sys.exit(1)

    # Extraire et formater
    resultats = extraire_declarations(data)
    markdown = generer_markdown(resultats, raw_data=data if (args.raw or not resultats) else None)
    print(markdown)

    # Si aucun résultat structuré, afficher un guide
    if not resultats:
        print("\n---\n", file=sys.stderr)
        print("  Pas de données structurées trouvées.", file=sys.stderr)
        print("  Le JSON brut est affiché ci-dessus pour analyse.", file=sys.stderr)
        print("  Partagez-le avec Claude pour adapter l'extraction.", file=sys.stderr)


if __name__ == "__main__":
    main()
