# GreenThumb – Smart Plant Care Assistant

**GreenThumb** is a Python desktop application (Tkinter GUI) that helps you track watering and fertilizing schedules for your plants.  
You can add plants, update care dates, search, delete, and view reminders.  
All data is saved persistently in a JSON file.

---

## 🌱 Features

✅ Add plants with watering and fertilizing intervals  
✅ Update care status (watered or fertilized)  
✅ Search and delete plants  
✅ View daily reminders for plants needing care  
✅ Data saved in `plants.json` (JSON format)  
✅ Simple, user‑friendly Tkinter GUI  

---

## ⚙️ Requirements

- **Python 3.10+** (Tkinter comes pre‑installed with most Python distributions)
- Standard libraries only (no additional installations needed):
  - `tkinter`
  - `json`
  - `os`
  - `datetime`

---

## 📥 Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/YOUR_USERNAME/GreenThumb.git
   cd GreenThumb

2. **Verify Python installation**
    ```bash
    python --version

    OR

    python3 --version

---

## ▶️ **How to Run**
Run the GUI application with:

    python greenthumb_gui.py

or, depending on your system:

    python3 greenthumb_gui.py

The main window will open.
You can immediately start adding plants and managing their care schedules.

---

## 💾 Data Persistence
All plant data is saved to a JSON file called plants.json in the same directory as the script.

If plants.json does not exist, it will be created automatically when you save.

---

## 📂 Files in This Repository

greenthumb_gui.py : Main application code (Tkinter GUI)

plants.json	: JSON file storing plant data (created after saving)

README.md	: Instructions for running the application

---

## 📜 License
This project is licensed under the MIT License.

---

## ✨ Authors
Wynstona Jackreece

Ella Smith

Code refined with assistance from ChatGPT (OpenAI GPT‑4) and GitHub Copilot Chat
