# Create a PDF class
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        # Add a title at the top of each page
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "IAMC Data Report", align="C", ln=True)

    def footer(self):
        # Add page number at the bottom of each page
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
