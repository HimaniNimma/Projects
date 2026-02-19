"""Design and develop a Python-based Student Performance Analyzer application that uses 
Object-Oriented Programming concepts to manage student records, performs statistical
analysis using NumPy, visualizes performance using Matplotlib, 
and provides a user-friendlyinterface using Tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BG_COLOR = "#F4F6F9"
CARD_COLOR = "#FFFFFF"
PRIMARY = "#2563EB"
SUCCESS = "#16A34A"
ACCENT = "#1E293B"
FONT_TITLE = ("Segoe UI Semibold", 18)
FONT_MAIN = ("Segoe UI", 11)
FONT_TABLE = ("Segoe UI", 10)

class Student:
    def __init__(self, roll, name, marks):
        self.roll, self.name, self.marks = roll, name, marks
    def average(self): 
        return np.mean(list(self.marks.values()))
        
class Analyzer:
    def __init__(self): 
        self.students = []
    def add(self, student):
        for i, s in enumerate(self.students):
            if s.roll == student.roll:  
                self.students[i] = student
                return
        self.students.append(student)
        
    def stats(self):
        if not self.students:
            messagebox.showerror("Error", "No student records!")
            return
        popup = Toplevel(parent)
        popup.title("Class Performance Dashboard")
        popup.geometry("520x500")
        popup.configure(bg="#111827")
        avgs = np.array([s.average() for s in self.students])
        names = [s.name for s in self.students]

        class_avg = np.mean(avgs)
        median = np.median(avgs)
        std_dev = np.std(avgs)
        highest = np.max(avgs)
        lowest = np.min(avgs)

        top_student = names[np.argmax(avgs)]
        low_student = names[np.argmin(avgs)]

        grades = {
            "A (>=85)": np.sum(avgs >= 85),
            "B (70-84)": np.sum((avgs >= 70) & (avgs < 85)),
            "C (50-69)": np.sum((avgs >= 50) & (avgs < 70)),
            "Fail (<50)": np.sum(avgs < 50),
        }
        tk.Label(popup, text="📊 Class Performance Overview",
                 font=("Segoe UI Semibold", 17),
                 bg="#111827", fg="white").pack(pady=20)

        info = f"""
Total Students: {len(self.students)}

Class Average: {class_avg:.2f}
Median Score: {median:.2f}
Standard Deviation: {std_dev:.2f}

Top Performer: {top_student} ({highest:.2f})
Lowest Performer: {low_student} ({lowest:.2f})
"""
        tk.Label(popup, text=info,
                 font=("Segoe UI", 12),
                 bg="#111827", fg="#D1D5DB",
                 justify="left").pack(pady=10)

        tk.Label(popup, text="Grade Distribution",
                 font=("Segoe UI Semibold", 14),
                 bg="#111827", fg="#60A5FA").pack(pady=10)

        for grade, count in grades.items():
            tk.Label(popup, text=f"{grade}: {count}",
                     font=("Segoe UI", 11),
                     bg="#111827", fg="white").pack()
                  
    def visualize(self, parent):
        if not self.students:
            messagebox.showerror("Error", "No student records!")
            return

        popup = Toplevel(parent)
        popup.title("Performance Analytics")
        popup.configure(bg="#0F172A")

        names = [s.name for s in self.students]
        avgs = np.array([s.average() for s in self.students])
        top_index = np.argmax(avgs)

        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)

        colors = []
        for i in range(len(avgs)):
            if i == top_index:
                colors.append("#22C55E")  # highlight topper
            else:
                colors.append("#3B82F6")

        bars = ax.bar(names, avgs,
                      color=colors,
                      edgecolor="white",
                      linewidth=1.2)

        ax.set_title("Student Performance Analysis",
                     fontsize=16, weight="bold", pad=15)

        ax.set_ylabel("Average Marks", fontsize=12)
        ax.set_ylim(0, 100)

        ax.grid(True, linestyle="--", alpha=0.3)
        plt.xticks(rotation=30, ha="right")

        for bar, val in zip(bars, avgs):
            ax.text(bar.get_x() + bar.get_width()/2,
                    val + 2,
                    f"{val:.1f}",
                    ha="center",
                    fontsize=10,
                    weight="bold")

        fig.patch.set_facecolor("#0F172A")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

class App:
    def __init__(self, root):
        self.analyzer = Analyzer()
        root.title("Student Performance Analyzer")
        root.geometry("600x400")
        frm = tk.LabelFrame(root, text="Add Student", padx=10, pady=10)
        frm.pack(fill="x", padx=10, pady=5)
        tk.Label(frm, text="Roll No").grid(row=0, column=0)
        self.roll = tk.Entry(frm, width=10); self.roll.grid(row=0, column=1, padx=5)
        tk.Label(frm, text="Name").grid(row=0, column=2)
        self.name = tk.Entry(frm, width=15); self.name.grid(row=0, column=3, padx=5)
        tk.Label(frm, text="Marks (comma-separated)").grid(row=0, column=4)
        self.marks = tk.Entry(frm, width=20); self.marks.grid(row=0, column=5, padx=5)
        tk.Button(frm, text="Add", command=self.add).grid(row=0, column=6, padx=5)
        self.table = ttk.Treeview(root, columns=("Roll", "Name", "Average"), show="headings")
        self.table.heading("Roll", text="Roll No")
        self.table.heading("Name", text="Name")
        self.table.heading("Average", text="Average Marks")
        self.table.pack(fill="both", expand=True, padx=10, pady=5)
        btns = tk.Frame(root); btns.pack(pady=5)
        tk.Button(btns, text="Show Stats", command=self.analyzer.stats, width=15).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Visualize", command=lambda: self.analyzer.visualize(root), width=15).grid(row=0, column=1, padx=5)
    def add(self):
        roll, name, marks_str = self.roll.get().strip(), self.name.get().strip(), self.marks.get().strip()
        if not roll or not name or not marks_str:
            messagebox.showerror("Error", "Please fill all fields!")
            return
        try:
            marks = list(map(int, marks_str.split(",")))
            if any(m < 0 or m > 100 for m in marks): raise ValueError
            subjects = {f"Sub{i+1}": m for i, m in enumerate(marks)}
        except:
            messagebox.showerror("Error", "Marks must be numbers (0-100) separated by commas.")
            return
        student = Student(roll, name, subjects)
        self.analyzer.add(student)
        self.table.delete(*self.table.get_children())
        for s in self.analyzer.students:
            self.table.insert("", "end", values=(s.roll, s.name, f"{s.average():.2f}"))
        self.roll.delete(0, tk.END); self.name.delete(0, tk.END); self.marks.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()



