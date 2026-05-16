import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes import Drzava
from podatki import drzave
import matplotlib.pyplot as plt

# Import your Drzava class from your existing file
# Assuming your file is named classes.py
from classes import Drzava 

class CountryApp:
    def __init__(self, root, country_data):
        self.root = root
        self.country_data = country_data
        
        # Configure the main window
        self.root.title("Eurostat Country Data Viewer")
        self.root.geometry("350x200")
        self.root.eval('tk::PlaceWindow . center') # Center the window

        # Create UI Elements
        self.setup_ui()

    def setup_ui(self):
        # Label
        label = ttk.Label(self.root, text="Select a country:", font=("Helvetica", 12))
        label.pack(pady=(20, 10))

        # Combobox (Dropdown menu)
        country_names = list(self.country_data.keys())
        self.selected_country = tk.StringVar()
        self.combobox = ttk.Combobox(self.root, textvariable=self.selected_country, values=country_names, state="readonly", font=("Helvetica", 11))
        self.combobox.pack(pady=10)
        
        # Set a default value if the list isn't empty
        if country_names:
            self.combobox.current(0)

        # Button
        show_btn = ttk.Button(self.root, text="Show Graphs", command=self.display_graphs)
        show_btn.pack(pady=20)

    def display_graphs(self):
        country_name = self.selected_country.get()
        
        if not country_name:
            messagebox.showwarning("Warning", "Please select a country first.")
            return

        # Retrieve the specific Drzava object
        country_obj = self.country_data[country_name]    
        # Create a 2x3 grid to host all 6 plots
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle(f"Economic Analysis Dashboard: {country_obj.name}", fontsize=16, fontweight='bold')
        
        try:
            # Row 0: Totals/Absolute Metrics
            country_obj.total_gdp_graph(ax=axes[0, 0])
            country_obj.total_adjusted_gdp_graph(ax=axes[0, 1])
            country_obj.inflation_graph(ax=axes[0, 2])
            
            # Row 1: Growth/Relative Metrics
            country_obj.relative_growth_gdp_graph(ax=axes[1, 0])
            country_obj.adjusted_relative_gdp_growth_graph(ax=axes[1, 1])
            country_obj.adjusted_relative_real_gdp_growth_graph(ax=axes[1, 2])
            
            # Format layout and cleanly render the window
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while plotting:\n{e}")

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Load your real data here (replacing create_mock_data)
    # my_data_dict = load_my_real_json_data() 
    my_data_dict = drzave
    
    # 2. Initialize and run the GUI
    root = tk.Tk()
    app = CountryApp(root, my_data_dict)
    root.mainloop()