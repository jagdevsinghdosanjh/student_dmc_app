# 🎓 Student DMC Generator

A modular Streamlit-based application for extracting, validating, and generating student DMCs (Detailed Marks Certificates) from PDF or Excel files. Built for educators and institutions to streamline academic record processing with QR verification, grade analytics, and bulk export capabilities.

---

## 🚀 Features

- ✅ **PDF & Excel Upload**: Extracts tabular student data from `.pdf` or `.xlsx` files.
- 🔍 **Validation Engine**: Checks for missing columns, duplicate headers, empty rows, and non-numeric marks.
- 📄 **DMC Generation**: Converts student data into printable PDF certificates using HTML templates.
- 📦 **Bulk Export**: Generates all DMCs and packages them into a downloadable ZIP file.
- 📊 **Grade Analytics Dashboard**: Visualizes grade distribution across subjects and students.
- 📎 **QR Code Embedding**: Adds a scannable QR code to each DMC for verification.
- 🧠 **Modular Architecture**: Clean separation of UI, data logic, PDF rendering, and utilities.

---

## 🧰 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python (pandas, pdfkit, Jinja2)
- **PDF Engine**: `wkhtmltopdf` (external binary)
- **QR Generator**: `qrcode`
- **Templating**: Jinja2

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jagdevsinghdosanjh/student-dmc-generator.git
   cd student_dmc_generator

🖥️ Usage
bash
streamlit run main.py
Upload a student data file (PDF or Excel)

Validate structure and content

Preview individual DMCs

Download single or bulk PDFs

View grade analytics

📁 Project Structure
Code
student_dmc_app/
│
├── main.py                     # Streamlit app entry point
├── requirements.txt
├── templates/
│   └── dmc_template.html       # Jinja2 template for DMC layout
│
├── modules/
│   ├── data_loader.py          # Excel/PDF data loading
│   ├── pdf_parser.py           # PDF table extraction
│   ├── report_generator.py     # Legacy PDF generator
│   ├── dmc_viewer.py           # HTML preview + PDF + ZIP
│   ├── ui_components.py        # Sidebar controls
│   └── utils.py                # Validation, formatting, QR
📌 Notes
Ensure column names match expected headers: Roll No, Student Name, Class, Section, and subject names.

QR codes embed student identity for verification.

PDF generation requires wkhtmltopdf installed and accessible.

🙌 Credits
Built by Jagdev Singh Dosanjh, Computer Faculty at GHS Chananke, Amritsar. Dedicated to empowering educators through scalable, transparent, and user-friendly tools.

📄 License
This project is licensed under the MIT License. See LICENSE for details.
