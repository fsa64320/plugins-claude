#!/usr/bin/env python3
"""
Génère un formulaire de rupture conventionnelle pré-rempli (substitut au CERFA 14598*01).
Le document généré est à imprimer, signer et soumettre via TéléRC pour homologation.
Prérequis : pip install reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime, timedelta
import math


def ask(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip() if default else input(f"{prompt} : ").strip()
    return val if val else default


def add_jours_calendaires(date_str, nb_jours):
    """Ajoute nb_jours calendaires à une date JJ/MM/AAAA."""
    try:
        d = datetime.strptime(date_str, "%d/%m/%Y")
        result = d + timedelta(days=nb_jours)
        return result.strftime("%d/%m/%Y")
    except ValueError:
        return "À calculer"


def add_jours_ouvrables(date_str, nb_jours):
    """Ajoute nb_jours ouvrables (hors samedi/dimanche) à une date."""
    try:
        d = datetime.strptime(date_str, "%d/%m/%Y")
        count = 0
        while count < nb_jours:
            d += timedelta(days=1)
            if d.weekday() < 5:  # lundi à vendredi
                count += 1
        return d.strftime("%d/%m/%Y")
    except ValueError:
        return "À calculer"


def calc_indemnite(anciennete_annees, salaire_brut_ref):
    """Calcule l'indemnité légale minimale de rupture conventionnelle."""
    try:
        s = float(salaire_brut_ref.replace(",", ".").replace(" ", ""))
        # 1/4 de mois par année pour les 10 premières années
        if anciennete_annees <= 10:
            indemnite = s * (1/4) * anciennete_annees
        else:
            indemnite = s * (1/4) * 10 + s * (1/3) * (anciennete_annees - 10)
        return round(indemnite, 2)
    except ValueError:
        return None


def collect_data():
    print("\n=== Rupture Conventionnelle — Formulaire CERFA 14598*01 (substitut) ===\n")
    data = {}

    print("-- Employeur (particulier) --")
    data["emp_nom"] = ask("Nom et prénom de l'employeur")
    data["emp_adresse"] = ask("Adresse complète")
    data["emp_tel"] = ask("Téléphone")
    data["emp_numero_cesu"] = ask("N° employeur CESU/PAJEMPLOI")

    print("\n-- Salarié --")
    data["sal_nom"] = ask("Nom et prénom du salarié")
    data["sal_ddn"] = ask("Date de naissance (JJ/MM/AAAA)")
    data["sal_adresse"] = ask("Adresse complète")
    data["sal_nss"] = ask("N° de sécurité sociale")
    data["sal_emploi"] = ask("Emploi occupé", "Employé(e) de maison")
    data["sal_date_entree"] = ask("Date d'entrée dans l'entreprise (JJ/MM/AAAA)")

    print("\n-- Convention --")
    data["date_signature"] = ask("Date de signature de la convention (JJ/MM/AAAA)",
                                  datetime.now().strftime("%d/%m/%Y"))

    # Calcul automatique des délais
    fin_retractation = add_jours_calendaires(data["date_signature"], 16)  # J+15 calendaires, expiration le 16
    data["fin_retractation"] = fin_retractation
    date_rupture_min = add_jours_ouvrables(fin_retractation, 15)
    # La date effective doit être au lendemain de l'homologation
    date_rupture_proposee = add_jours_calendaires(date_rupture_min, 1)
    data["date_rupture_proposee"] = date_rupture_proposee

    print(f"\n  → Fin du délai de rétractation (15 j calendaires) : {fin_retractation}")
    print(f"  → Date de rupture minimale possible                : {date_rupture_proposee}")

    date_rupture = ask(f"\nDate envisagée de rupture", date_rupture_proposee)
    data["date_rupture"] = date_rupture

    print("\n-- Indemnité de rupture conventionnelle --")
    data["sal_brut_ref"] = ask("Salaire brut mensuel de référence (€)")

    # Calcul ancienneté
    try:
        entree = datetime.strptime(data["sal_date_entree"], "%d/%m/%Y")
        signature = datetime.strptime(data["date_signature"], "%d/%m/%Y")
        anciennete_jours = (signature - entree).days
        anciennete_annees = anciennete_jours / 365.25
        indemnite_min = calc_indemnite(anciennete_annees, data["sal_brut_ref"])
        data["anciennete_str"] = f"{int(anciennete_annees)} an(s) et {int((anciennete_annees % 1) * 12)} mois"
        if indemnite_min:
            print(f"\n  → Ancienneté estimée : {data['anciennete_str']}")
            print(f"  → Indemnité légale minimale : {indemnite_min:.2f} €")
            data["indemnite_min"] = f"{indemnite_min:.2f}"
        else:
            data["anciennete_str"] = "À calculer"
            data["indemnite_min"] = "À calculer"
    except ValueError:
        data["anciennete_str"] = "À calculer"
        data["indemnite_min"] = "À calculer"

    data["indemnite"] = ask(f"Montant de l'indemnité spécifique brute (€)", data["indemnite_min"])
    data["date_generation"] = datetime.now().strftime("%d/%m/%Y")
    return data


