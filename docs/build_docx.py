#!/usr/bin/env python3
"""
build_docx.py — Generate docs/INMT5526_Assignment.docx from assignment content.

Usage:
    python3 docs/build_docx.py

Requirements:
    pip install python-docx

The script embeds docs/assets/erd.png into Appendix A and renders all SQL
blocks in a monospaced (Courier New) style.
"""

import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ERD_PNG    = os.path.join(SCRIPT_DIR, "assets", "erd.png")
OUTPUT     = os.path.join(SCRIPT_DIR, "INMT5526_Assignment.docx")

# ── Style helpers ──────────────────────────────────────────────────────────

def set_font(run, name="Calibri", size=11, bold=False, italic=False, color=None):
    run.font.name   = name
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_heading(doc, text, level):
    p = doc.add_heading(text, level=level)
    return p


def add_body(doc, text):
    p = doc.add_paragraph(text)
    p.style = doc.styles["Normal"]
    for run in p.runs:
        set_font(run)
    return p


def add_code_block(doc, code):
    """Add a monospaced code block paragraph."""
    # Use Normal style then override font to Courier New
    p = doc.add_paragraph()
    p.style = doc.styles["Normal"]
    # Add a light grey shading to the paragraph
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F2F2F2")
    pPr.append(shd)
    run = p.add_run(code)
    set_font(run, name="Courier New", size=9)
    return p


