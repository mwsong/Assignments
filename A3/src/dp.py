import numpy as np
from src.racetrack import RaceTrack

class DynamicProgramming:
    def __init__(self, env, gamma=0.9, theta=1e-6, max_iterations=1000):
        """
        Initialize Dynamic Programming solver for RaceTrack environment.
        
        Args:
            env (RaceTrack): Instance of RaceTrack environment.
            gamma (float): Discount factor.
            theta (float): Convergence threshold.
            max_iterations (int): Maximum iterations for policy evaluation.
        """
        self.env = env
        self.gamma = gamma
        self.theta = theta
        self.max_iterations = max_iterations
        self.value_function = {}  # Dictionary to store state values
        self.policy = {}  # Dictionary to store policy (action per state)
        self.all_states = self._generate_all_states()
        self._initialize_policy()
        self._initialize_value_function()
    
    def _generate_all_states(self):
        """
        Generate all possible states in the environment.
        
        Returns:
            list: A list of tuples representing all valid (x, y, vx, vy) states.
        """
        states = []
        for x in range(self.env.course.shape[0]):
            for y in range(self.env.course.shape[1]):
                for vx in range(-self.env.MAX_VELOCITY, self.env.MAX_VELOCITY + 1):
                    for vy in range(-self.env.MAX_VELOCITY, self.env.MAX_VELOCITY + 1):
                        if self.env.course[x, y] != -1:  # Not a wall
                            states.append((x, y, vx, vy))
        return states

    def _initialize_policy(self):
        """
        Initialize a random policy for each state.
        """
        for state in self.all_states:
            self.policy[state] = np.random.choice(self.env.n_actions)

    def _initialize_value_function(self):
        """
        Initialize the value function to zero for all states.
        """
        for state in self.all_states:
            self.value_function[state] = 0.0
    
    def policy_evaluation(self):
        """
        Evaluate the current policy by iteratively updating the value function.
        
        This function should update self.value_function in place until convergence.
        
        Returns:
            None
        """
        for iteration in range(self.max_iterations):
            delta = 0 

            for state in self.all_states:
                old_value = self.value_function[state]
                action = self.policy[state]
                reward, next_state = self._simulate_action(state, action)
                bellman_value = reward + self.gamma * self.value_function[next_state]

                self.value_function[state] = bellman_value

                change = abs(old_value - bellman_value)
                delta = max(delta, change)

            if delta < self.theta: 
                break 


    def policy_improvement(self):
        """
        Improve the policy using the current value function.
        
        Returns:
            bool: True if the policy is stable (no changes), False otherwise.
        """
        policy_stable = True

        for state in self.all_states:
            action = self.policy[state]
            p_action_values = []
            for p_action in range(self.env.n_actions):
                reward, next_state = self._simulate_action(state, p_action)
                p_action_val = reward + self.gamma * self.value_function[next_state]
                p_action_values.append(p_action_val)
            best_action = p_action_values.index(max(p_action_values))

            self.policy[state] = best_action 
            if action != best_action:
                policy_stable = False

        return policy_stable

    
    def policy_iteration(self):
        """
        Perform Policy Iteration algorithm.
        
        This function should alternate between policy evaluation and policy improvement
        until convergence.
        
        Returns:
            None
        """
        for iteration in range(self.max_iterations):
            self.policy_evaluation()
            if self.policy_improvement():
                break
        
    
    def value_iteration(self):
        """
        Perform Value Iteration algorithm.
        
        This function should update the value function and extract the optimal policy.
        
        Returns:
            None
        """
        for iteration in range(self.max_iterations):
            delta = 0

            for state in self.all_states:
                old_value = self.value_function[state]
                p_action_values = []
                for p_action in range(self.env.n_actions):
                    reward, next_state = self._simulate_action(state, p_action)
                    p_action_val = reward + self.gamma * self.value_function[next_state]
                    p_action_values.append(p_action_val)
                best_value = max(p_action_values)

                self.value_function[state] = best_value
                change = abs(old_value - best_value)
                delta = max(delta, change)

            if delta < self.theta:
                break 

        for state in self.all_states:
            p_action_values = []
            for p_action in range(self.env.n_actions):
                reward, next_state = self._simulate_action(state, p_action)
                p_action_val = reward + self.gamma * self.value_function[next_state]
                p_action_values.append(p_action_val)

            self.policy[state] = p_action_values.index(max(p_action_values))
        pass
    
    def _simulate_action(self, state, action):
        """
        Simulate taking an action from a given state.
        
        Args:
            state (tuple): The current state (x, y, vx, vy).
            action (int): The action to take.
        
        Returns:
            tuple: (reward, new_state) where new_state is the next state tuple.
        """
        x, y, vx, vy = state
        self.env.position = np.array([x, y])
        self.env.velocity = np.array([vx, vy])
        reward = self.env.take_action(int(action))
        new_state = tuple(self.env.get_state())
        return reward, new_state
    
    def solve(self, method='policy_iteration'):
        """
        Solve the environment using the specified DP method.
        
        Args:
            method (str): 'policy_iteration' or 'value_iteration'.
        
        Returns:
            None
        """
        if method == 'policy_iteration':
            self.policy_iteration()
        elif method == 'value_iteration':
            self.value_iteration()
        else:
            raise ValueError("Invalid method. Choose 'policy_iteration' or 'value_iteration'")
    
    def print_policy(self):
        """
        Print the policy in a readable format.
        """
        for y in range(self.env.course.shape[1] - 1, -1, -1):
            row = ''
            for x in range(self.env.course.shape[0]):
                state = (x, y, 0, 0)  # Default velocity
                if state in self.policy:
                    row += str(self.policy[state]) + ' '
                else:
                    row += 'W ' if self.env.course[x, y] == -1 else '. '
            print(row)

# Test the implementation
if __name__ == "__main__":
    tiny_course = [
        "WWWWWW",
        "Woooo+",
        "Woooo+",
        "WooWWW",
        "WooWWW",
        "WooWWW",
        "WooWWW",
        "W--WWW",
    ]
    env = RaceTrack(tiny_course)  # Use the tiny race track for testing
    dp_solver = DynamicProgramming(env)
    dp_solver.solve(method='policy_iteration')  # Change to 'value_iteration' if needed
    dp_solver.print_policy()

    dp_solver = DynamicProgramming(env)
    dp_solver.solve(method='value_iteration')  
    dp_solver.print_policy()


