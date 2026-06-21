import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import random
import statistics
import uuid

# ------------------------
# CONSTANTS & POOLS
# ------------------------
PASS_MARK = 60

FACULTIES = [
    "Faculty of Information & Communications Technology",
    "Faculty of Built Environment",
    "Faculty of Business Management & Globalisation",
    "Faculty of Communication, Media & Broadcasting",
    "Faculty of Design & Innovation",
    "Faculty of Architecture & the Built Environment",
]

PROGRAMMES = [
    "-- Select Programme --",
    "BSc (Hons) Computer Science",
    "BSc (Hons) Information Technology",
    "BSc (Hons) Software Engineering",
    "Diploma in Computing",
    "BA (Hons) Mass Communication",
    "BA (Hons) Graphic Design",
    "BSc (Hons) Business Management",
    "BSc (Hons) Architecture",
    "BA (Hons) Fashion Design",
    "BSc (Hons) Quantity Surveying",
]

MODULES = [
    "PROG103 - Principle of Structured Programming",
    "PROG102 - Principles of Software Engineering",
    "COMP105 - Data Communications",
    "COMP102 - Introduction to Database",
    "MATH101 - Computerized Mathematics",
    "COMP104 - Web Design Fundamentals",
    "COMP106 - Operating Systems",
    "COMP107 - Object Oriented Programming",
    "BUSS101 - Principles of Management",
    "COMM101 - Introduction to Mass Communication",
]

PROGRAMME_MODULES = {
    "BSc (Hons) Software Engineering": [
        "PROG103 - Principle of Structured Programming",
        "PROG102 - Principles of Software Engineering",
        "COMP107 - Object Oriented Programming",
        "COMP102 - Introduction to Database",
        "COMP106 - Operating Systems",
        "COMP104 - Web Design Fundamentals",
    ],
    "BSc (Hons) Computer Science": [
        "PROG103 - Principle of Structured Programming",
        "COMP107 - Object Oriented Programming",
        "COMP106 - Operating Systems",
        "MATH101 - Computerized Mathematics",
        "COMP102 - Introduction to Database",
    ],
    "BSc (Hons) Information Technology": [
        "COMP105 - Data Communications",
        "COMP102 - Introduction to Database",
        "COMP104 - Web Design Fundamentals",
        "BUSS101 - Principles of Management",
    ],
}

SEMESTERS = ["Semester " + str(i) for i in range(1, 9)]

MALE_NAMES = ["Mohamed","Ibrahim","Alpha","Sorie","Brima","Lamin","Alieu","Amadu","Foday","Abdul","Emmanuel","Joseph","David","Samuel","Musa","Hassan","Lansana","Gibril","Alfred","Sheku"]
FEMALE_NAMES = ["Aminata","Fatmata","Mariama","Adama","Hawa","Kadiatu","Isatu","Tenneh","Memunatu","Sia","Yenoh","Kumba","Binta","Fanta","Ramatu","Zainab","Rugiatu","Mabinty","Yeabu","Finda"]
LAST_NAMES = ["Kamara","Sesay","Conteh","Bangura","Koroma","Jalloh","Fofana","Turay","Kargbo","Tarawalie","Mansaray","Barrie","Bah","Kanu","Lahai","Dumbuya","Sheriff","Thomas","Cole","Kallon"]

# ------------------------
# DATA STORE
# ------------------------
students = []   # list of record dicts
current_module_scores = {}  # temporary scores keyed by module name
left_panel_expanded = True
# ------------------------
# HELPERS: grading, placeholder check, output coloring
# ------------------------
def get_grade(average):
    if average >= 80: return "A"
    if average >= 70: return "B"
    if average >= 60: return "C"
    if average >= 50: return "D"
    return "F"

def get_gpa(average):
    if average >= 80: return 4.0
    if average >= 70: return 3.0
    if average >= 60: return 2.0
    if average >= 50: return 1.0
    return 0.0

def grade_from_gpa(gpa):
    if gpa >= 3.5: return "A"
    if gpa >= 2.5: return "B"
    if gpa >= 1.5: return "C"
    if gpa >= 1.0: return "D"
    return "F"

def color_status_in_output():
    start = "1.0"
    while True:
        pos = output_box.search("PASSED", start, tk.END)
        if not pos: break
        end = f"{pos}+6c"
        output_box.tag_add("passed", pos, end)
        start = end
    output_box.tag_config("passed", foreground="green", font=("Courier", 10, "bold"))
    start = "1.0"
    while True:
        pos = output_box.search("FAILED", start, tk.END)
        if not pos: break
        end = f"{pos}+6c"
        output_box.tag_add("failed", pos, end)
        start = end
    output_box.tag_config("failed", foreground="red", font=("Courier", 10, "bold"))

def is_placeholder(value):
    """Return True if value is None, empty, or looks like a '-- Select ...' placeholder."""
    if value is None:
        return True
    text = str(value).strip()
    if text == "":
        return True
    return text.lower().startswith("-- select")

