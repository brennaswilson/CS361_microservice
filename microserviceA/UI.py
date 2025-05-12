import zmq

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

            data = {
                "startDate": start_date,
                "endDate": end_date,
                "hourlyWage": hourly_wage
            }

            socket.send_json(data)
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
        f"Total tips: ${message['total_tips']}\n"
        f"Total wages: ${message['total_wages']}\n"
        f"Gross earnings: ${message['gross_earnings']}\n"
        f"Start date: {message['start_date']}\n"
        f"End date: {message['end_date']}\n"
    )
    return formatted_message
    

if __name__ == "__main__":
    main()
