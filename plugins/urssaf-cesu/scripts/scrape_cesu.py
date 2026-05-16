#!/usr/bin/env python3
"""
Scraper CESU URSSAF — cesu.urssaf.fr
Récupère les données de salaire et cotisations pour tous les employés.

Usage:
    python3 scrape_cesu.py --annee 2025 --mois-debut 1 --mois-fin 12
"""

import argparse
import sys
from datetime import datetime

MOIS_FR = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
    5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
    9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre",
}

CESU_URL = "https://www.cesu.urssaf.fr/cesuwebsite/web/index.html"


def parse_args():
    parser = argparse.ArgumentParser(description="Scraper CESU URSSAF")
    parser.add_argument("--annee", type=int, default=datetime.now().year, help="Année fiscale")
    parser.add_argument("--mois-debut", type=int, default=1, help="Mois de début (1-12)")
    parser.add_argument("--mois-fin", type=int, default=12, help="Mois de fin (1-12)")
    return parser.parse_args()


def attendre_connexion(page):
    """Ouvre le portail et attend que l'utilisateur se connecte."""
    print(f"\n{'='*60}")
    print("  URSSAF CESU — Connexion manuelle requise")
    print(f"{'='*60}")
    print(f"\n  Le navigateur Chromium s'est ouvert sur :")
    print(f"  {CESU_URL}")
    print()
    print("  1. Connectez-vous avec vos identifiants URSSAF")
    print("  2. Attendez d'être sur le tableau de bord principal")
    print("  3. Revenez ici et appuyez sur ENTRÉE")
    print()

    try:
        input("  Appuyez sur ENTRÉE une fois connecté... ")
    except EOFError:
        print("\n  [Mode non-interactif détecté — attente 60s pour connexion manuelle]")
        page.wait_for_timeout(60_000)

    print("\n  Connexion confirmée. Extraction des données en cours...\n")


