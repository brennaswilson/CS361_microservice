import json
import zmq
from datetime import datetime



def calculate_income(data):
    try:
        with open("shifts.json", "r") as file:
            shift_data = json.load(file)["shifts"]
    except FileNotFoundError:
         return {"error": "shifts.json not found"}

    if not shift_data:
         return {"error": "No data found in shifts.json"}
    
    wage = data["hourlyWage"]
    startDate = datetime.strptime(data["startDate"], "%Y-%m-%d")
    endDate = datetime.strptime(data["endDate"], "%Y-%m-%d")
    hours_worked = 0
    total_tips = 0
    total_wages = 0

    for shift in shift_data:
        shift_date = datetime.strptime(shift["date"], "%Y-%m-%d")
        if shift_date >= startDate and shift_date <= endDate:
            hours_worked += shift["hours"]
            total_tips += shift["credit"] + shift["cash_tips"]


    if hours_worked == 0:
        return {"error": "No shifts found in the specified date range."}
    
    total_wages = wage * hours_worked
    gross_earnings = total_wages + total_tips

    earnings = {
        "total_hours_worked": hours_worked,
        "total_tips": total_tips,
        "total_wages": total_wages,
        "gross_earnings": gross_earnings,
        "start_date": startDate.strftime("%Y-%m-%d"),
        "end_date": endDate.strftime("%Y-%m-%d"),
    }       

    return earnings
    


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv_json()
    print("Creating report for the client…")
    report = calculate_income(message)
    socket.send_json(report)
    



    
