import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ---- CONSTANT ----
PASS_MARK = 60

# ---- RECORDS LIST ----
# Changed from storing plain text to storing dictionaries
# so we can use the data to build a summary table in view_records
students = []

# ---- FUNCTION 1: Get letter grade ----
def get_grade(average):

    if average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"

# ---- FUNCTION 2: Get GPA ----
def get_gpa(average):

    if average >= 80:
        return 4.0
    elif average >= 70:
        return 3.0
    elif average >= 60:
        return 2.0
    elif average >= 50:
        return 1.0
    else:
        return 0.0

# ---- HELPER FUNCTION: Color PASSED green and FAILED red ----
# This searches the output box for the words PASSED and FAILED
# and colors them - this is the "little magic" for professionalism
def color_status():

    # Search for every "PASSED" in the output box and color it green
    # We loop because there may be more than one PASSED in the box
    start = "1.0"
    while True:
        pos = output_box.search("PASSED", start, tk.END)
        if not pos:
            break
        end = f"{pos}+6c"           # +6c means 6 characters forward (len of PASSED)
        output_box.tag_add("passed", pos, end)
        start = end                  # move forward so we dont find the same one again

    # Apply the green bold style to all tagged "passed" text
    output_box.tag_config("passed", foreground="green", font=("Courier", 10, "bold"))

    # Search for every "FAILED" in the output box and color it red
    start = "1.0"
    while True:
        pos = output_box.search("FAILED", start, tk.END)
        if not pos:
            break
        end = f"{pos}+6c"
        output_box.tag_add("failed", pos, end)
        start = end

    # Apply the red bold style to all tagged "failed" text
    output_box.tag_config("failed", foreground="red", font=("Courier", 10, "bold"))

# ---- FUNCTION 3: Generate report ----
def generate_report():

    try:

        name        = entry_name.get()
        student_id  = entry_id.get()
        department  = entry_department.get()
        level       = entry_level.get()

        math        = int(entry_math.get())
        english     = int(entry_english.get())
        programming = int(entry_programming.get())
        database    = int(entry_database.get())

        total   = math + english + programming + database
        average = total / 4

        grade  = get_grade(average)
        gpa    = get_gpa(average)

        if average >= PASS_MARK:
            status = "PASSED"
        else:
            status = "FAILED"

        # Date now includes the time as well for precision
        current_date  = datetime.now().strftime("%d/%m/%Y  %H:%M")

        # Record number is how many students are already saved + 1
        record_number = len(students) + 1

        report = f"""
=================================
  ACADEMIC REPORT  [ #{record_number} ]
=================================
Student Name : {name}
Student ID   : {student_id}
Department   : {department}
Level        : {level}
---------------------------------
Math         : {math}
English      : {english}
Programming  : {programming}
Database     : {database}
---------------------------------
Total Score  : {total}
Average      : {average:.2f}
Grade        : {grade}
GPA          : {gpa}
Status       : {status}
---------------------------------
Date         : {current_date}
=================================
"""

        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, report)

        # Color the PASSED or FAILED in the output
        color_status()

        # Save all student data as a dictionary so we can use it in view_records
        students.append({
            "number"     : record_number,
            "name"       : name,
            "student_id" : student_id,
            "department" : department,
            "level"      : level,
            "math"       : math,
            "english"    : english,
            "programming": programming,
            "database"   : database,
            "total"      : total,
            "average"    : average,
            "grade"      : grade,
            "gpa"        : gpa,
            "status"     : status,
            "date"       : current_date,
            "report"     : report
        })

        # Update the counter in the header
        counter_label.config(text=f"Total Students Registered: {len(students)}")

    except:
        messagebox.showerror(
            "Error",
            "Enter valid scores (numbers only)"
        )

# ---- FUNCTION 4: New Student ----
# Clears only the INPUT fields so you can enter the next student
# Does NOT clear the output box - the last report stays visible
def new_student():

    entry_name.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    entry_department.delete(0, tk.END)
    entry_level.delete(0, tk.END)
    entry_math.delete(0, tk.END)
    entry_english.delete(0, tk.END)
    entry_programming.delete(0, tk.END)
    entry_database.delete(0, tk.END)

    # Move the cursor back to the name field automatically
    entry_name.focus()

# ---- FUNCTION 5: Clear everything including output ----
def clear_form():

    entry_name.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    entry_department.delete(0, tk.END)
    entry_level.delete(0, tk.END)
    entry_math.delete(0, tk.END)
    entry_english.delete(0, tk.END)
    entry_programming.delete(0, tk.END)
    entry_database.delete(0, tk.END)

    output_box.delete(1.0, tk.END)

