
from .token import WIT_TOKEN
import requests
import json
import copy
import sqlite3 as sql
from datetime import datetime
from datetime import date
from datetime import timedelta

DATABASE =  'C:\\Users\morga\OneDrive\Desktop\COMP9322\Assignment2\chatbot\database.db'
#DATABASE = "/service/database.db"

from .cinemaAPI import *
from .bookingAPI import *
# from .cinemaAPI import get_all_cinemas, movies_showing
# from .cinemaAPI import get_cinema_info

def wit(message, userName):
    ans = ''

    # try:
    user_info = get_user_status(userName)

    query = requests.get('https://api.wit.ai/message?v=20211115&q={}'.format(message), 
                            headers={'Authorization': WIT_TOKEN})

    result = query.json()
    print(result)

    #If no intent found to display confusion message
    if(result['intents']):
        intent = result['intents'][0]['name']
        print(intent)

        #Greetings/Feelings Intents
        if (intent == 'greeting'):
            ans = "Hello! How may I help you today?"
            return ans
        elif (intent == "greeting_with_status_question"):
            ans = "I am feeling amazing because I am a yellow chicklet."
            return ans

        elif(intent == "feeling_statement"):
            if (len(result['traits']) !=0):
                if((len(result['traits']['wit$sentiment']) !=0)):
                    if(result['traits']['wit$sentiment'][0]['value'] == "negative"):
                        ans = "Don't feel down. You are awesome and cool!"
                    elif(result['traits']['wit$sentiment'][0]['value'] == "positive"):
                        ans = "You should feel good because You are awesome and cool!"
                    else:
                        ans = "Do you want to hear a joke then. Why did the nut say to the other nut that it was chasing? I am cashew!!!"
                else:
                    ans = "I don't understand these humnan feelings. I am only a chicklet."
            else:
                ans = "I don't understand these human feelings. I am only a chicklet."
            return ans

        #Cinema Info Intents
        elif (intent == 'show_all_timeslots'):

            #No entities at all
            if(result['entities']):

                #Movie name is not detected
                if ('movie_name:movie_name' in result['entities']):
                    m_name = result['entities']['movie_name:movie_name'][0]['body']
                    movie_slots = get_timeslots_info(m_name)


                    #Movie name is invalid or cannot be found
                    if(len(movie_slots) == 0):
                        ans = "The movie you are asked about is a movie that is currently not showing in any cinema. I will instead give you all timeslots for you to see.\n\n"
                        timeslots = get_all_timeslots()

                        for i,slot in enumerate(list(timeslots)):
                            slot_num = 1 + i
                            ans +="Timeslot {}: {} time: {}-{} movie: {} cinema: {} theatre_type: {}\
                                 avail_seats: {} seat_capacity: {}\n\n".format(slot_num, slot['day'], 
                                                                                slot['start_time'], 
                                                                                slot["end_time"], 
                                                                                slot['movie_name'] ,
                                                                                slot['cinema_name'],
                                                                                slot['theatre_type'], 
                                                                                slot['avail_seats'],
                                                                                slot['max_seats'])

                        return ans

                    ans = "{} has the following timeslots:\n\n".format(m_name)
                    for i,slot in enumerate(list(movie_slots)):
                        slot_num = 1 + i
                        ans +="Timeslot {}: {} time: {}-{} movie: {} cinema: {} theatre_type: {}\
                                avail_seats: {} seat_capacity: {}\n\n".format(slot_num, slot['day'], 
                                                                            slot['start_time'], 
                                                                            slot["end_time"], 
                                                                            slot['movie_name'] ,
                                                                            slot['cinema_name'],
                                                                            slot['theatre_type'], 
                                                                            slot['avail_seats'],
                                                                            slot['max_seats'])
                
                
                else:                                                                                                                        
                    timeslots = get_all_timeslots()
                    ans = "Here are all the timeslots currently for all movies.\n\n"
                        
                    for i,slot in enumerate(list(timeslots)):
                        slot_num = 1 + i
                        ans +="Timeslot {}: {} time: {}-{} movie: {} cinema: {} theatre_type: {}\
                                avail_seats: {} seat_capacity: {}\n\n".format(slot_num, slot['day'], 
                                                                                slot['start_time'], 
                                                                                slot["end_time"], 
                                                                                slot['movie_name'] ,
                                                                                slot['cinema_name'],
                                                                                slot['theatre_type'], 
                                                                                slot['avail_seats'],
                                                                                slot['max_seats'])
            else:
                ans = "Here are all the timeslots currently for all movies.\n\n"
                timeslots = get_all_timeslots()
                for i,slot in enumerate(list(timeslots)):
                    slot_num = 1 + i
                    ans +="Timeslot {}: {} time: {}-{} movie: {} cinema: {} theatre_type: {}\
                            avail_seats: {} seat_capacity: {}\n\n".format(slot_num, slot['day'], 
                                                                            slot['start_time'], 
                                                                            slot["end_time"], 
                                                                            slot['movie_name'] ,
                                                                            slot['cinema_name'],
                                                                            slot['theatre_type'], 
                                                                            slot['avail_seats'],
                                                                            slot['max_seats'])
            
            
            return ans


        elif (intent == 'show_all_cinemas'):
            ans = get_all_cinemas()
            return ans

        #Show movies that are currently for a defined cinema or all cinemas
        elif (intent == 'movies_showing'):
            if(result['entities']):
                c_name = result['entities']['cinema_name:cinema_name'][0]['body']
            else:
                c_name = ""

            ans = movies_showing(c_name)

            print(ans)
            return ans
        
        #Show all snacks for a defined cinema or all cinemas
        elif (intent == 'snack_information'):
            print(result)
            print("c_name")

            if(result['entities']):
                c_name = result['entities']['cinema_name:cinema_name'][0]['body']
            else:
                c_name = ""
            ans = snack_info(c_name)

            if(ans == ""):
                ans = "The cinema yougiv are asking for is not valid cinema. Please check you cinema name again."
            return ans

        #Show cinemas that are showing the defined movie
        elif (intent == 'search_movies'):
            m_name = result['entities']['movie_name:movie_name'][0]['body']
            print(m_name)
            ans = search_movie(m_name)

            if(ans == ""):
                ans = "No movies can be found wth the following movie name. Please check you cinema name again."

            return ans  
        
        #Show more information about a cinema
        elif (intent == 'show_detailed_cinema'):
            cinema_name = result['entities']['cinema_name:cinema_name'][0]['body']

            ans = get_cinema_info(cinema_name)

            if(ans == ""):
                ans = "The cinema is are asking for is not valid cinema. Please check you cinema name again."

            return ans    

        #Search for movies with a defined description
        elif (intent == 'search_description'):
            description_string = result['entities']['description_string:description_string'][0]['body']
            ans = search_description(description_string)



            if(ans == ""):
                ans = "No movies can be found wth the following description. Please check you description again."

            return ans   


        #If current in the middle of a booking session
        #It cannot start deleting one of its tickets AND it cannot try booking another session
        if(user_info['Status'] == "booking"):


            if(intent == "wit$confirmation"):

                b_list = str(user_info['b_list']).split(",")

                if(len(b_list) != 1):
                    ans = "This is not an valid option."
                    return ans

                slot_id = b_list[0]
                people = user_info['people']

                #Add booking to ticket database and also update the available seats 
                slot = make_booking(slot_id, userName, people)
                ans = "You have now booked for this session!\n"
                ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {} tickets: {}\n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'], user_info['people'])
                ans += "What else can I help you with.\n"
                reset_user_info(userName)
                return ans

            #User selects an option
            elif(intent == "wit$select_item"):
                print("in selection wit")
                b_list = str(user_info['b_list']).split(",")
                opt = int(result['entities']['option_number:option_number'][0]['body'])
                #Check if number input is valid
                print(opt)
                if (opt > len(b_list) or opt <= 0):
                    ans = "Number selected is not a option. Please select again."
                    return ans
                else:
                    id = opt - 1
                    timeslot_id = b_list[id] 

                    print(timeslot_id)
                    ans = "You have now selected the following session to book. Type confirm to confirm this booking or cancel to cancel this booking.\n"
                    slot = get_timeslot_details(timeslot_id)
                    ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {}\n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])
                    update_blist_info(str(timeslot_id), userName)
                    return ans
            elif(intent == "wit$cancel"):
                ans = "This booking has now been cancelled and no tickets were purchased. What else can I help you with?"
                reset_user_info(userName)
                return ans
            elif(intent =='start_booking' or intent =='start_delete'):
                ans = "You cannot delete another ticket or book another ticket since you are currently in the middle of a movie booking. To exit this current booking type cancel."
                return ans

            else:
                

                ans = "I do not understand what you are asking. Ask me in another way. To exit this booking type cancel."
                return ans

        #if the user is currently cancelling a ticket 
        elif(user_info['Status'] == "canceling"):
      
            if(intent == "wit$confirmation"):
                b_list = str(user_info['b_list']).split(",")
                
                if(len(b_list) != 1):
                    ans = "This is not an valid option."
                    return ans


                slot_id = b_list[0]

                
                #Delete ticket at the given timeslot. Add back the number of people on the ticket to the timeslot
                slot = delete_ticket(userName, slot_id)
                ans = "You have now cancelled the following ticket:\n"
                ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {}\n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])
                ans += "What else can I help you with.\n"
                reset_user_info(userName)
                return ans

            #User selects an option
            if(intent == "wit$select_item"):
                b_list = str(user_info['b_list']).split(",")
                opt = int(result['entities']['option_number:option_number'][0]['body'])
                if (opt > len(b_list) or opt <= 0):
                    ans = "Number selected is not a option. Please select again."
                    return ans
                else:
                    id = opt - 1
                    timeslot_id = b_list[id] 

                    print(timeslot_id)
                    ans = "You have now selected the following ticket to delete. Type confirm to confirm this ticket cancellation or cancel to keep these tickets and exit this process.\n"
                    slot = get_timeslot_details(timeslot_id)
                    ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {}\n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])
                    update_blist_info(str(timeslot_id), userName)
                    return ans
            
            elif(intent == "wit$cancel"):
                ans = "The tickets have not been deleted and are now still booked for you. What else can I help you with today."
                reset_user_info(userName)
                return ans
            elif(intent =='start_booking' or intent =='start_delete'):
                ans = "You cannot delete another ticket or book another ticket since you are currently in the middle of cancelling a movie ticket. To exit this current ticket cancellation process type cancel.\n"
                return ans
            else:
                

                ans = "I do not understand what you are asking. To keep your current tickets and exit this process, type cancel."
                return ans

        


        #Start booking sequence
        #Check if booking details are given. Find information in the given order: Movie name, number of people, day and start time.
        #Extra information could include cinema name, theatre type, 
        #With
        elif(intent =='start_booking'):
            
            #start_booking(user_info)
            user_info["Status"] = "booking"


            result = update_user_info(user_info,result,userName)

            if(result != True):
                ans = "The time you have asked about is outside cinema times or is not clear. Please make a new booking with clearer time."
                reset_user_info(userName)
                return ans
                
            
            #Must have movie name and number of people entered before calling api
            if (user_info['m_name'] == None):
                ans = "A valid movie name is not found in your booking. Please include or correct your movie name and please try again."
                reset_user_info(userName)
                return ans
            if(user_info['people'] == None):
                ans = "A valid number of people is not found in your booking. Please include or correct the number of people for this booking and try again."
                reset_user_info(userName)
                return ans
                    
            print(user_info)
            #Get timeslots with matching movie and number of people
            #Also will not return timeslots that the user has already booked in - taken from the API
            slots = get_movie_people_times(user_info['m_name'], user_info['people'], userName)

            print("print the slots")
            print(slots)

            if (len(slots) == 0):
                ans = "There is no timeslots available for {} with {} available seats. Change your preferences and start a new booking.\n".format(user_info['m_name'],user_info['people'])
                reset_user_info(userName)
                return ans

            #Filter timeslots according to user preferences
            ans = filter_slots(user_info,slots, userName)

        #Start ticket cancellation process
        elif(intent == "start_delete"):

            # if (user_info["Status"] != "normal"):
            #     raise ValueError('The current state is not normal. There is a database error.')

            #Get all current tickets
            slots = get_current_tickets(userName)


            if (len(slots) == 0):
                ans = "You have no tickets currently to delete.\n"
                reset_user_info(userName)
                return ans


            user_info["Status"] = "canceling"

            #Extra information is given, filter tickets according to user preferences
            if (len(result['entities']) !=0):
                result = update_user_info(user_info, result, userName)

                if(result != True):
                    ans = "The time you have asked about is outside cinema times or is not clear. Please make a new ticket cancellation with clearer time."
                    reset_user_info(userName)
                    return ans
                
                ans = filter_tickets(user_info,slots, userName)
                return ans

            #If no ticket filters update the user status only
            else:
                update_status(user_info["Status"],userName)

                #Print out the results for the user and also update the ticket list that the user can select from if there is valid tickets
                ans = get_valid_tickets(slots, userName)
                return ans

            return ans
        else:
            ans = "I do not understand what you are asking. Ask me in another way please."
    else:
        
        #It in booking and intent is not found but user enters only a number assume it is a select option
        if(user_info['Status'] == "booking"):
            if(result['text'].isnumeric()):
                print("intent is not found")
                b_list = str(user_info['b_list']).split(",")
                opt = int(result['text'])
                #Check if number input is valid
                print(opt)
                if (opt > len(b_list) or opt <= 0):
                    ans = "Number selected is not a option. Please select again."
                    return ans
                else:
                    id = opt - 1
                    timeslot_id = b_list[id] 

                    print(timeslot_id)
                    ans = "You have now selected the following session to booking. Type confirm to confirm this booking and purchase these tickets or type cancel to cancel this booking.\n"
                    slot = get_timeslot_details(timeslot_id)
                    ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {}\n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])
                    update_blist_info(str(timeslot_id), userName)
                    return ans

        #It in canceling and intent is not found but user enters only a number assume it is a select option
        if(user_info['Status'] == "canceling"):
            if(result['text'].isnumeric()):

                b_list = str(user_info['b_list']).split(",")
                opt = int(result['text'])
                #Check if number input is valid
                print(opt)
                if (opt > len(b_list) or opt <= 0):
                    ans = "Number selected is not a option. Please select again."
                    return ans
                else:
                    id = opt - 1
                    timeslot_id = b_list[id] 

                    print(timeslot_id)
                    ans = "You have now selected the following session to delete. Type confirm to confirm this ticket cancellation or type cancel to keep these tickets and exit this process.\n"
                    slot = get_timeslot_details(timeslot_id)
                    ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {}\n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])
                    update_blist_info(str(timeslot_id), userName)
                    return ans


        ans = "I do not understand what you are asking. Ask me another question."
    # except:
    #     reset_user_info(userName)
    #     ans = "An error occurred. Please restart your enquiry."
    

    #ans = "I don't understand you message {}. Please try again.".format(userName)
    return ans

