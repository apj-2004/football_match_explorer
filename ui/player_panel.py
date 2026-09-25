import customtkinter as ctk

class PlayerPanel:

    def __init__(self, parent, player_selected_callback=None):

        self.parent = parent
        self.player_selected_callback = player_selected_callback

        self.main_frame = ctk.CTkFrame(
            self.parent
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        #space for players

        self.players_frame = ctk.CTkScrollableFrame(
            self.main_frame
        )

        self.players_frame.pack(
            fill="both",
            expand=True,
            padx=15,pady=10
        )

    def update_players(self, lineup_data):

        #clear slate everytime
        for widget in self.players_frame.winfo_children():
            widget.destroy()

        home_team = lineup_data.get("home_team")
        away_team = lineup_data.get("away_team")

        home_lineup = lineup_data.get("home_lineup")
        away_lineup = lineup_data.get("away_lineup")


        self.create_team_section(
            home_team,
            home_lineup
        )

        self.create_team_section(
            away_team,
            away_lineup
        )

    def create_team_section(self,team_name, lineup):

        team_frame = ctk.CTkFrame(
            self.players_frame
        )

        team_frame.pack(
            fill="x",
            pady=5
        )

        plyr_frame = ctk.CTkFrame(
            team_frame,
            fg_color="transparent"
        )

        team_button = ctk.CTkButton(
            team_frame,
            text=f"▼  {team_name}",
            anchor="w",
            font=("Segoe UI", 15, "bold"),
            command = lambda: self.toggle_team(
                team_button,
                plyr_frame,
                team_name
            )
        )

        team_button.pack(
            fill="x",
            padx=5, pady=5
        )

        for _, player in lineup.iterrows():

            player_label = ctk.CTkButton(
                plyr_frame,
                text=f'{player["jersey_number"]}    {player["player.name"]}',
                anchor="w",
                command= lambda p=player: self.select_player(p),
                font=("Segoe UI", 13)
            )

            player_label.pack(
                fill="x",
                padx=15, pady=3
            )

    def toggle_team(
        self,
        team_button,
        player_frame,
        team_name
    ):

        if player_frame.winfo_manager():

            player_frame.pack_forget()

            team_button.configure(
                text=f"▶  {team_name}"
            )

        else:

            player_frame.pack(
                fill="x",
                padx=5,
                pady=(0, 5)
            )

            team_button.configure(
                text=f"▼  {team_name}"
            )
    def select_player(self, player_data):

        self.selected_player = player_data

        player_id = player_data["player.id"]

        if self.player_selected_callback:
            self.player_selected_callback(player_id)
