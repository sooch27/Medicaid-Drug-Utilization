from flask import Flask, render_template
from data import get_top_drugs

app = Flask(__name__)

@app.route('/')
def index():
    results = get_top_drugs()
    # You don't need to check for state in the rows, as results is already a dictionary with state keys
    top_drugs = {}
    for state, rows in results.items():
        top_drugs[state] = rows[:10]

    return render_template('index.html', top_drugs=top_drugs)

if __name__ == '__main__':
    app.run(debug=True)