#def update_user_info(status,c_name, t_type, s_time,day,e_time,people,m_name, user_id):
def update_status(status, user_id):
    update_com = "UPDATE Users SET Status=? WHERE user_id=?"
    update_db(update_com, (status,str(user_id)))

def update_user_info(user_info, result, user_id):
    

    if (len(result['entities']) !=0):
        ans = "Lets make this booking"

        if('movie_name:movie_name' in result['entities']):
            user_info['m_name'] = result['entities']['movie_name:movie_name'][0]['body']

        if('num_people:num_people' in result['entities']):
            user_info['people'] = result['entities']['num_people:num_people'][0]['body']

        if('time_hour:time_hour' in result['entities']):
            hour_str = result['entities']['time_hour:time_hour'][0]['body']
            print(hour_str)

            hour_str = hour_str.replace(" ", "").lower()
            print(hour_str)
            #If 12 hour time include am/pm
            if( "am" in hour_str or "pm" in hour_str):
                print("Here is time")
                print(hour_str)
                #If time includes minutes
                if(":" in hour_str):
                    time = datetime.strptime(hour_str, '%I:%M%p')
                    if(check_time(time) == False):
                        return False
                    s_hour = time.strftime("%H:%M")
                #Else convert to 24 hour time
                else:
                    time = datetime.strptime(hour_str, '%I%p')
                    print(time.time())
                    print(type(time.time()))
                    if(check_time(time.time()) == False):
                        return False
                    s_hour = time.strftime("%H:%M")
            #If 24 hour time
            else:
                if(":" in hour_str):
                    time = datetime.strptime(hour_str, '%H:%M')
                    if(check_time(time.time()) == False):
                        return False
                    s_hour = time.strftime("%H:%M")
                else:
                    s_hour = convertHourString(hour_str)
                    if(s_hour == None):
                        return False

                    s_hour += ":00"

            user_info['start_time'] = s_hour

        if('time_day:time_day' in result['entities']):
            user_info['day'] = convertDay(result['entities']['time_day:time_day'][0]['body'])

        if("wit$datetime:datetime" in result['entities']):
            print(result)
            if ('time_day:time_day' not in result['entities'] and 'time_hour:time_hour' not in result['entities']):
                dateTimestr = result['entities']['wit$datetime:datetime'][0]['value']
                wording = result['entities']['wit$datetime:datetime'][0]['body']
                print(result)
                date_str = datetime.fromisoformat(dateTimestr)
                #If there is no day string use today day
                if(has_letters(wording) == False):
                    today = date.today()
                    day = getDayString(today.weekday())
                #If has day get the day string
                else:
                    day = getDayString(date_str.weekday())

                print()
                print(date_str)
                print(day)

                user_info['day'] = day

                #Check first if it has a time in string, then check time
                if(has_numbers(wording) == True):
                    print("It goes here")
                    time_str = date_str.time()
                    if(check_time(time_str) == False):
                        return False
                    time = date_str.strftime("%H:%M")
                    user_info['start_time'] = time
                    
                    #Check if is between cinema times
                    
                
                print(user_info)
                
                    
    

        if('cinema_name:cinema_name' in result['entities']):
            user_info['cinema_name'] = result['entities']['cinema_name:cinema_name'][0]['body']
        if('theatre:theatre' in result['entities']):

            user_info['theatre_type'] = result['entities']['theatre:theatre'][0]['body']

            #Remove all spaces and remove all words of theatre in the word
            user_info['theatre_type'] = user_info['theatre_type'].replace(" ", "").replace("theatre", "")

            #Take only the first three letter and in lower case
            user_info['theatre_type'] = (user_info['theatre_type'][0:3]).lower()

            print(user_info['theatre_type'])

    print("here now")
    print(user_info)

    update_com = "UPDATE Users SET Status=?, cinema_name=?, theatre_type=?, start_time=?, day=?, end_time=?, people=?, m_name=? WHERE user_id=?"
    update_db(update_com, (user_info['Status'], user_info['cinema_name'], user_info['theatre_type'], 
                            user_info['start_time'],user_info['day'], user_info['end_time'],user_info['people']
                            ,user_info['m_name'], str(user_id)))
    
    return True