# ---- FUNCTION 6: View all records ----
# Shows a summary table at the top then all full reports below
def view_records():

    output_box.delete(1.0, tk.END)

    if len(students) == 0:
        output_box.insert(
            tk.END,
            "\n   No Records Found.\n   Generate a report first."
        )

    else:

        # Summary header
        output_box.insert(tk.END, f"\n  TOTAL STUDENTS REGISTERED: {len(students)}\n")
        output_box.insert(tk.END, "=" * 55 + "\n")

        # Column headers for the summary table
        output_box.insert(
            tk.END,
            f"  {'#':<5}{'Name':<22}{'Average':<10}{'Grade':<8}{'GPA':<6}Status\n"
        )
        output_box.insert(tk.END, "-" * 55 + "\n")

        # One line per student in the summary table
        for student in students:
            output_box.insert(
                tk.END,
                f"  {student['number']:<5}"
                f"{student['name']:<22}"
                f"{student['average']:<10.2f}"
                f"{student['grade']:<8}"
                f"{student['gpa']:<6}"
                f"{student['status']}\n"
            )

        output_box.insert(tk.END, "=" * 55 + "\n")

        # Full reports section below the summary
        output_box.insert(tk.END, "\n\n  --- FULL REPORTS BELOW ---\n")

        for student in students:
            output_box.insert(tk.END, student["report"])

        # Color all PASSED and FAILED in the entire view
        color_status()

# ================================================================
# BUILD THE WINDOW
# ================================================================

root = tk.Tk()
root.title("Student Academic Portal")
root.geometry("800x730")

# ---- Header ----
header = tk.Frame(root, bg="navy")
header.pack(fill="x")

tk.Label(
    header,
    text="🎓 LIMKOKWING UNIVERSITY\nSTUDENT ACADEMIC PORTAL",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="navy"
).pack(pady=(15, 5))

# Counter label shown in the header - updates every time a report is generated
counter_label = tk.Label(
    header,
    text="Total Students Registered: 0",
    font=("Arial", 10),
    fg="lightblue",
    bg="navy"
)
counter_label.pack(pady=(0, 10))

# ---- Student Information Section ----
info_frame = tk.LabelFrame(root, text="Student Information")
info_frame.pack(fill="x", padx=10, pady=5)

tk.Label(info_frame, text="Student Name").grid(row=0, column=0, padx=5, pady=3, sticky="e")
entry_name = tk.Entry(info_frame, width=28)
entry_name.grid(row=0, column=1, padx=5, pady=3)

tk.Label(info_frame, text="Student ID").grid(row=1, column=0, padx=5, pady=3, sticky="e")
entry_id = tk.Entry(info_frame, width=28)
entry_id.grid(row=1, column=1, padx=5, pady=3)

tk.Label(info_frame, text="Department").grid(row=2, column=0, padx=5, pady=3, sticky="e")
entry_department = tk.Entry(info_frame, width=28)
entry_department.grid(row=2, column=1, padx=5, pady=3)

tk.Label(info_frame, text="Level").grid(row=3, column=0, padx=5, pady=3, sticky="e")
entry_level = tk.Entry(info_frame, width=28)
entry_level.grid(row=3, column=1, padx=5, pady=3)

# ---- Academic Results Section ----
score_frame = tk.LabelFrame(root, text="Academic Results")
score_frame.pack(fill="x", padx=10, pady=5)

tk.Label(score_frame, text="Math").grid(row=0, column=0, padx=5, pady=3, sticky="e")
entry_math = tk.Entry(score_frame, width=28)
entry_math.grid(row=0, column=1, padx=5, pady=3)

tk.Label(score_frame, text="English").grid(row=1, column=0, padx=5, pady=3, sticky="e")
entry_english = tk.Entry(score_frame, width=28)
entry_english.grid(row=1, column=1, padx=5, pady=3)

tk.Label(score_frame, text="Programming").grid(row=2, column=0, padx=5, pady=3, sticky="e")
entry_programming = tk.Entry(score_frame, width=28)
entry_programming.grid(row=2, column=1, padx=5, pady=3)

tk.Label(score_frame, text="Database").grid(row=3, column=0, padx=5, pady=3, sticky="e")
entry_database = tk.Entry(score_frame, width=28)
entry_database.grid(row=3, column=1, padx=5, pady=3)

# ---- Buttons ----
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Generate Report",
    command=generate_report,
    bg="navy",
    fg="white",
    width=14
).grid(row=0, column=0, padx=4)

# NEW BUTTON - clears form only, keeps the last report visible
tk.Button(
    button_frame,
    text="New Student",
    command=new_student,
    bg="dark green",
    fg="white",
    width=14
).grid(row=0, column=1, padx=4)

tk.Button(
    button_frame,
    text="View Records",
    command=view_records,
    bg="dark blue",
    fg="white",
    width=14
).grid(row=0, column=2, padx=4)

tk.Button(
    button_frame,
    text="Clear Form",
    command=clear_form,
    bg="orange",
    width=14
).grid(row=0, column=3, padx=4)

tk.Button(
    button_frame,
    text="Exit Portal",
    command=root.destroy,
    bg="dark red",
    fg="white",
    width=14
).grid(row=0, column=4, padx=4)

# ---- Output Box with Scrollbar ----
# Wrapped in a Frame so the scrollbar sits right beside the text box
output_frame = tk.Frame(root)
output_frame.pack(padx=10, pady=5)

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_box = tk.Text(
    output_frame,
    height=15,
    width=80,
    font=("Courier", 10),            # Courier is a monospace font - columns line up perfectly
    yscrollcommand=scrollbar.set     # connects the scrollbar to the text box
)
output_box.pack(side=tk.LEFT)

# connects the text box scrolling to the scrollbar
scrollbar.config(command=output_box.yview)

root.mainloop()