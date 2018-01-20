# (function(console){

#     console.save = function(data, filename){

#         if(!data) {
#             console.error('Console.save: No data')
#             return;
#         }

#         if(!filename) filename = 'console.json'

#         if(typeof data === "object"){
#             data = JSON.stringify(data, undefined, 4)
#         }

#         var blob = new Blob([data], {type: 'text/json'}),
#             e    = document.createEvent('MouseEvents'),
#             a    = document.createElement('a')

#         a.download = filename
#         a.href = window.URL.createObjectURL(blob)
#         a.dataset.downloadurl =  ['text/json', a.download, a.href].join(':')
#         e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
#         a.dispatchEvent(e)
#     }
# })(console)

# String.prototype.capitalize = function(){
#        return this.replace( /(^|\s)([a-z])/g , function(m,p1,p2){ return p1+p2.toUpperCase(); } );
#       };
# var table = document.getElementsByClassName("player-list-table stats-player-list-table");
# counter = 0
# requirement = {"GK": 0, "FB": 0, "CB": 0, "MF": 20, "ST": 20}
# var players = {}
# for (var i = 1, row; row = table[0].rows[i]; i++) {
# var points = parseInt(row.cells[11].innerText)
# var price = parseFloat(row.cells[12].innerText)
# var position = row.cells[0].innerText.trim()
# var name = row.cells[1].innerText.trim()
# var team  = row.cells[4].innerText.trim()

# if (points > requirement[position] || price == 3.2) {

# 	if (!(position in players)) players[position] = {}
# 	if (!(team in players[position])) players[position][team] = {}


# 	players[position][team][name.toLowerCase().capitalize()] = price
# 	counter++
# }
# }
# console.log(counter)
# console.save(players)


import urllib.request
import json
from enum import Enum
import datetime

SALARY_CAP = 55

# request = urllib.request.urlopen("https://raw.githubusercontent.com/bcaldwell/CFFL/master/player_list/player_list_trimmed.json").read()

player_scores_raw = urllib.request.urlopen(
    "https://cffl.bcaldwell.ca/player_scores.json").read()

player_scores = json.loads(player_scores_raw)

f = open("./console.json", "r")
request = f.read()
data = json.loads(request)

formation = [1, 2, 2, 4, 2]

# datetime.datetime.strptime('2017-08-11T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ').date()


def check_score(team):
    if team.verify():
        score_1 = team.calculate_score(2017, 12, 18)
        if score_1 != 17:
            return False
        score_2 = team.calculate_score(2017, 12, 25)
        if score_2 != 34:
            return False
        score_3 = team.calculate_score(2018, 1, 1)
        if score_3 != 14:
            return False
        score_4 = team.calculate_score(2018, 1, 8)
        if score_4 != 20:
            return False
        return True
    return False


class Position(Enum):
    GK = 0
    FB = 1
    CB = 2
    MF = 3
    ST = 4


class Player:

    def __init__(self, name, position, cost, team=""):
        self.name = name
        self.position = Position[position]
        self.cost = float(cost)
        self.team = team

    def __repr__(self):
        return "{:20}{:7}{:7}{}".format(self.name, self.position.name, self.team, self.cost)


class Team:
    def __init__(self):
        self.players = []
        self.formation = [0, 0, 0, 0, 0]

    def add_player(self, player):
        # player = None
        # if isinstance(player, Player):
        #     player = player
        # else:
        #     player = Player(name, position, cost)
        self.players.append(player)
        self.formation[player.position.value] += 1

    def formatation_string(self):
        return "-".join(str(x) for x in self.formation)

    def verify(self):
        if len(self.players) != 11:
            return False

        salaries = 0.0
        for player in self.players:
            salaries = salaries + player.cost
        return (salaries <= SALARY_CAP)

    def calculate_score(self, start_year, start_month, start_day):
        start_day = datetime.date(start_year, start_month, start_day)
        days = [start_day + datetime.timedelta(days=i) for i in range(7)]

        score = 0

        for player in self.players:
            for day in days:
                try:
                    current_score = player_scores[player.position.name][player.team][player.name].get(day.strftime(
                        '%Y-%m-%dT00:00:00Z'))
                    if current_score is not None:
                        score += int(current_score)
                except Exception as e:
                    print (e)
                    return 0

        return score

    def __repr__(self):
        output = ""
        for player in self.players:
            output += "{}\n".format(player)
        return output


def fetch_players(player_lists, position, status):
    return [player_lists[position][i] for i in status], status


def select_players(player_lists, position, count, status=None):
    player_count = len(player_lists[position]) - 1
    if not status:
        status = [i for i in range(count)]
    else:
        for i in range(count - 1, -1, -1):
            if status[i] == player_count:
                status[i] = 0
            else:
                status[i] += 1
                # skip duplicates
                while len(status) != len(set(status)):
                    status[i] += 1
                break

    if sum(status) >= player_count * count:
        return None, status

    return fetch_players(player_lists, position, status)


    # Transform player lists
player_lists = {}

for position in data:
    for team in data[position]:
        for player, cost in data[position][team].items():
            player_list = player_lists.get(position, [])
            player_list.append(Player(player, position, cost, team))
            player_lists[position] = player_list


counter = -1
curr_players = []
status = [[] for i in range(5)]

while True:
    team_changed = False
    team = Team()
    counter += 1
    for p in Position:
        if team_changed and counter > 0:
            curr_players, _ = fetch_players(
                player_lists, p.name, status[p.value])
        else:
            curr_players, status[p.value] = select_players(
                player_lists, p.name, formation[p.value], status[p.value])

            if curr_players == None:
                # reset position to start
                curr_players, status[p.value] = select_players(
                    player_lists, p.name, formation[p.value])
            else:
                team_changed = True

        for player in curr_players:
            team.add_player(player)

    if not team_changed:
        break

    # print(team.verify())
    # print(team)
    # print(status)
    # print()

    if counter % 10000000 == 0:
        print(counter)

    if check_score(team):
        print(team)
# print(counter)

# while curr_players is not None:
#     counter += 1
#     curr_players, status = select_players(player_lists, "FB", 2, status)
#     print("{} : {} {}".format(curr_players, status, counter))

# team = Team()
# team.add_player("me", "CB", "4.5")
# team.add_player("me", "ST", "4.5")
# print(team.verify())

# print(team.formatation_string())

# team2 = Team()
# team2.add_player("me", "ST", "4.5")
# print(team)
# print(team2.verify())
