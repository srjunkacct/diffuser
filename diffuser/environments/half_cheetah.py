import os
import numpy as np
from gymnasium import utils
from gymnasium.envs.mujoco import mujoco_env

class HalfCheetahFullObsEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        asset_path = os.path.join(
            os.path.dirname(__file__), 'assets/half_cheetah.xml')
        mujoco_env.MujocoEnv.__init__(self, asset_path, 5)
        utils.EzPickle.__init__(self)

    def step(self, action):
        xposbefore = self.sim.data.qpos[0]
        self.do_simulation(action, self.frame_skip)
        xposafter = self.sim.data.qpos[0]
        ob = self._get_obs()
        reward_ctrl = - 0.1 * np.square(action).sum()
        reward_run = (xposafter - xposbefore)/self.dt
        reward = reward_ctrl + reward_run
        done = False
        return ob, reward, done, dict(reward_run=reward_run, reward_ctrl=reward_ctrl)

    def _get_obs(self):
        return np.concatenate([
            # self.sim.data.qpos.flat[1:],
            self.sim.data.qpos.flat, #[1:],
            self.sim.data.qvel.flat,
        ])

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(low=-.1, high=.1, size=self.model.nq)
        qvel = self.init_qvel + self.np_random.randn(self.model.nv) * .1
        self.set_state(qpos, qvel)
        return self._get_obs()

    def viewer_setup(self):
        self.viewer.cam.distance = self.model.stat.extent * 0.5

    def set(self, state):
        qpos_dim = self.sim.data.qpos.size
        qpos = state[:qpos_dim]
        qvel = state[qpos_dim:]
        self.set_state(qpos, qvel)
        return self._get_obs()
