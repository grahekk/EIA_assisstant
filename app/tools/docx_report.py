from docx import Document
from docx.shared import Pt

def update_existing_section(doc):
    # Access the first paragraph and modify its text and formatting
    first_paragraph = doc.paragraphs[0]
    first_paragraph.text = 'Updated Text'

def add_chapter(doc, chapter):
    # Add chapter heading
    doc.add_heading(chapter.heading, level=1)

    # Add chapter description
    doc.add_paragraph(chapter.description)

    # Check if chapter has a table
    if chapter.table:
        # Add table heading
        doc.add_paragraph(chapter.table_description)

        # Add table
        try:
            # doc.add_table(chapter.table, chapter.table_columns)
            add_chapters_table(doc, chapter)
        except ValueError:
            # Handle if table data is empty or invalid
            doc.add_paragraph("Table data is missing or invalid.")

def report_from_docx_template(project, report):
    # Open an existing document
    template = r"app\tools\Template.docx"
    doc = Document(template)

    # Iterate over project chapters
    for chapter in project.chapters:
        if chapter.heading == "bla bla":
            # Update existing section if it's the "Natura chapter"
            update_existing_section(doc, "A.1	PODACI O EKOLOŠKOJ MREŽI", chapter.description)
        else:
            # Add a new chapter
            add_chapter(doc, chapter)

    # Save the modified document
    doc.save(report)


def add_chapters_table(doc, chapter):
    table = doc.add_table(rows=len(chapter.table)+1, cols=len(chapter.table_columns))
    table.style = 'DV_tablica'
    table.autofit = False
    table.allow_autofit = False
    for row in table.rows:
        for cell in row.cells:
            cell.width = Pt(100)
    for col in range(len(chapter.table_columns)):
        table.cell(0, col).text = chapter.table_columns[col]


    for i, row in enumerate(chapter.table, start=1):
        for col in range(len(chapter.table_columns)):
            table.cell(i, col).text = row[col]

            # table.cell(i, 0).text = row[0]
            # table.cell(i, 1).text = row[1]
            # table.cell(i, 2).text = row[2]