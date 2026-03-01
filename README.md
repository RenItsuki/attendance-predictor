Student Attendance AI
Project Overview
Student Attendance AI is a desktop application built using Python and Tkinter. It implements Logistic Regression from scratch (without external machine learning libraries) to predict student attendance probability based on daily conditions.
The system can:
•	• Train on past attendance data
•	• Predict today's student attendance probability
•	• Display model accuracy
•	• Continuously update the dataset with actual values
Core Files
•	data_model.py – Contains the Logistic Regression implementation including:
  - Sigmoid function
  - Training logic (Gradient Descent)
  - Prediction logic
  - Accuracy calculation
•	Window.py – GUI built using Tkinter:
  - View last 20 days attendance
  - Train model (Partial or Full dataset)
  - Predict today's attendance
  - Update dataset dynamically
Features
•	• Custom Logistic Regression (manual gradient descent)
•	• 50,000 training iterations
•	• Partial or full dataset training option
•	• Real-time accuracy calculation
•	• Dark-themed GUI interface
Required Files
•	• STD.csv – Full dataset
•	• STD10.csv – Last 20 days dataset
How to Run
1. Ensure Python 3 is installed.
2. Keep all project files in the same directory.
3. Run the application using the command:
   python Window.py
Input Parameters
•	• Precipitation chance (%)
•	• Exam (Yes/No)
•	• Priority (Low/Moderate/High)
•	• Practical (Yes/No)
•	• Day of the week
Built With
•	• Python
•	• Tkinter
•	• CSV
•	• Threading
•	• Custom Logistic Regression
