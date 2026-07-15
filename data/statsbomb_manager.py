#import
from statsbombpy import sb

class StatsBombManager:

    def __init__(self):
        self.competitions_df = sb.competitions()
        self.selected_competition_df = None
        self.matches_df = None

        self.selected_competition_id = None
        self.selected_season_id = None
        self.selected_match_id = None

        self.events_df = None
        self.lineups_df = None


    def get_competitions(self):
        return self.competitions_df

    def load_matches_df(self):
        self.matches_df = sb.matches(competition_id=self.selected_competition_id,
                        season_id = self.selected_season_id
                        )
        self.matches_df["display_names"] = self.matches_df["home_team"] + " vs " + self.matches_df["away_team"]
        return self.matches_df

    def get_matches_list(self):
        return self.matches_df["display_names"]

    def get_seasons(self, competition_name):
        self.selected_competition_df = self.competitions_df[self.competitions_df["competition_name"]==competition_name]

        return self.selected_competition_df["season_name"].tolist()

    def get_season_details(self, season):
        if self.selected_competition_df is None:
            raise ValueError("No competition selected")
        season_row = self.selected_competition_df[self.selected_competition_df["season_name"]==season]

        self.selected_competition_id = season_row.iloc[0]["competition_id"]
        self.selected_season_id = season_row.iloc[0]["season_id"]

        return self.selected_competition_id, self.selected_season_id

    def update_match_id(self, match):

        match_row = self.matches_df[self.matches_df["display_names"]==match]
        self.selected_match_id = match_row.iloc[0]["match_id"]

    def load_match(self):

        self.events_df = sb.events(match_id=self.selected_match_id)
        self.lineups_df = sb.lineups(match_id=self.selected_match_id)


    def check_events_lineups_df(self):
        return (
            self.events_df is not None
            and
            self.lineups_df is not None
        )

    def get_match_info(self):

        row = self.matches_df[
                        self.matches_df["match_id"] == self.selected_match_id
                    ]

        row = row.iloc[0]
        home_team = row["home_team"]
        away_team = row["away_team"]

        match_info = {
            "home_team": row["home_team"],
            "away_team": row["away_team"],
            "home_score": row["home_score"],
            "away_score": row["away_score"]
        }

        return match_info

    def get_team_statistics(self):

        statistics = {}

        row = self.matches_df[
                        self.matches_df["match_id"] == self.selected_match_id
                    ]

        row = row.iloc[0]
        home_team = row["home_team"]
        away_team = row["away_team"]

        #filtering passes

        pass_events = self.events_df[
            self.events_df["type"] == "Pass"
        ]

        completed_pass_events = pass_events[
            pass_events["pass_outcome"].isna()
        ]

        pass_counts = pass_events["team"].value_counts()

        passes_home = pass_counts.get(home_team, 0)
        passes_away = pass_counts.get(away_team, 0)

        completed_pass_counts = completed_pass_events["team"].value_counts()

        completed_passes_home = completed_pass_counts.get(home_team, 0)
        completed_passes_away = completed_pass_counts.get(away_team, 0)

        pass_accuracy_home = (completed_passes_home/passes_home) *100
        pass_accuracy_away = (completed_passes_away/passes_away) *100

        statistics["Attempted Passes"] = (
            passes_home,
            passes_away
        )

        statistics["Completed Passes"]  = (
            completed_passes_home,
            completed_passes_away
        )

        statistics["Pass Accuracy"] = (
            f"{pass_accuracy_home:.2f} %",
            f"{pass_accuracy_away:.2f} %"
        )

        #filtering Shots

        shot_events = self.events_df[
            self.events_df["type"] == "Shot"
        ]

        shot_counts = shot_events["team"].value_counts()

        shots_home = shot_counts.get(home_team,0)
        shots_away = shot_counts.get(away_team,0)

        statistics["Shots"] =(
            shots_home,
            shots_away
        )

        #needs refinement on how shots on target is computed
        shots_target_events = shot_events[
            shot_events["shot_outcome"] != "Off T"
        ]

        shots_target_counts = shots_target_events["team"].value_counts()

        shots_target_home = shots_target_counts.get(home_team,0)
        shots_target_away = shots_target_counts.get(away_team,0)

        statistics["On Target"] =(
            shots_target_home,
            shots_target_away
        )

        #filtering corners

        corner_events = pass_events[
            pass_events["pass_type"] == "Corner"
        ]

        corner_counts = corner_events["team"].value_counts()

        corner_home = corner_counts.get(home_team, 0)
        corner_away = corner_counts.get(away_team, 0)

        statistics["Corners"] = (
            corner_home,
            corner_away
        )

        #filtering Saves
        save_events = self.events_df[
            self.events_df["goalkeeper_type"] == "Shot Saved"
        ]

        save_counts = save_events["team"].value_counts()

        saves_home = save_counts.get(home_team, 0)
        saves_away = save_counts.get(away_team, 0)

        statistics["Saves"] =(
            saves_home,
            saves_away
        )

        #computing Possession
        possession_events = self.events_df.drop_duplicates(subset="possession")

        total_events = len(possession_events)

        possession_counts = possession_events["possession_team"].value_counts()

        possession_home = int(possession_counts.get(home_team, 0))/ int(total_events)
        possession_home *= 100

        possession_away = int(possession_counts.get(away_team, 0))/ int(total_events)
        possession_away *= 100

        print(total_events, possession_counts)

        statistics["Possession"] = (
            f"{possession_home:.2f} %",
            f"{possession_away:.2f} %"
        )

        return statistics
