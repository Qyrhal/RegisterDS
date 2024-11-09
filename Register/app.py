from flask import Flask, render_template, redirect, url_for
from system import EmployeeScheduler
from typing import Dict, List

app = Flask(__name__)

def format_shift_data(schedule: Dict) -> List[List[List[str]]]:
    """
    Format the schedule data for template rendering
    Returns a 7x2 matrix (7 days, 2 shifts per day) of employee lists
    """
    formatted_data = []
    for day in range(7):
        day_shifts = []
        for shift in range(2):
            if day in schedule and shift in schedule[day]:
                employees = [emp.get_name() for emp in schedule[day][shift]]
                day_shifts.append(employees)
            else:
                day_shifts.append([])
        formatted_data.append(day_shifts)
    return formatted_data

@app.route('/populate')
def populate():
    try:
        scheduler = EmployeeScheduler()
        schedule = scheduler.calculate_shifts()
        formatted_data = format_shift_data(schedule)
        return render_template('index.html', schedule=formatted_data)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)