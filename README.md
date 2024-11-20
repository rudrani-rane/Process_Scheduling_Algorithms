# **Process Scheduling Algorithms Web Application**

This mini basic web application implements several process scheduling algorithms, including First-Come-First-Serve (FCFS), Shortest Job First (SJF), Round Robin, and Priority Scheduling. 
It allows users to input process details such as arrival times, burst times, and (in some cases) priorities, and it calculates the scheduling results. 
The application also generates a Gantt chart that visually represents the execution order of processes.


## Features
### Four Scheduling Algorithms:
FCFS (First-Come-First-Serve)
SJF (Shortest Job First)
Round Robin
Priority Scheduling

### Process Input:
Users can enter the arrival times, burst times, and, where necessary, priorities and time quantum.

### Results:
Waiting time
Turnaround time
Gantt chart of processes

### User Interface:
A simple, responsive web interface with a modern design.
Forms for entering process details.
Real-time display of results and Gantt chart after form submission.


## Technologies Used
Backend: Python, Flask
Frontend: HTML, CSS, JavaScript
Gantt Chart: Dynamically generated using custom CSS and JavaScript
Package Manager: pip


## Project Structure
/process-scheduling-web-app
│
├── app.py                    # Flask backend logic
├── /templates
│   └── index.html            # Main frontend page
├── /static
│   ├── style.css             # Custom CSS styles
│   └── script.js             # JavaScript to handle form submissions and results
└── README.md                 # Project documentation


## Installation
Clone the repository: git clone <repository-url>
Navigate to the project directory: cd process-scheduling-web-app
Install required Python packages: pip install flask
Run the Flask application: python app.py
Access the web application: Open your browser and go to http://localhost:5000 to use the app.


## Group Members:
Rudrani Yogesh Rane 
Avani Atul Dongare 
Srushti Kangaonkar 
