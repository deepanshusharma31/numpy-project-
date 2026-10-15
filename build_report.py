import os, glob
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted,
                                Table, TableStyle, KeepTogether)

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "Week2_NumPy_Pandas_Assignment_Report.pdf")
NAVY, GREY = colors.HexColor("#1F3A5F"), colors.HexColor("#555555")
styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], textColor=NAVY, fontSize=15, spaceBefore=4, spaceAfter=4)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], textColor=NAVY, fontSize=11, spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=9.5, leading=13.5)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8.5, textColor=GREY)
FRAME_W = A4[0] - 30 * mm

def mono(text, bg, fg=colors.black, max_size=7.5, min_size=4.8, chunk=28):
    """Monospace block drawn as stacked table cells (so the background renders and long text can split across pages)."""
    lines = text.rstrip("\n").split("\n")
    longest = max(len(l) for l in lines)
    size = max(min_size, min(max_size, (FRAME_W - 12) / (0.6 * longest)))
    st = ParagraphStyle("m", fontName="Courier", fontSize=size, leading=size * 1.25, textColor=fg)
    out = []
    for i in range(0, len(lines), chunk):
        part = "\n".join(lines[i:i + chunk])
        t = Table([[Preformatted(part, st)]], colWidths=[FRAME_W])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg),
                               ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                               ("TOPPADDING", (0, 0), (-1, -1), 5 if i == 0 else 0),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 5 if i + chunk >= len(lines) else 0)]))
        out.append(t)
    return out

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8); canvas.setFillColor(GREY)
    canvas.drawString(15 * mm, 9 * mm, "Week 2 Assignment - NumPy & Pandas for Data Analytics")
    canvas.drawRightString(A4[0] - 15 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()

def read(p):
    with open(os.path.join(BASE, p), encoding="utf-8") as f:
        return f.read()

TASKS = [
 ("task01_numpy_arrays", "Task 1: NumPy Introduction & Arrays", 10,
  "Imports NumPy and builds a 12-element array, then reports its shape, size and data type with <b>.shape</b>, <b>.size</b> and <b>.dtype</b>. "
  "A one-dimensional array is created with <b>np.arange()</b> and a 3x4 two-dimensional array from a list of lists; <b>.ndim</b> confirms the dimensions."),
 ("task02_indexing_slicing_reshaping", "Task 2: NumPy Indexing, Slicing & Reshaping", 10,
  "Demonstrates positional indexing (including negative indexes), slicing with <b>start:stop:step</b>, and 2-D access of single elements, whole rows, whole columns and sub-matrices. "
  "A 12-element array is reshaped into (3,4), (4,3) and (2,2,3); the original is left unchanged because <b>reshape()</b> returns a new view."),
 ("task03_numpy_math_stats", "Task 3: NumPy Mathematical & Statistical Operations", 10,
  "Uses the marks of 10 students in two subjects. Addition, subtraction, multiplication and division are applied element-wise (vectorised, no loops). "
  "Mean, median, min, max, standard deviation and sum are computed for each subject; <b>axis</b> is used to get per-subject and per-student means."),
 ("task04_pandas_series_dataframe", "Task 4: Pandas Series & DataFrame", 10,
  "Creates a labelled Series of marks and a student DataFrame (Name, Age, Course, Marks). Shows the DataFrame, <b>.columns</b> and <b>.index</b>, "
  "then adds two new columns: <b>Result</b> (via apply/lambda) and <b>Grade</b> (via <b>pd.cut</b>) and displays the updated table."),
 ("task05_read_inspect", "Task 5: Reading & Inspecting Data", 10,
  "Reads <b>sales_data.csv</b> (200 orders, 10 columns) with <b>pd.read_csv()</b>, then inspects it using head(), tail(), shape, columns, dtypes, info() and describe(). "
  "info() already reveals the missing values (non-null counts below 200 in quantity, unit_price, discount and region)."),
 ("task06_select_filter_sort", "Task 6: Selecting, Filtering & Sorting Data", 10,
  "Selects columns with <b>df[[...]]</b>, rows with <b>iloc</b>/<b>loc</b>, and filters with boolean conditions: a single condition (unit_price &gt; 20000), "
  "multiple AND conditions (&amp;), and <b>isin()</b>. Sorting uses <b>sort_values()</b> in ascending and descending order, plus a two-column sort."),
 ("task07_missing_values", "Task 7: Handling Missing Values", 10,
  "Finds missing values with <b>isnull()</b> and counts them per column (40 missing cells across 38 rows). Two approaches are compared: "
  "<b>dropna()</b> (loses 38 rows, 19% of the data) and <b>fillna()</b> with sensible values: median for quantity, the product's average price for unit_price, 0 for discount and the mode for region. "
  "Before/after views are shown. <b>Why it matters:</b> missing data biases averages and totals, breaks many functions and models, and dropping too much shrinks the sample, so handling it carefully keeps analysis accurate and trustworthy."),
 ("task08_merge_groupby_pivot", "Task 8: Merge, Concatenate, GroupBy & Pivot Table", 15,
  "Merges <b>sales</b> with <b>customers</b> on <b>customer_id</b> (left join) to add customer name, city and segment; concatenates DataFrames row-wise and column-wise with <b>pd.concat()</b>. "
  "<b>groupby()</b> produces revenue by category, multi-aggregate summaries by region (sum, mean, count, min, max) and segment averages. "
  "<b>pd.pivot_table()</b> summarises revenue as category x region (with totals) and average quantity as segment x payment mode."),
 ("task09_export", "Task 9: Exporting Data", 5,
  "Applies the cleaning steps, adds a computed <b>revenue</b> column and exports with <b>to_csv(index=False)</b> to <i>output/processed_sales_data.csv</i>. "
  "The file is read back to verify shape, columns, zero missing values and that its values match the in-memory DataFrame."),
 ("task10_mini_project", "Task 10: Mini Data Analysis Project - Sales Performance", 10,
  "End-to-end analysis of the sales dataset joined with customer data: load, inspect, handle missing values, engineer features (revenue, month, order size via <b>np.where</b>), "
  "select/filter, sort, GroupBy analysis, two pivot tables, NumPy statistics (mean, median, std, percentile), and export of the cleaned dataset to <i>output/cleaned_sales_project.csv</i>."),
]

story = []
# ---------------- Cover ----------------
story += [Spacer(1, 45 * mm),
          Paragraph("Week 2 Assignment", ParagraphStyle("t0", parent=H1, fontSize=14, textColor=GREY, alignment=1)),
          Paragraph("NumPy &amp; Pandas for Data Analytics", ParagraphStyle("t1", parent=H1, fontSize=26, leading=32, alignment=1)),
          Spacer(1, 8 * mm),
          Paragraph("Practical Report: Source Code, Outputs, Explanations &amp; Insights", ParagraphStyle("t2", parent=BODY, fontSize=12, alignment=1)),
          Spacer(1, 25 * mm)]
cover = Table([["Submitted by", "Deepanshu"],
               ["Total Marks", "100"],
               ["Tools used", "Python 3, NumPy, Pandas"],
               ["Google Drive link", "PASTE YOUR LINK HERE (set access to 'Anyone with the link can view')"]],
              colWidths=[40 * mm, 115 * mm])
cover.setStyle(TableStyle([("FONTSIZE", (0, 0), (-1, -1), 10), ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                           ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey), ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EEF2F7")),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
story += [cover, PageBreak()]

# ---------------- Contents + datasets ----------------
story.append(Paragraph("Contents &amp; Marks Breakdown", H1))
rows = [["#", "Task", "Marks", "Script file"]]
for i, (fn, title, marks, _) in enumerate(TASKS, 1):
    rows.append([str(i), title.split(": ", 1)[1], str(marks), fn + ".py"])
t = Table(rows, colWidths=[8 * mm, 85 * mm, 15 * mm, 62 * mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                       ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
                       ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7FA")])]))
story += [t, Spacer(1, 6 * mm)]

story.append(Paragraph("Datasets Used", H1))
story.append(Paragraph(
    "Tasks 5-10 use two CSV files stored in the <b>data/</b> folder. They were generated with <i>make_datasets.py</i> (fixed random seed, so results are reproducible). "
    "The sales file intentionally contains missing values so that Task 7 has real gaps to handle. Tasks 1-4 use small arrays and DataFrames created inside the scripts.", BODY))
story.append(Paragraph("sales_data.csv - 200 rows x 10 columns", H2))
story.append(Paragraph("order_id, order_date, customer_id, product, category, quantity, unit_price, discount, region, payment_mode. "
                       "Missing values: quantity (12), unit_price (10), discount (10), region (8).", BODY))
story.append(Spacer(1, 2 * mm))
story.extend(mono("\n".join(read("data/sales_data.csv").splitlines()[:8]), colors.HexColor("#F4F4F4")))
story.append(Paragraph("customers.csv - 50 rows x 4 columns", H2))
story.append(Paragraph("customer_id, customer_name, city, segment (Consumer / Corporate / Home Office).", BODY))
story.append(Spacer(1, 2 * mm))
story.extend(mono("\n".join(read("data/customers.csv").splitlines()[:6]), colors.HexColor("#F4F4F4")))
story.append(PageBreak())

# ---------------- Tasks ----------------
for i, (fn, title, marks, expl) in enumerate(TASKS):
    story.append(Paragraph(f"{title} <font size=9 color='#777777'>({marks} marks)</font>", H1))
    story.append(Paragraph(f"<b>Explanation.</b> {expl}", BODY))
    blk = mono(read(fn + ".py"), colors.HexColor("#F4F6F8"), max_size=7)
    story.append(KeepTogether([Paragraph(f"Source code: {fn}.py", H2), blk[0]])); story.extend(blk[1:])
    blk = mono(read(f"output/{fn}.txt"), colors.HexColor("#1E1E1E"), colors.HexColor("#D4F7D4"), max_size=7)
    story.append(KeepTogether([Paragraph("Program output", H2), blk[0]])); story.extend(blk[1:])
    story.append(PageBreak())

# ---------------- Insights ----------------
story.append(Paragraph("Key Findings from the Mini Data Analysis Project", H1))
story.append(Paragraph("Based on 200 orders worth Rs 50.14 lakh in total revenue (January - June 2026) after cleaning:", BODY))
story.append(Spacer(1, 2 * mm))
findings = [
 ("Electronics dominates revenue.", "Electronics brings in about 88% of revenue (Rs 44.10 lakh). Laptops alone contribute 49% from just 13 orders, and Smartphones add another 35%."),
 ("Revenue is highly concentrated.", "The top 20% of orders generate 83.6% of total revenue. The mean order value (Rs 25,070) is more than four times the median (Rs 5,720), a strongly right-skewed distribution driven by a few big-ticket laptop orders."),
 ("West and South lead regionally; North lags.", "West (Rs 19.2 lakh, 38%) and South (Rs 15.4 lakh, 31%) account for roughly 70% of sales, while North contributes only about 9%, a clear growth opportunity."),
 ("Pune, Chennai and Delhi are the top cities.", "Pune alone generates about 28% of revenue (Rs 13.97 lakh), followed by Chennai (Rs 11.44 lakh) and Delhi (Rs 9.32 lakh)."),
 ("Sales peak in March-April.", "April is the best month (Rs 11.37 lakh) and March close behind (Rs 10.82 lakh), while February is the weakest (Rs 5.71 lakh). Electronics drives these swings."),
 ("Consumers are the biggest segment.", "The Consumer segment contributes about 61% of revenue and also has the highest average order value (Rs 30,460) versus Corporate (Rs 18,508)."),
 ("UPI is the preferred payment method.", "UPI accounts for 94 of 200 orders (47%), followed by Credit Card (25%), Debit Card (20%) and Cash (8%)."),
 ("Discounts barely change basket size.", "Average quantity per order only moves from 3.15 (no discount) to about 3.3 (10-15% discount), so deeper discounts do not appear to drive much extra volume."),
]
for h, d in findings:
    story.append(Paragraph(f"<b>{h}</b> {d}", BODY)); story.append(Spacer(1, 1.8 * mm))
story.append(Paragraph("Recommendations", H2))
for r in ["Protect and grow the Electronics line (stock availability, bundles) since it carries most of the revenue.",
          "Run targeted campaigns in the North region and for Corporate customers to broaden the revenue base.",
          "Review blanket discounts: they cost margin without a visible lift in quantity.",
          "Plan inventory and promotions around the March-April peak and look for ways to lift February."]:
    story.append(Paragraph("&bull; " + r, BODY))
story.append(Spacer(1, 4 * mm))
story.append(Paragraph("Note: the dataset is synthetically generated for practice, so these findings illustrate the analysis workflow rather than real business results.", SMALL))

story.append(Spacer(1, 8 * mm))
story.append(Paragraph("Files Submitted (Google Drive)", H1))
story.extend(mono("""Week2_Assignment/
 |-- task01_numpy_arrays.py ... task10_mini_project.py   (10 scripts)
 |-- make_datasets.py                                    (generates the CSV data)
 |-- data/
 |     |-- sales_data.csv        (input, contains missing values)
 |     `-- customers.csv         (input)
 `-- output/
       |-- processed_sales_data.csv   (Task 9 export)
       |-- cleaned_sales_project.csv  (Task 10 export)
       `-- taskNN_*.txt               (captured outputs)""", colors.HexColor("#F4F6F8")))

SimpleDocTemplate(OUT, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=14 * mm,
                  bottomMargin=16 * mm, title="Week 2 Assignment - NumPy & Pandas", author="Deepanshu").build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF built:", OUT)
