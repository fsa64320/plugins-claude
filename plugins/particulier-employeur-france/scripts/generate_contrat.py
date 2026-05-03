#!/usr/bin/env python3
"""
Génère un contrat de travail CDI pour particulier employeur (CCN 2111).
Prérequis : pip install reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
import os


def ask(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip() if default else input(f"{prompt} : ").strip()
    return val if val else default


def collect_data():
    print("\n=== Contrat de travail CDI — Particulier Employeur ===\n")
    print("-- Informations employeur --")
    data = {}
    data["emp_nom"] = ask("Nom et prénom de l'employeur")
    data["emp_adresse"] = ask("Adresse complète de l'employeur")
    data["emp_numero_cesu"] = ask("Numéro employeur CESU/PAJEMPLOI")

    print("\n-- Informations salarié --")
    data["sal_nom"] = ask("Nom et prénom du salarié")
    data["sal_ddn"] = ask("Date de naissance (JJ/MM/AAAA)")
    data["sal_adresse"] = ask("Adresse complète du salarié")
    data["sal_nss"] = ask("Numéro de sécurité sociale (optionnel)")

    print("\n-- Conditions du contrat --")
    data["date_debut"] = ask("Date de début du contrat (JJ/MM/AAAA)")
    data["essai_duree"] = ask("Durée de la période d'essai", "1 mois")
    data["lieu_travail"] = ask("Lieu(x) de travail")
    data["taches"] = ask("Description des tâches (ex: aide ménagère, repassage, garde d'enfant)")
    data["heures_semaine"] = ask("Nombre d'heures par semaine (ex: 20h)")
    data["repartition"] = ask("Répartition des horaires (ex: Lundi, mercredi, vendredi 9h-13h)")
    data["salaire_brut_horaire"] = ask("Salaire brut horaire (€, ex: 12.50)")
    try:
        brut_h = float(data["salaire_brut_horaire"].replace(",", "."))
        heures = float(data["heures_semaine"].replace("h", "").strip())
        salaire_brut_mensuel = round(brut_h * heures * 52 / 12, 2)
        salaire_net_mensuel = round(salaire_brut_mensuel * 0.86, 2)
        data["salaire_brut_mensuel"] = f"{salaire_brut_mensuel:.2f}"
        data["salaire_net_mensuel"] = f"{salaire_net_mensuel:.2f}"
    except ValueError:
        data["salaire_brut_mensuel"] = "À calculer"
        data["salaire_net_mensuel"] = "À calculer"

    data["date_generation"] = datetime.now().strftime("%d/%m/%Y")
    return data


def build_pdf(data):
    filename = f"contrat_CDI_{data['sal_nom'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", parent=styles["Heading1"], alignment=TA_CENTER, fontSize=14)
    body_style = ParagraphStyle("body", parent=styles["Normal"], fontSize=10, leading=16, alignment=TA_JUSTIFY)
    section_style = ParagraphStyle("section", parent=styles["Heading2"], fontSize=11, spaceAfter=6)
    center_style = ParagraphStyle("center", parent=styles["Normal"], alignment=TA_CENTER, fontSize=10)

    story = []

    # En-tête
    story.append(Paragraph("CONTRAT DE TRAVAIL À DURÉE INDÉTERMINÉE", title_style))
    story.append(Paragraph("Particulier Employeur — Convention Collective Nationale IDCC 2111", center_style))
    story.append(Spacer(1, 0.6*cm))

    # Parties
    story.append(Paragraph("ENTRE LES SOUSSIGNÉS", section_style))
    story.append(Paragraph(
        f"<b>L'Employeur :</b> {data['emp_nom']}, demeurant {data['emp_adresse']}, "
        f"numéro employeur CESU/PAJEMPLOI : {data['emp_numero_cesu']},<br/>"
        f"ci-après dénommé « l'Employeur »,",
        body_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"<b>Le Salarié :</b> {data['sal_nom']}, né(e) le {data['sal_ddn']}, "
        f"demeurant {data['sal_adresse']}"
        + (f", numéro de sécurité sociale : {data['sal_nss']}" if data['sal_nss'] else "") +
        ",<br/>ci-après dénommé(e) « le Salarié »,",
        body_style))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("IL A ÉTÉ CONVENU CE QUI SUIT :", section_style))

    # Articles
    articles = [
        ("Article 1 — Nature du contrat",
         f"Le présent contrat est conclu pour une durée indéterminée (CDI) à compter du "
         f"<b>{data['date_debut']}</b>, sous réserve d'une période d'essai définie à l'article 2."),
        ("Article 2 — Période d'essai",
         f"Le présent contrat est soumis à une période d'essai de <b>{data['essai_duree']}</b> "
         f"à compter de la date de prise d'effet. Durant cette période, chacune des parties peut "
         f"mettre fin au contrat sans préavis ni indemnité, sauf accord différent entre les parties."),
        ("Article 3 — Lieu de travail",
         f"Le Salarié exercera ses fonctions principalement à l'adresse suivante : "
         f"<b>{data['lieu_travail']}</b>."),
        ("Article 4 — Fonctions et tâches",
         f"Le Salarié est engagé en qualité d'<b>employé(e) de maison</b>. Ses tâches comprennent "
         f"notamment : {data['taches']}. Cette liste n'est pas exhaustive et pourra être complétée "
         f"par accord des parties."),
        ("Article 5 — Durée du travail",
         f"La durée hebdomadaire de travail est fixée à <b>{data['heures_semaine']}</b>, répartie "
         f"comme suit : {data['repartition']}. Toute modification des horaires fera l'objet d'un "
         f"accord écrit entre les parties avec un délai de prévenance raisonnable."),
        ("Article 6 — Rémunération",
         f"Le Salarié percevra un salaire brut horaire de <b>{data['salaire_brut_horaire']} €</b>, "
         f"soit un salaire brut mensuel de <b>{data['salaire_brut_mensuel']} €</b> "
         f"(net estimatif : {data['salaire_net_mensuel']} €). "
         f"Ce salaire est payé mensuellement et déclaré via le portail CESU/PAJEMPLOI de l'URSSAF."),
        ("Article 7 — Congés payés",
         "Le Salarié bénéficie de congés payés à raison de 2,5 jours ouvrables par mois de travail "
         "effectif, conformément aux dispositions légales et conventionnelles. L'indemnité de congés "
         "payés est versée au choix des parties soit lors de la prise effective des congés, soit "
         "mensuellement sous forme d'une indemnité compensatrice égale à 10% de la rémunération "
         "brute totale."),
        ("Article 8 — Convention collective",
         "Le présent contrat est soumis aux dispositions de la <b>Convention Collective Nationale "
         "des Salariés du Particulier Employeur (IDCC 2111)</b> et à ses avenants en vigueur."),
        ("Article 9 — Mutuelle",
         "Le Salarié bénéficiera de la couverture complémentaire santé obligatoire prévue par la "
         "CCN 2111, organisée auprès d'Ipsec (ipsec.fr). L'Employeur prend en charge 50% minimum "
         "de la cotisation."),
        ("Article 10 — Rupture du contrat",
         "La rupture du présent contrat est soumise aux dispositions légales et conventionnelles "
         "applicables (démission, rupture conventionnelle homologuée, licenciement). Les préavis "
         "applicables sont ceux prévus par la CCN 2111."),
    ]

    for title, content in articles:
        story.append(Paragraph(title, section_style))
        story.append(Paragraph(content, body_style))
        story.append(Spacer(1, 0.3*cm))

    # Signatures
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Fait à _________________, le {data['date_generation']}, en deux exemplaires originaux.", body_style))
    story.append(Spacer(1, 0.8*cm))

    sig_data = [
        ["L'Employeur", "Le/La Salarié(e)"],
        [f"{data['emp_nom']}", f"{data['sal_nom']}"],
        ["(Signature précédée de la mention\n« Lu et approuvé »)", "(Signature précédée de la mention\n« Lu et approuvé »)"],
        ["\n\n\n__________________", "\n\n\n__________________"],
    ]
    sig_table = Table(sig_data, colWidths=[8*cm, 8*cm])
    sig_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(sig_table)

    doc.build(story)
    return filename


if __name__ == "__main__":
    data = collect_data()
    filename = build_pdf(data)
    print(f"\n✓ Contrat généré : {filename}")
    print("  → Imprimer en 2 exemplaires, signer et conserver un exemplaire chacun.")
