from fpdf import FPDF
import datetime
import os

class VikiReportGenerator(FPDF):
    """Генератор отчетов v1.5.1 Stable: Forensic Anatomy Edition."""
    
    def __init__(self, logo_path="logo.png"):
        super().__init__()
        self.logo_path = logo_path

    def footer(self):
        # Нижний колонтитул с номером страницы
        self.set_y(-15)
        self.set_font("Courier", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()} | RSA Deterministic Audit Protocol", align="C")

    def generate_forensic_pdf(self, agent_name, case_data, output_path):
        self.add_page()
        
        # 1. Header & Logo
        if os.path.exists(self.logo_path):
            self.image(self.logo_path, 10, 8, 33)
        
        self.set_font("Courier", "B", 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "V.I.K.I. DEEP ANATOMY REPORT", ln=True, align="C")
        self.set_font("Courier", "", 10)
        self.cell(0, 10, f"ID: {case_data['id']} | DATE: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
        self.ln(10)

        # 2. Target Summary
        self.set_fill_color(30, 30, 30)
        self.set_text_color(255, 255, 255)
        self.set_font("Courier", "B", 12)
        self.cell(0, 10, f" AGENT: {agent_name}", ln=True, fill=True)
        self.ln(5)

        # 3. Vulnerability Origin
        self.set_text_color(0, 0, 0)
        self.set_font("Courier", "B", 11)
        self.cell(0, 10, "[01] VULNERABILITY ORIGIN (The 'Why')", ln=True)
        self.set_font("Courier", "", 10)
        self.multi_cell(0, 7, case_data['vulnerability_origin'])
        self.ln(5)

        # 4. Code-Level Flaw (Grey Block)
        self.set_font("Courier", "B", 11)
        self.cell(0, 10, "[02] ARCHITECTURAL FLAW (The 'Where')", ln=True)
        self.set_fill_color(240, 240, 240) # Светло-серый фон для кода
        self.set_font("Courier", "B", 9)
        self.multi_cell(0, 7, case_data['code_flaw'], fill=True)
        self.set_fill_color(255, 255, 255) # ИСПРАВЛЕНО: Сброс цвета фона
        self.ln(5)

        # 5. RSA Intervention
        self.set_text_color(0, 120, 0) # Зеленый для V.I.K.I.
        self.set_font("Courier", "B", 11)
        self.cell(0, 10, "[03] RSA INTERVENTION (The 'How')", ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Courier", "", 10)
        self.multi_cell(0, 7, case_data['intervention_logic'])
        self.ln(5)

        # 6. Trajectory Comparison
        self.set_font("Courier", "B", 11)
        self.cell(0, 10, "[04] TRAJECTORY COMPARISON", ln=True)
        self.set_font("Courier", "", 10)
        self.cell(0, 7, f"Vanilla Path:    {case_data['vanilla_path']}", ln=True)
        self.set_text_color(0, 120, 0)
        self.cell(0, 7, f"Guarded Path:    {case_data['guarded_path']}", ln=True)

        self.output(output_path)
        print(f"📄 [ANATOMY] Expert Forensic Report created: {output_path}")
        