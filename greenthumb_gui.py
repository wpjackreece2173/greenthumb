import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime, timedelta

class Plant:
    def __init__(self, name, water_interval, fertilize_interval):
        self.name = name
        self.water_interval = int(water_interval)
        self.fertilize_interval = int(fertilize_interval)
        self.last_watered = datetime.now()
        self.last_fertilized = datetime.now()

    def status(self):
        water_due = self.last_watered + timedelta(days=self.water_interval)
        fert_due = self.last_fertilized + timedelta(days=self.fertilize_interval)
        return f"{self.name}: Water by {water_due.date()}, Fertilize by {fert_due.date()}"

    def needs_care_today(self):
        today = datetime.now().date()
        return (self.last_watered + timedelta(days=self.water_interval)).date() <= today or \
               (self.last_fertilized + timedelta(days=self.fertilize_interval)).date() <= today

class PlantCareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GreenThumb - Plant Care Assistant")
        self.plants = []

        # Listbox
        self.listbox = tk.Listbox(root, width=60, height=10)
        self.listbox.pack(pady=10)

        # Buttons
        tk.Button(root, text="Add New Plant", command=self.add_plant).pack(pady=2)
        tk.Button(root, text="Update Care", command=self.update_care).pack(pady=2)
        tk.Button(root, text="View Today’s Reminders", command=self.view_reminders).pack(pady=2)
        tk.Button(root, text="Save and Exit", command=self.save_and_exit).pack(pady=2)

    def add_plant(self):
        name = simpledialog.askstring("New Plant", "Enter plant name:")
        if not name:
            return
        water = simpledialog.askinteger("Water Interval", f"Water every how many days?")
        fert = simpledialog.askinteger("Fertilizer Interval", f"Fertilize every how many days?")
        if water is not None and fert is not None:
            new_plant = Plant(name, water, fert)
            self.plants.append(new_plant)
            self.refresh_list()

    def update_care(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Update Care", "Select a plant to update.")
            return
        index = selection[0]
        plant = self.plants[index]
        action = simpledialog.askstring("Care Update", "Type 'water', 'fertilize', or 'both':")
        if action:
            if 'water' in action:
                plant.last_watered = datetime.now()
            if 'fertilize' in action:
                plant.last_fertilized = datetime.now()
            self.refresh_list()

    def view_reminders(self):
        reminders = [p.status() for p in self.plants if p.needs_care_today()]
        if reminders:
            messagebox.showinfo("Today's Care Reminders", "\n".join(reminders))
        else:
            messagebox.showinfo("All Good!", "No care needed today.")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for plant in self.plants:
            self.listbox.insert(tk.END, plant.status())

    def save_and_exit(self):
        # You can add actual file save functionality here if needed.
        self.root.quit()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PlantCareApp(root)
    root.mainloop()
