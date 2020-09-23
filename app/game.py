import json
from statistics import median
from datetime import datetime


class Game():
    def __init__(self, commence_time, home_team, home_odds, away_team, away_odds):
        self.commence_time = commence_time

        self.home_team = home_team
        self.home_odds = home_odds
        self.home_median_odds = round(median(home_odds), 2)

        self.away_team = away_team
        self.away_odds = away_odds
        self.away_median_odds = round(median(away_odds), 2)

        self.diff_odds = abs(self.home_median_odds - self.away_median_odds)

    def median_str(self, median_odds):
        return '{:.2f}'.format(median_odds)

    def median_home(self):
        return self.median_str(self.home_median_odds)

    def median_away(self):
        return self.median_str(self.away_median_odds)

    def __lt__(self, other):
        return self.diff_odds < other.diff_odds

    def __str__(self):
        # date = datetime.fromisoformat(
        #     self.commence_time.replace("Z", "+00:00"))
        # return f'{date.strftime("%b %d %Y %H:%M")}'\
        #     f' - {self.home_team.rjust(20," ")} {self.median_home()}' \
        #     f' x {self.median_away()} {self.away_team}'
        return f'{self.home_team.rjust(20," ")} {self.median_home()} x {self.median_away()} {self.away_team}'

    # def toJSON(self):
    #     data = {}
    #     date = datetime.fromisoformat(
    #         self.commence_time.replace("Z", "+00:00"))
    #     data['DATE'] = date.strftime("%b %d %Y %H:%M")

    #     best_team = self.home_team if self.home_median_odds < self.away_median_odds else self.away_team
    #     data['TEAM'] = best_team.upper()

    #     data['AWAY'] = self.away_team
    #     data['AWAY ODDS'] = self.away_median_odds

    #     data['HOME ODDS'] = self.home_median_odds
    #     data['HOME'] = self.home_team

    #     return json.dumps(data)
