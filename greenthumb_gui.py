"""
green_thumb_gui.py
==================
GreenThumb – Smart Plant Care Assistant (Tkinter GUI)

This file defines two classes:

1. Plant – a data model for each plant.
2. PlantCareApp – the main Tkinter application window.

The program lets users add plants, track watering / fertilizing
schedules, search, delete, and receive reminders. All data is
persistently stored in a JSON file (`plants.json`).

Author(s): Wynstona Jackreece, Ella Smith
License : MIT
"""

# ---------- Standard Library Imports ----------
import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog

# ------------ Module‑Level Constants ----------
DATA_FILE = "plants.json"          # default save file
DATE_FMT   = "%Y-%m-%d"            # ISO style for persistence


# ======================================================================
#                              Plant Model
# ======================================================================
class Plant:
    """
    A single plant with watering / fertilizing schedules.

    Attributes
    ----------
    name : str
        Common name supplied by the user.
    water_interval : int
        Days between watering.
    fertilize_interval : int
        Days between fertilizing.
    last_watered : datetime
    last_fertilized : datetime
    """

    def __init__(self,
                 name: str,
                 water_interval: int,
                 fertilize_interval: int,
                 last_watered: str | None = None,
                 last_fertilized: str | None = None):
        self.name               = name
        self.water_interval     = int(water_interval)
        self.fertilize_interval = int(fertilize_interval)

        # Parse saved dates or use "now" for new plants
        self.last_watered = (
            datetime.strptime(last_watered, DATE_FMT)
            if last_watered else datetime.now()
        )
        self.last_fertilized = (
            datetime.strptime(last_fertilized, DATE_FMT)
            if last_fertilized else datetime.now()
        )

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------
    def next_water_due(self) -> datetime:
        """Return next watering date."""
        return self.last_watered + timedelta(days=self.water_interval)

    def next_fert_due(self) -> datetime:
        """Return next fertilizing date."""
        return self.last_fertilized + timedelta(days=self.fertilize_interval)

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------
    def status(self) -> str:
        """Human‑readable status string for listbox."""
        return (f"{self.name}: "
                f"Water by {self.next_water_due().date()}, "
                f"Fertilize by {self.next_fert_due().date()}")

    def needs_care_today(self) -> bool:
        """True if either care action is due today or overdue."""
        today = datetime.now().date()
        return (self.next_water_due().date() <= today or
                self.next_fert_due().date() <= today)

    def to_dict(self) -> dict:
        """Serialize for JSON persistence."""
        return {
            "name": self.name,
            "water_interval": self.water_interval,
            "fertilize_interval": self.fertilize_interval,
            "last_watered": self.last_watered.strftime(DATE_FMT),
            "last_fertilized": self.last_fertilized.strftime(DATE_FMT),
        }


