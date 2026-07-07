#import
import customtkinter as ctk


class NavigationPanel:

    def __init__(self, parent, competition_names):

        self.parent = parent
        self.competition_names= competition_names

        #competition droplist
        self.competition_dropdown = ctk.CTkComboBox(
            self.parent,
            values=self.competition_names,
            width=300
        )
        self.competition_dropdown.pack(pady=10)

        #season droplist
        self.season_dropdown = ctk.CTkComboBox(
            self.parent,
            values=["Select Season"],
            width=300
        )

        self.season_dropdown.pack(pady=10)

        #match droplist
        self.match_droplist = ctk.CTkComboBox(
            self.parent,
            values=['Select Matches'],
            width=300
        )

        self.match_droplist.pack(pady=10)

        #load match button
        self.load_match_button = ctk.CTkButton(
            self.parent,
            text="Load Match"
        )
        self.load_match_button.pack(pady=10)

    def set_competition_callback(self, callback):
        self.competition_dropdown.configure(command= callback)

    def set_season_callback(self, callback):
        self.season_dropdown.configure(command= callback)

    def set_match_callback(self, callback):
        self.match_droplist.configure(command = callback)

    def set_load_match_button_callback(self, callback):
        self.load_match_button.configure(command=callback)

    def update_seasons(self, season_names):
        self.season_dropdown.configure(values=season_names)

    def update_matches(self, match_names):
        self.match_droplist.configure(values=match_names)
