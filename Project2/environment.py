import gym
import tube
import numpy as np


# ACTION SPACE - MOVE BALL FROM X TO Y 
# e.g. for 2 tubes (simple), can move from 1 to 1, 1 to 2, 2 to 1 or 2 to 2 -> [1,4]
# (ACTION / num of tubes) - 1 = FROM TUBE 
# ACTION % num of tubes = TO TUBE

# OBSERVATION SPACE/STATE - THE PUZZLE ITSELF
# e.g. [[1],[1,1,1]]

class Environment(gym.Env):
    state = tube.Game([])
    states = {}
    i = 0

    def __init__(self):
        self.action_space = gym.spaces.Discrete(4)  # num of tubes ^ num of tubes
        self.observation_space = tube.Game([])  # puzzle

    def step(self, action):
        state, reward = self.react(action)
        self.put_dict(state)
        done = state.finished()
        info = {}
        return state, reward, done, info

    def reset(self):
        self.state = tube.Game([[1], [1, 1, 1]])
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
        from_tube = action // 2
        to_tube = action % 2

        state = self.state
        valid = state.move_ball(from_tube, to_tube)

        reward = state.evaluate3(valid, to_tube)
        return state, reward