def reset_user_info(user_id):
    update_com = "UPDATE Users SET Status='normal', cinema_name=null, theatre_type=null, start_time=null, day=null, end_time=null, people=null, m_name=null, b_list=null WHERE user_id=?"
    update_db(update_com, (str(user_id),))

def update_blist_info(b_list, user_id):
    update_com = "UPDATE Users SET b_list=? WHERE user_id=?"
    update_db(update_com, ((b_list),user_id))


def get_user_status(userName):
    user_t = query_db('SELECT * FROM Users WHERE user_id=?', (str(userName),))
    user_info = {}
    user_info['Status'] = user_t['Status']
    user_info['user_id'] = user_t['user_id']
    user_info['cinema_name'] = user_t['cinema_name']
    user_info['theatre_type'] = user_t['theatre_type']
    user_info['start_time'] = user_t['start_time']
    user_info['end_time'] = user_t['end_time']
    user_info['day'] = user_t['day']
    user_info['people'] = user_t['people']
    user_info['m_name'] = user_t['m_name']
    user_info['b_list'] = user_t['b_list']

    return user_info



def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchone()
    cur.close()
    return rv
    #return (rv[0] if rv else None) if one else rv

def insert_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()

def update_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()


def get_db():
    db =  sql.connect(DATABASE)
    db.row_factory = sql.Row
    return db

