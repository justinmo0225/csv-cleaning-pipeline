import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# reportlab imports for PDF generation
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def run_visuals():
    # connects to the SQLite database and reads the employees table into a DataFrame
    connected = sqlite3.connect("employee.db")
    df = pd.read_sql("SELECT * FROM employees", connected)
    connected.close()

    fig, axes = plt.subplots(1, 2, figsize = (12, 5)) # this plots both graphs side by side

    # graph of salary distribution
    axes[0].hist(df["salary"], bins = 10, edgecolor = "black", linewidth = 1.2, alpha = 0.8)    # histogram with edges
    axes[0].set_title("Salary Distribution --- Histogram")
    axes[0].set_xlabel("Salary ($)")
    axes[0].set_ylabel("# of Employees")

    # graph of average salary by department
    df["department"] = df["department_region"].str.split("-").str[0]
    dept_salary = df.groupby("department")["salary"].mean()
    axes[1].bar(dept_salary.index, dept_salary.values, edgecolor = "black", linewidth = 1.2, alpha = 0.8)   # bar chart with edges
    axes[1].set_title("Avg Salary by Department --- Bar Chart")
    axes[1].set_xlabel("Department")
    axes[1].set_ylabel("Avg Salary ($)")
    axes[1].tick_params(axis = 'x', rotation = 45)

    plt.tight_layout()
    plt.show()

    # summary statistics that display numbers in the reports folder
    df.describe().to_csv("reports/summary_stats.csv")   # basic statistics
    dept_salary.to_csv("reports/department_salary.csv") # department salary analysis
    df.to_csv("reports/cleaned_data.csv", index=False)  # cleaned dataset
    df["status"].value_counts().to_csv("reports/status_distribution.csv")   # employee status distribution (pending, active, or inactive)

    generate_pdf_report(df, dept_salary)

# generate a PDF report
def generate_pdf_report(df, dept_salary):
    file_path = "reports/employee_report.pdf"
    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()
    content = []

    # title
    content.append(Paragraph("Employee Analytics Report", styles["Title"]))
    content.append(Spacer(1, 12))

    # summary stats
    summary_text = f"""
    <b>Total Employees:</b> {len(df)}<br/>
    <b>Average Salary:</b> $ {df['salary'].mean():.2f}<br/>
    <b>Max Salary:</b> $ {df['salary'].max():.2f}<br/>
    <b>Min Salary:</b> $ {df['salary'].min():.2f}<br/>
    """

    content.append(Paragraph(summary_text, styles["Normal"]))
    content.append(Spacer(1, 12))

    # department salary table
    table_data = [["Department", "Avg Salary"]]

    for dept, salary in dept_salary.items():
        table_data.append([dept, f"{salary:.2f}"])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    content.append(table)

    doc.build(content)  # build PDF

    print("PDF report generated at:", file_path)