import customtkinter as ctk
from ui.stat_row import StatRow

class MatchPanel:

    def __init__(self, parent):

        self.parent= parent

        self.main_frame = ctk.CTkFrame(
            self.parent
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        self.title_label= ctk.CTkLabel(
            self.main_frame,
            text="Match Information",
            font=("Segoe UI", 18, "bold")
        )

        self.title_label.pack(
            pady=(15,10)
        )

        #creating the header frame

        self.header_frame = ctk.CTkFrame(
            self.main_frame
        )
        self.header_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.header_frame.grid_columnconfigure(0,weight=1)
        self.header_frame.grid_columnconfigure(1,weight=1)
        self.header_frame.grid_columnconfigure(2,weight=1)


        #labels for teams and score,
        self.home_team_label = ctk.CTkLabel(
            self.header_frame,
            text =  "Home Team",
            font=("Segoe UI", 14, "bold")
        )
        self.home_team_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5
        )
        self.score_label = ctk.CTkLabel(
            self.header_frame,
            text= "0 - 0",
            font=("Segoe UI", 18, "bold")
        )
        self.score_label.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5
        )
        self.away_team_label = ctk.CTkLabel(
            self.header_frame,
            text="Away Team",
            font=("Segoe UI", 14, "bold")
        )
        self.away_team_label.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=5
        )

        self.statistics_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.statistics_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        statistics = [
            "Possession",
            "Attempted Passes",
            "Completed Passes",
            "Pass Accuracy",
            "Shots",
            "On Target",
            "Corners",
            "Saves",
        ]
        self.stat_rows = {}

        for statistic in statistics:

            row = StatRow(self.statistics_frame)
            self.stat_rows[statistic] = row
            row.update_values(
                "--",
                statistic,
                "--"
            )



    def update_match_info(self, match_info):

        self.home_team_label.configure(text=match_info["home_team"])
        self.away_team_label.configure(text=match_info["away_team"])

        score_text = (
            str(match_info["home_score"])
            +" - "
            + str(match_info["away_score"])
        )

        self.score_label.configure(text=score_text)

    def update_team_statistics(self, statistics):

        for statistic, values in statistics.items():

            row = self.stat_rows[statistic]
            row.update_values(
                values[0],
                statistic,
                values[1]
            )
