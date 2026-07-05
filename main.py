#this is the main python code file for the football match explorer  project
# Author:   APJ
#StartDate: 24-06-2026

#import
import customtkinter as ctk
from data.statsbomb_manager import StatsBombManager

## App Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

## Main Window

root = ctk.CTk()

root.title("Football Match Explorer")
root.geometry("800x600")

#main frame
main_frame = ctk.CTkFrame(root)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

#title
title_label = ctk.CTkLabel(
    main_frame,
    text="Football Match Explorer",
    font=("Segoe UI", 24, "bold")
)

title_label.pack(pady=20)


##Loading the matches

#StatsBombManager
manager = StatsBombManager()

#competitions_df
competitions_df = manager.get_competitions()
competition_names = sorted(
    competitions_df["competition_name"]
    .unique()
    .tolist()
)

#competition selected
def competition_selected(choice):
    season_names = manager.get_seasons(choice)

    season_dropdown.configure(
        values = season_names
    )

def season_selected(choice):
    manager.get_season_details(choice)

    manager.load_matches()

    matches_name = manager.get_matches_list()

    match_droplist.configure(
        values=matches_name
    )

def match_selected(choice):

    manager.update_match_id(choice)

#competition droplist
competition_dropdown = ctk.CTkComboBox(
    main_frame,
    values=competition_names,
    width=300
)
competition_dropdown.pack(pady=10)

competition_dropdown.configure(
    command=competition_selected
)

#season droplist
season_dropdown = ctk.CTkComboBox(
    main_frame,
    values=["Select Season"],
    width=300
)

season_dropdown.pack(pady=10)
season_dropdown.configure(
    command=season_selected
)

#match droplist
match_droplist = ctk.CTkComboBox(
    main_frame,
    values=['Select Matches'],
    width=300
)

match_droplist.configure(
    command = match_selected
)
match_droplist.pack(pady=10)

#
root.mainloop()
