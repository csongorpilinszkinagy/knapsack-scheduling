import logging

logging.basicConfig(level=logging.INFO)

def calculate_task_value(task, time_value):
    return (task['money_earned'] - task['money_spent']) + (task['time_earned'] - task['time_spent']) * time_value

def knapsack(tasks, max_time, initial_time_value=0):
    time_value = initial_time_value
    iterations = 100 # Adjust the number of iterations as needed

    for iteration in range(1, iterations + 1):
        for task in tasks:
            task['value'] = calculate_task_value(task, time_value)
        # Sort tasks based on the calculated task value
        tasks.sort(key=lambda task: task['value'], reverse=True)

        # Initialize the matrix for dynamic programming
        dp = [[0] * (max_time + 1) for _ in range(len(tasks) + 1)]

        # Populate the matrix using dynamic programming
        for i in range(1, len(tasks) + 1):
            for t in range(1, max_time + 1):
                if tasks[i - 1]['time_spent'] <= t:
                    dp[i][t] = max(dp[i - 1][t], dp[i - 1][t - tasks[i - 1]['time_spent']] + tasks[i - 1]['value'])
                else:
                    dp[i][t] = dp[i - 1][t]

        # Find the selected tasks
        selected_tasks = []
        i, t = len(tasks), max_time
        while i > 0 and t > 0:
            if dp[i][t] != dp[i - 1][t]:
                selected_tasks.append(tasks[i - 1])
                t -= tasks[i - 1]['time_spent']
            i -= 1

        # Calculate the average hourly rate of the chosen tasks
        value_created = sum([task['value'] for task in selected_tasks])
        time_spent = sum([task['time_spent'] for task in selected_tasks])
        average_hourly_rate = value_created / time_spent

        # Update the time value for the next iteration
        time_value = time_value * 0.9 + average_hourly_rate * 0.1

        # Log the chosen tasks for this iteration
        #logging.info(f"Iteration {iteration}: Time Value: {time_value:.0f}, Chosen Tasks: {[(task['name'], round(task['value'], 0)) for task in selected_tasks]}")

    return selected_tasks

# Longer test case
tasks = [
    {'name': 'Running', 'time_spent': 1, 'money_spent': 0, 'time_earned': 3, 'money_earned': 0},
    {'name': 'Work1', 'time_spent': 1, 'money_spent': 0, 'time_earned': 0, 'money_earned': 6000},
    {'name': 'Work2', 'time_spent': 1, 'money_spent': 0, 'time_earned': 0, 'money_earned': 8000},
    {'name': 'Work3', 'time_spent': 1, 'money_spent': 0, 'time_earned': 0, 'money_earned': 10000},
    {'name': 'Work4', 'time_spent': 1, 'money_spent': 0, 'time_earned': 0, 'money_earned': 12000},
    {'name': 'Work5', 'time_spent': 1, 'money_spent': 0, 'time_earned': 0, 'money_earned': 14000},
    {'name': 'Work6', 'time_spent': 1, 'money_spent': 0, 'time_earned': 0, 'money_earned': 16000},
    {'name': 'Invest', 'time_spent': 1, 'money_spent': 1000, 'time_earned': 0, 'money_earned': 10000},
    #{'name': 'Read', 'time_spent': 5, 'money_spent': 5000, 'time_earned': 100, 'money_earned': 0},
    # Add more tasks as needed
]

max_time_available = 6
result = knapsack(tasks, max_time_available)
print([task['name'] for task in result])