def filter_tickets(user_info,slots, userName):
    if(user_info['m_name'] != None):

        for t_slots in list(slots):

            if(("movie_name",user_info['m_name']) not in t_slots.items()):
                slots.remove(t_slots)

        if(len(slots)== 0):
            reset_user_info(userName)
            ans = "There is no available tickets to delete suitable for your movie preferences. Please change your movie selection and try again."
            return ans
    

    # if(user_info['people'] != None):

    #     for t_slots in list(slots):
    #         if(("people",user_info['people']) not in t_slots.items()):
    #             slots.remove(t_slots)

    #     if(len(slots)== 0):
    #         reset_user_info(userName)
    #         ans = "There is no available tickets to delete suitable for your ticket preferences. Please change your ticket selection."
    #         return ans
    
    if(user_info['cinema_name'] != None):
        
        # cinema_list = get_all_cinemas.split('\n')[1:]
        # print("this is cinema_list")
        # print(cinema_list)

        for t_slots in list(slots):
            if(("cinema_name",user_info['cinema_name']) not in t_slots.items()):
                slots.remove(t_slots)

        if(len(slots)== 0):
            reset_user_info(userName)
            ans = "There is no available tickets to delete suitable for your cinema preferences. Please change your cinema selection and try again."
            return ans
    


    if(user_info['theatre_type'] != None):
        for t_slots in list(slots):
            if(("theatre_type",user_info['theatre_type']) not in t_slots.items()):
                slots.remove(t_slots)

        if(len(slots)== 0):
            reset_user_info(userName)
            ans = "There is no available tickets to delete suitable for your theatre type. Please change your theatre_type and try again."
            return ans

    if(user_info['day'] != None):
        for t_slots in list(slots):
            if(("day",user_info['day']) not in t_slots.items()):
                slots.remove(t_slots)
        if(len(slots)== 0):
            reset_user_info(userName)
            ans = "There is no tickets to delete suitable for this day. Please choose an another day and try again."
            return ans

    if(user_info['start_time'] != None):
        new_ids = []
        keep_day_slots = []
        for index, t_slots in enumerate(list(slots)):
            if(("start_time",user_info['start_time']) not in t_slots.items()):
                slots.remove(t_slots)
                keep_day_slots.append(t_slots)
                print(slots)


        if(len(slots) == 0):

            if(len(keep_day_slots) > 1):

                t_ids = []
                ans = "There are no tickets to delete that matches your movie time. However below are purchased movie tickets that are the closest to your preferred time.  Type the option number you want to cancel OR type cancel to keep these tickets and exit this process.\n\n"
                for i, slot in enumerate(list(keep_day_slots)):
                    o_num = i+1

                    #Order in t_ids is important as the number that user selects will be the index of the timeslot id chosen
                    new_ids.append(str(slot['timeslot_id']))
                    ans += "Option {}: {} time: {}-{} movie: {} cinema: {} theatre_type: {} \n\n".format(o_num,slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])

                b_list = ",".join(new_ids)
                update_blist_info(b_list, userName)
                return ans
            #If there is only only only ticket that fits the user preferences
            elif(len(keep_day_slots) == 1):
                slot = keep_day_slots[0] 
                ans = "There are no tickets to delete that matches your movie time. However below are is one movie ticket that is closest to your movie time. Type confirm to delete this ticket OR type cancel to keep this ticket and exit this process.\n\n"
                ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {} \n\n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])

                
                update_blist_info(str(slot['timeslot_id']), userName)
                return ans
            #No slots available
            else:
                reset_user_info(userName)
                ans = "There is no tickets to delete with your given preferences.\n"
                return ans
    
    t_ids = []
    #If there are multiple tickets that fit the user preferences
    if(len(slots) > 1):

        ans = "There are {} booked movie sessions that matches your preferences. Type the option number you want to remove from your current tickets or type cancel to keep these tickets and exit this process:\n\n".format(len(slots))
        for i, slot in enumerate(list(slots)):
            o_num = i+1

            #Order in t_ids is important as the number that user selects will be the index of the timeslot id chosen
            t_ids.append(str(slot['timeslot_id']))
            ans += "Option {}: {} time: {}-{} movie: {} cinema: {} theatre_type: {} \n\n".format(o_num,slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])

        b_list = ",".join(t_ids)
        update_blist_info(b_list, userName)
        return ans
    #If there is only only only ticket that fits the user preferences
    elif(len(slots) == 1):
        slot = slots[0] 
        ans = "There is one booked movie session that matches your preferences. Type confirm to remove this session from you current tickets OR type cancel to keep this ticket exit this process.\n\n"
        ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {} \n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])
        
        update_blist_info(str(slot['timeslot_id']), userName)
        return ans
    #No slots available
    else:
        reset_user_info(userName)
        ans = "There is no booked movie sessions with your given preferences. Change your ticket preferences and try again.\n"
        return ans

    return ans

