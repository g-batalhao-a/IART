import gym
import tube
import numpy as np

# ACTION SPACE - MOVE BALL FROM X TO Y 
# e.g. for 2 tubes (simple), can move from 1 to 1, 1 to 2, 2 to 1 or 2 to 2 -> [1,4]
# (ACTION / num of tubes) - 1 = FROM TUBE 
# ACTION % num of tubes = TO TUBE

# OBSERVATION SPACE - THE PUZZLE ITSELF ()
# e.g. [[1],[1,1,1]]

class Environment(gym.Env):
    def __init__(self):
            self.action_space = gym.spaces.Discrete(4) #num of tubes ^ num of tubes
            self.observation_space = gym.spaces.Box(low=0, high=1, shape=(2,2), dtype=np.float16) # num of tubes 

    def step(self, action):
            state,reward = self.react()
                
            done = state.finished()
            info = {}
            return state, reward, done, info

    def reset(self):
            state = [[0,0,0,1],[0,1,1,1]]
            return state

    def render(self, mode='human', close=False):
        print()

    def react(action):
        from_tube = (action//2)-1
        to_tube = action%2

        state = tube.Game(self.state)
        state.move_ball(from_tube,to_tube)

        reward = state.evaluate()
        return state.to_list(),reward



