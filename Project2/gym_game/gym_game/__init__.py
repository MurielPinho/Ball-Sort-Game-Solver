from gym.envs.registration import register

register(
    id='ballsort-env-v0',
    entry_point='ballsort_game.envs:BallSortEnv',
)
