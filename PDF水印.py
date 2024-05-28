import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

def create_watermark(watermark_text, page_width, page_height):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Set transparency
    can.setFillAlpha(0.1)

    # Set font and size
    can.setFont("Helvetica", 8)

    # Set text color (light gray)
    can.setFillColorRGB(0.5, 0.5, 0.5)

    # Rotate and draw the watermark text at intervals
    step_x = page_width / 8
    step_y = page_height / 8
    for y in range(0, int(page_height), int(step_y)):
        for x in range(0, int(page_width), int(step_x)):
            can.saveState()
            can.translate(x, y)
            can.rotate(45)
            can.drawString(0, 0, watermark_text)
            can.restoreState()

    can.save()
    packet.seek(0)
    return PdfReader(packet)

def add_watermark(input_pdf_path, output_pdf_path, watermark_text):
    # Read the original PDF
    original_pdf = PdfReader(input_pdf_path)
    output = PdfWriter()

    # Get the size of the first page
    first_page = original_pdf.pages[0]
    page_width = first_page.mediabox.width
    page_height = first_page.mediabox.height

    # Create the watermark with detected page size
    watermark = create_watermark(watermark_text, page_width, page_height)

    # Add watermark to each page
    for i in range(len(original_pdf.pages)):
        page = original_pdf.pages[i]
        page.merge_page(watermark.pages[0])
        output.add_page(page)

    # Save the result
    with open(output_pdf_path, "wb") as outputStream:
        output.write(outputStream)
        
    char_spacing = 6 

watermark_text = "© 2024 JD.Z - 9E2A 2242 2326 7511 2961 A183 90FA 9574 7000 A102"
add_watermark('input.pdf', 'output.pdf', watermark_text)