def get_valid_tickets(slots, userName):
    ans = ""
    t_ids = []
    #If there are multiple tickets that fit the user preferences
    if(len(slots) > 1):

        ans = "There are {} booked movie sessions that matches your preferences. Type the option number you want to remove from your current tickets or type cancel to keep these tickets and exit this process:\n\n".format(len(slots))
        for i, slot in enumerate(list(slots)):
            o_num = i+1
            #Order in t_ids is important as the number that user selects will be the index of the timeslot id chosen
            t_ids.append(str(slot['timeslot_id']))
            ans += "Option {}: {} time: {}-{} movie: {} cinema: {} theatre_type: {} \n\n".format(o_num,slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])

        b_list = ",".join(t_ids)
        update_blist_info(b_list, userName)
        return ans
    #If there is only only only ticket that fits the user preferences
    elif(len(slots) == 1):
        slot = slots[0] 
        ans = "There is one booked movie session that matches your preferences. Type confirm to remove this session from you current tickets OR type cancel to keep this ticket exit this process.\n\n"
        ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {} \n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'])
        
        update_blist_info(str(slot['timeslot_id']), userName)
        return ans
    #No slots available
    else:
        reset_user_info(userName)
        ans = "There is no booked movie sessions with your given preferences. Change your ticket preferences and try again.\n"
        return ans

    return ans

