# ================================================================
#
#   ███████╗████████╗██╗   ██╗██████╗ ███████╗███╗   ██╗████████╗
#   ██╔════╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝████╗  ██║╚══██╔══╝
#   ███████╗   ██║   ██║   ██║██║  ██║█████╗  ██╔██╗ ██║   ██║
#   ╚════██║   ██║   ██║   ██║██║  ██║██╔══╝  ██║╚██╗██║   ██║
#   ███████║   ██║   ╚██████╔╝██████╔╝███████╗██║ ╚████║   ██║
#   ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝
#
#              M A N A G E M E N T   S Y S T E M
#
# ================================================================
#  PROJECT   : Student Management System (SMS)
#  AUTHOR    : Priyanraj J
#  VERSION   : 2.0  (Complete Commented Edition)
#  LANGUAGE  : Python 3 (No external libraries needed)
#  PURPOSE   : A full-featured command-line application to manage
#              student records including marks, attendance,
#              statistics, search, export, backup, and logging.
# ================================================================
#
#  HOW THIS FILE IS ORGANIZED:
#  ─────────────────────────────────────────────────────────────
#  SECTION 1  → Imports & Constants
#  SECTION 2  → Utility / Helper Functions
#  SECTION 3  → File Persistence (Load / Save / Backup)
#  SECTION 4  → Input Validation Functions
#  SECTION 5  → Student Record Builder & Marks Logic
#  SECTION 6  → Display / Print Functions
#  SECTION 7  → Core Features (Add / View / Search / Update /
#                Delete / Attendance / Stats / Sort / Export)
#  SECTION 8  → Sub-Menus (Attendance Menu, Export Menu)
#  SECTION 9  → Main Menu (Program Entry Point)
# ─────────────────────────────────────────────────────────────


# ================================================================
#  SECTION 1 — IMPORTS & CONSTANTS
# ================================================================
#  We import only Python's BUILT-IN libraries so no installation
#  is required. Each library serves a specific role:
#
#   os       → Clear the terminal screen, check if files exist
#   json     → Save and load student data as a .json file
#   csv      → Export student records as a spreadsheet-ready CSV
#   re       → Regular expressions for validating email/phone
#   datetime → Timestamps for logs, attendance dates, exports
# ================================================================

import os
import json
import csv
import re
from datetime import datetime, date

# ── File Names ─────────────────────────────────────────────────
#  These are the names of the files this program creates/uses.
#  Keeping them as constants at the top makes it easy to rename.

DATA_FILE   = "students_data.json"    # Main student database
LOG_FILE    = "activity_log.txt"      # Records every user action
BACKUP_FILE = "students_backup.json"  # Safety copy of data


# ================================================================
#  SECTION 2 — UTILITY / HELPER FUNCTIONS
# ================================================================
#  These are small reusable functions used throughout the program.
#  They handle common tasks like clearing the screen, printing
#  divider lines, and showing a "Press ENTER" pause.
# ================================================================

def clear_screen():
    """
    Clears the terminal window so each menu looks clean.
    Uses 'cls' on Windows and 'clear' on Mac/Linux.
    """
    os.system("cls" if os.name == "nt" else "clear")


def press_enter():
    """
    Pauses the program and waits for the user to press ENTER.
    Called after every action so the user can read the output
    before the screen is cleared for the next menu.
    """
    input("\n  Press ENTER to continue...")


def divider(char="─", width=55):
    """
    Prints a horizontal line using a repeated character.
    Used to visually separate sections inside menus.
    Example output:  ───────────────────────────────────────
    """
    print(f"  {char * width}")


def header(title):
    """
    Clears the screen and prints a formatted page header.
    Every menu/feature calls this first to give a consistent
    look across all screens.

    Example:
      ═══════════════════════════════════════════════════════
               STUDENT MANAGEMENT SYSTEM
      ═══════════════════════════════════════════════════════
                    ➕  ADD NEW STUDENT
      ───────────────────────────────────────────────────────
    """
    clear_screen()
    divider("═")
    print(f"  {'STUDENT MANAGEMENT SYSTEM':^55}")
    divider("═")
    print(f"  {title:^55}")
    divider()
    print()


def log_activity(action: str, detail: str):
    """
    Appends a timestamped record of every user action to the
    activity log file (activity_log.txt).

    Role: Tracks WHO did WHAT and WHEN — useful for auditing.

    Parameters:
        action  → Short label like "ADD", "DELETE", "SEARCH"
        detail  → More info like "Roll: 101  Name: Alice"

    Example log entry:
        [2026-05-30 14:32:10]  ADD                  Roll: 101  Name: Alice
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]  {action:<20}  {detail}\n")


# ================================================================
#  SECTION 3 — FILE PERSISTENCE (LOAD / SAVE / BACKUP / RESTORE)
# ================================================================
#  Student data is stored as a JSON file on disk so it survives
#  after the program closes. JSON is human-readable and easy to
#  work with in Python using the built-in `json` library.
#
#  Database structure (dictionary of dictionaries):
#  {
#    "101": { "name": "Alice", "age": 20, "subjects": {...}, ... },
#    "102": { "name": "Bob",   "age": 21, "subjects": {...}, ... }
#  }
#  Key = Roll Number (string), Value = full student record (dict)
# ================================================================

def load_data() -> dict:
    """
    Loads all student records from the JSON file into memory.

    Role: Called ONCE when the program starts. Returns the full
    student database as a Python dictionary.

    - If the file doesn't exist yet → returns an empty dict {}
    - If the file is corrupted (bad JSON) → warns and returns {}
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)          # Parse JSON → Python dict
        except (json.JSONDecodeError, ValueError):
            print("  ⚠  Data file corrupted. Starting fresh.")
    return {}   # Empty database if file doesn't exist