def build_pdf(data):
    filename = f"convention_rupture_{data['sal_nom'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    s = getSampleStyleSheet()
    title_s = ParagraphStyle("t", parent=s["Heading1"], alignment=TA_CENTER, fontSize=13)
    subtitle_s = ParagraphStyle("st", parent=s["Normal"], alignment=TA_CENTER, fontSize=9, textColor=colors.grey)
    body_s = ParagraphStyle("b", parent=s["Normal"], fontSize=10, leading=16, alignment=TA_JUSTIFY)
    section_s = ParagraphStyle("sec", parent=s["Heading2"], fontSize=10, spaceAfter=4, spaceBefore=10)
    center_s = ParagraphStyle("c", parent=s["Normal"], alignment=TA_CENTER, fontSize=10)
    warning_s = ParagraphStyle("w", parent=body_s, backColor=colors.lightyellow,
                                borderPad=6, borderWidth=1, borderColor=colors.orange, fontSize=9)

    story = []

    story.append(Paragraph("CONVENTION DE RUPTURE CONVENTIONNELLE", title_s))
    story.append(Paragraph("(Substitut au formulaire CERFA 14598*01 — À soumettre via TéléRC pour homologation officielle)", subtitle_s))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "⚠️ Ce document est généré à titre de préparation. La demande d'homologation officielle "
        "doit être soumise via <b>rupture-conventionnelle.travail.gouv.fr</b> (TéléRC) "
        "ou par courrier recommandé AR à la DREETS compétente.", warning_s))
    story.append(Spacer(1, 0.4*cm))

    # Bloc parties
    story.append(Paragraph("I. PARTIES À LA CONVENTION", section_s))
    parties_data = [
        ["EMPLOYEUR (particulier)", "SALARIÉ(E)"],
        [f"Nom : {data['emp_nom']}", f"Nom : {data['sal_nom']}"],
        [f"Adresse : {data['emp_adresse']}", f"Adresse : {data['sal_adresse']}"],
        [f"Tél. : {data['emp_tel']}", f"Date de naissance : {data['sal_ddn']}"],
        [f"N° CESU/PAJEMPLOI : {data['emp_numero_cesu']}", f"N° SS : {data['sal_nss']}"],
        ["", f"Emploi : {data['sal_emploi']}"],
        ["", f"Entrée le : {data['sal_date_entree']}"],
    ]
    pt = Table(parties_data, colWidths=[8*cm, 8*cm])
    pt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(pt)
    story.append(Spacer(1, 0.4*cm))

    # Bloc convention
    story.append(Paragraph("II. TERMES DE LA CONVENTION", section_s))
    story.append(Paragraph(
        f"Les parties ont convenu d'une rupture conventionnelle du contrat de travail à durée "
        f"indéterminée, conformément aux articles L.1237-11 à L.1237-16 du Code du travail.", body_s))
    story.append(Spacer(1, 0.3*cm))

    conv_data = [
        ["Date de signature de la convention", data["date_signature"]],
        ["Date de fin du délai de rétractation (15 jours calendaires)", data["fin_retractation"]],
        ["Date envisagée de rupture du contrat", data["date_rupture"]],
        ["Ancienneté du salarié", data["anciennete_str"]],
        ["Indemnité spécifique de rupture conventionnelle (brut, €)", data["indemnite"]],
    ]
    ct = Table(conv_data, colWidths=[10*cm, 6*cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(ct)
    story.append(Spacer(1, 0.4*cm))

    # Délai de rétractation
    story.append(Paragraph("III. DÉLAI DE RÉTRACTATION", section_s))
    story.append(Paragraph(
        f"Chaque partie dispose d'un délai de <b>15 jours calendaires</b> à compter du lendemain "
        f"de la signature (soit jusqu'au <b>{data['fin_retractation']}</b>) pour se rétracter, "
        f"par lettre recommandée avec accusé de réception adressée à l'autre partie. "
        f"Passé ce délai, la demande d'homologation sera déposée.", body_s))
    story.append(Spacer(1, 0.3*cm))

    # Homologation
    story.append(Paragraph("IV. HOMOLOGATION", section_s))
    story.append(Paragraph(
        "À l'expiration du délai de rétractation, la demande d'homologation sera déposée auprès "
        "de la DREETS compétente via le portail TéléRC. La DREETS dispose d'un délai de "
        "<b>15 jours ouvrables</b> pour instruire la demande. L'absence de réponse vaut "
        "homologation tacite. La rupture ne peut intervenir qu'au lendemain de l'homologation.", body_s))
    story.append(Spacer(1, 0.5*cm))

    # Signatures
    story.append(Paragraph("V. SIGNATURES", section_s))
    story.append(Paragraph(
        f"Fait en deux exemplaires originaux à _________________, le {data['date_generation']}.", body_s))
    story.append(Spacer(1, 0.8*cm))

    sig_data = [
        ["L'Employeur", "Le/La Salarié(e)"],
        [data["emp_nom"], data["sal_nom"]],
        ["(Lu et approuvé — signature)", "(Lu et approuvé — signature)"],
        ["Possibilité de se faire assister\npar un conseiller du salarié",
         "Possibilité de se faire assister\npar un conseiller du salarié"],
        ["\n\n__________________", "\n\n__________________"],
    ]
    sig_t = Table(sig_data, colWidths=[8*cm, 8*cm])
    sig_t.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(sig_t)

    doc.build(story)
    return filename


if __name__ == "__main__":
    data = collect_data()
    filename = build_pdf(data)
    print(f"\n✓ Convention générée : {filename}")
    print("\n  Étapes suivantes :")
    print(f"  1. Imprimer en 2 exemplaires et signer avec le/la salarié(e)")
    print(f"  2. Attendre la fin du délai de rétractation : {data['fin_retractation']}")
    print(f"  3. Soumettre la demande d'homologation sur rupture-conventionnelle.travail.gouv.fr")
    print(f"  4. Date de rupture envisagée : {data['date_rupture']}")
