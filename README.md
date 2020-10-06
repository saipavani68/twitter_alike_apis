# CPSC 449 Web Back-End Engineering - Fall 2020
# Contributors: 
1. Sai Pavani Nagisetti (CWID: 888160793, Email: nagisettipavani@csu.fullerton.edu)
2. Rushabh Shah 

# Project description: 

This project involves creating two microservices: Users & Timelines for a microblogging service. It consists of two Flask applications connected to a  single SQLite Version 3 database.

The following are the steps to run the project:
1. Clone the github repository https://github.com/nagisettipavani/cpsc449
2. Install the pip package manager by running the following commands
    sudo apt update
    sudo apt install --yes python3-pip
   
3. Install Flask by:
    python3 -m pip install Flask python-dotenv
   
4. Run the following commands to install Foreman and HTTPie:
    sudo apt update
    sudo apt install --yes ruby-foreman httpie (However, we tested the apis using Postman)

5. Then cd into the project2 folder
    Run the following commands:
    flask init
    foreman start
    
Now, you will be to see that the two flask applications run on two different ports as configured in the Procfile.
Now the apis can be tested either using Postman(the one we followed) or using HTTPie(https://httpie.org/#examples).
   



