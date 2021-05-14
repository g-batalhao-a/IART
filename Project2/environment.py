import gym
import tube
import numpy as np
import copy
from math import perm


# ACTION SPACE - MOVE BALL FROM X TO Y 
# e.g. for 2 tubes (simple), can move from 1 to 1, 1 to 2, 2 to 1 or 2 to 2 -> [1,4]
# (ACTION / num of tubes) - 1 = FROM TUBE 
# ACTION % num of tubes = TO TUBE

# OBSERVATION SPACE/STATE - THE PUZZLE ITSELF
# e.g. [[1],[1,1,1]] -> 

class Environment(gym.Env):
    states = {}
    i = 0

    def __init__(self, game):
        self.initial_state = copy.deepcopy(game)
        self.n_tubes = len(game)
        self.state = tube.Game(game)
        self.action_space = gym.spaces.Discrete(pow(len(game), 2))  # Combinacoes de N, 2 a 2 (N = numero de tubos)
        self.observation_space = tube.Game(game)  # puzzle

    def step(self, action):
        state, reward, from_tube, to_tube = self.react(action)
        self.put_dict(state)
        done = state.finished()
        info = {'from_tube': from_tube, 'to_tube': to_tube}
        self.state=state
        return state, reward, done, info

    def reset(self):
        self.state = tube.Game(copy.deepcopy(self.initial_state))
        self.put_dict(self.state)
        return self.state

    def put_dict(self, o):
        if o not in self.states:
            self.states[self.state] = self.i
            self.i += 1

    def render(self, mode='human', close=False):
        self.state.print()

    def get_index(self, o):
        return self.states[o]

    def react(self, action):
        from_tube = action // self.n_tubes
        to_tube = action % self.n_tubes

        if from_tube == to_tube:
            valid = False
        else:
            valid = self.state.move_ball(from_tube, to_tube)

        reward = self.state.evaluate3(valid, to_tube)
        return self.state, reward, from_tube, to_tube