def filter_slots(user_info, slots, userName):

    if(user_info['cinema_name'] != None):
        cinema_list = get_all_cinemas().split('\n')[1:]
        print("this is cinema_list")
        if(user_info['cinema_name'].lower() in cinema_list):

            for t_slots in list(slots):
                if(("cinema_name",user_info['cinema_name']) not in t_slots.items()):
                    slots.remove(t_slots)
        elif( "cinema" != user_info['cinema_name'].lower()):
            reset_user_info(userName)
            ans = "There is no available timeslots suitable for your cinema name. Please change your cinema selection and start a new booking"
            return ans

        if(len(slots)== 0):
            reset_user_info(userName)
            ans = "There is no available timeslots suitable for your cinema name. Please change your cinema selection and start a new booking"
            return ans
    if(user_info['theatre_type'] != None):
        for t_slots in list(slots):
            if(("theatre_type",user_info['theatre_type']) not in t_slots.items()):
                slots.remove(t_slots)

        if(len(slots)== 0):
            reset_user_info(userName)
            ans = "There is no available timeslots suitable for your theatre type. Please change your theatre_type and start a new booking."
            return ans

    if(user_info['day'] != None):
        new_slots = slots

        for t_slots in list(slots):
            if(("day",user_info['day']) not in t_slots.items()):
                
                slots.remove(t_slots)

        if(len(slots)== 0):
            reset_user_info(userName)
            ans = "There is no timeslots for this day. Please choose an another day to visit."
            return ans

    if(user_info['start_time'] != None):
        new_ids = []
        keep_day_slots = []
        for index, t_slots in enumerate(list(slots)):
            if(("start_time",user_info['start_time']) not in t_slots.items()):
                slots.remove(t_slots)
                keep_day_slots.append(t_slots)
                print(slots)



        if(len(slots) == 0):
            if(len(keep_day_slots) > 1):

                ans = "There are no timeslots that match your preferred movie time. However below are movie sessions that are the closest to your preferred time.  Type the option number you want to select a session OR type cancel to cancel booking.\n\n"
                for i, slot in enumerate(list(keep_day_slots)):
                    o_num = i+1
                    #Order in new_ids is important as the number that user selects will be the index of the timeslot id chosen
                    new_ids.append(str(slot['timeslot_id']))

                    
                    ans += "Option {}: {} time: {}-{} movie: {} cinema: {} theatre_type: {} tickets: {}\n\n".format(o_num,slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'], user_info['people'])
                b_list = ",".join(new_ids)
                update_blist_info(b_list, userName)
                return ans
            #If there is only only only timeslot that fits the user preferences
            elif(len(keep_day_slots) == 1):
                slot = keep_day_slots[0] 
                ans = "There are no timeslots that match your preferred movie time. However there is one  movie session that is the closest to your preferred time. Type confirm to make this booking OR type cancel to cancel this booking.\n\n"
                #t_ids.append(str(slot['timeslot_id']))
                ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {} tickets: {}\n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'], user_info['people'])
                #b_list = ",".join(t_ids)
                update_blist_info(str(slot['timeslot_id']), userName)
                return ans
            #No slots available
            else:
                reset_user_info(userName)
                ans = "There is no timeslots available for your given preferences. Change your preferences and start a new booking.\n"
                return ans
            

    t_ids = []

    #Check if available slots are within the times previously booked 
    #If slots are wthin 2 hours windows of previously booked tickets they are filtered out.
    tickets = get_current_tickets(userName)


    for slot in list(slots):
        for t in tickets:
            #Continue only if days match
            if(slot['day'] == t['day']):
                slot_time = datetime.strptime(slot['start_time'], '%H:%M')
                slot_etime = slot_time + timedelta(hours=2)
                slot_start = slot_time.time()
                slot_end = slot_etime.time()
                ticket_time = datetime.strptime(t['start_time'], '%H:%M')
                ticket_etime = ticket_time + timedelta(hours=2)
                ticket_start = ticket_time.time()
                ticket_end = ticket_etime.time()
                #If start times match then remove
                if(slot_time == ticket_time):
                    slots.remove(slot)

                #Check if slot start starts after ticket start and before ticket end
                elif(slot_start > ticket_start and slot_start < ticket_end):
                    slots.remove(slot)

                #Check if slot end starts after ticket start and before ticket end
                elif(slot_end  > ticket_start and slot_end < ticket_end):
                    slots.remove(slot)


    #If there are multiple timeslots that fit the user preferences
    if(len(slots) > 1):

        ans = "There are {} available timeslots. Type the option number you want to select OR type cancel to cancel this booking\n\n".format(len(slots))
        for i, slot in enumerate(list(slots)):
            o_num = i+1

            #Order in t_ids is important as the number that user selects will be the index of the timeslot id chosen
            t_ids.append(str(slot['timeslot_id']))
            ans += "Option {}: {} time: {}-{} movie: {} cinema: {} theatre_type: {} tickets: {}\n\n".format(o_num,slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'], user_info['people'])

        b_list = ",".join(t_ids)
        update_blist_info(b_list, userName)
    #If there is only only only timeslot that fits the user preferences
    elif(len(slots) == 1):
        slot = slots[0] 
        ans = "There is one available timeslot. Type confirm to make this booking OR type cancel to cancel this booking.\n\n"
        #t_ids.append(str(slot['timeslot_id']))
        ans += "{} time: {}-{} movie: {} cinema: {} theatre_type: {} tickets: {}\n\n".format(slot['day'], slot['start_time'], slot["end_time"], slot['movie_name'] ,slot['cinema_name'],slot['theatre_type'], user_info['people'])
        #b_list = ",".join(t_ids)
        update_blist_info(str(slot['timeslot_id']), userName)
    #No slots available
    else:
        reset_user_info(userName)
        ans = "There is no timeslots available for your given preferences. Change your preferences and start a new booking.\n"
        return ans

    return ans







def convertDay(dayString):
    return (dayString[0:3].lower())

def getDayString(day):
    if (day == 0):
        return "mon"
    if (day == 1):
        return "tue"
    if (day == 2):
        return "wed"
    if (day == 3):
        return "thu"
    if (day == 4):
        return "fri"
    if (day == 5):
        return "sat"
    if (day == 6):
        return "sun"
    else:
        return "This is error"

def convertHourString(hour):
    if (hour == "1"):
        return "13"
    if (hour == "2"):
        return "14"
    if (hour == "3"):
        return "15"
    if (hour == "4"):
        return "16"
    if (hour == "5"):
        return "17"
    if (hour == "6"):
        return "18"
    if (hour == "7"):
        return "19"
    if (hour == "8"):
        return "20"
    if (hour == "9"):
        return "21"
    if (hour == "10"):
        return "22"
    if (hour == "11"):
        return "23"
    else:
        return None

def check_time(time_str):
    cinema_start = datetime.strptime("13:00","%H:%M").time()
    cinema_end = datetime.strptime("23:00","%H:%M").time()

    if(time_str > cinema_end or time_str < cinema_start):
        return False
    return True

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def has_letters(inputString):
    return any(char.isalpha() for char in inputString)