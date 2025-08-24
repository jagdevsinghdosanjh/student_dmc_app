from jinja2 import Environment, FileSystemLoader
import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")


# def generate_dmc(data_row, template_path="templates"):
def generate_dmc(data_row, template_path="templates"):
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("dmc_template.html")
    html_out = template.render(student=data_row)
    pdfkit.from_string(html_out, f"DMC_{data_row['Roll No']}.pdf", configuration=config)
