from pathlib import Path
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUT = Path(__file__).with_name("My_CV_updated.pdf")

BODY_SIZE = 11.2
BODY_LEADING = 13.4
SMALL_SIZE = 10.8


def e(text):
    return escape(text, quote=False)


def bold(text):
    return f"<b>{e(text)}</b>"


def italic(text):
    return f"<i>{e(text)}</i>"


def link(text, href):
    return f'<link href="{href}">{e(text)}</link>'


styles = {
    "name": ParagraphStyle(
        "name",
        fontName="Times-Bold",
        fontSize=25,
        leading=29,
        alignment=TA_CENTER,
        spaceAfter=4,
    ),
    "contact": ParagraphStyle(
        "contact",
        fontName="Times-Roman",
        fontSize=10.9,
        leading=13,
        alignment=TA_CENTER,
        spaceAfter=18,
    ),
    "section": ParagraphStyle(
        "section",
        fontName="Times-Bold",
        fontSize=14,
        leading=16,
        alignment=TA_LEFT,
        spaceBefore=9,
        spaceAfter=2,
    ),
    "body": ParagraphStyle(
        "body",
        fontName="Times-Roman",
        fontSize=BODY_SIZE,
        leading=BODY_LEADING,
        alignment=TA_LEFT,
    ),
    "body_right": ParagraphStyle(
        "body_right",
        fontName="Times-Italic",
        fontSize=BODY_SIZE,
        leading=BODY_LEADING,
        alignment=TA_RIGHT,
    ),
    "body_bold": ParagraphStyle(
        "body_bold",
        fontName="Times-Bold",
        fontSize=BODY_SIZE,
        leading=BODY_LEADING,
        alignment=TA_LEFT,
    ),
    "detail": ParagraphStyle(
        "detail",
        fontName="Times-Roman",
        fontSize=BODY_SIZE,
        leading=BODY_LEADING,
        leftIndent=18,
    ),
    "bullet": ParagraphStyle(
        "bullet",
        fontName="Times-Roman",
        fontSize=BODY_SIZE,
        leading=BODY_LEADING,
        leftIndent=14,
        firstLineIndent=-14,
        spaceAfter=4.8,
    ),
    "award_bullet": ParagraphStyle(
        "award_bullet",
        fontName="Times-Roman",
        fontSize=BODY_SIZE,
        leading=BODY_LEADING,
        leftIndent=14,
        firstLineIndent=-14,
        spaceAfter=4.0,
    ),
    "skills": ParagraphStyle(
        "skills",
        fontName="Times-Roman",
        fontSize=BODY_SIZE,
        leading=BODY_LEADING,
        spaceAfter=1.5,
    ),
}


def section(title):
    return KeepTogether(
        [
            Paragraph(e(title), styles["section"]),
            HRFlowable(width="100%", thickness=0.7, color=colors.black, spaceBefore=0, spaceAfter=6),
        ]
    )


def role_entry(title, dates, detail):
    data = [
        [
            Paragraph("- " + bold(title), styles["body_bold"]),
            Paragraph(e(dates), styles["body_right"]),
        ],
        [Paragraph(e(detail), styles["detail"]), ""],
    ]
    table = Table(data, colWidths=[4.95 * inch, 1.85 * inch], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("SPAN", (0, 1), (1, 1)),
            ]
        )
    )
    return table


def bullet(markup, style_name="bullet"):
    return Paragraph("- " + markup, styles[style_name])


def pub(authors, title, venue, tail=""):
    return bullet(f"{authors}. {italic(title)}. {venue}{e(tail)}")


story = []
story.append(Paragraph("YUE CAO", styles["name"]))
story.append(
    Paragraph(
        "caoyppsp@gmail.com&nbsp;&nbsp;&bull;&nbsp;&nbsp;"
        + link("https://yuec15.github.io", "https://yuec15.github.io")
        + "&nbsp;&nbsp;&bull;&nbsp;&nbsp;"
        + link(
            "Google Scholar",
            "https://scholar.google.com/citations?hl=en&user=bcPdM7MAAAAJ&view_op=list_works",
        )
        + "&nbsp;&nbsp;&bull;&nbsp;&nbsp;"
        + link("LinkedIn", "https://www.linkedin.com/in/yuecao94/"),
        styles["contact"],
    )
)

story.append(section("PROFESSIONAL EXPERIENCE"))
story.append(role_entry("Meta MSL Lab", "Mar. 2022 - Present", "AI Research Scientist"))
story.append(Spacer(1, 12))

story.append(section("EDUCATION"))
story.append(role_entry("Texas A&M University", "Sep. 2016 - Dec. 2021", "Ph.D. in Electrical Engineering"))
story.append(Spacer(1, 5))
story.append(
    role_entry(
        "University of Science and Technology of China",
        "Sep. 2012 - June 2016",
        "B.S. in Applied Physics",
    )
)
story.append(Spacer(1, 12))

