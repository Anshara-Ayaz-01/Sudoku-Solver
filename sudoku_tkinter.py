import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from sudoku_logic import SudokuApp


class SudokuBoard(tk.Frame):
    def __init__(self, master, level):
        tk.Frame.__init__(self, master)
        self.level = level
        self.create_widgets()

    def create_widgets(self):
        # Create a colored canvas with a vertical scrollbar for the Sudoku board
        canvas = tk.Canvas(self, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Set background color for SudokuBoard frame
        self.configure(bg="#f0f0f0")

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")

        sudoku_board = self.generate_sudoku_board()

        # Calculate cell size based on the number of rows and columns
        cell_size = 50

        for i, row in enumerate(sudoku_board):
            for j, value in enumerate(row):
                x = j * cell_size
                y = i * cell_size
                canvas.create_rectangle(x, y, x + cell_size, y + cell_size, outline="black", fill="#f0f0f0")
                canvas.create_text(x + cell_size / 2, y + cell_size / 2, text=str(value), font=("Arial", 12))

        back_button = tk.Button(self, text="Back to Main Menu", command=self.back_to_main_menu, font=("Arial", 12), bg="#ff6666")
        back_button.pack(pady=10)


    def back_to_main_menu(self):
        self.master.switch_frame(MainMenu)

class MainMenu(tk.Frame):
    # Make background_image_tk a class variable
    background_image_tk = None

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        if MainMenu.background_image_tk is None:
            # Load the image only if it hasn't been loaded before
            background_image = Image.open('img.png')
            background_image_resized = background_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
            MainMenu.background_image_tk = ImageTk.PhotoImage(background_image_resized)

        # Create a colored canvas with the background image
        colored_canvas = tk.Canvas(self, bg="#f0f0f0", width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        colored_canvas.pack()

        background_label = tk.Label(colored_canvas, image=MainMenu.background_image_tk, bg="#f0f0f0")
        background_label.image = MainMenu.background_image_tk
        background_label.place(relwidth=1, relheight=1)

        play_button = tk.Button(colored_canvas, text="Play", command=self.show_level_selection, font=("Arial", 16), bg="#66c2ff", width=10, height=2)
        play_button.place(relx=0.5, rely=0.4, anchor="center")

        help_button = tk.Button(colored_canvas, text="Help", command=self.display_help, font=("Arial", 12), bg="#ffcc66", width=10, height=2)
        help_button.place(relx=0.5, rely=0.5, anchor="center")

        exit_button = tk.Button(colored_canvas, text="Exit", command=self.master.destroy, font=("Arial", 12), bg="#ff6666", width=10, height=2)
        exit_button.place(relx=0.5, rely=0.6, anchor="center")

    class LevelSelection(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self, master)
            self.master = master
            self.create_widgets()

    def display_help(self):
        help_text = (
            "Welcome to Sudoku Game!\n\n"
            "Rules:\n"
            "1. Fill each row, column, and 3x3 box with the numbers 1-9.\n"
            "2. Each number must appear exactly once in each row, column, and box.\n\n"
            "How to Play:\n"
            "1. Click 'Play' to select the difficulty level (Easy, Medium, Hard).\n"
            "2. Once the level is selected, a Sudoku board will be displayed.\n"
            "3. Fill in the empty cells by clicking on them and entering the numbers.\n"
            "4. Click 'Back to Main Menu' to return to the main menu."
        )
        messagebox.showinfo("Help", help_text)


class SudokuApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Sudoku Game")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self._frame = None
        self.switch_frame(MainMenu)

    def switch_frame(self, frame_class, *args):
        if self._frame is not None:
            self._frame.destroy()
        new_frame = frame_class(self, *args)
        new_frame.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        self.title(new_frame.winfo_class())
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")

if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()

