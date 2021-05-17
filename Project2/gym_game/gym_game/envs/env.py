import gym
from gym import spaces, error, utils
from gym.utils import seeding

N_TUBES = 3
N_COLORS = 2
H_TUBES = 3

DEFAULT_BOARD = [
    [2, 1, 2],
    [2, 1, 1],
    [0, 0, 0]
]

class BallSortEnv(gym.Env):
    def __init__(self, alpha=0.02):
        self.action_space = spaces.Tuple(
            (spaces.Discrete(N_TUBES), spaces.Discrete(N_TUBES)))
        self.observation_space = spaces.Box(
            low=0, high=N_COLORS, shape=(N_TUBES, H_TUBES), dtype=np.uint8)
        self.alpha = alpha
        self.reset()

        print(self.observation_space)

    def render(self, mode='human'):
        print(self.board)

    def step(self, action):
        done = True
        info = {}
        reward = 1

        return self.board, reward, done, info

    def reset(self):
        self.board = DEFAULT_BOARD
        return self.board

    def close(self):
        pass
