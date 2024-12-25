from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/check_deadlock', methods=['POST'])
def check_deadlock():
    max_need = list(map(int, request.form.getlist('max_need[]')))
    allocation = list(map(int, request.form.getlist('allocation[]')))
    available = int(request.form['available'])

    num_processes = len(max_need)
    need = [max_need[i] - allocation[i] for i in range(num_processes)]

    def is_safe(available, allocation, need):
        work = available
        finish = [False] * num_processes
        safe_sequence = []

        while len(safe_sequence) < num_processes:
            allocated = False
            for i in range(num_processes):
                if not finish[i] and need[i] <= work:
                    work += allocation[i]
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