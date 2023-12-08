import numpy as np


class WindyGridworld:
    def __init__(self):
        self.width = 10
        self.height = 7
        self.wind = np.array([0, 0, 0, 1, 1, 1, 2, 2, 1, 0])
        self.start = (3, 0)  # Start at row 3, column 0
        self.goal = (3, 7)  # Goal at row 3, column 7
        self.state = self.start

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        i, j = self.state
        j = j + self.wind[i]  # Apply wind effect based on current row

        if action == 0:  # up
            i = max(i - 1, 0)
        elif action == 1:  # down
            i = min(i + 1, self.height - 1)
        elif action == 2:  # left
            j = max(j - 1, 0)
        elif action == 3:  # right
            j = min(j + 1, self.width - 1)

        self.state = (i, j)
        reward = -1 if self.state != self.goal else 0
        done = self.state == self.goal
        return self.state, reward, done

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) == self.state:
                    print('A', end=' ')
                elif (i, j) == self.start:
                    print('S', end=' ')
                elif (i, j) == self.goal:
                    print('G', end=' ')
                else:
                    print('.', end=' ')
            print('')


def choose_action(state, q_table, epsilon):
    if np.random.random() < epsilon:
        return np.random.randint(4)  # Choose a random action
    else:
        return np.argmax(q_table[state])  # Choose the best action based on Q-table


def update_q_table(q_table, state, action, reward, next_state, alpha, gamma):
    best_next_action = np.argmax(q_table[next_state])
    q_table[state + (action,)] += alpha * (
            reward + gamma * q_table[next_state + (best_next_action,)] - q_table[state + (action,)])


def train_windy_gridworld(episodes, alpha, gamma, epsilon):
    env = WindyGridworld()
    q_table = np.zeros((env.width, env.height, 4))

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            action = choose_action(state, q_table, epsilon)
            next_state, reward, done = env.step(action)
            update_q_table(q_table, state, action, reward, next_state, alpha, gamma)
            state = next_state

    return q_table


# Training the agent
q_table = train_windy_gridworld(1000, 0.1, 0.9, 0.1)


def choose_best_action(state, q_table):
    x, y = state
    action_values = q_table[x, y]
    best_action = np.argmax(action_values)
    return best_action


# Example of using the function
current_state = (5, 3)  # Assuming the agent is at position (5, 3)
best_action = choose_best_action(current_state, q_table)
print(f"The best action at state {current_state} is {best_action}")