story.append(section("RESEARCH INTERESTS & EXPERIENCE"))
story.append(
    Paragraph(
        f"{bold('Interests:')} My research focuses on agentic post-training, "
        "including multi-agents, vertical agentic applications, and AI for science.",
        styles["skills"],
    )
)
story.append(Spacer(1, 4))
story.append(Paragraph(bold("Experience:"), styles["skills"]))
story.append(
    bullet(
        f"{bold('Avocado (Muse Spark)')}: Tech lead for agentic vertical ability, model product behaviour. "
        "Core contributor to multi-agents and visual coding.",
        style_name="award_bullet",
    )
)
story.append(
    bullet(
        f"{bold('Llama3')}: Core contributor to tool-use capabilities and safety.",
        style_name="award_bullet",
    )
)
story.append(
    bullet(
        f"{bold('AI for Science')}: LLM for protein design and docking.",
        style_name="award_bullet",
    )
)
story.append(Spacer(1, 10))

story.append(section("PUBLICATIONS"))
publications = [
    (
        f"A. Grattafiori and other authors including {bold('Y. Cao')}",
        "The Llama 3 Herd of Models",
        bold("arXiv preprint"),
        " arXiv:2407.21783, 2024.",
    ),
    (
        f"Y. You, {bold('Y. Cao')}, T. Chen, Z. Wang, and Y. Shen",
        "Bayesian Modeling and Uncertainty Quantification for Learning to Optimize: What, Why, and How",
        bold("International Conference on Learning Representations"),
        ", 2021.",
    ),
    (
        f"{bold('Y. Cao')}, P. Das, V. Chenthamarakshan, P. Chen, I. Melnyk, and Y. Shen",
        "Fold2Seq: A Joint Sequence(1D)-Fold(3D) Embedding-based Generative Model for Protein Design",
        bold("International Conference on Machine Learning"),
        " 139, 1261-1271, 2021.",
    ),
    (
        f"{bold('Y. Cao')}, T. Chen, Z. Wang, and Y. Shen",
        "Learning to Optimize in Swarms",
        bold("Advances in Neural Information Processing Systems"),
        " 32, 15018-15028, 2019.",
    ),
    (
        f"{bold('Y. Cao')} and Y. Shen",
        "TALE: Transformer-based protein function Annotation with joint sequence-Label Embedding",
        bold("Bioinformatics"),
        " 37(18), 2825-2833, 2021.",
    ),
    (
        f"R. Taftaf and other authors including {bold('Y. Cao')}",
        "ICAM1 initiates CTC cluster formation and trans-endothelial migration in lung metastasis of breast cancer",
        bold("Nature Communications"),
        " 12, 4867, 2021.",
    ),
    (
        f"{bold('Y. Cao')} and Y. Shen",
        "Bayesian Active Learning for Optimization and Uncertainty Quantification in Protein Docking",
        bold("Journal of Chemical Theory and Computation"),
        " 16(8), 5334-5347, 2020.",
    ),
    (
        f"{bold('Y. Cao')} and Y. Shen",
        "Energy-based Graph Convolutional Networks for Scoring Protein Docking Models",
        bold("Proteins: Structure, Function, and Bioinformatics"),
        " 88(8), 1091-1099, 2020.",
    ),
    (
        f"M. Karimi*, S. Zhu*, {bold('Y. Cao')}* and Y. Shen",
        "De Novo Protein Design for Novel Folds Using Guided Conditional Wasserstein Generative Adversarial Networks",
        bold("Journal of Chemical Information and Modeling"),
        " 60(12), 5667-5681, 2020.",
    ),
    (
        f"{bold('Y. Cao')}, Y. Sun, M. Karimi, H. Chen, O. Moronfoye, and Y. Shen",
        "Predicting Pathogenicity of Missense Variants with Weakly Supervised Regression",
        bold("Human Mutation"),
        " 40(9), 1579-1592, 2019.",
    ),
    (
        f"M. Kawaguchi, N. Dashzeveg, {bold('Y. Cao')}, Y. Jia, X. Liu, Y. Shen, and H. Liu",
        "Extracellular Domains I and II of cell-surface glycoprotein CD44 mediate its trans-homophilic dimerization and tumor cluster aggregation",
        bold("Journal of Biological Chemistry"),
        " 295(9), 2640-2649, 2020.",
    ),
    (
        f"X. Liu and other authors including {bold('Y. Cao')}",
        "Homophilic CD44 Interactions Mediate Tumor Cell Aggregation and Polyclonal Metastasis in Patient-derived Breast Cancer Models",
        bold("Cancer Discovery"),
        " 9(1), 96-113, 2019.",
    ),
    (
        f"M. S. Cline, G. Babbi, S. Bonache, {bold('Y. Cao')}, et al",
        "Assessment of blind predictions of the clinical significance of BRCA1 and BRCA2 variants",
        bold("Human Mutation"),
        " 40(9), 1546-1556, 2019.",
    ),
    (
        f"M. Lensink and other authors including {bold('Y. Cao')}",
        "Blind prediction of Homo- and Hetero- Protein Complexes: The CASP13-CAPRI Experiment",
        bold("Proteins: Structure, Function, and Bioinformatics"),
        " 87(12), 1200-1221, 2019.",
    ),
    (
        f"A. Voskanian and other authors including {bold('Y. Cao')}",
        "Assessing the Performance of in-silico Methods for Predicting the Pathogenicity of Variants in the Gene CHEK2 among Hispanic Females with Breast Cancer",
        bold("Human Mutation"),
        " 40(9), 1612-1622, 2019.",
    ),
]
for item in publications:
    story.append(pub(*item))

