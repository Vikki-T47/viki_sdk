from fpdf import FPDF
import datetime
import os

class VikiReportGenerator:
    """Генератор PDF-отчетов об аудите."""
    def __init__(self, logo_path="logo.png"):
        self.logo_path = logo_path

    def generate_pdf(self, agent_name, metrics, analysis, output_path):
        pdf = FPDF()
        pdf.add_page()
        
        # Логотип
        if os.path.exists(self.logo_path):
            pdf.image(self.logo_path, 10, 8, 33)
        
        pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 10, "V.I.K.I. FORENSIC AUDIT REPORT", ln=True, align="C")
        pdf.set_font("Courier", "", 10)
        pdf.cell(0, 10, f"DATE: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
        pdf.ln(20)

        # Таблица метрик
        pdf.set_fill_color(30, 30, 30)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, f" AGENT UNDER AUDIT: {agent_name}", ln=True, fill=True)
        pdf.ln(5)
        
        pdf.set_text_color(0, 0, 0)
        for key, val in metrics.items():
            pdf.cell(60, 8, f"{key}:", border=1)
            pdf.cell(0, 8, f" {val}", border=1, ln=True)
        
        pdf.ln(10)
        pdf.set_font("Courier", "B", 12)
        pdf.cell(0, 10, "ANALYSIS:", ln=True)
        pdf.set_font("Courier", "", 10)
        pdf.multi_cell(0, 10, analysis)

        pdf.output(output_path)
        print(f"📄 [GENERATOR] PDF Report saved: {output_path}")