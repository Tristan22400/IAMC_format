# Create a PDF class
from fpdf import FPDF

class PDFReport(FPDF):
    
        
    def header(self):
        # Logo
        self.image('Geeds.jpg', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Report Scenario', 1, 0, 'C')
        # Line break
        self.ln(20)

    def footer(self):
        # Add page number at the bottom of each page
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
