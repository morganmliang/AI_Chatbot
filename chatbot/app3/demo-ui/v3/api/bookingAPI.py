import json
import requests

def get_timeslots_info(movie_name):

    c_results = requests.get('http://127.0.0.1:5008/v4/timeslots')

    dets = c_results.json()
    movie_slots = []
    movie_name_clean = movie_name.replace(" ", "").lower()
    for slot in dets:
        if(slot['movie_name'].replace(" ", "").lower() == movie_name_clean):
            movie_slots.append(slot)


    # ans += "Cinema Name: {}\n".format(cinema_name)
    # ans += "Address: {}\n".format(dets['address'])
    # ans += "Phone Number: {}\n".format(dets['phone'])
    # ans += "Available Snacks: " + ",".join(dets['snacks']) + '\n'
    # for m in dets['movies']:
    #     movie_list.append(m['name'])
    # ans += "Movies Now Showing: " + ",".join(movie_list) + '\n'
    print(movie_slots)
    return movie_slots


def get_all_timeslots():

    c_results = requests.get('http://127.0.0.1:5008/v4/timeslots')

    dets = c_results.json()
    movie_slots = []



    # ans += "Cinema Name: {}\n".format(cinema_name)
    # ans += "Address: {}\n".format(dets['address'])
    # ans += "Phone Number: {}\n".format(dets['phone'])
    # ans += "Available Snacks: " + ",".join(dets['snacks']) + '\n'
    # for m in dets['movies']:
    #     movie_list.append(m['name'])
    # ans += "Movies Now Showing: " + ",".join(movie_list) + '\n'
    return dets



def get_movie_people_times(movie_name, people, userName):


    c_results = requests.get('http://127.0.0.1:5008/v4/timeslots/{}/{}/{}'.format(movie_name.lower(), userName,people))

    timeslots = c_results.json()
    movie_list = []


    return timeslots


def get_current_tickets(userName):
    c_results = requests.get('http://127.0.0.1:5008/v4/timeslots/{}/booked_tickets'.format(userName))

    timeslots = c_results.json()
    movie_list = []


    print(timeslots)
    return timeslots



def get_timeslot_details(timeslot_id):

    c_results = requests.get('http://127.0.0.1:5008/v4/timeslots/{}'.format(timeslot_id,))
    print(c_results)
    timeslots = c_results.json()


    return timeslots

def make_booking(timeslot_id, userName, people):

    c_results = requests.put('http://127.0.0.1:5008/v4/timeslots/{}/{}/{}/add'.format(timeslot_id,userName,people))
    print(c_results)
    timeslots = c_results.json()


    return timeslots

def delete_ticket(userName, timeslot_id):


    c_results = requests.put('http://127.0.0.1:5008/v4/timeslots/{}/{}/delete'.format(userName, timeslot_id))
    print(c_results)
    timeslots = c_results.json()


    return timeslots