story.append(Spacer(1, 8))
story.append(section("AWARDS AND HONORS"))
awards = [
    "Received the NeurIPS Travel Award. Oct. 2019",
    "Received the NIH-funded CAGI Travel Fellowship. Nov. 2019",
    "Our team (Y. Cao and Y. Shen) ranked the 2nd among 26 groups for difficult targets in the 3rd joint CASP-CAPRI (Critical Assessment of protein Structure Prediction and Critical Assessment of PRedicted Interactions), a community-wide experiment on comparative evaluation of protein structure prediction and protein docking methods. Apr. 2019",
    "Our team (Y. Cao and Y. Shen) ranked the 3rd/51 for difficult targets in the 7th CAPRI (Critical Assessment of PRedicted Interactions), 2017-2019",
    "Received the First-class Award for Excellent Students in University of Science and Technology of China. Sep. 2015",
    "Bronze Medal in the 4th Asia-Pacific Informatics Olympiad. May 2010",
    "First-class Award in the National Olympiad in Physics in China. Nov. 2011",
    "First-class Award in the National Olympiad in Informatics in China. Nov. 2011",
    "First-class Award in the National Olympiad in Informatics in China. Dec. 2010",
    "First-class Award in the National Olympiad in Informatics in China. Dec. 2009",
]
for item in awards:
    story.append(bullet(e(item), style_name="award_bullet"))

story.append(Spacer(1, 8))
story.append(section("INVITED PRESENTATIONS"))
presentations = [
    f"{bold('Y. Cao')}, T. Chen, Z. Wang, Y. Shen. {italic('Learning to Optimize in Swarms')}. {italic('(Poster)')} {bold('Advances in Neural Information Processing Systems (NeurIPS)')}, Dec. 2019, Vancouver, Canada.",
    f"{bold('Y. Cao')}, Y. Sun, M. Karimi, H. Chen, O. Moronfoye, and Y. Shen. {italic('Predicting Pathogenicity of Missense Variants with Weakly Supervised Regression')}. {bold('Critical Assessment of Genome Interpretation (CAGI) Workshop')}, Dec. 2019, San Francisco, USA.",
    f"{bold('Y. Cao')} and Y. Shen. {italic('Bayesian Active Learning for Optimization and Uncertainty Quantification in Protein Docking')} {italic('(Presented by Yang Shen)')}. {bold('Intelligent Systems for Molecular Biology (ISMB)')}, July 2019, Basel, Switzerland.",
    f"M. Karimi*, S. Zhu*, {bold('Y. Cao')}* and Y. Shen. {italic('De Novo Protein Design of Novel Folds using Guided Conditional Generative Adversarial Networks (gcWGAN)')} {italic('(Poster)')}. {bold('Intelligent Systems for Molecular Biology (ISMB)')}, July 2019, Basel, Switzerland.",
    f"{bold('Y. Cao')} and Y. Shen. {italic('Bayesian Active Learning for Optimization and Uncertainty Quantification in Protein Docking')} {italic('(Presented by Yang Shen)')}. {bold('7th CAPRI Evaluation Meeting')}, April 2019, Hinxton, UK.",
    f"{bold('Y. Cao')} and Y. Shen. {italic('Bayesian Active Learning for Optimization and Uncertainty Quantification in Protein Docking')} {italic('(Poster)')}. {bold('Modeling of Protein Interaction (MPI)')}, November 2018, Lawrence, KS, USA.",
    f"{bold('Y. Cao')} and Y. Shen. {italic('Bayesian Active Learning for Optimization and Uncertainty Quantification in Protein Docking')} {italic('(Poster)')}. {bold('Bioinformatics and Cancer Symposium')}, Sep. 2018, College Station, TX, USA.",
]
for item in presentations:
    story.append(bullet(item, style_name="award_bullet"))

story.append(Spacer(1, 8))
story.append(section("TECHNICAL SKILLS"))
skills = [
    (bold("Programming Languages:"), "Python, C++, Bash Scripts"),
    (bold("Deep Learning Frameworks:"), "PyTorch, TensorFlow"),
    (bold("Operating Systems:"), "Linux, Mac OS, Windows"),
    (bold("Other Computer Skills:"), "Git, PyMOL, LaTeX, CHARMM"),
]
for label, value in skills:
    story.append(Paragraph(f"{label} {e(value)}", styles["skills"]))


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.82 * inch,
        rightMargin=0.82 * inch,
        topMargin=0.58 * inch,
        bottomMargin=0.55 * inch,
    )
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    main()
