from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/process')
def process():
    resource_types = int(request.args.get('resource_types', 1))
    return render_template('process.html', resource_types=resource_types)

@app.route('/check_deadlock', methods=['POST'])
def check_deadlock():
    """
    Checks for deadlock in a system using the Banker's algorithm.
    This function retrieves resource allocation data from an HTTP request,
    calculates the need matrix, and determines if the system is in a safe state.
    If the system is in a safe state, it returns the safe sequence of processes.
    Otherwise, it returns an empty list indicating a deadlock.
    Returns:
        render_template: Renders the 'result.html' template with the result of the deadlock check.
    """
    
    resource_types = int(request.form.get('resource_types', 1))
    max_need = []
    allocation = []
    available = []

    for i in range(resource_types):
        max_need.append(list(map(int, request.form.getlist(f'max_need_{i}[]'))))
        allocation.append(list(map(int, request.form.getlist(f'allocation_{i}[]'))))
        available.append(int(request.form[f'available_{i}']))

    num_processes = len(max_need[0])
    need = [[max_need[i][j] - allocation[i][j] for j in range(num_processes)] for i in range(resource_types)]

    def is_safe(available, allocation, need):
        work = available[:]
        finish = [False] * num_processes
        safe_sequence = []

        while len(safe_sequence) < num_processes:
            allocated = False
            for i in range(num_processes):
                if not finish[i] and all(need[j][i] <= work[j] for j in range(resource_types)):
                    for j in range(resource_types):
                        work[j] += allocation[j][i]
                    finish[i] = True
                    safe_sequence.append(i)
                    allocated = True
            if not allocated:
                return False, []
        return True, safe_sequence

    safe, safe_sequence = is_safe(available, allocation, need)

    if safe:
        result = safe_sequence
    else:
        result = []

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)