def extraire_declarations(page, annee, mois_debut, mois_fin):
    """
    Navigue sur le portail CESU et extrait les déclarations pour la période.
    Retourne une liste de dicts : {employe, mois, annee, brut, net, cotis_pat, cotis_sal}
    """
    resultats = []

    # Sélecteurs CSS cibles sur cesu.urssaf.fr
    # Ces sélecteurs ont été identifiés sur la structure du portail CESU v2
    # Adapter si l'interface évolue.
    SELECTEURS = {
        # Navigation vers les déclarations
        "menu_declarations": "a[href*='mesDeclarations'], a[href*='declarations'], nav a",
        # Tableau des déclarations
        "tableau_declarations": "table.tableau-declarations, table[class*='declaration'], .liste-declarations",
        # Lignes du tableau
        "lignes": "tbody tr, .ligne-declaration",
        # Cellules clés par index ou attribut data-*
        "employe": "td:nth-child(1), [data-employe], .nom-employe",
        "periode": "td:nth-child(2), [data-periode], .periode",
        "brut": "td:nth-child(3), [data-brut], .salaire-brut",
        "net": "td:nth-child(4), [data-net], .salaire-net",
        "cotis_patronale": "td:nth-child(5), [data-cotis-pat], .cotisation-patronale",
        "cotis_salariale": "td:nth-child(6), [data-cotis-sal], .cotisation-salariale",
    }

    try:
        # Rechercher et cliquer sur le menu "Mes déclarations"
        menu_links = page.locator("nav a, .menu a, header a, aside a").all()
        declaration_link = None

        for link in menu_links:
            try:
                texte = link.inner_text().strip().lower()
                href = link.get_attribute("href") or ""
                if any(mot in texte for mot in ["déclaration", "declaration", "bulletin", "salarié"]):
                    declaration_link = link
                    break
                if any(mot in href for mot in ["declaration", "bulletin", "salarie"]):
                    declaration_link = link
                    break
            except Exception:
                continue

        if declaration_link:
            declaration_link.click()
            page.wait_for_load_state("networkidle", timeout=15_000)
        else:
            # Tentative de navigation directe vers les URLs connues du portail CESU
            urls_essais = [
                "https://www.cesu.urssaf.fr/cesuwebsite/web/index.html#/mes-declarations",
                "https://www.cesu.urssaf.fr/cesuwebsite/web/index.html#/declarations",
                "https://www.cesu.urssaf.fr/cesuwebsite/web/index.html#/bulletins",
            ]
            for url in urls_essais:
                page.goto(url, timeout=10_000)
                page.wait_for_load_state("networkidle", timeout=10_000)
                if page.locator("table, .declaration, .bulletin").count() > 0:
                    break

        # Filtrer par année si le portail le permet
        # Chercher un sélecteur d'année ou un champ filtre
        selects = page.locator("select").all()
        for sel in selects:
            try:
                options = sel.locator("option").all()
                for opt in options:
                    if str(annee) in (opt.inner_text() or ""):
                        sel.select_option(value=opt.get_attribute("value") or str(annee))
                        page.wait_for_load_state("networkidle", timeout=5_000)
                        break
            except Exception:
                continue

        # Extraire les lignes du tableau
        lignes = page.locator("tbody tr, .ligne-declaration, [class*='row-declaration']").all()

        if not lignes:
            print("  [AVERTISSEMENT] Aucune ligne de déclaration trouvée.", file=sys.stderr)
            print("  Vérifiez que vous êtes bien sur la page des déclarations.", file=sys.stderr)
            return []

        for ligne in lignes:
            try:
                cellules = ligne.locator("td").all()
                if len(cellules) < 3:
                    continue

                # Extraction des cellules — l'ordre peut varier selon la version du portail
                textes = [c.inner_text().strip() for c in cellules]

                # Heuristique : chercher la cellule contenant un mois
                mois_num = None
                employe = ""
                brut = "0,00"
                net = "0,00"
                cotis_pat = "0,00"
                cotis_sal = "0,00"

                for i, texte in enumerate(textes):
                    # Détection du mois
                    for num, nom in MOIS_FR.items():
                        if nom.lower() in texte.lower() or f"{num:02d}/{annee}" in texte or f"{num}/{annee}" in texte:
                            mois_num = num
                            break

                    # Détection des montants (format : "1 234,56" ou "1234.56")
                    import re
                    if re.match(r"[\d\s]+[,\.]\d{2}", texte.replace("\xa0", " ")):
                        montant = texte.replace("\xa0", "").replace(" ", "").replace("€", "").strip()
                        # Attribution par position relative (ordre typique du portail CESU)
                        if i == len(textes) - 4:
                            brut = montant
                        elif i == len(textes) - 3:
                            cotis_pat = montant
                        elif i == len(textes) - 2:
                            cotis_sal = montant
                        elif i == len(textes) - 1:
                            net = montant

                    # Premier champ non-montant = nom employé
                    if i == 0 and not re.match(r"[\d\s]+[,\.]\d{2}", texte):
                        employe = texte

                if mois_num is None:
                    continue

                if mois_num < mois_debut or mois_num > mois_fin:
                    continue

                resultats.append({
                    "employe": employe or "—",
                    "mois": MOIS_FR[mois_num],
                    "mois_num": mois_num,
                    "annee": annee,
                    "brut": brut,
                    "net": net,
                    "cotis_pat": cotis_pat,
                    "cotis_sal": cotis_sal,
                })

            except Exception as e:
                print(f"  [AVERTISSEMENT] Ligne ignorée : {e}", file=sys.stderr)
                continue

    except Exception as e:
        print(f"  [ERREUR] Navigation échouée : {e}", file=sys.stderr)

    return resultats


def parser_montant(s):
    """Convertit une chaîne montant ('1 234,56' ou '1234.56') en float."""
    try:
        return float(s.replace("\xa0", "").replace(" ", "").replace(",", "."))
    except (ValueError, AttributeError):
        return 0.0


def formater_montant(v):
    """Formate un float en chaîne '1 234,56 €'."""
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")
    return f"{s} €"


