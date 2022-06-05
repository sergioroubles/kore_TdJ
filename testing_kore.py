
from kaggle_environments.envs.kore_fleets.helpers import *
from random import randint

from kaggle_environments import make
env = make("kore_fleets", debug=True)
print(env.name, env.version)



rounds = 10

victories = 0
for i in range(rounds):
    env = make("kore_fleets", debug=True)
    players = ["eagle_mod.py", "carlos_expansive_miner.py"]
    result = env.run(players)
    score = {players[player_id] : info[0] for player_id, info in enumerate(result[-1][0]["observation"]["players"])}
    print(score)
    if score[players[0]] >= max(score.values()):
        victories +=1
    print(f"Round {1+i:>4}/{rounds} (Victories: {victories})")
print(f"Victories: {victories:>4}/{rounds} ({victories/rounds:.1%})")