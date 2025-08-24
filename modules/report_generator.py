from jinja2 import Environment, FileSystemLoader
import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")


# def generate_dmc(data_row, template_path="templates"):
def generate_dmc(data_row, template_path="templates", preview=False):
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("dmc_template.html")
    html_out = template.render(student=data_row)

    if preview:
        return html_out  # For Streamlit preview

    pdfkit.from_string(html_out, f"DMC_{data_row['Roll No']}.pdf", configuration=config)
