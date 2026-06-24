from fpdf import FPDF
import datetime
import os

class ForensicPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Courier", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()} | RSA Forensic Audit Standard v1.7.1", align="C")

class VikiReportGenerator:
    def __init__(self, logo_path="logo.png"):
        self.logo_path = logo_path

    def generate_forensic_pdf(self, agent_name, repo_url, case_data, output_path):
        # ВАЖНО: Теперь здесь 4 аргумента (включая repo_url)
        pdf = ForensicPDF()
        pdf.add_page()
        
        if os.path.exists(self.logo_path):
            pdf.image(self.logo_path, 10, 8, 33)
        
        pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 10, "V.I.K.I. DEEP ANATOMY REPORT", ln=True, align="C")
        pdf.set_font("Courier", "", 10)
        pdf.cell(0, 10, f"ID: {case_data['id']} | DATE: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
        pdf.ln(10)

        # Agent Header
        pdf.set_fill_color(30, 30, 30); pdf.set_text_color(255, 255, 255)
        pdf.set_font("Courier", "B", 11)
        pdf.cell(0, 10, f" TARGET: {agent_name}", ln=True, fill=True)
        # ВСТАВЛЯЕМ URL В PDF
        pdf.set_fill_color(50, 50, 50); pdf.set_font("Courier", "I", 8)
        pdf.cell(0, 7, f" SOURCE: {repo_url}", ln=True, fill=True)
        pdf.ln(5); pdf.set_text_color(0, 0, 0); pdf.set_font("Courier", "", 10)
        
        # Sections 01-03
        for section in [("[01] VULNERABILITY ORIGIN", case_data['vulnerability_origin']),
                        ("[02] ARCHITECTURAL FLAW", case_data['code_flaw']),
                        ("[03] RSA INTERVENTION", case_data['intervention_logic'])]:
            pdf.set_font("Courier", "B", 11); pdf.cell(0, 10, section[0], ln=True)
            pdf.set_font("Courier", "", 10)
            if "[02]" in section[0]:
                pdf.set_fill_color(240, 240, 240); pdf.set_font("Courier", "B", 9)
                pdf.multi_cell(0, 7, section[1], fill=True)
                pdf.set_fill_color(255, 255, 255)
            else:
                pdf.multi_cell(0, 7, section[1])
            pdf.ln(3)

        # [04] Trajectory
        pdf.set_font("Courier", "B", 11); pdf.cell(0, 10, "[04] TRAJECTORY COMPARISON", ln=True)
        pdf.set_font("Courier", "", 9)
        pdf.cell(0, 7, f"Vanilla: {case_data['vanilla_path']}", ln=True)
        pdf.set_text_color(0, 120, 0); pdf.cell(0, 7, f"Guarded: {case_data['guarded_path']}", ln=True)
        pdf.set_text_color(0, 0, 0); pdf.ln(5)

        # [05] ECONOMIC IMPACT
        pdf.set_font("Courier", "B", 11); pdf.cell(0, 10, "[05] ECONOMIC IMPACT", ln=True)
        pdf.set_fill_color(255, 240, 240); pdf.set_font("Courier", "", 10)
        pdf.multi_cell(0, 7, case_data['economic_impact'], fill=True)
        pdf.set_fill_color(255, 255, 255); pdf.ln(5)

        # [06] REMEDIATION
        pdf.set_font("Courier", "B", 11); pdf.cell(0, 10, "[06] RECOMMENDED REMEDIATION", ln=True)
        pdf.set_fill_color(240, 255, 240); pdf.set_font("Courier", "B", 9)
        pdf.multi_cell(0, 7, case_data['remediation'], fill=True)
        
        pdf.output(output_path)
        print(f"📄 [v1.7.1] Forensic PDF generated: {os.path.basename(output_path)}")