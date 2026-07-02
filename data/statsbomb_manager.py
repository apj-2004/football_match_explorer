#import
from statsbombpy import sb

class StatsBombManager:

    def __init__(self):
        self.competitions_df = sb.competitions()
        self.selected_competition_df = None
        self.selected_competition_id = None
        self.selected_season_id = None
        self.selected_match_id = None
        self.events_df = None
        self.lineups_df = None


    def get_competitions(self):
        return self.competitions_df

    def get_matches(self, competition_id, season_id):
        return sb.matches(competition_id=competition_id,
                        season_id = season_id
                        )

    def get_seasons(self, competition_name):
        self.selected_competition_df = self.competitions_df[self.competitions_df["competition_name"]==competition_name]

        return self.selected_competition_df["season_name"].tolist()

    def get_ids(self, season):
        if self.selected_competition_df is None:
            raise ValueError("No competition selected")
        season_row = self.selected_competition_df[self.selected_competition_df["season_name"]==season]

        self.selected_competition_id = season_row.iloc[0]["competition_id"]
        self.selected_season_id = season_row.iloc[0]["season_id"]
        return self.selected_competition_id, self.selected_season_id
