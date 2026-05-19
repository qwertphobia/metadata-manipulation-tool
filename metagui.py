#!/usr/bin/env python3
import tkinter as tk
import tkintermapview
import json

class Menu:
    def __init__(self, master, initial_text): 
        self.initial_text = initial_text    
        self.master = master
        self.master.title("EDIT METADATA MENU")
        
        # Variable to hold the final result
        self.result_data = None
        self.done_event = False 

        # Create main screen widgets
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)
        
        self.edit_button = tk.Label(self.main_frame, text="EDIT METADATA MENU", font=("monospace", 18))
        self.edit_button.place(x=270, y=200)

        self.notepad_button = tk.Button(self.main_frame, text="Virtual Notepad", command=self.open_notepad)
        self.notepad_button.place(x=320, y=250)
        
        self.map_button = tk.Button(self.main_frame, text="World Map(gps)", command=self.open_map)
        self.map_button.place(x=320, y=300)

        self.notepad_frame = None
        self.error_label = None # To display validation errors

    def open_notepad(self):  
        self.main_frame.pack_forget()
        self.notepad_frame = tk.Frame(self.master)
        self.notepad_frame.pack(fill="both", expand=True)
        
        self.textarea = tk.Text(self.notepad_frame, wrap='word', font=("Courier", 12))
        self.textarea.pack(fill="both", expand=True, padx=10, pady=10)
        
        if self.initial_text:
            self.textarea.insert("1.0", self.initial_text)
        
        # Create red Back button
        back_button = tk.Button(self.notepad_frame, text="Back (Save)", fg="red", command=self.close_notepad)
        back_button.pack(pady=5)

        # Label to show JSON errors
        self.error_label = tk.Label(self.notepad_frame, text="", fg="red", font=("Arial", 10))
        self.error_label.pack(pady=5)

    def close_notepad(self):
        # 1. Get text from the widget
        raw_text = self.textarea.get("1.0", tk.END).strip()
        
        # Clear previous error
        if self.error_label:
            self.error_label.config(text="")

        try:
            # 2. Parse as JSON
            self.result_data = json.loads(raw_text)
            print("Metadata parsed successfully.")
            
            # 3. Signal completion and hide frame
            self.done_event = True
            self.notepad_frame.pack_forget()
            self.main_frame.pack(fill="both", expand=True)
            
        except json.JSONDecodeError as e:
            # 4. Handle Syntax Errors Gracefully
            error_msg = f"Invalid JSON: {e.msg} at line {e.lineno}, column {e.colno}"
            print(error_msg)
            
            # Show error in the GUI so the user knows what to fix
            if self.error_label:
                self.error_label.config(text=error_msg)
            
            # Do NOT close the notepad; let the user fix it
            # Optionally, highlight the line (advanced, but good to keep simple here)
            return 

    def open_map(self): 
        self.main_frame.pack_forget()
        self.map_frame = tk.Frame(self.master)
        self.map_frame.pack(fill="both", expand=True)

        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, width=800, height=600)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(0.0, 0.0)
        self.map_widget.set_zoom(2)
        
        self.coord_label = tk.Label(self.map_frame, text="Right click on the map to copy gps coordinates")
        self.coord_label.pack(pady=5)

        back_button = tk.Button(self.map_frame, text="Back", fg="red", command=self.close_map)
        back_button.pack(pady=5)

    def close_map(self):
        self.map_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)