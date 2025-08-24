from jinja2 import Environment, FileSystemLoader
import pdfkit
import logging
import os
from modules.utils import generate_qr
import base64

def render_dmc_html(data_row, template_path="templates"):
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("dmc_template.html")

    qr_data = f"Roll No: {data_row.get('Roll No')}, Name: {data_row.get('Student Name')}"
    qr_bytes = generate_qr(qr_data)
    qr_base64 = base64.b64encode(qr_bytes).decode("utf-8")

    html_out = template.render(student=data_row, qr_code=qr_base64)
    return html_out

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

def generate_dmc_pdf(data_row, output_dir="generated_dmc", template_path="templates"):
    """Generate and save DMC PDF."""
    os.makedirs(output_dir, exist_ok=True)
    html_out = render_dmc_html(data_row, template_path)
    roll_no = data_row.get("Roll No", "Unknown")
    filename = f"DMC_{roll_no}.pdf"
    output_path = os.path.join(output_dir, filename)

    try:
        pdfkit.from_string(html_out, output_path, configuration=config, options={"encoding": "UTF-8"})
        logging.info(f"✅ PDF generated: {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"❌ PDF generation failed for Roll No {roll_no}: {e}")
        return None
