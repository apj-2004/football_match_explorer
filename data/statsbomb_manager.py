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

    def load_matches(self):
        self.matches_df = sb.matches(competition_id=self.selected_competition_id,
                        season_id = self.selected_season_id
                        )
        return self.matches_df

    def get_matches_list(self):
        self.matches_df["display_names"] = self.matches_df["home_team"] + " vs " + self.matches_df["away_team"]
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

    def get_match_id(self, match):

        match_row = self.matches_df[self.matches_df["display_names"]==match]
        self.selected_match_id = match_row.iloc[0]["match_id"]

        print(self.selected_match_id)
