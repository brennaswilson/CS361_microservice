import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def main():
    print("\n///////////////////////////////////////////\n")
    print("Welcome to the earnings report generator.\n")
    print("///////////////////////////////////////////\n\n")
    print("This program will help you generate a report of your earnings.\n")

    while True:

        choice = input("Would you like to pull a report on your earnings?(y/n): ").strip().lower()

        if choice == "y":

            print("\nPlease enter the date range for your report and your hourly wage.")
            start_date = input("Start date (YYYY-MM-DD): ").strip() 
            end_date = input("End date (YYYY-MM-DD): ").strip()
            hourly_wage = input("Hourly wage: ").strip()
            hourly_wage = float(hourly_wage)

            with open("shifts.json", "r") as file:
                shift_data = json.load(file)

            shift_data['startDate'] = start_date
            shift_data['endDate'] = end_date
            shift_data['hourlyWage'] = hourly_wage
 
            with open('shifts.json', 'w') as file:
                json.dump(shift_data, file, indent=2)

            socket.send_string("Please create a report for the client…")
            print("Your report is being generated…\n")
            message = socket.recv_json()
            if "error" in message:
                print(f"Error: {message['error']}\n")
                continue
            else:
                print(format_message(message))
        elif choice == "n":
            print("Thank you for using the report generator.\n")
            break

def format_message(message):
    formatted_message = (
        f"Total hours worked: {message['total_hours_worked']}\n"
        f"Total cash tips: ${message['cash_tips']}\n"
        f"Total credit tips: ${message['credit_tips']}\n"
        f"Total tips: ${message['total_tips']}\n"
        f"Total wages: ${message['total_wages']}\n"
        f"Gross earnings: ${message['gross_earnings']}\n"
        f"Start date: {message['start_date']}\n"
        f"End date: {message['end_date']}\n"
    )
    return formatted_message
    

if __name__ == "__main__":
    main()
