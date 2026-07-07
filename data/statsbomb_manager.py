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
        match_info = {
            "home_team": row["home_team"],
            "away_team": row["away_team"],
            "home_score": row["home_score"],
            "away_score": row["away_score"]
        }

        return match_info
