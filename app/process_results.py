import json
import sys
from types import SimpleNamespace
from datetime import datetime

from .game import Game


def dumper(obj):
    try:
        data = {}
        date = datetime.fromisoformat(
            obj.commence_time.replace("Z", "+00:00"))
        data['DATE'] = date.strftime("%b %d %Y %H:%M")

        best_team = obj.home_team if obj.home_median_odds < obj.away_median_odds else obj.away_team
        data['TEAM'] = best_team.upper()

        data['AWAY'] = obj.away_team
        data['AWAY ODDS'] = obj.away_median_odds

        data['HOME ODDS'] = obj.home_median_odds
        data['HOME'] = obj.home_team

        return data

    except:
        return ''


def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result


class Results:
    def __init__(self, results):
        self.results = results

    def process(self):
        games = []
        for game in self.results:
            home_odds = []
            away_odds = []
            for site in game.sites:
                home_odds.append(site.odds.h2h[0])
                away_odds.append(site.odds.h2h[1])

            thisGame = Game(game.commence_time,
                            game.teams[0], home_odds, game.teams[1], away_odds)
            games.append(thisGame)
            # print(thisGame)

        games.sort(reverse=True)
        return json.dumps(games, default=dumper)

        # teams_did_choose = 'did_choose.json'
        # with open(teams_did_choose, encoding='utf-8') as json_file:
        #     my_chosen = json.load(
        #         json_file, object_hook=lambda d: SimpleNamespace(**d))

        # sep = '\n'+'*'*140+'\n'
        # print(sep)

        # with open('results.txt', 'a', encoding='utf-8') as f:
        #     f.write(sep)
        #     f.write('%s\n\n' % datetime.now().strftime("%b %d %Y %H:%M"))

        #     for game in games:
        #         # print(game)
        #         best_team = game.home_team if game.home_median_odds < game.away_median_odds else game.away_team
        #         best_team = best_team.upper()

        #         team_str = best_team.center(24, ' ')
        #         team_str = strike(
        #             team_str) if best_team in my_chosen else team_str
        #         if len(sys.argv) > 1 and sys.argv[1] == 'True':
        #             my_chosen.append(best_team)
        #             with open(teams_did_choose, 'w', encoding='utf-8') as f:
        #                 json.dump(my_chosen, f,
        #                           ensure_ascii=False, indent=4)

        #         date = datetime.fromisoformat(
        #             game.commence_time.replace("Z", "+00:00"))
        #         date_str = f'{date.strftime("%b %d %Y %H:%M")}'
        #         item = f'{date_str}\t{team_str} \t-\t {game}'
        #         print(item)
        #         f.write('%s\n' % item)

        #     f.write(sep)
        #     print(sep)
