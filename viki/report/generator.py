from fpdf import FPDF
import datetime
import os

class ForensicPDF(FPDF):
    """Подкласс для стандартизации вёрстки RSA."""
    def footer(self):
        self.set_y(-15)
        self.set_font("Courier", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()} | RSA Deterministic Audit Protocol", align="C")

class VikiReportGenerator:
    """Генератор отчетов v1.6.1 Stable: Industrial Edition."""
    
    def __init__(self, logo_path="logo.png"):
        self.logo_path = logo_path

    def generate_forensic_pdf(self, agent_name, case_data, output_path):
        # Создаем объект нашего кастомного класса
        pdf = ForensicPDF()
        pdf.add_page()
        
        # 1. Header & Logo
        if os.path.exists(self.logo_path):
            pdf.image(self.logo_path, 10, 8, 33)
        
        pdf.set_font("Courier", "B", 16)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "V.I.K.I. DEEP ANATOMY REPORT", ln=True, align="C")
        pdf.set_font("Courier", "", 10)
        pdf.cell(0, 10, f"ID: {case_data['id']} | DATE: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
        pdf.ln(10)

        # 2. Target Summary
        pdf.set_fill_color(30, 30, 30)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Courier", "B", 12)
        pdf.cell(0, 10, f" AGENT: {agent_name}", ln=True, fill=True)
        pdf.ln(5)

        # 3. Vulnerability Origin
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Courier", "B", 11)
        pdf.cell(0, 10, "[01] VULNERABILITY ORIGIN", ln=True)
        pdf.set_font("Courier", "", 10)
        pdf.multi_cell(0, 7, case_data['vulnerability_origin'])
        pdf.ln(5)

        # 4. Code-Level Flaw
        pdf.set_font("Courier", "B", 11)
        pdf.cell(0, 10, "[02] ARCHITECTURAL FLAW", ln=True)
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Courier", "B", 9)
        pdf.multi_cell(0, 7, case_data['code_flaw'], fill=True)
        pdf.set_fill_color(255, 255, 255)
        pdf.ln(5)

        # 5. RSA Intervention
        pdf.set_text_color(0, 120, 0)
        pdf.set_font("Courier", "B", 11)
        pdf.cell(0, 10, "[03] RSA INTERVENTION", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Courier", "", 10)
        pdf.multi_cell(0, 7, case_data['intervention_logic'])
        pdf.ln(5)

        # 6. Trajectory Comparison
        pdf.set_font("Courier", "B", 11)
        pdf.cell(0, 10, "[04] TRAJECTORY COMPARISON", ln=True)
        pdf.set_font("Courier", "", 10)
        pdf.cell(0, 7, f"Vanilla Path:    {case_data['vanilla_path']}", ln=True)
        pdf.set_text_color(0, 120, 0)
        pdf.cell(0, 7, f"Guarded Path:    {case_data['guarded_path']}", ln=True)

        pdf.output(output_path)
        print(f"📄 [FACTORY] Forensic PDF generated: {os.path.basename(output_path)}")