# ------------------------
# RECORD BUILDER
# ------------------------
def build_semester_record(name, student_id, age, gender, faculty, programme, semester, modules_scores, date_str=None, record_id=None):
    """
    modules_scores: list of dict { 'module':name, 'assignment1':int, 'final_project':int, 'test':int, 'exam':int }
    If record_id provided, use it; otherwise create new unique id.
    """
    uid = record_id if record_id is not None else str(uuid.uuid4())

    module_reports = []
    module_gpas = []
    module_summaries = []

    for m in modules_scores:
        a1 = m['assignment1']; fp = m['final_project']; test = m['test']; exam = m['exam']
        total = a1 + fp + test + exam
        average = total / 4.0
        grade = get_grade(average)
        gpa = get_gpa(average)
        status = "PASSED" if average >= PASS_MARK else "FAILED"
        module_code = m['module'].split(" - ")[0]
        module_reports.append(
            f"Module: {m['module']}\n"
            f"  Assignment 1 : {a1}\n"
            f"  Final Project: {fp}\n"
            f"  Test Score   : {test}\n"
            f"  Exam         : {exam}\n"
            f"  Average      : {average:.2f}\n"
            f"  Grade        : {grade}\n"
            f"  GPA          : {gpa}\n"
            f"  Status       : {status}\n"
            "---------------------------------\n"
        )
        module_gpas.append(gpa)
        module_summaries.append({
            "module": m['module'],
            "module_code": module_code,
            "assignment1": a1,
            "final_project": fp,
            "test": test,
            "exam": exam,
            "total": total,
            "average": average,
            "grade": grade,
            "gpa": gpa,
            "status": status
        })

    cgpa = statistics.mean(module_gpas) if module_gpas else 0.0
    overall_grade = grade_from_gpa(cgpa)
    status = "PASSED" if cgpa >= (get_gpa(PASS_MARK)) else "FAILED"

    if date_str is None:
        date_str = datetime.now().strftime("%d/%m/%Y  %H:%M")

    report_header = f"""
=================================
  SEMESTER ACADEMIC REPORT
=================================
Student Name : {name}
Student ID   : {student_id}
Age          : {age}
Gender       : {gender}
---------------------------------
Faculty      : {faculty}
Programme    : {programme}
Semester     : {semester}
---------------------------------
"""
    modules_section = "\n".join(module_reports)
    summary_section = f"""
---------------------------------
Semester CGPA : {cgpa:.2f}
Semester Grade: {overall_grade}
Status        : {status}
---------------------------------
Date         : {date_str}
=================================
"""
    report = report_header + "\n--- MODULE RESULTS ---\n" + modules_section + summary_section

    record = {
        "id": uid,
        "name": name,
        "student_id": student_id,
        "age": int(age),
        "gender": gender,
        "faculty": faculty,
        "programme": programme,
        "semester": semester,
        "modules": module_summaries,
        "cgpa": cgpa,
        "average": cgpa,
        "grade": overall_grade,
        "gpa": cgpa,
        "status": status,
        "date": date_str,
        "report": report
    }
    return record

# ------------------------
# UI BUILD
# ------------------------
root = tk.Tk()
root.title("Limkokwing University - Student Academic Portal")
root.geometry("1200x920")

# Top header
top_header = tk.Frame(root, bg="black", height=70)
top_header.pack(fill="x"); top_header.pack_propagate(False)
tk.Label(top_header, text="LIMKOKWING UNIVERSITY", font=("Arial", 18, "bold"), fg="white", bg="black").pack(side="left", padx=12, pady=8)
big_header_total = tk.Label(top_header, text="0", font=("Arial", 28, "bold"), fg="white", bg="black")
big_header_total.pack(side="right", padx=16, pady=6)

# Main two-column layout
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=8, pady=6)

# LEFT column (fixed)
left_container = tk.Frame(main_frame)
left_container.pack(side="left", fill="y")

canvas = tk.Canvas(left_container, width=360)
scrollbar = tk.Scrollbar(left_container,
orient="vertical", command=canvas.yview)

scroll_frame = tk.Frame(canvas)

