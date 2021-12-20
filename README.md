# AI-based Chatbot

## System Architecture
For this project 4 services are deployed and are shown below with their port numbers. Each service must be built and deployed individually in order for the chatbot to operate.
The Frontend and Chatbot is operated on the localhost

The Cinema Service and the Booking Service operates on their own individual docker container.

![alt text](https://github.com/morganmliang/ALchatbot/images/arch.png "System Architecture")

## Persisting Resources
Sqlite3 is used as the databases to store our data. There are three databases in total that are used for this project. 

*	Cinema database is stored inside its  cinema service docker container and contains information about the cinemas and its movies

*	Booking database is stored inside its booking service docker container and contains information about user tickets and timeslots

* User database is stored along with the chatbot locally. This contains information about the user. A unique user id is stored.

## User Information
Since user login and signup was not apart of the spec, the user id was hardcoded into the chatbot to identify the user. The user id is on line 70 of “./frontend/index.html” with user_id = 9.


## Stateless RESTful API
Our REST architecture stores not store any state about the client session on the server-side. Each API call from the client to the server contains al necessary information to understand the request.
An information about the application session state is kept entirely on the client which in this case is the chatbot. The chatbot stores and handles information of the user status (whether it is in a booking or cancellation state). The cinema and booking API remain stateless and all API calls from the chatbot client to the server APIs are all self-contained within the chat messages.

# Setup Instructions
Run the following commands in terminal:
```
run.sh
````
 * This will build and run two docker containers for the cinema service and the booking service. 

```
python ./chatbot/app3/demo-ui/v3/__init__.py
```
* Run the above command in a separate terminal
* This command will also run flask application of the chatbot on localhost:5000

```
cd ./frontend
python -m http.server 8000
```
* cd to the frontend folder and run the second command in a separate terminal
* This command will set up a local server to run the frontend on localhost:8000


<strong>To demo the chatbot enter 127.0.0.1:8000 to a browser. </strong>


# Chatbot Scenarios

The chatbot provides the following functionalities:

1.	Greetings

    a. Replies back to simple user greeting. (Eg. Hello, Hi.)
    
    b. Also replies to simple statements about user feelings. (Eg. “I am happy.”, “I am sad”)
  
2.	Cinema Information

    a.	Provides a list of cinemas that is current playing a specified movie
    
    b.	Provides detailed information of a specified information if needed
    
    c.	Provides snack information of a cinema
    
3.	Timeslots

    a.	Provides all the timeslots for a specified movie
    
    b.	Provided all the timeslots if no movie is specified for the user.
    
    c.	Each Timeslot details:
    
          i.	Day
          
          ii.	Start and End Times
          
          iii.	Cinema Name
          
          iv.	Seats Available
          
          v.	Seat Capacity
          
          vi.	Movie name
          
          vii.	Theatre type
          
4.	Movies

    a.	Shows movies that are currently showing for a specified cinema
    
    b.	If cinema is not specified will display all movies showing at each cinema
    
    c.	Search movies by name
    
    d.	Search movie by description
    
5.	Book a movie session
    
    a.	Provides a list of available timeslots that can be booked filtered for the user preferences
    
    b.	Available movie sessions are filtered according to:
    
          i.	Movie name
          
          ii.	Number of seats available for the number of people
          
          iii.	Cinema name
          
          iv.	Theatre type
          
          v.	Start times 
          
          vi.	Day 

      c.	Timeslots are also filtered such that no timeslots given are within the 2 hour time windows of previously booked tickets

      d.	If no timeslots are valid for the given time preferences, the chatbot will provide other timeslots within the same day that matches the user’s other preferences.

      e.	Users are required to provide a movie name and number of people for their reservation in order to start a new booking. This is to limit the number of options that is provided by the chatbot. 

      f.	User selects option from a list of timeslots provided by the chatbot

      g.	Chatbot asks for confirmation on selected timeslot

      h.	User enters confirmation

      <strong> User can cancel the booking any time during this booking process </strong>
      
      <strong>  User can still ask about cinema and movie information when in the process of booking a ticket </strong>
      


6.	Cancel a current movie reservation

    a.	Provides a list of purchased tickets filtered for the user preferences
    
    b.	User selects option from a list of tickets provided by the chatbot
    
    c.	Chatbot asks for confirmation on selected ticket
    
    d.	User enters confirmation


    <strong> User can stop the ticket cancellation any time during this cancellation process </strong> 
    
    <strong> User can only cancel or make one booking at any one time. The user must cancel or complete its current ticket cancellation process or current booking process to make a new cancellation or booking </strong>
    
    <strong>  User can still ask about cinema and movie information when in the process of canceling a ticket </strong>
    
    
    
    
    
    
    
    
    