# ======================================================================
#                              Main  GUI
# ======================================================================
class PlantCareApp:
    """Tkinter application for managing plants."""

    # ------------------------------------------------------------------
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("GreenThumb – Plant Care Assistant")
        self.root.geometry("700x460")

        # Internal collections
        self.plants: list[Plant]         = []
        self.filtered_plants: list[Plant] = []

        # Build UI widgets & load data
        self._build_menubar()
        self._build_widgets()
        self.load_data()

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------
    def _build_menubar(self) -> None:
        """Create a menubar with File and Help menus."""
        menubar      = tk.Menu(self.root)
        file_menu    = tk.Menu(menubar, tearoff=False)
        help_menu    = tk.Menu(menubar, tearoff=False)

        # File menu
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_widgets(self) -> None:
        """Create search bar, listbox, buttons, and status bar."""
        # Search frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=6, fill=tk.X)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(6, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_filter)
        ttk.Entry(search_frame,
                  textvariable=self.search_var,
                  width=30).pack(side=tk.LEFT, padx=(0, 6))

        # Manual refresh button (optional, but nice UX)
        ttk.Button(search_frame,
                   text="Refresh List",
                   command=self.refresh_list).pack(side=tk.LEFT)

        # Listbox (main display)
        self.listbox = tk.Listbox(self.root,
                                  width=90,
                                  height=15,
                                  activestyle="dotbox")
        self.listbox.pack(pady=10)

        # Button grid
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=6)
        ttk.Button(btn_frame, text="Add Plant",
                   command=self.add_plant)       .grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text="Update Care",
                   command=self.update_care)     .grid(row=0, column=1, padx=4)
        ttk.Button(btn_frame, text="Delete Plant",
                   command=self.delete_plant)    .grid(row=0, column=2, padx=4)
        ttk.Button(btn_frame, text="Today’s Reminders",
                   command=self.view_reminders)  .grid(row=0, column=3, padx=4)
        ttk.Button(btn_frame, text="Save",
                   command=self.save_data)       .grid(row=0, column=4, padx=4)
        ttk.Button(btn_frame, text="Exit",
                   command=self.exit_app)        .grid(row=0, column=5, padx=4)

        # Status bar
        self.status_var = tk.StringVar(value="Welcome to GreenThumb!")
        ttk.Label(self.root,
                  textvariable=self.status_var,
                  relief=tk.SUNKEN,
                  anchor="w").pack(side=tk.BOTTOM, fill=tk.X)

    # ------------------------------------------------------------------
    # Menu / Dialog Actions
    # ------------------------------------------------------------------
    def _show_about(self) -> None:
        """Display an about dialog with version and authorship."""
        messagebox.showinfo(
            "About GreenThumb",
            "GreenThumb – Smart Plant Care Assistant\n\n"
            "Version 1.0.0\n\n"
            "Authors: Wynstona Jackreece, Ella Smith\n"
            "License: MIT"
        )

    # ------------------------------------------------------------------
    # Core Functionalities
    # ------------------------------------------------------------------
    def update_filter(self, *_) -> None:
        """Filter list as the user types in search box."""
        term = self.search_var.get().lower()
        self.filtered_plants = [p for p in self.plants if term in p.name.lower()]
        self.refresh_list()

    def refresh_list(self) -> None:
        """Redraw the listbox from self.filtered_plants."""
        self.listbox.delete(0, tk.END)
        for plant in self.filtered_plants:
            line = plant.status()
            if plant.needs_care_today():
                line += " ⚠️"
            self.listbox.insert(tk.END, line)

    # -------------- CRUD Operations --------------
    def add_plant(self) -> None:
        """Prompt user for new plant info and append to list."""
        name = simpledialog.askstring("Plant Name", "Enter plant name:")
        if not name:
            return  # canceled

        try:
            water = int(simpledialog.askstring(
                "Water Interval", "Water every how many days?"))
            fert  = int(simpledialog.askstring(
                "Fertilize Interval", "Fertilize every how many days?"))
        except (TypeError, ValueError):
            messagebox.showerror("Invalid Input", "Please enter whole numbers.")
            return

        new_plant = Plant(name, water, fert)
        self.plants.append(new_plant)
        self.filtered_plants = self.plants[:]
        self.refresh_list()
        self.status_var.set(f"Added plant: {name}")

    def update_care(self) -> None:
        """Mark a selected plant as watered, fertilized, or both."""
        if not self._validate_selection():
            return
        plant = self.filtered_plants[self.listbox.curselection()[0]]
        action = (simpledialog.askstring(
            "Care Update",
            "Type 'water', 'fertilize', or 'both':") or "").lower()

        if "water" in action:
            plant.last_watered = datetime.now()
        if "fertilize" in action:
            plant.last_fertilized = datetime.now()

        self.refresh_list()
        self.status_var.set(f"Updated care for {plant.name}")

    def delete_plant(self) -> None:
        """Remove selected plant after confirmation."""
        if not self._validate_selection():
            return
        plant = self.filtered_plants[self.listbox.curselection()[0]]
        if messagebox.askyesno("Delete Plant",
                               f"Are you sure you want to delete '{plant.name}'?"):
            self.plants.remove(plant)
            self.filtered_plants.remove(plant)
            self.refresh_list()
            self.status_var.set(f"Deleted plant: {plant.name}")

    # -------------- Reminders --------------
    def view_reminders(self) -> None:
        """Show plants that need care today in a popup."""
        reminders = [p.status() for p in self.plants if p.needs_care_today()]
        if reminders:
            messagebox.showinfo("Today's Care Reminders", "\n".join(reminders))
        else:
            messagebox.showinfo("You're Good!", "No plants need care today.")
        self.status_var.set("Checked reminders")

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def save_data(self) -> None:
        """Write plant list to JSON file (prompt for location if chosen)."""
        # Allow user to pick a file if they wish
        file_path = filedialog.asksaveasfilename(
            title="Save Plant Data",
            initialfile=DATA_FILE,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return  # canceled

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([p.to_dict() for p in self.plants], f, indent=4)
            self.status_var.set(f"Data saved to {os.path.basename(file_path)}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Save Error", str(exc))
            self.status_var.set("Failed to save data.")

    def load_data(self) -> None:
        """Load plant data from default JSON file, if present."""
        if not os.path.exists(DATA_FILE):
            self.filtered_plants = self.plants[:]  # nothing to load
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                for entry in json.load(f):
                    self.plants.append(Plant(**entry))
            self.filtered_plants = self.plants[:]
            self.refresh_list()
            self.status_var.set("Data loaded from plants.json")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Load Error", str(exc))

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def _validate_selection(self) -> bool:
        """Return True if a listbox item is selected, else show info box."""
        if not self.listbox.curselection():
            messagebox.showinfo("Select Plant",
                                "Please select a plant first.")
            return False
        return True

    def exit_app(self) -> None:
        """Gracefully quit the application."""
        self.root.quit()


# ======================================================================
#                           Script Entrypoint
# ======================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app  = PlantCareApp(root)
    root.mainloop()