scroll_frame.bind(
    "<Configure>",
    lambda e:
canvas.configure(scrollregion=canvas.bbox("all")
)
)
canvas.create_window((0,0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="y")
scrollbar.pack(side="right", fill="y")

# Student Registration frame
info_frame = tk.LabelFrame(scroll_frame, text="Student Registration", padx=8, pady=6)
info_frame.pack(fill="x", padx=6, pady=6)

tk.Label(info_frame, text="Student Name").grid(row=0, column=0, sticky="w")
entry_name = tk.Entry(info_frame, width=28)
entry_name.grid(row=1, column=0, pady=3)

tk.Label(info_frame, text="Student ID").grid(row=2, column=0, sticky="w")
entry_id = tk.Entry(info_frame, width=28)
entry_id.grid(row=3, column=0, pady=3)

tk.Label(info_frame, text="Age").grid(row=4, column=0, sticky="w")
entry_age = tk.Entry(info_frame, width=12)
entry_age.grid(row=5, column=0, pady=3, sticky="w")

tk.Label(info_frame, text="Gender").grid(row=6, column=0, sticky="w")
gender_var = tk.StringVar(value="Male")
gender_menu = tk.OptionMenu(info_frame, gender_var, "Male", "Female")
gender_menu.grid(row=7, column=0, pady=3, sticky="w")

tk.Label(info_frame, text="Faculty / Department").grid(row=8, column=0, sticky="w")
dept_var = tk.StringVar(value="-- Select Faculty --")
dept_menu = tk.OptionMenu(info_frame, dept_var, *["-- Select Faculty --"] + FACULTIES)
dept_menu.config(width=30)
dept_menu.grid(row=9, column=0, pady=3, sticky="w")

# Programme var defined once and used everywhere
programme_var = tk.StringVar(value="-- Select Programme --")
tk.Label(info_frame, text="Programme").grid(row=10, column=0, sticky="w")
prog_menu = tk.OptionMenu(info_frame, programme_var, *PROGRAMMES)
prog_menu.config(width=30)
prog_menu.grid(row=11, column=0, pady=3, sticky="w")

tk.Label(info_frame, text="Semester").grid(row=12, column=0, sticky="w")
semester_var = tk.StringVar(value="-- Select Semester --")
semester_menu = tk.OptionMenu(info_frame, semester_var, *["-- Select Semester --"] + SEMESTERS)
semester_menu.config(width=20)
semester_menu.grid(row=13, column=0, pady=3, sticky="w")

# Module selection and scores
module_frame = tk.LabelFrame(scroll_frame, text="Modules & Scores", padx=6, pady=6)
module_frame.pack(fill="both", expand=False, padx=6, pady=(0,6))

tk.Label(module_frame, text="Available Modules (multi-select):").pack(anchor="w")
module_listbox = tk.Listbox(module_frame, selectmode=tk.MULTIPLE, height=7, width=45)
module_listbox.pack(padx=4, pady=4)
for m in MODULES:
    module_listbox.insert(tk.END, m)

tk.Button(module_frame, text="Generate Modules", command=lambda: open_module_scores_popup(), bg="navy", fg="white", width=20).pack(pady=(4,6))
tk.Label(module_frame, text="Enter Assignment 1, Final Project, Test, Exam for each selected module", wraplength=320, font=("Arial",9,"italic")).pack(padx=4)

# Action buttons: New Student clears inputs only; Clear Form clears output only
actions_frame = tk.Frame(scroll_frame)
actions_frame.pack(fill="x", padx=6, pady=6)
tk.Button(actions_frame, text="Generate Report", command=lambda: generate_report_action(), bg="navy", fg="white", width=16).pack(fill="x", pady=2)
tk.Button(actions_frame, text="New Student", command=lambda: new_student_action(), bg="dark green", fg="white", width=12).pack(fill="x", pady=2)
tk.Button(actions_frame, text="Clear Form", command=lambda: clear_output_action(), bg="orange", width=12).pack(fill="x", pady=2)
tk.Button(
    actions_frame,
    text="Exit",
    command=root.destroy,
    bg="red",
    fg="white",
    width=12
).pack(fill="x", pady=2)
# RIGHT column
right_col = tk.Frame(main_frame)
right_col.pack(side="left", fill="both", expand=True)

controls_frame = tk.Frame(right_col)
controls_frame.pack(fill="x", padx=4, pady=(0,6))
tk.Button(controls_frame, text="View Records", command=lambda: refresh_treeview(), width=14).pack(side="left", padx=6)
tk.Button(controls_frame, text="Filter & Search", command=lambda: open_filter_window(), width=14).pack(side="left", padx=6)
tk.Button(controls_frame, text="Delete Selected", command=lambda: delete_selected_action(), bg="dark red", fg="white", width=14).pack(side="right", padx=8)

# Dashboard tiles
tiles_frame = tk.Frame(right_col)
tiles_frame.pack(fill="x", padx=4, pady=(0,6))

def make_tile(parent, title):
    f = tk.Frame(parent, bg="#f2f2f2", bd=1, relief="solid", height=70)
    f.pack_propagate(False)
    tk.Label(f, text=title, font=("Arial",9), bg="#f2f2f2").pack(anchor="nw", padx=8, pady=(6,0))
    val = tk.Label(f, text="0", font=("Arial",20,"bold"), bg="#f2f2f2")
    val.pack(expand=True)
    return f, val

tile_total, label_total = make_tile(tiles_frame, "TOTAL STUDENTS")
tile_male, label_male = make_tile(tiles_frame, "MALE STUDENTS")
tile_female, label_female = make_tile(tiles_frame, "FEMALE STUDENTS")
tile_risk, label_risk = make_tile(tiles_frame, "HIGH RISK (FAILED)")

tile_total.pack(side="left", padx=6, fill="x", expand=True)
tile_male.pack(side="left", padx=6, fill="x", expand=True)
tile_female.pack(side="left", padx=6, fill="x", expand=True)
tile_risk.pack(side="left", padx=6, fill="x", expand=True)

# Notebook with Records & Statistics
notebook = ttk.Notebook(right_col)
notebook.pack(fill="both", expand=True, padx=4, pady=6)

# Records tab
records_tab = tk.Frame(notebook)
notebook.add(records_tab, text="Records")
cols = ("No", "Name", "Age", "Gender", "Semester", "CGPA", "Grade", "Status")
records_tree = ttk.Treeview(records_tab, columns=cols, show="headings", selectmode="extended")
for c in cols:
    records_tree.heading(c, text=c)
records_tree.column("No", width=50, anchor="w")
records_tree.column("Name", width=220, anchor="w")
records_tree.column("Age", width=50, anchor="center")
records_tree.column("Gender", width=70, anchor="center")
records_tree.column("Semester", width=100, anchor="center")
records_tree.column("CGPA", width=80, anchor="center")
records_tree.column("Grade", width=70, anchor="center")
records_tree.column("Status", width=90, anchor="center")
records_tree.pack(fill="both", expand=False, padx=4, pady=(4,0), ipady=6)
records_tree.bind("<<TreeviewSelect>>", lambda e: show_record_report(e))
records_tree.bind("<Double-1>", lambda e: edit_selected_action(e))

# Output box
output_frame = tk.Frame(records_tab, bd=1, relief="sunken")
output_frame.pack(fill="both", expand=True, padx=4, pady=6)
output_scroll_y = tk.Scrollbar(output_frame); output_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
output_box = tk.Text(output_frame, font=("Courier",10), wrap="none", yscrollcommand=output_scroll_y.set)
output_box.pack(fill="both", expand=True)
output_scroll_y.config(command=output_box.yview)

# Statistics tab
stats_tab = tk.Frame(notebook)
notebook.add(stats_tab, text="Statistics")
stat_frame = tk.Frame(stats_tab, padx=12, pady=12)
stat_frame.pack(fill="both", expand=True)
stat_total_var = tk.StringVar(value="0")
stat_male_var = tk.StringVar(value="0")
stat_female_var = tk.StringVar(value="0")
stat_pass_rate_var = tk.StringVar(value="0%")
stat_avg_cgpa_var = tk.StringVar(value="0.00")
tk.Label(stat_frame, text="Total Students:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=6); tk.Label(stat_frame, textvariable=stat_total_var, font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w")
tk.Label(stat_frame, text="Male Students:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=6); tk.Label(stat_frame, textvariable=stat_male_var, font=("Arial", 12, "bold")).grid(row=1, column=1, sticky="w")
tk.Label(stat_frame, text="Female Students:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=6); tk.Label(stat_frame, textvariable=stat_female_var, font=("Arial", 12, "bold")).grid(row=2, column=1, sticky="w")
tk.Label(stat_frame, text="Pass Rate:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=6); tk.Label(stat_frame, textvariable=stat_pass_rate_var, font=("Arial", 12, "bold")).grid(row=3, column=1, sticky="w")
tk.Label(stat_frame, text="Average CGPA:", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=6); tk.Label(stat_frame, textvariable=stat_avg_cgpa_var, font=("Arial", 12, "bold")).grid(row=4, column=1, sticky="w")

# ------------------------
# BEHAVIOR FUNCTIONS
# ------------------------
def refresh_treeview():
    for row in records_tree.get_children():
        records_tree.delete(row)
    for idx, rec in enumerate(students, start=1):
        records_tree.insert("", "end", iid=rec['id'], values=(idx, rec['name'], rec['age'], rec['gender'], rec['semester'], f"{rec['cgpa']:.2f}", rec['grade'], rec['status']))

def update_dashboard_metrics():
    total = len(students)
    males = sum(1 for s in students if s.get('gender') == 'Male')
    females = sum(1 for s in students if s.get('gender') == 'Female')
    fails = sum(1 for s in students if s.get('status') == 'FAILED')
    avg_cgpa = statistics.mean([s['cgpa'] for s in students]) if students else 0.0
    label_total.config(text=str(total)); label_male.config(text=str(males)); label_female.config(text=str(females)); label_risk.config(text=str(fails))
    big_header_total.config(text=str(total))
    stat_total_var.set(str(total)); stat_male_var.set(str(males)); stat_female_var.set(str(females))
    stat_pass_rate_var.set(f"{(1 - (fails/total)) * 100:.1f}%" if total else "0%")
    stat_avg_cgpa_var.set(f"{avg_cgpa:.2f}")

def show_record_report(event=None):
    sel = records_tree.selection()
    if not sel:
        return
    rec_id = sel[0]
    rec = next((r for r in students if r['id'] == rec_id), None)
    if rec:
        output_box.delete(1.0, tk.END); output_box.insert(tk.END, rec['report']); color_status_in_output()

def delete_selected_action():
    sel = records_tree.selection()
    if not sel:
        messagebox.showinfo("Delete Selected", "Please select one or more records in the table to delete.")
        return
    if not messagebox.askyesno("Confirm Delete", f"Delete {len(sel)} selected record(s)? This cannot be undone."):
        return
    for rec_id in sel:
        idx = next((i for i,r in enumerate(students) if r['id'] == rec_id), None)
        if idx is not None:
            students.pop(idx)
    refresh_treeview(); update_dashboard_metrics(); output_box.delete(1.0, tk.END)

def edit_selected_action(event=None):
    sel = records_tree.selection()
    if not sel:
        messagebox.showinfo("Edit Record", "Double-click a row or select one and click Edit to update a record.")
        return
    rec_id = sel[0]
    rec = next((r for r in students if r['id'] == rec_id), None)
    if not rec:
        return
    popup = tk.Toplevel(root); popup.title("Edit Student Record"); popup.geometry("600x600"); popup.transient(root)
    tk.Label(popup, text="Edit Student Details", font=("Arial",12,"bold")).pack(pady=(8,4))
    form = tk.Frame(popup); form.pack(padx=8, pady=4, fill="x")
    tk.Label(form, text="Name").grid(row=0, column=0, sticky="w"); e_name = tk.Entry(form, width=36); e_name.grid(row=0, column=1, sticky="w"); e_name.insert(0, rec['name'])
    tk.Label(form, text="Student ID").grid(row=1, column=0, sticky="w"); e_sid = tk.Entry(form, width=20); e_sid.grid(row=1, column=1, sticky="w"); e_sid.insert(0, rec['student_id'])
    tk.Label(form, text="Age").grid(row=2, column=0, sticky="w"); e_age = tk.Entry(form, width=6); e_age.grid(row=2, column=1, sticky="w"); e_age.insert(0, str(rec['age']))
    tk.Label(form, text="Gender").grid(row=3, column=0, sticky="w"); g_var = tk.StringVar(value=rec['gender']); tk.OptionMenu(form, g_var, "Male","Female").grid(row=3, column=1, sticky="w")
    tk.Label(form, text="Faculty").grid(row=4, column=0, sticky="w"); f_var = tk.StringVar(value=rec['faculty']); f_menu = tk.OptionMenu(form, f_var, *FACULTIES); f_menu.config(width=30); f_menu.grid(row=4, column=1, sticky="w")
    tk.Label(form, text="Programme").grid(row=5, column=0, sticky="w"); p_var = tk.StringVar(value=rec['programme']); p_menu = tk.OptionMenu(form, p_var, *PROGRAMMES); p_menu.config(width=30); p_menu.grid(row=5, column=1, sticky="w")
    tk.Label(form, text="Semester").grid(row=6, column=0, sticky="w"); sem_var = tk.StringVar(value=rec['semester']); sem_menu = tk.OptionMenu(form, sem_var, *SEMESTERS); sem_menu.grid(row=6, column=1, sticky="w")
    modules_container = tk.Frame(popup); modules_container.pack(fill="both", expand=True, padx=8, pady=8)
    tk.Label(modules_container, text="Module Scores (edit values then Save):", font=("Arial",10,"bold")).pack(anchor="w")
    canvas = tk.Canvas(modules_container); sb = tk.Scrollbar(modules_container, orient="vertical", command=canvas.yview); inner = tk.Frame(canvas)
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=inner, anchor="nw"); canvas.configure(yscrollcommand=sb.set); canvas.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
    edit_entries = {}
    for idx, m in enumerate(rec['modules'], start=1):
        f = tk.LabelFrame(inner, text=f"{idx}. {m['module']}", padx=6, pady=6); f.pack(fill="x", padx=6, pady=6)
        tk.Label(f, text="Assignment 1:").grid(row=0, column=0); e_a1 = tk.Entry(f, width=8); e_a1.grid(row=0, column=1, padx=6); e_a1.insert(0, str(m['assignment1']))
        tk.Label(f, text="Final Project:").grid(row=0, column=2); e_fp = tk.Entry(f, width=8); e_fp.grid(row=0, column=3, padx=6); e_fp.insert(0, str(m['final_project']))
        tk.Label(f, text="Test Score:").grid(row=1, column=0); e_test = tk.Entry(f, width=8); e_test.grid(row=1, column=1, padx=6); e_test.insert(0, str(m['test']))
        tk.Label(f, text="Exam:").grid(row=1, column=2); e_exam = tk.Entry(f, width=8); e_exam.grid(row=1, column=3, padx=6); e_exam.insert(0, str(m['exam']))
        edit_entries[m['module']] = {'assignment1': e_a1, 'final_project': e_fp, 'test': e_test, 'exam': e_exam}
    def save_edited():
        new_name = e_name.get().strip(); new_sid = e_sid.get().strip()
        try:
            new_age = int(e_age.get().strip())
        except:
            messagebox.showerror("Invalid", "Age must be a number", parent=popup); return
        new_gender = g_var.get(); new_fac = f_var.get(); new_prog = p_var.get(); new_sem = sem_var.get()
        if not new_name or not new_sid:
            messagebox.showerror("Missing", "Name and Student ID required", parent=popup); return
        new_modules_scores = []
        for mod_name, widgets in edit_entries.items():
            try:
                a1 = int(widgets['assignment1'].get()); fp = int(widgets['final_project'].get()); test = int(widgets['test'].get()); exam = int(widgets['exam'].get())
            except:
                messagebox.showerror("Invalid", f"Scores for {mod_name} must be whole numbers", parent=popup); return
            for val,label in [(a1,"Assignment 1"), (fp,"Final Project"), (test,"Test"), (exam,"Exam")]:
                if val < 0 or val > 100:
                    messagebox.showerror("Invalid", f"{label} for {mod_name} must be 0-100", parent=popup); return
            new_modules_scores.append({'module': mod_name, 'assignment1': a1, 'final_project': fp, 'test': test, 'exam': exam})
        new_record = build_semester_record(new_name, new_sid, new_age, new_gender, new_fac, new_prog, new_sem, new_modules_scores, record_id=rec['id'])
        idx = next((i for i,r in enumerate(students) if r['id'] == rec['id']), None)
        if idx is not None:
            students[idx] = new_record
        refresh_treeview(); update_dashboard_metrics()
        output_box.delete(1.0, tk.END); output_box.insert(tk.END, new_record['report']); color_status_in_output()
        popup.destroy()
    tk.Button(popup, text="Save Changes", command=save_edited, bg="navy", fg="white", width=18).pack(pady=8)

def open_module_scores_popup():
    selection = module_listbox.curselection()
    if not selection:
        messagebox.showerror("No Modules Selected", "Please select one or more modules from the list first.")
        return
    modules = [module_listbox.get(i) for i in selection]
    popup = tk.Toplevel(root); popup.title("Enter Module Scores"); popup.geometry("620x420"); popup.transient(root)
    canvas = tk.Canvas(popup); scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview); scroll_frame = tk.Frame(canvas)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw"); canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    entries = {}
    for idx, mod in enumerate(modules):
        frame = tk.LabelFrame(scroll_frame, text=f"{idx+1}. {mod}", padx=8, pady=6); frame.pack(fill="x", padx=6, pady=6)
        tk.Label(frame, text="Assignment 1:").grid(row=0, column=0, sticky="e"); e_a1 = tk.Entry(frame, width=8); e_a1.grid(row=0, column=1, padx=(6,20))
        tk.Label(frame, text="Final Project:").grid(row=0, column=2, sticky="e"); e_fp = tk.Entry(frame, width=8); e_fp.grid(row=0, column=3, padx=(6,20))
        tk.Label(frame, text="Test Score:").grid(row=1, column=0, sticky="e"); e_test = tk.Entry(frame, width=8); e_test.grid(row=1, column=1, padx=(6,20))
        tk.Label(frame, text="Exam:").grid(row=1, column=2, sticky="e"); e_exam = tk.Entry(frame, width=8); e_exam.grid(row=1, column=3, padx=(6,20))
        prev = current_module_scores.get(mod)
        if prev:
            e_a1.insert(0, str(prev.get('assignment1',''))); e_fp.insert(0, str(prev.get('final_project',''))); e_test.insert(0, str(prev.get('test',''))); e_exam.insert(0, str(prev.get('exam','')))
        entries[mod] = {'assignment1': e_a1, 'final_project': e_fp, 'test': e_test, 'exam': e_exam}
    def save_scores():
        for mod, widget_dict in entries.items():
            try:
                a1 = int(widget_dict['assignment1'].get()); fp = int(widget_dict['final_project'].get()); test = int(widget_dict['test'].get()); exam = int(widget_dict['exam'].get())
            except:
                messagebox.showerror("Invalid Input", f"All scores for {mod} must be whole numbers 0-100", parent=popup); return
            for val, label in [(a1,"Assignment 1"), (fp,"Final Project"), (test,"Test"), (exam,"Exam")]:
                if val < 0 or val > 100:
                    messagebox.showerror("Invalid Input", f"{label} score for {mod} must be between 0 and 100", parent=popup); return
            current_module_scores[mod] = {'assignment1': a1, 'final_project': fp, 'test': test, 'exam': exam}
        messagebox.showinfo("Saved", "Module scores saved for the selected modules.", parent=popup); popup.destroy()
    tk.Button(popup, text="Save Scores", command=save_scores, bg="navy", fg="white", width=18).pack(pady=10)

# New Student: clears registration inputs & module selection (keeps output area)
def new_student_action():
    entry_name.delete(0, tk.END); entry_id.delete(0, tk.END); entry_age.delete(0, tk.END)
    gender_var.set("Male"); dept_var.set("-- Select Faculty --"); programme_var.set("-- Select Programme --"); semester_var.set("-- Select Semester --")
    module_listbox.selection_clear(0, tk.END); current_module_scores.clear()
    output_box.deleted(1.0, tk.END)
    entry_name.focus()

# Clear Form: clears the report DISPLAY only (output area), does NOT delete saved records
def clear_output_action():
    output_box.delete(1.0, tk.END)

def generate_report_action():
    name = entry_name.get().strip(); studentid_text = entry_id.get().strip(); age_text = entry_age.get().strip()
    gender = gender_var.get(); faculty = dept_var.get(); programme = programme_var.get(); semester = semester_var.get()
    if not name:
        messagebox.showerror("Missing Information", "Please enter the student's full name"); return
    if not studentid_text:
        messagebox.showerror("Missing Information", "Please enter the Student ID"); return
    if not age_text:
        messagebox.showerror("Missing Information", "Please enter the student's age"); return
    if is_placeholder(faculty):
        messagebox.showerror("Missing Information", "Please select a Faculty / Department"); return
    if is_placeholder(programme):
        messagebox.showerror("Missing Information", "Please select a Programme"); return
    if is_placeholder(semester):
        messagebox.showerror("Missing Information", "Please select a Semester"); return
    try:
        age = int(age_text)
    except:
        messagebox.showerror("Error", "Age must be a valid whole number"); return
    if age < 15 or age > 60:
        messagebox.showerror("Invalid Input", "Age must be between 15 and 60"); return
    selection = module_listbox.curselection(); selected_modules = [module_listbox.get(i) for i in selection]
    if not selected_modules:
        messagebox.showerror("No Modules Selected", "Please select one or more modules for this semester."); return
    missing = [m for m in selected_modules if m not in current_module_scores]
    if missing:
        messagebox.showerror("Missing Scores", "Please click 'Enter Module Scores' and enter scores for every selected module.\nMissing: " + ", ".join(missing)); return
    modules_scores = []
    for m in selected_modules:
        sc = current_module_scores.get(m)
        try:
            a1 = int(sc['assignment1']); fp = int(sc['final_project']); test = int(sc['test']); exam = int(sc['exam'])
        except:
            messagebox.showerror("Invalid Input", f"All scores for {m} must be whole numbers."); return
        for val,label in [(a1,"Assignment 1"), (fp,"Final Project"), (test,"Test"), (exam,"Exam")]:
            if val < 0 or val > 100:
                messagebox.showerror("Invalid Input", f"{label} score for {m} must be between 0 and 100"); return
        modules_scores.append({'module': m, 'assignment1': a1, 'final_project': fp, 'test': test, 'exam': exam})
    new_rec = build_semester_record(name, studentid_text, age, gender, faculty, programme, semester, modules_scores)
    students.append(new_rec); refresh_treeview(); update_dashboard_metrics()
    output_box.delete(1.0, tk.END); output_box.insert(tk.END, new_rec['report']); color_status_in_output()
    # DO NOT clear the report automatically; keep visible. Clear inputs for next entry if you want:
    # new_student_action()  # optional automatic clearing

def open_filter_window():
    win = tk.Toplevel(root); win.title("Filter & Search Students"); win.geometry("480x780"); win.resizable(False, False)
    tk.Label(win, text="🔍  Filter & Search Students", font=("Arial", 13, "bold")).pack(pady=(14, 8))
    tk.Label(win, text="Leave a filter on 'All' to ignore it. Combine as many as you like.", font=("Arial", 8, "italic"), fg="grey30").pack(pady=(0, 8))
    tk.Label(win, text="Search by Student Name:", font=("Arial", 9, "bold")).pack()
    search_entry = tk.Entry(win, width=36); search_entry.pack(pady=(2, 10))
    tk.Label(win, text="Age Range:", font=("Arial", 9, "bold")).pack()
    age_row = tk.Frame(win); age_row.pack(pady=(2, 10))
    min_age_entry = tk.Entry(age_row, width=8); min_age_entry.pack(side="left", padx=4)
    tk.Label(age_row, text="to").pack(side="left")
    max_age_entry = tk.Entry(age_row, width=8); max_age_entry.pack(side="left", padx=4)
    tk.Label(win, text="Gender:", font=("Arial", 9, "bold")).pack()
    f_gender_var = tk.StringVar(value="All"); tk.OptionMenu(win, f_gender_var, "All", "Male", "Female").pack(pady=(2, 10))
    tk.Label(win, text="Faculty / Department:", font=("Arial", 9, "bold")).pack()
    f_faculty_var = tk.StringVar(value="All"); tk.OptionMenu(win, f_faculty_var, "All", *FACULTIES).pack(pady=(2, 10))
    tk.Label(win, text="Programme:", font=("Arial", 9, "bold")).pack()
    f_programme_var = tk.StringVar(value="All"); tk.OptionMenu(win, f_programme_var, "All", *PROGRAMMES[1:]).pack(pady=(2, 10))
    tk.Label(win, text="Semester:", font=("Arial", 9, "bold")).pack()
    f_semester_var = tk.StringVar(value="All"); tk.OptionMenu(win, f_semester_var, "All", *SEMESTERS).pack(pady=(2, 10))
    tk.Label(win, text="Module / Course Unit:", font=("Arial", 9, "bold")).pack()
    f_module_var = tk.StringVar(value="All"); tk.OptionMenu(win, f_module_var, "All", *MODULES).pack(pady=(2, 10))
    tk.Label(win, text="Status:", font=("Arial", 9, "bold")).pack()
    f_status_var = tk.StringVar(value="All"); tk.OptionMenu(win, f_status_var, "All", "PASSED", "FAILED").pack(pady=(2, 10))
    result_label = tk.Label(win, text="", font=("Arial", 9, "bold")); result_label.pack(pady=(6, 4))
    def do_apply():
        name_query = search_entry.get().strip().lower()
        min_age_text = min_age_entry.get().strip()
        max_age_text = max_age_entry.get().strip()
        filtered = students[:]
        if name_query:
            filtered = [s for s in filtered if name_query in s["name"].lower()]
        if min_age_text:
            try: min_age_val = int(min_age_text)
            except:
                messagebox.showerror("Invalid Input", "Minimum age must be a number", parent=win); return
            filtered = [s for s in filtered if s["age"] >= min_age_val]
        if max_age_text:
            try: max_age_val = int(max_age_text)
            except:
                messagebox.showerror("Invalid Input", "Maximum age must be a number", parent=win); return
            filtered = [s for s in filtered if s["age"] <= max_age_val]
        if f_gender_var.get() != "All":
            filtered = [s for s in filtered if s["gender"] == f_gender_var.get()]
        if f_faculty_var.get() != "All":
            filtered = [s for s in filtered if s["faculty"] == f_faculty_var.get()]
        if f_programme_var.get() != "All":
            filtered = [s for s in filtered if s["programme"] == f_programme_var.get()]
        if f_semester_var.get() != "All":
            filtered = [s for s in filtered if s.get("semester") == f_semester_var.get()]
        if f_module_var.get() != "All":
            filtered = [s for s in filtered if ((s.get("modules") and any(m['module'] == f_module_var.get() for m in s['modules'])))]
        if f_status_var.get() != "All":
            filtered = [s for s in filtered if s["status"] == f_status_var.get()]
        if len(filtered) == 0:
            result_label.config(text="❌  No students found.", fg="red")
            messagebox.showinfo("Not Found", "No students were found matching your search or filter criteria.", parent=win)
        else:
            result_label.config(text=f"✅  Found {len(filtered)} student(s).", fg="dark green")
            for row in records_tree.get_children(): records_tree.delete(row)
            for idx, r in enumerate(filtered, start=1):
                records_tree.insert("", "end", iid=r['id'], values=(idx, r['name'], r['age'], r['gender'], r['semester'], f"{r['cgpa']:.2f}", r['grade'], r['status']))
    def do_clear():
        search_entry.delete(0, tk.END); min_age_entry.delete(0, tk.END); max_age_entry.delete(0, tk.END)
        f_gender_var.set("All"); f_faculty_var.set("All"); f_programme_var.set("All"); f_semester_var.set("All"); f_module_var.set("All"); f_status_var.set("All")
        result_label.config(text=""); refresh_treeview()
    tk.Button(win, text="Apply Filter", command=do_apply, bg="navy", fg="white", width=24).pack(pady=4)
    tk.Button(win, text="Clear & Show All", command=do_clear, width=24).pack(pady=2)
    tk.Button(win, text="Close", command=win.destroy, width=24).pack(pady=(2, 14))

# ------------------------
# Dummy data loader
# ------------------------
def load_dummy_data():
    random.seed(12)
    start_date = datetime(2026, 3, 2); end_date = datetime(2026, 6, 13); day_range = (end_date - start_date).days
    for i in range(50):
        gender = random.choice(["Male", "Female"])
        first_name = random.choice(MALE_NAMES if gender == "Male" else FEMALE_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        student_id = f"LUCT-{1000 + i}"
        age = random.randint(18, 32)
        faculty = random.choice(FACULTIES)
        programme = random.choice(PROGRAMMES[1:])
        semester = random.choice(SEMESTERS)
        available = MODULES.copy()
        if len(available) >= 6:
            mods = random.sample(available, k=6)
        else:
            mods = [random.choice(available) for _ in range(6)]
        modules_scores = []
        for mod in mods:
            a1 = random.randint(35, 100); fp = random.randint(35, 100); test = random.randint(35, 100); exam = random.randint(35, 100)
            modules_scores.append({'module': mod, 'assignment1': a1, 'final_project': fp, 'test': test, 'exam': exam})
        random_day = random.randint(0, day_range)
        random_time = start_date + timedelta(days=random_day, hours=random.randint(8, 17), minutes=random.choice([0, 15, 30, 45]))
        date_str = random_time.strftime("%d/%m/%Y  %H:%M")
        rec = build_semester_record(name, student_id, age, gender, faculty, programme, semester, modules_scores, date_str)
        students.append(rec)

# Connect programme_var trace AFTER UI elements exist (module_listbox)
def on_programme_change_fn(*args):
    prog = programme_var.get()
    module_listbox.delete(0, tk.END)
    modules_to_show = PROGRAMME_MODULES.get(prog, MODULES)
    for m in modules_to_show: module_listbox.insert(tk.END, m)
    current_module_scores.clear(); module_listbox.selection_clear(0, tk.END)

programme_var.trace("w", on_programme_change_fn)

# Load dummy data and populate UI
load_dummy_data()
refresh_treeview()
update_dashboard_metrics()

# Welcome note
#output_box.insert(tk.END,
   # "\n  Welcome to the Limkokwing University Student Academic Portal.\n\n"
    #"  50 sample student records have been loaded automatically (each with 6 modules and CGPA).\n\n"
   # "  - Use the left column to add a new student and Enter Module Scores for each selected module.\n"
   # "  - Click 'Generate Report' to save; the Records tab shows all records. Double-click a row to edit.\n  - 'New Student' clears the input form only (keeps the report visible).\n  - 'Clear Form' clears the report DISPLAY only (keeps the saved record in Records).\n"
#)
color_status_in_output()

root.mainloop()