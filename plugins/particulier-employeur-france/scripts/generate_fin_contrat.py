#!/usr/bin/env python3
"""
Génère les 3 documents de fin de contrat pour rupture conventionnelle :
  1. Certificat de travail
  2. Reçu pour solde de tout compte
  3. Attestation France Travail (brouillon — à télédéclarer sur francetravail.fr)
Prérequis : pip install reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime, date


def ask(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip() if default else input(f"{prompt} : ").strip()
    return val if val else default


def collect_data():
    print("\n=== Documents de fin de contrat — Rupture Conventionnelle ===\n")
    data = {}

    print("-- Informations employeur --")
    data["emp_nom"] = ask("Nom et prénom de l'employeur")
    data["emp_adresse"] = ask("Adresse complète de l'employeur")
    data["emp_numero_cesu"] = ask("Numéro employeur CESU/PAJEMPLOI")

    print("\n-- Informations salarié --")
    data["sal_nom"] = ask("Nom et prénom du salarié")
    data["sal_ddn"] = ask("Date de naissance (JJ/MM/AAAA)")
    data["sal_adresse"] = ask("Adresse complète du salarié")
    data["sal_nss"] = ask("Numéro de sécurité sociale (15 chiffres)")
    data["sal_emploi"] = ask("Intitulé de l'emploi", "Employé(e) de maison")

    print("\n-- Dates du contrat --")
    data["date_entree"] = ask("Date d'entrée dans l'emploi (JJ/MM/AAAA)")
    data["date_rupture"] = ask("Date effective de rupture / dernier jour travaillé (JJ/MM/AAAA)")

    print("\n-- Éléments financiers du STC --")
    data["salaire_brut_ref"] = ask("Salaire brut mensuel de référence (€)")
    data["conges_non_pris"] = ask("Nombre de jours ouvrables de congés payés non soldés", "0")
    data["indemnite_rc"] = ask("Montant de l'indemnité de rupture conventionnelle (€)")
    data["autres_elements"] = ask("Autres éléments de rémunération (laisser vide si aucun)", "")

    data["date_generation"] = datetime.now().strftime("%d/%m/%Y")
    return data


def calc_stc(data):
    """Calcule les éléments du solde de tout compte."""
    try:
        brut = float(data["salaire_brut_ref"].replace(",", ".").replace(" ", ""))
        conges = float(data["conges_non_pris"].replace(",", "."))
        indemnite = float(data["indemnite_rc"].replace(",", ".").replace(" ", ""))

        # Indemnité compensatrice de CP = (salaire brut ref / 22 jours ouvrés) * nb jours
        indem_cp = round((brut / 22) * conges, 2)
        total_brut = round(brut + indem_cp + indemnite, 2)  # indemnité RC exonérée de charges

        return {
            "salaire_brut": f"{brut:.2f}",
            "indem_cp": f"{indem_cp:.2f}",
            "indemnite_rc": f"{indemnite:.2f}",
            "total": f"{total_brut:.2f}",
        }
    except ValueError:
        return {
            "salaire_brut": data["salaire_brut_ref"],
            "indem_cp": "À calculer",
            "indemnite_rc": data["indemnite_rc"],
            "total": "À calculer",
        }


def styles_base():
    s = getSampleStyleSheet()
    title = ParagraphStyle("title", parent=s["Heading1"], alignment=TA_CENTER, fontSize=13, spaceAfter=10)
    body = ParagraphStyle("body", parent=s["Normal"], fontSize=10, leading=16, alignment=TA_JUSTIFY)
    section = ParagraphStyle("section", parent=s["Heading2"], fontSize=11, spaceAfter=4, spaceBefore=12)
    center = ParagraphStyle("center", parent=s["Normal"], alignment=TA_CENTER, fontSize=10)
    bold = ParagraphStyle("bold", parent=s["Normal"], fontSize=10, leading=14)
    return title, body, section, center, bold


# ── Document 1 : Certificat de travail ───────────────────────────────────────

def build_certificat(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=2.5*cm, leftMargin=2.5*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm)
    title_s, body_s, section_s, center_s, bold_s = styles_base()
    story = []

    story.append(Paragraph("CERTIFICAT DE TRAVAIL", title_s))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        f"Je soussigné(e) <b>{data['emp_nom']}</b>, demeurant {data['emp_adresse']}, "
        f"numéro employeur CESU/PAJEMPLOI : {data['emp_numero_cesu']}, "
        f"certifie que :", body_s))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph(
        f"<b>{data['sal_nom']}</b>, né(e) le {data['sal_ddn']}, "
        f"demeurant {data['sal_adresse']},", body_s))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        f"a été employé(e) en qualité de <b>{data['sal_emploi']}</b> "
        f"du <b>{data['date_entree']}</b> au <b>{data['date_rupture']}</b>.", body_s))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "Le présent contrat a pris fin par <b>rupture conventionnelle homologuée</b> "
        "par la DREETS compétente.", body_s))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "Ce certificat est délivré à l'intéressé(e) pour lui servir et valoir ce que de droit.",
        body_s))

    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        f"Fait à _________________, le {data['date_generation']}", center_s))
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph(f"Signature de l'employeur : {data['emp_nom']}", body_s))
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("__________________________", center_s))

    doc.build(story)


# ── Document 2 : Reçu pour solde de tout compte ──────────────────────────────

def build_stc(data, filename):
    stc = calc_stc(data)
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=2.5*cm, leftMargin=2.5*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm)
    title_s, body_s, section_s, center_s, bold_s = styles_base()
    story = []

    story.append(Paragraph("REÇU POUR SOLDE DE TOUT COMPTE", title_s))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph(
        f"<b>Employeur :</b> {data['emp_nom']}, {data['emp_adresse']}<br/>"
        f"<b>N° CESU/PAJEMPLOI :</b> {data['emp_numero_cesu']}", body_s))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"<b>Salarié(e) :</b> {data['sal_nom']}, né(e) le {data['sal_ddn']}<br/>"
        f"<b>Adresse :</b> {data['sal_adresse']}<br/>"
        f"<b>N° SS :</b> {data['sal_nss']}<br/>"
        f"<b>Emploi occupé :</b> {data['sal_emploi']}", body_s))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"Période d'emploi : du <b>{data['date_entree']}</b> au <b>{data['date_rupture']}</b>.<br/>"
        f"Motif de rupture : rupture conventionnelle homologuée.", body_s))

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Détail des sommes versées :", section_s))

    table_data = [
        ["Élément", "Montant brut (€)"],
        [f"Dernier salaire brut (mois en cours, prorata)", stc["salaire_brut"]],
        [f"Indemnité compensatrice de congés payés ({data['conges_non_pris']} jours)", stc["indem_cp"]],
        ["Indemnité spécifique de rupture conventionnelle (exonérée de charges)", stc["indemnite_rc"]],
    ]
    if data["autres_elements"]:
        table_data.append([data["autres_elements"], "À préciser"])
    table_data.append(["TOTAL", stc["total"]])

    t = Table(table_data, colWidths=[11*cm, 4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightyellow),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Le présent reçu est établi en deux exemplaires. Le/la salarié(e) dispose d'un délai "
        "de <b>6 mois</b> à compter de sa signature pour le dénoncer par lettre recommandée "
        "avec accusé de réception.", body_s))

    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph(f"Fait à _________________, le {data['date_generation']}", center_s))
    story.append(Spacer(1, 0.8*cm))

    sig_data = [
        ["Signature de l'employeur", "Signature du/de la salarié(e)"],
        [data["emp_nom"], data["sal_nom"]],
        ["(précédée de « Reçu pour\nsolde de tout compte »)", "(précédée de « Reçu pour\nsolde de tout compte »)"],
        ["\n\n__________________", "\n\n__________________"],
    ]
    sig_t = Table(sig_data, colWidths=[8*cm, 8*cm])
    sig_t.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("FONTSIZE", (0, 0), (-1, -1), 9)]))
    story.append(sig_t)

    doc.build(story)


# ── Document 3 : Attestation France Travail (brouillon) ──────────────────────

def build_attestation_ft(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=2.5*cm, leftMargin=2.5*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm)
    title_s, body_s, section_s, center_s, bold_s = styles_base()
    story = []

    story.append(Paragraph("ATTESTATION EMPLOYEUR — FRANCE TRAVAIL", title_s))
    story.append(Paragraph("(Brouillon de préparation — Télédéclarer sur francetravail.fr)", center_s))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Spacer(1, 0.4*cm))

    warning = ParagraphStyle("warning", parent=body_s, backColor=colors.lightyellow,
                             borderPad=6, borderWidth=1, borderColor=colors.orange)
    story.append(Paragraph(
        "⚠️ Ce document est un brouillon de préparation uniquement. L'attestation officielle "
        "DOIT être télédéclarée sur francetravail.fr (espace employeur) ou via le formulaire "
        "cerfa n°14693 pour être valide auprès de France Travail.", warning))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("1. Informations sur l'employeur", section_s))
    story.append(Paragraph(
        f"Nom/Raison sociale : {data['emp_nom']}<br/>"
        f"Adresse : {data['emp_adresse']}<br/>"
        f"N° employeur CESU/PAJEMPLOI : {data['emp_numero_cesu']}<br/>"
        f"Type d'employeur : Particulier employeur", body_s))

    story.append(Paragraph("2. Informations sur le salarié", section_s))
    story.append(Paragraph(
        f"Nom et prénom : {data['sal_nom']}<br/>"
        f"Date de naissance : {data['sal_ddn']}<br/>"
        f"Adresse : {data['sal_adresse']}<br/>"
        f"N° de sécurité sociale : {data['sal_nss']}", body_s))

    story.append(Paragraph("3. Emploi et contrat", section_s))
    story.append(Paragraph(
        f"Emploi occupé : {data['sal_emploi']}<br/>"
        f"Type de contrat : CDI<br/>"
        f"Date d'embauche : {data['date_entree']}<br/>"
        f"Date de fin de contrat : {data['date_rupture']}<br/>"
        f"Motif de fin de contrat : <b>Rupture conventionnelle homologuée</b>", body_s))

    story.append(Paragraph("4. Rémunération de référence", section_s))
    story.append(Paragraph(
        f"Salaire brut mensuel de référence : {data['salaire_brut_ref']} €<br/>"
        f"(Calculé sur les 12 derniers mois ou les 3 derniers mois, selon le plus favorable)", body_s))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Le salarié peut prétendre aux allocations chômage (ARE) à compter de la fin de son "
        "contrat de travail, sous réserve de remplir les conditions d'ouverture de droits auprès "
        "de France Travail.", body_s))

    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph(f"Fait à _________________, le {data['date_generation']}", center_s))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph(f"Signature de l'employeur : {data['emp_nom']}", body_s))
    story.append(Paragraph("__________________________", center_s))

    doc.build(story)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    data = collect_data()
    base = data['sal_nom'].replace(' ', '_')
    date_str = datetime.now().strftime('%Y%m%d')

    f1 = f"certificat_travail_{base}_{date_str}.pdf"
    f2 = f"solde_tout_compte_{base}_{date_str}.pdf"
    f3 = f"attestation_ft_{base}_{date_str}.pdf"

    build_certificat(data, f1)
    build_stc(data, f2)
    build_attestation_ft(data, f3)

    print(f"\n✓ Documents générés :")
    print(f"  1. Certificat de travail      : {f1}")
    print(f"  2. Solde de tout compte       : {f2}")
    print(f"  3. Attestation France Travail : {f3} (brouillon — télédéclarer sur francetravail.fr)")
    print("\n  → Remettre les documents 1 et 2 signés au salarié le dernier jour de travail.")
    print("  → Télédéclarer l'attestation France Travail sur francetravail.fr.")
