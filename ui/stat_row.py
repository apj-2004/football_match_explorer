import customtkinter as ctk

class StatRow:

    def __init__(self, parent):

        self.parent= parent

        self.main_frame = ctk.CTkFrame(
            self.parent
        )

        self.main_frame.pack(
            fill="x",
            pady=10,
            padx=5
        )

        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_columnconfigure(1,weight=1)
        self.main_frame.grid_columnconfigure(2,weight=1)


        self.left_label = ctk.CTkLabel(
            self.main_frame,
            text=" -- "
        )
        self.left_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5
        )

        self.center_label = ctk.CTkLabel(
            self.main_frame,
            text = "Stats",
            font=("Segoe UI", 13, "bold")
        )
        self.center_label.grid(
            row = 0,
            column = 1,
            sticky="ew",
            padx=5
        )

        self.right_label = ctk.CTkLabel(
            self.main_frame,
            text= "--"
        )
        self.right_label.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=5
        )

    def update_values(self, left, statistic, right):

        self.left_label.configure(text = left)
        self.center_label.configure(text= statistic)
        self.right_label.configure(text=right)
