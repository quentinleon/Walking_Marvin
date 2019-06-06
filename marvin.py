import gym
import structures
env = gym.make('Marvin-v0')

print("Action space info")
print(env.action_space)
print(env.action_space.high)
print(env.action_space.low)

print()
print("Observation space info")
print(env.observation_space)
print(env.observation_space.high)
print(env.observation_space.low)

for i_episode in range(5):
	observation = env.reset()
	t = 0
	while True: #t in range(100):
		t += 1
		env.render()
		action = env.action_space.sample()
		observation, reward, done, info = env.step(action)
		if done:
			print("Episode finished after {} timesteps".format(t+1))
			break
env.close()