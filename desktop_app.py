import tkinter as tk
from tkinter import ttk, messagebox
from water_jug import solve

class WaterJugApp:
    def __init__(self, root):
        self.root = root
        root.title("Intelligent Water-Jug Solver")
        root.geometry("760x650")
        root.minsize(650, 580)
        self.result = None
        self.step = 0

        main = ttk.Frame(root, padding=18)
        main.pack(fill="both", expand=True)
        ttk.Label(main, text="Intelligent Water-Jug Problem Solver",
                  font=("Arial", 17, "bold")).pack(pady=(0, 14))

        form = ttk.LabelFrame(main, text="Problem setup", padding=12)
        form.pack(fill="x")
        self.a_var = tk.StringVar(value="4")
        self.b_var = tk.StringVar(value="3")
        self.target_var = tk.StringVar(value="2")
        self.alg_var = tk.StringVar(value="BFS")
        for col, label, var in [
            (0, "Jug A capacity", self.a_var),
            (1, "Jug B capacity", self.b_var),
            (2, "Target quantity", self.target_var)
        ]:
            ttk.Label(form, text=label).grid(row=0, column=col, padx=6, sticky="w")
            ttk.Entry(form, textvariable=var, width=13).grid(row=1, column=col, padx=6, pady=5)
        ttk.Label(form, text="Algorithm").grid(row=0, column=3, padx=6, sticky="w")
        ttk.Combobox(form, textvariable=self.alg_var,
                     values=["BFS", "DFS", "UCS", "GREEDY", "ASTAR"],
                     state="readonly", width=12).grid(row=1, column=3, padx=6)
        ttk.Button(form, text="Solve", command=self.solve_problem).grid(
            row=2, column=0, columnspan=4, sticky="ew", pady=(10, 0))

        self.canvas = tk.Canvas(main, width=560, height=270, bg="white",
                                highlightthickness=1, highlightbackground="#cccccc")
        self.canvas.pack(fill="x", pady=16)
        self.status = ttk.Label(main, text="Enter values and click Solve.")
        self.status.pack(pady=4)
        controls = ttk.Frame(main)
        controls.pack()
        self.prev_btn = ttk.Button(controls, text="← Previous", command=self.previous, state="disabled")
        self.prev_btn.pack(side="left", padx=6)
        self.next_btn = ttk.Button(controls, text="Next →", command=self.next, state="disabled")
        self.next_btn.pack(side="left", padx=6)
        self.path = tk.Text(main, height=9, wrap="word")
        self.path.pack(fill="both", expand=True, pady=(12, 0))
        self.draw_jugs(4, 3, 0, 0)

    def solve_problem(self):
        try:
            a = int(self.a_var.get())
            b = int(self.b_var.get())
            target = int(self.target_var.get())
            self.result = solve(a, b, target, self.alg_var.get())
            self.step = 0
            self.path.delete("1.0", "end")
            if not self.result["found"]:
                messagebox.showinfo("No solution", self.result.get("message", "No solution found."))
                self.status.config(text="No solution found.")
                self.prev_btn.config(state="disabled")
                self.next_btn.config(state="disabled")
                return
            self.path.insert("end", "Complete solution path:\n")
            for i, state in enumerate(self.result["states"]):
                action = "Start" if i == 0 else self.result["actions"][i-1]
                self.path.insert("end", f"{i}. {action} -> {state}\n")
            self.status.config(text=f'{self.alg_var.get()}: {len(self.result["actions"])} operations | '
                                    f'{self.result["expanded"]} expanded states | '
                                    f'{self.result["elapsed_ms"]:.3f} ms')
            self.update_view()
        except ValueError as exc:
            messagebox.showerror("Input error", str(exc))

    def draw_jugs(self, cap_a, cap_b, amount_a, amount_b):
        self.canvas.delete("all")
        max_cap = max(cap_a, cap_b)
        scale = 190 / max_cap
        base_y = 225
        for x, cap, amount, name in [(145, cap_a, amount_a, "Jug A"),
                                     (365, cap_b, amount_b, "Jug B")]:
            height = cap * scale
            water_height = amount * scale
            self.canvas.create_rectangle(x, base_y-height, x+100, base_y,
                                         outline="#333333", width=3)
            if amount:
                self.canvas.create_rectangle(x+3, base_y-water_height, x+97, base_y-3,
                                             fill="#78bde8", outline="")
            self.canvas.create_text(x+50, base_y-height-18,
                                    text=f"{name}: {amount}/{cap} L", font=("Arial", 11, "bold"))
        self.canvas.create_text(330, 250, text="Water level visualization", fill="#555555")

    def update_view(self):
        cap_a, cap_b = int(self.a_var.get()), int(self.b_var.get())
        a, b = self.result["states"][self.step]
        self.draw_jugs(cap_a, cap_b, a, b)
        if self.step == 0:
            operation = "Initial state: both jugs are empty."
        else:
            operation = self.result["actions"][self.step-1]
        self.status.config(text=f"Step {self.step}/{len(self.result['states'])-1}: "
                                f"{operation} | Current state {a, b}")
        self.prev_btn.config(state="normal" if self.step > 0 else "disabled")
        self.next_btn.config(state="normal" if self.step < len(self.result["states"])-1 else "disabled")

    def previous(self):
        if self.result and self.step > 0:
            self.step -= 1
            self.update_view()

    def next(self):
        if self.result and self.step < len(self.result["states"])-1:
            self.step += 1
            self.update_view()

if __name__ == "__main__":
    root = tk.Tk()
    WaterJugApp(root)
    root.mainloop()
