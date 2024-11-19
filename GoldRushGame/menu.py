import tkinter as tk

class Menu:
    def __init__(self, root, start_game_callback, settings_callback):
        self.root = root
        self.start_game_callback = start_game_callback
        self.settings_callback = settings_callback
        self.show_menu()

    def show_menu(self):
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create menu options
        self.canvas = tk.Canvas(self.root, width=500, height=400, bg='black')
        self.canvas.pack()
        self.canvas.create_text(self.canvas.winfo_width() / 2 + 250, 50, text="Gold Rush", fill="white", font=("Arial", 24), anchor=tk.CENTER)

        # Create a frame to hold the buttons in the center
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        start_button = tk.Button(button_frame, text="Start", command=self.start_game_callback, font=("Arial", 14), width=10)
        settings_button = tk.Button(button_frame, text="Settings", command=self.settings_callback, font=("Arial", 14), width=10)
        exit_button = tk.Button(button_frame, text="Exit", command=self.root.quit, font=("Arial", 14), width=10)

        # Position buttons within the frame
        start_button.pack(pady=10)
        settings_button.pack(pady=10)
        exit_button.pack(pady=10)

    def show_settings(self):
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Settings label
        self.canvas = tk.Canvas(self.root, width=500, height=400, bg='black')
        self.canvas.pack()
        # Create a frame for the back button in the center
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        back_button = tk.Button(button_frame, text="Back", command=self.show_menu, font=("Arial", 14), width=10)
        back_button.pack(pady=20)
