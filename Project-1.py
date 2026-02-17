"""Design and develop a Python-based Student Performance Analyzer application that uses Object-Oriented Programming concepts to manage student records, performs statistical
analysis using NumPy, visualizes performance using Matplotlib, and provides a user-friendlyinterface using Tkinter."""

#Python Code
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        avgs = [s.average() for s in self.students]
        msg = (f"Class Average: {np.mean(avgs):.2f}\n"
               f"Highest Average: {np.max(avgs):.2f}\n"
               f"Lowest Average: {np.min(avgs):.2f}")
        messagebox.showinfo("📊 Statistics", msg)
    def visualize(self, parent):
        if not self.students:
            messagebox.showerror("Error", "No student records!")
            return
        popup = Toplevel(parent); 
        popup.title("Performance Chart")
        names, avgs = [s.name for s in self.students], [s.average() for s in self.students]
        fig_width = max(5, len(names) * 0.6)
        fig, ax = plt.subplots(figsize=(fig_width, 4), dpi=100)
        bars = ax.bar(names, avgs, color="#4DA6FF", width=0.5, edgecolor="black")
        ax.set_title("Average Marks per Student", fontsize=12)
        ax.set_ylabel("Marks"); ax.set_ylim(0, 100)
        plt.xticks(rotation=30, ha="right")
        for bar, val in zip(bars, avgs):
            ax.text(bar.get_x() + bar.get_width()/2, val + 1, f"{val:.1f}",
                    ha="center", fontsize=9, color="black")
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw(); 
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
