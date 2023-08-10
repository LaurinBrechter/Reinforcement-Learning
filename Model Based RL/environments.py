import numpy as np
import pandas as pd
import tensorflow_probability as tfp
from gym import spaces
from tensorflow_probability import distributions as tfd

class DS_DA():
    def __init__(self) -> None:
        self.action_space = spaces.Discrete(2)
        self.dynamics = [
            [
                [0.3,0.2,0.5],
                [0.7,0.2,0.1],
                [0.3,0.3,0.4]
            ],
            [
                [0.2,0.2,0.6],
                [0.1,0.9,0],
                [0.4,0.3,0.4]
            ]
        ]

        self.reward_dynamics = [tfd.Normal(1000, 200), tfd.Normal(1500, 200), tfd.Normal(1700, 200)]

    def step(self,state, action):
        
        s_prime = tfd.Categorical(probs=self.dynamics[action][state]).sample(1)
        reward = self.reward_dynamics[state].sample(1)

        return s_prime, reward


class CS_DA_deterministic():
    def __init__(self, lim=10) -> None:
        self.action_space = spaces.Discrete(3)
        self.state = np.array([0, 0, 0, 0], dtype=np.float32)
        self.demand = np.array([500, 200, 300, 400], dtype=np.float32)
        self.supplier = np.array([
            [500, 200, 300, 400], # quantity of product that the supplier will deliver
            [800, 500, 600, 700],
            [400, 100, 200, 300]
        ], dtype=np.float32)
        self.counter = 0
        self.lim=lim
    def step(self, action):
        self.counter += 1
        s_prime = self.state + self.supplier[action] - self.demand
        self.state = s_prime
        if self.counter == self.lim:

            s_prime = self.state + self.supplier[action] - self.demand
            self.state = s_prime
            # return s_prime, -np.sum(np.abs(self.state)), True
            return s_prime, -np.sum(np.abs(self.state)), True
        else:
            # return s_prime, - np.sum(np.abs(self.state)), False
            return s_prime, -np.sum(np.abs(self.supplier[action] - self.demand)), False


class BayesianGridEnv():
    def __init__(self, theta) -> None:
        self.grid = np.ones((3,4)) * -0.04
        self.grid[0,-1] = 1 # goal
        self.grid[1,-1] = -1 # penalty
        self.theta = theta
        self.action_space = [0,1,2,3] # up=0, down=1, left=2, right=3
        

    def reset(self):
        self.player_position = [-1,0]
    

    def _check_valid_actions(self):

        valid_actions = []
        if self.player_position[0] == 0:
            valid_actions.append(1)
        else:
            valid_actions.append(0)

        if self.player_position[1] == 0:
            valid_actions.append(3)
        
        if self.player_position[1] == None:
            valid_actions.append(2)





    def step(self, action): # up=0, down=1, left=2, right=3

        # next_state = self.player_position
        
        rand = np.random.rand()
        if action == "up":
            if self.player_position[0] != 0:
                if rand<self.theta:
                    self.player_position[0] -= 1
                else:
                    self.player_position[1]


        # elif action == "down":
        #     if self.player_position[0] != 9:
        #         self.player_position[0] += 1 
        # elif action == "left":
        #     if self.player_position[1] != 0:
        #         self.player_position[1] -= 1
        # elif action == "right":
        #     if self.player_position[1] != 9:
        #         self.player_position[1] += 1


        # reward = self.grid[tuple(next_state)]
        # done = True if self.player_position == [0,9] else False

        # return next_state, reward, done