#import
from statsbombpy import sb

class StatsBombManager:

    def __init__(self):
        pass

    def get_competitions(self):
        return sb.competitions()

    def get_matches(self, competition_id, season_id):
        return sb.matches(competition_id=competition_id,
                        season_id = season_id
                        )
