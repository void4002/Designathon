from reportlab.pdfgen import canvas

def generate_certificate(name, date, school_name, reason_for_transfer):
    """Generates a PDF transfer certificate with the given information."""
    # Create a PDF document
    pdf = canvas.Canvas("./static/certificate.pdf")
  
    # Define font and size
    font_size = 12
  
    # Add certificate title
    pdf.setFont("Helvetica-Bold", font_size + 4)
    pdf.drawString(180, 750, "TRANSFER CERTIFICATE")
  
    # Add student name
    pdf.setFont("Helvetica", font_size)
    pdf.drawString(40, 680, f"This is to certify that {name}")
  
    # Add school name
    pdf.drawString(180, 680, f"studied in {school_name}")
    
    # Add reason for transfer
    pdf.drawString(350, 680, f"and his/her transfer was due to {reason_for_transfer}")
  
    # Add date
    pdf.drawString(420, 720, f"Date: {date}")
  
    # Add signature line
    pdf.drawString(50, 630, "______________________")
    pdf.drawString(50, 615, "Principal's Signature")
  
    # Save the PDF document
    pdf.save()
