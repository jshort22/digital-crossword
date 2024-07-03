import tkinter as tk
from tkinter import messagebox
from typing import List, Any
from saturday_clues import grid_fill, across_clues, down_clues


class Crossword:
    def __init__(self, root: tk.Tk):

        # Window
        self.root = root
        self.root.title("Crossword Puzzle")
        self.root.geometry("1000x500")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Crossword Frame
        self.cw_frame = tk.Frame(self.root)
        self.cw_frame.grid(row=0, column=0, sticky="nsew")

        # Across Frame
        self.across_frame = tk.Frame(self.root)
        self.across_frame.grid(row=0, column=1, sticky="nsew")

        # Down Frame
        self.down_frame = tk.Frame(self.root)
        self.down_frame.grid(row=0, column=2, sticky="nsew")

        # Expanded Weights
        self.across_frame.grid_rowconfigure(0, weight=1)
        self.down_frame.grid_rowconfigure(0, weight=1)
        self.across_frame.grid_columnconfigure(0, weight=1)
        self.down_frame.grid_columnconfigure(0, weight=1)

        # Across List Box
        self.across_box = tk.Listbox(
            self.across_frame,
            selectbackground="#008080",
            selectforeground="white",
            activestyle="none",
        )
        self.across_box.grid(sticky="nsew")

        # Down List Box
        self.down_box = tk.Listbox(
            self.down_frame,
            selectbackground="#008080",
            selectforeground="white",
            activestyle="none",
        )
        self.down_box.grid(sticky="nsew")

        self.grid_layout2: List[list[str]] = grid_fill
        self.entries: List[List[Any]] = [[None for _ in range(15)] for _ in range(15)]

    def build_grid(self):

        for i in range(15):
            self.cw_frame.grid_rowconfigure(i, weight=1)
            self.cw_frame.grid_columnconfigure(i, weight=1)

        box_counter = 1
        # Crossword grid
        for x, row in enumerate(grid_fill):
            for y, letter in enumerate(row):

                # 15 x 15 FRAME
                letter_frame = tk.Frame(
                    self.cw_frame,
                    borderwidth=0,
                    highlightthickness=0,
                    bg="#000000",
                )
                letter_frame.grid(row=x, column=y, sticky="nsew")

                letter_frame.grid_rowconfigure(0, weight=1)
                letter_frame.grid_columnconfigure(0, weight=1)

                # BLACK AND WHITE SQUARES
                letter_box = tk.Entry(
                    letter_frame,
                    width=2,
                    borderwidth=0,
                    justify="center",
                    highlightthickness=0.5,
                    highlightcolor="#00FF00",
                    relief="solid",
                    foreground="#000000",
                    background="#000000" if letter == " " else "#FFFFFF",
                    state="disabled" if letter == " " else "normal",
                    font=("Arial", 16),
                )
                letter_box.grid(sticky="nsew")

                letter_box.bind("<KeyRelease>", self.on_key_release)
                letter_box.bind("<BackSpace>", self.delete_and_focus_prev)

                letter_box.grid_rowconfigure(0, weight=1)
                letter_box.grid_columnconfigure(0, weight=1)

                if letter != " ":
                    letter_box.expected_value = letter
                    self.entries[x][y] = letter_box
                else:
                    self.entries[x][y] = None

                # ASSIGN NUMBERS
                if letter != " ":
                    if (grid_fill[x - 1][y] == " " or x == 0) or (
                        grid_fill[x][y - 1] == " " or y == 0
                    ):

                        box_number = tk.Text(
                            letter_frame,
                            highlightthickness=0,
                            borderwidth=0,
                            bg="#FFFFFF",
                            fg="#000000",
                            font=("Arial", 8),
                        )
                        box_number.insert(tk.END, str(box_counter))
                        box_counter += 1

                        box_number.place(x=1, y=1, width=11, height=10)

    def capitalize_letter(self, event: Any):
        current_letter = event.widget.get()
        uppercase_letter = current_letter.upper()
        event.widget.delete(0, tk.END)
        event.widget.insert(0, uppercase_letter)

    def focus_next_entry(self, event: Any):
        current_widget = event.widget
        next_widget = current_widget.tk_focusNext()

        while True:
            if isinstance(next_widget, tk.Entry) and not next_widget.get():
                next_widget.focus()
                break

            next_widget = next_widget.tk_focusNext()

    def on_key_release(self, event: Any):
        self.capitalize_letter(event)
        if self.check_grid_full(event):
            if not self.compare_grids(event):
                messagebox.showwarning(
                    "Update", "At least 1 letter is wrong. Keep trying!"
                )
            return
        self.focus_next_entry(event)

    def delete_and_focus_prev(self, event: Any):
        latest_widget = event.widget
        previous_widget = latest_widget.tk_focusPrev()
        start_widget = previous_widget

        while True:
            if isinstance(previous_widget, tk.Entry) and previous_widget.get():
                previous_widget.delete(0, tk.END)
                previous_widget.focus()
                break

            previous_widget = previous_widget.tk_focusPrev()

            if start_widget == previous_widget:
                break

    def check_grid_full(self, event: Any):
        for row in self.entries:
            for entry in row:
                if entry is not None and not entry.get().strip():
                    return False
        return True

    def compare_grids(self, event: Any):
        for x, row in enumerate(self.entries):
            for y, entry in enumerate(row):
                if entry is not None:
                    current_value = entry.get().upper()
                    expected_value = entry.expected_value
                    if current_value != expected_value:
                        return False

        print("The grid is correct!")
        messagebox.showinfo("Update", "Congrats! You solved the puzzle!")
        return True

    def upload_across_clues(self):
        for clue in across_clues:
            if clue:
                self.across_box.insert(tk.END, clue)

    def upload_down_clues(self):
        for clue in down_clues:
            if clue:
                self.down_box.insert(tk.END, clue)


if __name__ == "__main__":
    root = tk.Tk()
    app = Crossword(root)
    app.build_grid()
    app.upload_across_clues()
    app.upload_down_clues()
    root.mainloop()