def generer_markdown(resultats, annee, mois_debut, mois_fin):
    """Génère un tableau Markdown à partir des résultats."""
    if not resultats:
        return (
            f"## Données CESU URSSAF — {annee} ({MOIS_FR[mois_debut]} à {MOIS_FR[mois_fin]})\n\n"
            "_Aucune déclaration trouvée pour cette période._\n"
        )

    # Trier par employé puis par mois
    resultats_tries = sorted(resultats, key=lambda r: (r["employe"], r["mois_num"]))

    lignes_md = []
    lignes_md.append(f"## Données CESU URSSAF — {annee} ({MOIS_FR[mois_debut]} à {MOIS_FR[mois_fin]})\n")
    lignes_md.append(
        "| Employé | Mois | Salaire brut | Salaire net | Cotis. patronales | Cotis. salariales | Coût total employeur |"
    )
    lignes_md.append(
        "|---------|------|:------------:|:-----------:|:-----------------:|:-----------------:|:--------------------:|"
    )

    tot_brut = tot_net = tot_pat = tot_sal = 0.0

    for r in resultats_tries:
        brut_v = parser_montant(r["brut"])
        net_v = parser_montant(r["net"])
        pat_v = parser_montant(r["cotis_pat"])
        sal_v = parser_montant(r["cotis_sal"])
        cout_total = brut_v + pat_v  # coût total employeur = brut + cotisations patronales

        tot_brut += brut_v
        tot_net += net_v
        tot_pat += pat_v
        tot_sal += sal_v

        lignes_md.append(
            f"| {r['employe']} | {r['mois']} {r['annee']} "
            f"| {formater_montant(brut_v)} "
            f"| {formater_montant(net_v)} "
            f"| {formater_montant(pat_v)} "
            f"| {formater_montant(sal_v)} "
            f"| {formater_montant(cout_total)} |"
        )

    # Ligne totaux
    tot_cout = tot_brut + tot_pat
    lignes_md.append(
        f"| **TOTAL** | — "
        f"| **{formater_montant(tot_brut)}** "
        f"| **{formater_montant(tot_net)}** "
        f"| **{formater_montant(tot_pat)}** "
        f"| **{formater_montant(tot_sal)}** "
        f"| **{formater_montant(tot_cout)}** |"
    )

    lignes_md.append("")
    lignes_md.append(f"_Extrait le {datetime.now().strftime('%d/%m/%Y à %H:%M')} — {len(resultats)} déclaration(s) trouvée(s)_")

    return "\n".join(lignes_md)


def main():
    args = parse_args()

    if args.mois_debut < 1 or args.mois_debut > 12:
        print("Erreur : --mois-debut doit être entre 1 et 12", file=sys.stderr)
        sys.exit(1)
    if args.mois_fin < 1 or args.mois_fin > 12:
        print("Erreur : --mois-fin doit être entre 1 et 12", file=sys.stderr)
        sys.exit(1)
    if args.mois_debut > args.mois_fin:
        print("Erreur : --mois-debut doit être ≤ --mois-fin", file=sys.stderr)
        sys.exit(1)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Erreur : Playwright n'est pas installé.", file=sys.stderr)
        print("Installez-le avec : pip3 install playwright && python3 -m playwright install chromium", file=sys.stderr)
        sys.exit(1)

    resultats = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        try:
            page.goto(CESU_URL, timeout=30_000)
            page.wait_for_load_state("domcontentloaded", timeout=15_000)
        except Exception as e:
            print(f"Erreur : impossible d'ouvrir le portail CESU : {e}", file=sys.stderr)
            browser.close()
            sys.exit(1)

        attendre_connexion(page)

        resultats = extraire_declarations(page, args.annee, args.mois_debut, args.mois_fin)

        browser.close()

    markdown = generer_markdown(resultats, args.annee, args.mois_debut, args.mois_fin)
    print(markdown)


if __name__ == "__main__":
    main()