def add_horizontal_rule(doc):
    """Add a thin horizontal rule (border on the bottom of a blank paragraph)."""
    p = doc.add_paragraph()
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"),   "single")
    bottom.set(qn("w:sz"),    "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "999999")
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


# ── SQL blocks ─────────────────────────────────────────────────────────────

DDL = """\
CREATE DATABASE fifo_db;
USE fifo_db;

CREATE TABLE Employee (
  employee_id INT AUTO_INCREMENT,
  name        VARCHAR(100) NOT NULL,
  role        VARCHAR(50),
  contact     VARCHAR(100),
  PRIMARY KEY (employee_id)
);

CREATE TABLE Site (
  site_id   INT AUTO_INCREMENT,
  site_name VARCHAR(100) NOT NULL,
  location  VARCHAR(100),
  PRIMARY KEY (site_id)
);

CREATE TABLE Room (
  room_id  INT AUTO_INCREMENT,
  capacity INT CHECK (capacity > 0),
  site_id  INT,
  PRIMARY KEY (room_id),
  FOREIGN KEY (site_id) REFERENCES Site(site_id)
);

CREATE TABLE Shift (
  shift_id   INT AUTO_INCREMENT,
  start_date DATE NOT NULL,
  end_date   DATE NOT NULL,
  PRIMARY KEY (shift_id)
);

CREATE TABLE Allocation (
  allocation_id INT AUTO_INCREMENT,
  employee_id   INT,
  room_id       INT,
  shift_id      INT,
  PRIMARY KEY (allocation_id),
  FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
  FOREIGN KEY (room_id)     REFERENCES Room(room_id),
  FOREIGN KEY (shift_id)    REFERENCES Shift(shift_id)
);\
"""

DML_INSERT = """\
INSERT INTO Employee (name, role, contact)
VALUES ('Alex Johnson', 'Engineer',   '0412 000 001'),
       ('Sarah Lee',    'Technician', '0412 000 002');

INSERT INTO Site (site_name, location)
VALUES ('Site A', 'Western Australia'),
       ('Site B', 'Western Australia');

INSERT INTO Room (capacity, site_id)
VALUES (2, 1),
       (1, 2);

INSERT INTO Shift (start_date, end_date)
VALUES ('2026-04-01', '2026-04-14'),
       ('2026-04-15', '2026-04-28');

INSERT INTO Allocation (employee_id, room_id, shift_id)
VALUES (1, 1, 1),
       (2, 2, 2);\
"""

QUERY_ALL = "SELECT * FROM Employee;"

QUERY_JOIN = """\
SELECT e.name,
       s.site_name,
       sh.start_date
FROM   Allocation a
JOIN   Employee e  ON a.employee_id = e.employee_id
JOIN   Room     r  ON a.room_id     = r.room_id
JOIN   Site     s  ON r.site_id     = s.site_id
JOIN   Shift    sh ON a.shift_id    = sh.shift_id;\
"""

QUERY_AGG1 = """\
SELECT site_id,
       COUNT(room_id) AS total_rooms
FROM   Room
GROUP BY site_id;\
"""

QUERY_AGG2 = """\
SELECT role,
       COUNT(*) AS total_employees
FROM   Employee
GROUP BY role;\
"""

APPENDIX_B_SQL = """\
-- ── Database setup ──────────────────────────────────────────────────────
CREATE DATABASE fifo_db;
USE fifo_db;

-- ── Table definitions ───────────────────────────────────────────────────
CREATE TABLE Employee (
  employee_id INT AUTO_INCREMENT,
  name        VARCHAR(100) NOT NULL,
  role        VARCHAR(50),
  contact     VARCHAR(100),
  PRIMARY KEY (employee_id)
);

CREATE TABLE Site (
  site_id   INT AUTO_INCREMENT,
  site_name VARCHAR(100) NOT NULL,
  location  VARCHAR(100),
  PRIMARY KEY (site_id)
);

CREATE TABLE Room (
  room_id  INT AUTO_INCREMENT,
  capacity INT CHECK (capacity > 0),
  site_id  INT,
  PRIMARY KEY (room_id),
  FOREIGN KEY (site_id) REFERENCES Site(site_id)
);

CREATE TABLE Shift (
  shift_id   INT AUTO_INCREMENT,
  start_date DATE NOT NULL,
  end_date   DATE NOT NULL,
  PRIMARY KEY (shift_id)
);

CREATE TABLE Allocation (
  allocation_id INT AUTO_INCREMENT,
  employee_id   INT,
  room_id       INT,
  shift_id      INT,
  PRIMARY KEY (allocation_id),
  FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
  FOREIGN KEY (room_id)     REFERENCES Room(room_id),
  FOREIGN KEY (shift_id)    REFERENCES Shift(shift_id)
);

-- ── Sample data ─────────────────────────────────────────────────────────
INSERT INTO Employee (name, role, contact)
VALUES ('Alex Johnson', 'Engineer',   '0412 000 001'),
       ('Sarah Lee',    'Technician', '0412 000 002');

INSERT INTO Site (site_name, location)
VALUES ('Site A', 'Western Australia'),
       ('Site B', 'Western Australia');

INSERT INTO Room (capacity, site_id)
VALUES (2, 1),
       (1, 2);

INSERT INTO Shift (start_date, end_date)
VALUES ('2026-04-01', '2026-04-14'),
       ('2026-04-15', '2026-04-28');

INSERT INTO Allocation (employee_id, room_id, shift_id)
VALUES (1, 1, 1),
       (2, 2, 2);

-- ── Queries ─────────────────────────────────────────────────────────────
-- All employees
SELECT * FROM Employee;

-- Employee allocation summary
SELECT e.name,
       s.site_name,
       sh.start_date
FROM   Allocation a
JOIN   Employee e  ON a.employee_id = e.employee_id
JOIN   Room     r  ON a.room_id     = r.room_id
JOIN   Site     s  ON r.site_id     = s.site_id
JOIN   Shift    sh ON a.shift_id    = sh.shift_id;

-- Rooms per site
SELECT site_id,
       COUNT(room_id) AS total_rooms
FROM   Room
GROUP BY site_id;

-- Employees per role
SELECT role,
       COUNT(*) AS total_employees
FROM   Employee
GROUP BY role;\
"""


# ── Document assembly ─────────────────────────────────────────────────────

def build():
    doc = Document()

    # ── Page margins (narrow) ──
    for section in doc.sections:
        section.top_margin    = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin   = Inches(1.25)
        section.right_margin  = Inches(1.25)

    # ── Title ──────────────────────────────────────────────────────────────
    title = doc.add_heading("INMT5526 Individual Assignment", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sub = doc.add_paragraph(
        "Business Intelligence  |  Semester 1, 2026  |  University of Western Australia"
    )
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in sub.runs:
        set_font(run, size=11, italic=True)

    doc.add_paragraph()  # spacer

    # ── 1. Introduction ────────────────────────────────────────────────────
    add_heading(doc, "1. Introduction", 1)
    add_body(doc, (
        "This report focuses on designing and implementing a database solution to address a "
        "business problem related to workforce and accommodation management in FIFO (Fly-In "
        "Fly-Out) operations. FIFO systems are commonly used in industries such as mining in "
        "Western Australia, where workers are transported to remote locations for specific time "
        "periods."
    ))
    add_body(doc, (
        "The main objective of this assignment is to apply database concepts learned in the "
        "first four topics of the unit, including entity-relationship modelling and SQL, to "
        "develop a structured solution. The report outlines the problem, explains the design "
        "process, presents the implementation and reflects on the effectiveness of the solution."
    ))

    add_horizontal_rule(doc)

    # ── 2. Background ──────────────────────────────────────────────────────
    add_heading(doc, "2. Background", 1)
    add_body(doc, (
        "FIFO operations involve managing multiple components at the same time, including "
        "employees, accommodation, shifts and site locations. In many organisations, this process "
        "is still handled using spreadsheets or basic systems, which can create several issues "
        "such as data duplication, errors and inefficiencies."
    ))
    add_body(doc, (
        "A key problem is the lack of a centralised and structured system to manage workforce "
        "allocation and accommodation. For example, employees may be assigned to overlapping "
        "shifts or rooms may be overbooked due to poor tracking. These issues can affect "
        "operational efficiency and increase costs."
    ))
    add_body(doc, (
        "Databases provide a more reliable solution because they allow data to be stored in a "
        "structured format and accessed efficiently. As discussed in the unit, databases are "
        "designed to organise data in a consistent way so that it can be retrieved and analysed "
        "to support decision-making (Date, 2003). Compared to spreadsheets, databases are more "
        "suitable when dealing with large amounts of data and multiple users."
    ))
    add_body(doc, (
        "The proposed solution is to develop a relational database system that stores information "
        "about employees, shifts, rooms and site locations. This system would allow managers to "
        "easily track which employees are assigned to which shifts and where they are staying."
    ))
    add_body(doc, (
        "This problem is worth solving because it improves coordination, reduces errors and "
        "supports better decision-making. From a business intelligence perspective, having "
        "structured and reliable data is essential for generating insights and making informed "
        "decisions (Kimball & Ross, 2013)."
    ))

    add_horizontal_rule(doc)

    # ── 3. Design ──────────────────────────────────────────────────────────
    add_heading(doc, "3. Design", 1)
    add_body(doc, (
        "The database design was developed using entity-relationship modelling, which is used to "
        "represent real-world objects as entities and define the relationships between them. An "
        "entity refers to something we store data about, such as an employee or a site, while "
        "attributes describe the properties of that entity (Chen, 1976)."
    ))

    add_heading(doc, "Entities and Attributes", 2)
    add_body(doc, (
        "The following five entities were identified for the system: Employee, Site, Room, "
        "Shift and Allocation. Each entity has a surrogate integer primary key (AUTO_INCREMENT) "
        "and a set of descriptive attributes. The Allocation entity acts as an associative "
        "(junction) table, holding foreign keys that link an Employee to a Room and a Shift for "
        "a given deployment period."
    ))

    add_heading(doc, "Relationships", 2)
    rels = [
        "A Site can contain multiple Rooms (one-to-many).",
        "An Employee can have multiple Allocations (one-to-many).",
        "A Room can be assigned to multiple Allocations over time (one-to-many).",
        "A Shift can include multiple employees through Allocations (one-to-many).",
    ]
    for rel in rels:
        p = doc.add_paragraph(rel, style="List Bullet")
        for run in p.runs:
            set_font(run)

    add_body(doc, (
        "These relationships reflect how FIFO operations function in reality and allow the "
        "system to store data efficiently without redundancy. The full entity-relationship "
        "diagram is provided in Appendix A."
    ))

    add_heading(doc, "Design Justification", 2)
    add_body(doc, (
        "The design follows normalisation principles, meaning that data is organised into "
        "separate tables to reduce redundancy. Each table represents a single entity and "
        "relationships are managed through foreign keys. This approach ensures data consistency "
        "and avoids duplication — for example, employee details are stored only once and "
        "referenced where needed."
    ))
    add_body(doc, (
        "Another important aspect of the design is planning before implementation. As highlighted "
        "in the lectures, designing the structure first helps avoid issues when writing SQL "
        "queries later (Elmasri & Navathe, 2016)."
    ))

    add_heading(doc, "Use of Unit Concepts", 2)
    concepts = [
        "Entity-relationship modelling (Topic 2)",
        "Primary and foreign keys (Topic 2)",
        "Normalisation to reduce redundancy (Topic 3)",
        "Planning before implementation (Topic 1)",
    ]
    for c in concepts:
        p = doc.add_paragraph(c, style="List Bullet")
        for run in p.runs:
            set_font(run)

    add_horizontal_rule(doc)

    # ── 4. Solution ────────────────────────────────────────────────────────
    add_heading(doc, "4. Solution", 1)
    add_body(doc, (
        "The solution was implemented using SQL, which is used to create, manage and query "
        "relational databases. The implementation follows CRUD operations (Create, Read, Update "
        "and Delete), which form the basis of database systems (Connolly & Begg, 2015)."
    ))

    add_heading(doc, "Database and Table Creation", 2)
    add_code_block(doc, DDL)

    add_heading(doc, "Data Insertion", 2)
    add_code_block(doc, DML_INSERT)

    add_heading(doc, "Queries", 2)
    add_body(doc, "Retrieve all employees:")
    add_code_block(doc, QUERY_ALL)

    add_body(doc, "Join query — employee name, site name and shift start date:")
    add_code_block(doc, QUERY_JOIN)

    add_body(doc, "Aggregation — total rooms per site:")
    add_code_block(doc, QUERY_AGG1)

    add_body(doc, "Aggregation — total employees per role:")
    add_code_block(doc, QUERY_AGG2)

    add_heading(doc, "Explanation", 2)
    add_body(doc, (
        "The SQL implementation demonstrates how data can be created, stored and retrieved "
        "efficiently. The use of JOIN statements allows multiple tables to be combined in a "
        "single query, reflecting the relationships defined during the design phase. Aggregation "
        "functions such as COUNT and GROUP BY help generate useful summaries that support "
        "business decision-making."
    ))
    add_body(doc, (
        "This reflects how databases support business intelligence by transforming raw data "
        "into meaningful information (Kimball & Ross, 2013). Each SQL block directly corresponds "
        "to a technique covered in the first four topics of the unit."
    ))

    add_horizontal_rule(doc)

    # ── 5. Conclusion ──────────────────────────────────────────────────────
    add_heading(doc, "5. Conclusion", 1)
    add_body(doc, (
        "Overall, the database solution successfully addresses the problem of managing FIFO "
        "workforce and accommodation. By organising data into structured tables and defining "
        "clear relationships, the system improves efficiency and reduces the likelihood of errors."
    ))
    add_body(doc, (
        "The solution meets the requirements by ensuring data consistency, enabling efficient "
        "queries and supporting decision-making. However, the system is still relatively basic "
        "and could be improved by adding features such as automated scheduling or integration "
        "with business intelligence tools for deeper reporting."
    ))
    add_body(doc, (
        "One challenge during the process was ensuring that relationships between tables were "
        "correctly defined, particularly when working with foreign keys. This was resolved by "
        "carefully reviewing the ER design before implementation, which reinforced the value of "
        "the design-first approach taught in the unit."
    ))
    add_body(doc, (
        "If this project were to be completed again, I would focus on expanding the system "
        "further and including more advanced queries — for example, window functions or stored "
        "procedures — to generate deeper insights and better demonstrate the capabilities of a "
        "relational database in a FIFO context."
    ))

    add_horizontal_rule(doc)

    # ── Appendix A — ER Diagram ────────────────────────────────────────────
    doc.add_page_break()
    add_heading(doc, "Appendix A — Design (ER Diagram)", 1)
    add_body(doc, (
        "The entity-relationship diagram below illustrates the five entities and the "
        "relationships between them as described in Section 3."
    ))

    if os.path.exists(ERD_PNG):
        doc.add_picture(ERD_PNG, width=Inches(6.0))
        caption = doc.add_paragraph("Figure 1. ER Diagram — FIFO Workforce Allocation Database.")
        caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in caption.runs:
            set_font(run, size=10, italic=True)
    else:
        add_body(doc, f"[ERD image not found at {ERD_PNG}. Run docs/generate_erd.py first.]")

    add_horizontal_rule(doc)

    # ── Appendix B — SQL ───────────────────────────────────────────────────
    doc.add_page_break()
    add_heading(doc, "Appendix B — Implementation (SQL Statements)", 1)
    add_body(doc, "The complete SQL implementation is reproduced below for reference.")
    add_code_block(doc, APPENDIX_B_SQL)

    add_horizontal_rule(doc)

    # ── References ─────────────────────────────────────────────────────────
    doc.add_page_break()
    add_heading(doc, "References", 1)

    refs = [
        (
            "Chen, P. P. (1976). The entity-relationship model — toward a unified view of data. "
            "ACM Transactions on Database Systems, 1(1), 9–36. "
            "https://doi.org/10.1145/320434.320440"
        ),
        (
            "Connolly, T., & Begg, C. (2015). Database systems: A practical approach to design, "
            "implementation and management (6th ed.). Pearson."
        ),
        (
            "Date, C. J. (2003). An introduction to database systems (8th ed.). Addison-Wesley."
        ),
        (
            "Elmasri, R., & Navathe, S. B. (2016). Fundamentals of database systems (7th ed.). "
            "Pearson."
        ),
        (
            "Kimball, R., & Ross, M. (2013). The data warehouse toolkit: The definitive guide "
            "to dimensional modeling (3rd ed.). Wiley."
        ),
        "[Additional references to be inserted as appropriate.]",
    ]

    for ref in refs:
        p = doc.add_paragraph(ref, style="Normal")
        p.paragraph_format.left_indent    = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        for run in p.runs:
            set_font(run, size=11)
        doc.add_paragraph()  # spacer between refs

    # ── Save ───────────────────────────────────────────────────────────────
    doc.save(OUTPUT)
    print(f"Document saved: {OUTPUT}")


if __name__ == "__main__":
    build()
