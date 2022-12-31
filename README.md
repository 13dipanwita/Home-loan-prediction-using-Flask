# Home-loan-prediction-using-Flask
Home loan prediction using Flask, ML model building and pickling
Domain:
○ Finance and Banking.
Context:
Dream Housing Finance company deals in all home loans. They have presence
across all urban, semi urban and rural areas. Customers first apply for a home loan
after that company manually validates the customer eligibility for loan.
Company wants to automate the loan eligibility process based on customer detail
provided while filling the details online.
They need a web application where a user can access their website and register,
login, and enter the required details such as Gender, Marital Status, Education,
Number of Dependents, Income, Loan Amount, Credit History and others for checking
the eligibility for the home loan.
Project Objective:
1. To build a Python Flask ML application,
a. Where a user can get registered by entering the username and password
and login to the website and then enter their details to check whether they
are eligible for loan or not.
b. Where a business admin can fetch the registered user details and
generate insights out of it.
c. Build a classification model to predict whether a customer is eligible for
loan or not based on a given set of independent variable(s).
Steps:
Develop a ML application with following functionalities (The first 4 steps are already developed
during the TA session)
○ STEP-1: The application should have a homepage for customers to read some details
about the website and buttons for registering and logging in to the application.
○ STEP-2: The application should be able to register new customers in the database
dynamically in the db which can be used for authentication purposes.
■ This should take username and password and store the details in the user
database.
○ STEP-3: The application should be able to allow an existing customer to login to the
website using correct credentials.
■ Only a registered user with a correct password can be logged in.
○ STEP-4: Once the user has logged in, there should be an endpoint to check for loan
approval status. The user needs to enter the details to get the loan eligibility status.
○ STEP-5: Your application should have an option for logout. And if the user clicks on
logout, it will redirect to the login page. 
● BUSINESS INTERFACE
○ STEP-6: Your application should save the details entered by an user and the predicted
outcome in the DB (You can create a new table or use the same table).
○ STEP-7: Your application should have an endpoint to fetch the statistical summary of all
registered users for a business report.
○ STEP-8: Your application should have an endpoint to get a summary of the outcome.
Report what percentage of users got approved for the loan. 
