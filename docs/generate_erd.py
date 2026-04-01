#!/usr/bin/env python3
"""
Generate docs/assets/erd.png — ER diagram for the FIFO workforce
allocation database using Graphviz DOT.
"""

import subprocess
import os

DOT_SOURCE = r"""
digraph ERD {
    graph [
        rankdir=LR,
        fontname="Helvetica",
        fontsize=12,
        splines=ortho,
        nodesep=0.8,
        ranksep=1.2,
        bgcolor="white"
    ]
    node [
        shape=none,
        fontname="Helvetica",
        fontsize=11
    ]
    edge [fontname="Helvetica", fontsize=10]

    // ─── Entity nodes (HTML-like label tables) ───

    Employee [label=<
        <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4"
               BGCOLOR="#D6EAF8" STYLE="rounded">
          <TR><TD COLSPAN="2" BGCOLOR="#2E86C1" ALIGN="CENTER">
            <FONT COLOR="white"><B>Employee</B></FONT></TD></TR>
          <TR><TD ALIGN="LEFT"><U><B>employee_id</B></U> PK</TD><TD ALIGN="LEFT">INT</TD></TR>
          <TR><TD ALIGN="LEFT">name</TD><TD ALIGN="LEFT">VARCHAR(100)</TD></TR>
          <TR><TD ALIGN="LEFT">role</TD><TD ALIGN="LEFT">VARCHAR(50)</TD></TR>
          <TR><TD ALIGN="LEFT">contact</TD><TD ALIGN="LEFT">VARCHAR(100)</TD></TR>
        </TABLE>>]

    Site [label=<
        <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4"
               BGCOLOR="#D5F5E3" STYLE="rounded">
          <TR><TD COLSPAN="2" BGCOLOR="#1E8449" ALIGN="CENTER">
            <FONT COLOR="white"><B>Site</B></FONT></TD></TR>
          <TR><TD ALIGN="LEFT"><U><B>site_id</B></U> PK</TD><TD ALIGN="LEFT">INT</TD></TR>
          <TR><TD ALIGN="LEFT">site_name</TD><TD ALIGN="LEFT">VARCHAR(100)</TD></TR>
          <TR><TD ALIGN="LEFT">location</TD><TD ALIGN="LEFT">VARCHAR(100)</TD></TR>
        </TABLE>>]

    Room [label=<
        <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4"
               BGCOLOR="#FDEBD0" STYLE="rounded">
          <TR><TD COLSPAN="2" BGCOLOR="#CA6F1E" ALIGN="CENTER">
            <FONT COLOR="white"><B>Room</B></FONT></TD></TR>
          <TR><TD ALIGN="LEFT"><U><B>room_id</B></U> PK</TD><TD ALIGN="LEFT">INT</TD></TR>
          <TR><TD ALIGN="LEFT">capacity</TD><TD ALIGN="LEFT">INT</TD></TR>
          <TR><TD ALIGN="LEFT">site_id FK</TD><TD ALIGN="LEFT">INT</TD></TR>
        </TABLE>>]

    Shift [label=<
        <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4"
               BGCOLOR="#F9EBEA" STYLE="rounded">
          <TR><TD COLSPAN="2" BGCOLOR="#A93226" ALIGN="CENTER">
            <FONT COLOR="white"><B>Shift</B></FONT></TD></TR>
          <TR><TD ALIGN="LEFT"><U><B>shift_id</B></U> PK</TD><TD ALIGN="LEFT">INT</TD></TR>
          <TR><TD ALIGN="LEFT">start_date</TD><TD ALIGN="LEFT">DATE</TD></TR>
          <TR><TD ALIGN="LEFT">end_date</TD><TD ALIGN="LEFT">DATE</TD></TR>
        </TABLE>>]

    Allocation [label=<
        <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4"
               BGCOLOR="#F3E5F5" STYLE="rounded">
          <TR><TD COLSPAN="2" BGCOLOR="#6C3483" ALIGN="CENTER">
            <FONT COLOR="white"><B>Allocation</B></FONT></TD></TR>
          <TR><TD ALIGN="LEFT"><U><B>allocation_id</B></U> PK</TD><TD ALIGN="LEFT">INT</TD></TR>
          <TR><TD ALIGN="LEFT">employee_id FK</TD><TD ALIGN="LEFT">INT</TD></TR>
          <TR><TD ALIGN="LEFT">room_id FK</TD><TD ALIGN="LEFT">INT</TD></TR>
          <TR><TD ALIGN="LEFT">shift_id FK</TD><TD ALIGN="LEFT">INT</TD></TR>
        </TABLE>>]

    // ─── Relationships ───
    Site -> Room       [label="1..*  contains", arrowhead=crow, arrowtail=tee, dir=both]
    Employee -> Allocation [label="1..*  has", arrowhead=crow, arrowtail=tee, dir=both]
    Room -> Allocation [label="1..*  used in", arrowhead=crow, arrowtail=tee, dir=both]
    Shift -> Allocation [label="1..*  covers", arrowhead=crow, arrowtail=tee, dir=both]
}
"""

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    dot_path = os.path.join(assets_dir, "erd.dot")
    png_path = os.path.join(assets_dir, "erd.png")

    with open(dot_path, "w") as f:
        f.write(DOT_SOURCE)

    result = subprocess.run(
        ["dot", "-Tpng", "-Gdpi=150", dot_path, "-o", png_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Error generating ERD:", result.stderr)
        raise SystemExit(1)

    print(f"ERD PNG generated: {png_path}")

if __name__ == "__main__":
    main()
