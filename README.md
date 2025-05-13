This microservice receives shift data and returns wage information based on a shifts.json file. Communication occurs over TCP using ZeroMQ in REQ-REP mode.

Requirements before you can use the microservice:
- pip install pyzmq

Requesting Data
- To send a request to the microservice, ensure the microservice is running, and use the ZeroMQ REQ socket and send a string:
      socket.send_string("Generate Report")

- The microservice listens on: tcp://localhost:5555

Receiving Data
- You can receive the wage data by using: 
      message = socket.recv_json()

- If configured successfully, you will receive a JSON object, which you can format, as shown below:

    earnings = {
        "total_hours_worked": hours_worked,
        "cash_tips": round(cash_tips, 2),
        "credit_tips": round(credit_tips, 2),
        "total_tips": round(total_tips,2),
        "total_wages": round(total_wages, 2),
        "gross_earnings": round(gross_earnings, 2),
        "start_date": startDate.strftime("%Y-%m-%d"),
        "end_date": endDate.strftime("%Y-%m-%d"),
    }          

- You may also receive an error message such as:
      Error: No shifts found in the specified date range.


![image](https://github.com/user-attachments/assets/b4d99e06-d576-4e19-87f3-a23379b47ca4)