def save_data(db: dict):
    """
    Saves the current in-memory database to the JSON file.

    Role: Called after EVERY change (add, update, delete, mark
    attendance) so no data is lost if the program closes.

    indent=4 makes the JSON file human-readable with indentation.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)


def backup_data(db: dict):
    """
    Creates a full copy of the database in a separate backup file.

    Role: Safety net — if the main file gets corrupted, the user
    can restore from this backup without losing any data.
    """
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)
    print(f"  ✅  Backup saved → {BACKUP_FILE}")
    log_activity("BACKUP", f"Total records: {len(db)}")


def restore_from_backup() -> dict:
    """
    Loads student records from the backup file.

    Role: Disaster recovery — if main data is lost or corrupted,
    this restores the last saved backup.

    Returns the backup dict on success, None if no backup exists.
    """
    if not os.path.exists(BACKUP_FILE):
        print("  ⚠  No backup file found.")
        return None
    with open(BACKUP_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)
    print(f"  ✅  Restored {len(db)} records from backup.")
    log_activity("RESTORE", f"Total records: {len(db)}")
    return db


# ================================================================
#  SECTION 4 — INPUT VALIDATION FUNCTIONS
# ================================================================
#  Validation ensures the user enters correct data before it is
#  saved. Bad data (wrong email format, letters in phone number,
#  age = 999) can corrupt reports and statistics.
#
#  All validators return True (valid) or False (invalid).
#  The `re` module uses Regular Expressions (regex) — patterns
#  that describe what a valid string looks like.
# ================================================================

def is_valid_email(email: str) -> bool:
    """
    Checks if the email address has a proper format.
    Pattern: characters @ characters . domain
    Example valid: alice@gmail.com, student@college.edu
    """
    return bool(re.match(r"^[\w.\-+]+@[\w\-]+\.\w{2,}$", email))


def is_valid_phone(phone: str) -> bool:
    """
    Checks if the phone number is exactly 10 digits.
    Rejects spaces, dashes, and letters.
    Example valid: 9876543210
    """
    return bool(re.match(r"^\d{10}$", phone))


def is_valid_age(age_str: str) -> bool:
    """
    Checks that the age is a whole number between 5 and 100.
    Prevents nonsense like age = 0 or age = 500.
    """
    return age_str.isdigit() and 5 <= int(age_str) <= 100


def is_valid_roll(roll: str) -> bool:
    """
    Checks that the roll number contains only letters, digits,
    hyphens, or slashes — and is not longer than 20 characters.
    Example valid: CS101, 2024-A-01, ENG/001
    """
    return bool(re.match(r"^[A-Za-z0-9\-/]+$", roll)) and len(roll) <= 20


def input_validated(prompt, validator, error_msg, allow_blank=False):
    """
    A smart input() that keeps asking until the user provides
    a valid value — or leaves it blank (if allow_blank=True).

    Role: Replaces repetitive while-loop validation everywhere.
    Instead of writing the retry loop 10 times, we call this once.

    Parameters:
        prompt      → The question shown to the user
        validator   → Function that returns True/False
        error_msg   → Message shown when input is invalid
        allow_blank → If True, pressing ENTER skips the field
    """
    while True:
        value = input(prompt).strip()
        if allow_blank and value == "":
            return value                     # Empty is acceptable
        if validator(value):
            return value                     # Valid → return it
        print(f"  ⚠  {error_msg}")          # Invalid → show error, retry


# ================================================================
#  SECTION 5 — STUDENT RECORD BUILDER & MARKS / GPA LOGIC
# ================================================================
#  This section handles two things:
#   A) Grading logic — converting marks to letters and GPA
#   B) Record builder — collecting all student details via input
#
#  The student record is stored as a Python dictionary with
#  fields for personal info, marks, attendance, and metadata.
# ================================================================

# ── 5A. GRADING SCALE ──────────────────────────────────────────
#  Standard 10-band grading scale.
#  Used to auto-assign a letter grade from average marks.

GRADES = ["A+", "A", "B+", "B", "C+", "C", "D", "F", "N/A"]


def get_grade_from_marks(marks: float) -> str:
    """
    Converts a numeric average (0–100) into a letter grade.

    Role: Auto-assigns grade whenever marks are added or updated.
    This removes human error from grading.

    Grade boundaries:
        90–100 → A+    70–79 → B+    50–59 → C+    Below 35 → F
        80–89  → A     60–69 → B     40–49 → C
        35–39  → D
    """
    if marks >= 90:   return "A+"
    elif marks >= 80: return "A"
    elif marks >= 70: return "B+"
    elif marks >= 60: return "B"
    elif marks >= 50: return "C+"
    elif marks >= 40: return "C"
    elif marks >= 35: return "D"
    else:             return "F"


def collect_marks():
    """
    Prompts the user to enter marks for each of the 5 subjects.

    Role: Called during Add Student and Update Marks. Subjects can
    be skipped by pressing ENTER (useful if a student didn't
    appear for a particular exam).

    Returns a dict like: {"Mathematics": 87.5, "Science": 92.0}
    Only subjects with valid marks (0–100) are included.
    """
    subjects = {}
    print("  Enter marks for each subject (0–100). Press ENTER to skip.")
    subject_list = ["Mathematics", "Science", "English", "History", "Computer Science"]
    for sub in subject_list:
        val = input(f"    {sub:<22}: ").strip()
        if val == "":
            continue                                   # Skip this subject
        if val.replace(".", "", 1).isdigit():          # Allow decimals like 87.5
            m = float(val)
            if 0 <= m <= 100:
                subjects[sub] = round(m, 2)
            else:
                print("      ⚠  Marks must be between 0 and 100. Skipped.")
        else:
            print("      ⚠  Invalid input. Skipped.")
    return subjects


def calculate_gpa(subjects: dict) -> float:
    """
    Converts the subject average into a GPA on a 10-point scale.

    Role: GPA is commonly used in college transcripts alongside
    percentage. We keep both so the record is more useful.

    Formula: GPA = Average Marks / 10
    Example: Average 85% → GPA 8.5 / 10
    """
    if not subjects:
        return 0.0
    avg = sum(subjects.values()) / len(subjects)
    return round(avg / 10, 2)


def build_student_record(roll: str) -> dict:
    """
    Collects all information for a new student through a series
    of input prompts and returns a complete student dictionary.

    Role: The master builder for a student record. Called only
    during Add Student. Every field is either validated or
    optional (allow_blank=True) so the form never gets stuck.

    The dictionary it returns has these sections:
        Personal  → name, age, gender, email, phone, address
        Academic  → department, year, subjects, average, grade, gpa
        Tracking  → attendance dict, enrolled_on, last_updated
        Notes     → free-text notes field (empty by default)
    """
    print()
    # Personal information inputs
    name  = input("  Full Name         : ").strip().title()   # .title() = Capitalize Each Word
    age   = input_validated("  Age               : ", is_valid_age,
                            "Age must be a number between 5 and 100.")
    gender_map = {"1": "Male", "2": "Female", "3": "Other"}
    print("  Gender  (1-Male, 2-Female, 3-Other): ", end="")
    gender = gender_map.get(input().strip(), "Not Specified")

    # Academic information inputs
    dept  = input("  Department/Class  : ").strip().title()
    year  = input("  Year/Semester     : ").strip()

    # Contact information — optional fields (allow_blank=True)
    email = input_validated("  Email Address     : ", is_valid_email,
                            "Enter a valid email (e.g. name@domain.com).",
                            allow_blank=True)
    phone = input_validated("  Phone Number      : ", is_valid_phone,
                            "Enter a valid 10-digit phone number.",
                            allow_blank=True)
    addr      = input("  Address           : ").strip()
    guardian  = input("  Guardian Name     : ").strip().title()

    # Marks collection — calls the dedicated collect_marks() function
    print("\n  ── Subject Marks ──")
    subjects = collect_marks()

    # Auto-calculate academic summary from entered marks
    avg   = round(sum(subjects.values()) / len(subjects), 2) if subjects else 0.0
    grade = get_grade_from_marks(avg) if subjects else "N/A"
    gpa   = calculate_gpa(subjects)

    # Assemble the complete student dictionary
    record = {
        "roll_number"   : roll,
        "name"          : name,
        "age"           : int(age),
        "gender"        : gender,
        "department"    : dept,
        "year"          : year,
        "email"         : email,
        "phone"         : phone,
        "address"       : addr,
        "guardian"      : guardian,
        "subjects"      : subjects,          # Dict of subject → marks
        "average_marks" : avg,               # Computed average
        "grade"         : grade,             # Computed letter grade
        "gpa"           : gpa,               # Computed GPA / 10
        "attendance"    : {},                # Will be filled by attendance manager
        "enrolled_on"   : str(date.today()), # Automatically set to today
        "last_updated"  : str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "notes"         : ""                 # Blank — can be filled via Update
    }
    return record


# ================================================================
#  SECTION 6 — DISPLAY / PRINT FUNCTIONS
# ================================================================
#  These functions format and print student data to the terminal.
#  Having them separate keeps the logic functions clean — they
#  only manage data, not how it looks on screen.
# ================================================================

def display_student(s: dict, brief=False):
    """
    Prints a single student's information to the screen.

    Role: The main "view" function. Used in View All, Search
    results, and anywhere a student record needs to be shown.

    Parameters:
        s     → The student dictionary to display
        brief → If True, shows a short summary (3 lines).
                If False, shows ALL fields including subjects,
                GPA, attendance summary, and notes.

    The marks section renders a visual bar chart using █ symbols:
        Mathematics    87.5%  A   █████████████████
    """
    divider()
    print(f"  Roll No    : {s['roll_number']}")
    print(f"  Name       : {s['name']}")

    if brief:
        # Short view — just the essentials
        print(f"  Dept/Year  : {s['department']} | {s['year']}")
        print(f"  Average    : {s['average_marks']}%  Grade: {s['grade']}  GPA: {s['gpa']}")
        return

    # Full view — all personal and academic fields
    print(f"  Age/Gender : {s['age']} | {s['gender']}")
    print(f"  Dept/Year  : {s['department']} | {s['year']}")
    print(f"  Email      : {s.get('email', 'N/A')}")
    print(f"  Phone      : {s.get('phone', 'N/A')}")
    print(f"  Address    : {s.get('address', 'N/A')}")
    print(f"  Guardian   : {s.get('guardian', 'N/A')}")
    print(f"  Enrolled   : {s.get('enrolled_on', 'N/A')}")
    print(f"  Updated    : {s.get('last_updated', 'N/A')}")

    # Subject marks with visual bar chart
    if s.get("subjects"):
        print(f"\n  ── Subject Marks ──")
        for sub, mark in s["subjects"].items():
            g   = get_grade_from_marks(mark)
            bar = "█" * int(mark / 5)   # Each block = 5 marks (max 20 blocks = 100%)
            print(f"    {sub:<22} {mark:>6.1f}%  {g:>3}  {bar}")

    # Academic summary line
    print(f"\n  Average Marks : {s['average_marks']}%")
    print(f"  Grade         : {s['grade']}")
    print(f"  GPA (10-pt)   : {s['gpa']}")

    # Notes field (if any)
    if s.get("notes"):
        print(f"\n  Notes  : {s['notes']}")

    # Attendance summary — counts P/A/L entries and shows percentage
    att = s.get("attendance", {})
    if att:
        total   = len(att)
        present = sum(1 for v in att.values() if v == "P")
        pct     = round(present / total * 100, 1) if total else 0
        print(f"\n  Attendance : {present}/{total} days present ({pct}%)")


def display_all(db: dict, brief=True):
    """
    Iterates over all students in the database and prints each one.

    Role: Called by View All Students. Supports both brief
    (summary table) and full (detailed) modes.

    Parameters:
        db    → The full student database dictionary
        brief → Passed through to display_student()
    """
    if not db:
        print("  ⚠  No student records found.")
        return
    for s in db.values():
        display_student(s, brief=brief)
    divider()
    print(f"  Total records: {len(db)}")


# ================================================================
#  SECTION 7 — CORE FEATURES
# ================================================================
#  Each function below handles one complete feature of the system.
#  They all follow the same pattern:
#    1. Show a header
#    2. Get input from the user
#    3. Validate the input
#    4. Perform the action on the database (db dict)
#    5. Save changes to disk
#    6. Log the action
# ================================================================


# ── FEATURE 1: ADD STUDENT ─────────────────────────────────────
#  Collects a new student's full profile and saves it.
#  Rejects duplicate roll numbers to prevent data conflicts.

def add_student(db: dict):
    """
    Adds a brand new student record to the database.

    Steps:
        1. Ask for roll number and validate format
        2. Check it doesn't already exist (no duplicates)
        3. Call build_student_record() to collect all fields
        4. Store in db dict, save to file, log the action
    """
    header("➕  ADD NEW STUDENT")
    roll = input("  Enter Roll Number : ").strip().upper()

    # Validate roll number format
    if not is_valid_roll(roll):
        print("  ⚠  Invalid roll number. Use letters, numbers, - or / only.")
        return

    # Prevent duplicate entries
    if roll in db:
        print(f"  ⚠  Roll number '{roll}' already exists in database.")
        return

    # Collect all student details via the record builder
    record = build_student_record(roll)
    db[roll] = record          # Add to in-memory database
    save_data(db)              # Persist immediately to JSON file
    log_activity("ADD", f"Roll: {roll}  Name: {record['name']}")
    print(f"\n    Student '{record['name']}' added successfully!")


# ── FEATURE 2: VIEW ALL STUDENTS ───────────────────────────────
#  Shows every student in the database. User can choose
#  between a quick summary or full detailed view.

def view_all_students(db: dict):
    """
    Displays all student records in the database.

    Asks the user whether they want full details or a brief
    summary — useful when there are many students.
    """
    header("  ALL STUDENTS")
    if not db:
        print("  No records yet. Add a student first.")
        press_enter()
        return
    # Let user choose detail level
    detail = input("  Show full detail? (y/n, default n): ").strip().lower() == "y"
    display_all(db, brief=not detail)


# ── FEATURE 3: SEARCH STUDENT ──────────────────────────────────
#  Multi-field search — find students by 5 different criteria.
#  Partial name matching is supported (no need for exact spelling).

def search_student(db: dict):
    """
    Searches for students using one of 5 search methods:
        1. Roll Number (exact)
        2. Name (partial match — case insensitive)
        3. Department (partial match)
        4. Grade (exact, e.g. "A+")
        5. Email (partial match)

    Role: Makes it easy to find a student without remembering
    their exact roll number. Returns all matching records.
    """
    header("  SEARCH STUDENT")
    print("  Search by: 1-Roll  2-Name  3-Dept  4-Grade  5-Email")
    choice  = input("  Choose (1–5): ").strip()
    results = []   # Will hold matching student dicts

    if choice == "1":
        roll = input("  Roll Number : ").strip().upper()
        if roll in db:
            results = [db[roll]]

    elif choice == "2":
        # .lower() on both sides makes search case-insensitive
        name = input("  Name (partial OK) : ").strip().lower()
        results = [s for s in db.values() if name in s["name"].lower()]

    elif choice == "3":
        dept = input("  Department : ").strip().lower()
        results = [s for s in db.values() if dept in s["department"].lower()]

    elif choice == "4":
        grade = input("  Grade (e.g. A+) : ").strip().upper()
        results = [s for s in db.values() if s["grade"] == grade]

    elif choice == "5":
        email = input("  Email : ").strip().lower()
        results = [s for s in db.values() if email in s.get("email", "").lower()]

    else:
        print("  ⚠  Invalid choice.")
        return

    # Show results or "not found" message
    if not results:
        print("  ⚠  No matching students found.")
    else:
        print(f"\n  Found {len(results)} result(s):")
        for s in results:
            display_student(s, brief=False)

    log_activity("SEARCH", f"Method: {choice}  Results: {len(results)}")


# ── FEATURE 4: UPDATE STUDENT ──────────────────────────────────
#  Allows editing any specific field of an existing student.
#  Does NOT require re-entering all fields — only the chosen one.

def update_student(db: dict):
    """
    Updates a specific field of an existing student record.

    Role: Instead of deleting and re-adding a student to fix
    one field, this lets you update just that field.

    Supports updating: name, age, department, year, email,
    phone, address, guardian, notes, and subject marks.

    After any update, last_updated timestamp is refreshed
    and changes are saved to disk.
    """
    header("   UPDATE STUDENT RECORD")
    roll = input("  Roll Number to update : ").strip().upper()
    if roll not in db:
        print("  ⚠  Student not found.")
        return

    s = db[roll]
    print(f"  Editing record for: {s['name']}")
    divider()

    # Menu of editable fields (mapped by number to field name)
    fields = {
        "1": "name", "2": "age",     "3": "department",
        "4": "year", "5": "email",   "6": "phone",
        "7": "address", "8": "guardian", "9": "notes"
    }
    print("  Which field do you want to update?")
    for k, v in fields.items():
        print(f"    {k}. {v.replace('_', ' ').title()}")
    print("    10. Update Subject Marks")

    choice = input("  Choose: ").strip()

    if choice in fields:
        field = fields[choice]
        old   = s[field]
        new   = input(f"  New {field.title()} [{old}]: ").strip()
        if new:
            # Apply type conversion where needed
            if field == "name": new = new.title()
            if field == "age":
                if not is_valid_age(new):
                    print("  ⚠  Invalid age.")
                    return
                new = int(new)
            s[field] = new
            log_activity("UPDATE", f"Roll: {roll}  Field: {field}  {old} → {new}")

    elif choice == "10":
        # Update marks and recalculate grade/GPA automatically
        new_subjects = collect_marks()
        if new_subjects:
            s["subjects"].update(new_subjects)   # Merge new marks into existing
            avg           = round(sum(s["subjects"].values()) / len(s["subjects"]), 2)
            s["average_marks"] = avg
            s["grade"]         = get_grade_from_marks(avg)
            s["gpa"]           = calculate_gpa(s["subjects"])
        log_activity("UPDATE", f"Roll: {roll}  Marks updated, Avg: {s['average_marks']}")

    else:
        print("  ⚠  Invalid choice.")
        return

    # Refresh the last_updated timestamp and save
    s["last_updated"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    save_data(db)
    print("    Record updated and saved successfully.")


# ── FEATURE 5: DELETE STUDENT ──────────────────────────────────
#  Permanently removes a student record from the database.
#  Requires the user to type "yes" to confirm before deleting.

def delete_student(db: dict):
    """
    Deletes a student record permanently from the database.

    Role: Removes a student who has left or was added by mistake.
    A confirmation step (type "yes") prevents accidental deletion.
    The action is logged so there is a record of who was removed.
    """
    header("   DELETE STUDENT")
    roll = input("  Roll Number to delete : ").strip().upper()
    if roll not in db:
        print("  ⚠  Student not found.")
        return

    s = db[roll]
    print(f"\n  Found: {s['name']}  |  {s['department']}  |  {s['average_marks']}%")
    confirm = input("\n  Type 'yes' to confirm permanent deletion: ").strip().lower()

    if confirm == "yes":
        del db[roll]            # Remove from in-memory dict
        save_data(db)           # Persist the deletion to disk
        log_activity("DELETE", f"Roll: {roll}  Name: {s['name']}")
        print("    Student record deleted permanently.")
    else:
        print("  ↩  Deletion cancelled. Record is safe.")


# ── FEATURE 6: ATTENDANCE MANAGER ─────────────────────────────
#  Marks daily attendance for all students.
#  Attendance is stored inside each student record as a dict:
#  { "2026-05-30": "P", "2026-05-31": "A", ... }

def manage_attendance(db: dict):
    """
    Marks attendance for all students for today's date.

    Role: Daily attendance tracking. The user enters P, A, or L
    for each student. If a date already has a mark, it shows
    the existing value so the user can update or skip.

    Status codes:
        P = Present
        A = Absent
        L = Leave / Medical
    """
    header("  MARK ATTENDANCE")
    if not db:
        print("  No students found. Add students first.")
        return

    today   = str(date.today())    # e.g. "2026-05-30"
    print(f"  Date: {today}")
    print(f"  Status: P = Present  |  A = Absent  |  L = Leave\n")

    updated = 0
    for roll, s in db.items():
        already = s["attendance"].get(today, "")
        prompt  = f"  {s['name']:<25} Roll: {roll:<10}"
        if already:
            prompt += f"  (already marked: {already})"
        val = input(prompt + "  → ").strip().upper()
        if val in ("P", "A", "L"):
            s["attendance"][today] = val
            updated += 1
        # If user presses ENTER without a valid code, skip that student

    save_data(db)
    log_activity("ATTENDANCE", f"Date: {today}  Students marked: {updated}")
    print(f"\n    Attendance saved for {updated} student(s).")


def view_attendance(db: dict):
    """
    Shows a summary of attendance for one student or all students.

    Role: Helps identify students with low attendance (below 75%)
    who may be at risk or need a warning.

    Shows: Total days, Present/Absent/Leave counts, percentage,
    and last 5 attendance entries.
    """
    header("  ATTENDANCE REPORT")
    roll = input("  Enter Roll Number (or press ENTER for all): ").strip().upper()

    # If roll given and found, show just that student; else show all
    students = [db[roll]] if roll and roll in db else list(db.values())

    for s in students:
        att = s.get("attendance", {})
        if not att:
            print(f"\n  {s['name']}: No attendance data recorded yet.")
            continue

        total   = len(att)
        present = sum(1 for v in att.values() if v == "P")
        absent  = sum(1 for v in att.values() if v == "A")
        leave   = sum(1 for v in att.values() if v == "L")
        pct     = round(present / total * 100, 1)

        # Warn if attendance is below the common 75% threshold
        status  = "✅ Good Standing" if pct >= 75 else "⚠  Below 75% — At Risk"

        print(f"\n  ── {s['name']}  ({s['roll_number']}) ──")
        print(f"  Total: {total}  |  Present: {present}  |  Absent: {absent}  |  Leave: {leave}")
        print(f"  Attendance %  : {pct}%  {status}")
        # Show most recent 5 entries
        recent = dict(list(att.items())[-5:])
        print(f"  Recent (last 5): {recent}")


# ── FEATURE 7: STATISTICS & REPORTS ───────────────────────────
#  Analyses the entire database and shows class-level insights
#  including averages, grade distribution, top students, and
#  students who have failed or are below threshold.

def show_statistics(db: dict):
    """
    Generates a full statistical report for the entire class.

    Role: Gives teachers and administrators a quick overview
    of class performance without looking at individual records.

    Calculates:
        - Total students, class average, highest/lowest score
        - Grade distribution with visual bar chart (█ symbols)
        - Student count per department
        - Top 3 performing students
        - Students with average below 35% (failed)
    """
    header("📈  CLASS STATISTICS & REPORT")
    if not db:
        print("  No data available. Add students first.")
        press_enter()
        return

    all_avg   = [s["average_marks"] for s in db.values()]
    grade_cnt = {}    # Count of students per grade
    dept_cnt  = {}    # Count of students per department

    for s in db.values():
        # Build grade frequency table
        grade_cnt[s["grade"]] = grade_cnt.get(s["grade"], 0) + 1
        # Build department frequency table
        dept_cnt[s["department"]] = dept_cnt.get(s["department"], 0) + 1

    class_avg = round(sum(all_avg) / len(all_avg), 2)

    # ── Overall Summary ──
    print(f"  Total Students   : {len(db)}")
    print(f"  Class Average    : {class_avg}%")
    print(f"  Highest Average  : {max(all_avg)}%")
    print(f"  Lowest Average   : {min(all_avg)}%")

    # ── Grade Distribution Chart ──
    divider()
    print("  Grade Distribution  (each █ = 1 student)")
    for g in ["A+", "A", "B+", "B", "C+", "C", "D", "F"]:
        c   = grade_cnt.get(g, 0)
        bar = "█" * c
        print(f"    {g:>3} : {c:>3}  {bar}")

    # ── Department Breakdown ──
    divider()
    print("  Students per Department:")
    for dept, cnt in sorted(dept_cnt.items(), key=lambda x: -x[1]):
        print(f"    {dept:<28}: {cnt}")

    # ── Top 3 Students ──
    divider()
    top3 = sorted(db.values(), key=lambda s: s["average_marks"], reverse=True)[:3]
    print("  🏆 Top 3 Students:")
    medals = ["🥇", "🥈", "🥉"]
    for i, s in enumerate(top3):
        print(f"    {medals[i]}  {s['name']:<25} {s['average_marks']}%  Grade: {s['grade']}")

    # ── Failed Students (below 35%) ──
    failed = [s for s in db.values() if s["average_marks"] < 35]
    if failed:
        divider()
        print(f"  ⚠  Students with Average < 35% (needs attention): {len(failed)}")
        for s in failed:
            print(f"     {s['name']:<25} ({s['roll_number']})  {s['average_marks']}%")


# ── FEATURE 8: SORT & RANK ─────────────────────────────────────
#  Sorts and displays all students ranked by a chosen field.
#  Useful for generating merit lists or alphabetical directories.

def sort_and_rank(db: dict):
    """
    Displays all students ranked by a selected attribute.

    Role: Generates merit lists (by marks/GPA), alphabetical
    directories (by name), or department-wise listings.

    Sort options:
        1. Name (A→Z)
        2. Average Marks (High→Low)
        3. GPA (High→Low)
        4. Department (A→Z)
        5. Age (Low→High)
    """
    header("  SORT & RANK STUDENTS")
    print("  Sort by: 1-Name  2-Average Marks  3-GPA  4-Department  5-Age")
    choice = input("  Choose (1–5): ").strip()

    # Map choice number to the lambda that extracts the sort key
    key_map = {
        "1": lambda s: s["name"],
        "2": lambda s: s["average_marks"],
        "3": lambda s: s["gpa"],
        "4": lambda s: s["department"],
        "5": lambda s: s["age"]
    }
    if choice not in key_map:
        print("  ⚠  Invalid choice.")
        return

    # Marks and GPA should be descending (highest first)
    reverse = choice in {"2", "3"}
    sorted_students = sorted(db.values(), key=key_map[choice], reverse=reverse)

    print()
    for rank, s in enumerate(sorted_students, 1):
        print(f"  {rank:>3}. {s['name']:<25} "
              f"Avg: {s['average_marks']:>6.1f}%  "
              f"Grade: {s['grade']}  "
              f"Dept: {s['department']}")


# ── FEATURE 9: EXPORT FUNCTIONS ────────────────────────────────
#  Export the database in different file formats for use outside
#  this program (Excel, reports, printing, etc.)

def export_to_csv(db: dict):
    """
    Exports all student records to a CSV file.

    Role: CSV files can be opened in Microsoft Excel, Google
    Sheets, or any spreadsheet program. Useful for sharing
    data with other staff or doing further analysis.

    File is saved as: students_export_YYYY-MM-DD.csv
    """
    header(" EXPORT TO CSV")
    if not db:
        print("  No data to export.")
        return

    filename = f"students_export_{date.today()}.csv"

    # Only include flat fields (not nested dicts like subjects/attendance)
    keys = ["roll_number", "name", "age", "gender", "department",
            "year", "email", "phone", "average_marks", "grade", "gpa",
            "enrolled_on"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()       # Write the column names row
        writer.writerows(db.values())   # Write one row per student

    log_activity("EXPORT CSV", f"File: {filename}  Records: {len(db)}")
    print(f"    Exported {len(db)} records → {filename}")


def export_to_txt(db: dict):
    """
    Exports a readable text report of all students.

    Role: Generates a printable report that looks clean in
    any text editor — useful for physical notice boards or
    sharing via email without requiring Excel.

    File is saved as: students_report_YYYY-MM-DD.txt
    """
    filename = f"students_report_{date.today()}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"STUDENT REPORT  |  Generated: {datetime.now()}\n")
        f.write("=" * 60 + "\n")
        for s in db.values():
            f.write(f"\nRoll : {s['roll_number']}   Name: {s['name']}\n")
            f.write(f"  Dept     : {s['department']}   Year: {s['year']}\n")
            f.write(f"  Average  : {s['average_marks']}%   Grade: {s['grade']}   GPA: {s['gpa']}\n")
            f.write("-" * 60 + "\n")
    log_activity("EXPORT TXT", f"File: {filename}  Records: {len(db)}")
    print(f"  ✅  Text report saved → {filename}")


# ── FEATURE 10: VIEW ACTIVITY LOG ─────────────────────────────

def view_log():
    """
    Displays the last 30 entries from the activity log file.

    Role: Full audit trail — shows every action taken in the
    program with the exact timestamp. Useful for tracking who
    added, deleted, or modified a record and when.

    Every function in this program calls log_activity() so
    nothing goes unrecorded.
    """
    header(" ACTIVITY LOG  (Last 30 Actions)")
    if not os.path.exists(LOG_FILE):
        print("  No activity recorded yet.")
        return
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[-30:]:       # Show only the most recent 30 lines
        print(" ", line.rstrip())
    print(f"\n  (Showing last {min(30, len(lines))} of {len(lines)} total log entries)")


# ================================================================
#  SECTION 8 — SUB-MENUS
# ================================================================
#  Some features have multiple options grouped under one menu.
#  These sub-menus keep the main menu clean and uncluttered.
# ================================================================

def attendance_menu(db: dict):
    """
    Sub-menu for all attendance-related actions.

    Role: Groups 'Mark Attendance' and 'View Report' under
    one menu so the main menu doesn't get too long.
    Loops until the user chooses to go back.
    """
    while True:
        header("  ATTENDANCE MENU")
        print("  1. Mark Today's Attendance")
        print("  2. View Attendance Report")
        print("  3. Back to Main Menu")
        ch = input("\n  ► Choose: ").strip()
        if ch == "1":
            manage_attendance(db)
            press_enter()
        elif ch == "2":
            view_attendance(db)
            press_enter()
        elif ch == "3":
            break
        else:
            print("  ⚠  Invalid choice. Please try again.")


def export_menu(db: dict):
    """
    Sub-menu for all data export and backup actions.

    Role: Groups CSV export, text report, backup, and restore
    under one menu. The restore option updates the in-memory
    db dict using .clear() and .update() so changes are
    reflected immediately without restarting the program.
    """
    while True:
        header("  EXPORT & BACKUP MENU")
        print("  1. Export to CSV (Excel-compatible)")
        print("  2. Export to Text Report")
        print("  3. Backup Data (JSON snapshot)")
        print("  4. Restore from Last Backup")
        print("  5. Back to Main Menu")
        ch = input("\n  ► Choose: ").strip()

        if ch == "1":
            export_to_csv(db)
            press_enter()
        elif ch == "2":
            export_to_txt(db)
            press_enter()
        elif ch == "3":
            backup_data(db)
            press_enter()
        elif ch == "4":
            restored = restore_from_backup()
            if restored is not None:
                db.clear()          # Remove all current entries
                db.update(restored) # Replace with backup entries
                save_data(db)       # Write restored data to main file
            press_enter()
        elif ch == "5":
            break


# ================================================================
#  SECTION 9 — MAIN MENU (PROGRAM ENTRY POINT)
# ================================================================
#  The main menu is the heart of the program. It:
#    1. Loads the database from disk when the program starts
#    2. Shows the full feature list
#    3. Routes user input to the correct function
#    4. Loops forever until the user chooses Exit (0)
#
#  The `db` dictionary is passed as a parameter to every
#  function — this single dictionary IS the in-memory database.
#  Keeping it in one place means all functions always work on
#  the same current copy of the data.
# ================================================================

def main_menu():
    """
    Entry point for the entire program.

    Role: Loads data, displays the main navigation menu, and
    dispatches to the correct feature based on user input.
    Loops until the user exits. Saves data on exit.
    """
    db = load_data()    # Load existing records from JSON file into memory

    while True:
        header("🎓  MAIN MENU")
        print(f"  Students in database: {len(db)}")
        divider()
        print("  1.    Add New Student")
        print("  2.    View All Students")
        print("  3.    Search Student")
        print("  4.    Update Student Record")
        print("  5.    Delete Student")
        print("  6.    Attendance Manager")
        print("  7.    Class Statistics & Reports")
        print("  8.    Sort & Rank Students")
        print("  9.    Export / Backup Data")
        print("  10.   View Activity Log")
        print("  0.    Exit Program")
        divider()

        choice = input("  ► Choose an option: ").strip()
        print()

        # Route to the correct function based on user's choice
        if   choice == "1":   add_student(db);         press_enter()
        elif choice == "2":   view_all_students(db);    press_enter()
        elif choice == "3":   search_student(db);       press_enter()
        elif choice == "4":   update_student(db);       press_enter()
        elif choice == "5":   delete_student(db);       press_enter()
        elif choice == "6":   attendance_menu(db)       # Sub-menu (no press_enter needed)
        elif choice == "7":   show_statistics(db);      press_enter()
        elif choice == "8":   sort_and_rank(db);        press_enter()
        elif choice == "9":   export_menu(db)           # Sub-menu
        elif choice == "10":  view_log();               press_enter()
        elif choice == "0":
            print("  👋  Goodbye! All data has been saved. See you next time!\n")
            save_data(db)   # Final save before exiting
            break
        else:
            print("  ⚠  Invalid option. Please choose a number from the menu.")
            press_enter()


# ================================================================
#  PROGRAM START
# ================================================================
#  Python runs this block only when you execute the file directly.
#  (Not when it's imported as a module into another script.)
#
#  if __name__ == "__main__" is the standard Python way to define
#  the "run this as a script" entry point.
# ================================================================

if __name__ == "__main__":
    log_activity("PROGRAM START", "Student Management System launched")
    main_menu()
    log_activity("PROGRAM EXIT", "Student Management System closed")

# ================================================================
#  END OF FILE
#  Total Sections  : 9
#  Total Features  : 10
#  External Libs   : None (100% built-in Python)
#  Run command     : python student_management_system.py
# ================================================================
