import json
import requests

def get_all_cinemas():

    r = requests.get('http://127.0.0.1:5001/v1/Cinema')
    results=r.json()
    print(results)
    
    l_cinemas = []

    for c in results:
        l_cinemas.append(c['name'])

    print("l cinemas")
    print(l_cinemas)
    ans = "The available cinemas to you are: \n" + "\n".join(l_cinemas)

    print(ans)

    return ans

def movies_showing(c_name):

    r = requests.get('http://127.0.0.1:5001/v1/Cinema')
    results=r.json()

    
    ans = ""
    if(c_name == ""):
        for c in results:
            movie_list = [m['name'] for m in c['movies']]
            ans += "{} is currently showing:\n".format(c['name']) + "\n".join(movie_list) +'\n'
    else:
        for c in results:
            if (c['name'] == c_name):
                movie_list = [m['name'] for m in c['movies']]
                ans += "{} is currently showing:\n".format(c['name']) + "\n".join(movie_list) +'\n'

    if(ans == ""):
        ans = "There is an error in your query."
    return ans

def snack_info(c_name):

    r = requests.get('http://127.0.0.1:5001/v1/Cinema')
    results=r.json()

    print(results)

    l_cinemas = []
    ans = ""
    if(c_name == ""):
        for c in results:
            ans += "{} stocks the following snacks:\n".format(c['name']) + "\n".join(c['snacks']) +'\n'
    else:
        for c in results:
            if (c['name'] == c_name):
                ans += "{} stocks the following snacks:\n".format(c['name']) + "\n".join(c['snacks']) + '\n'

    print(ans)
    return ans

def get_movies_info():

    r = requests.get('http://127.0.0.1:5001/v1/Cinema')
    results=r.json()

    #print(results)

    ans = ""
    for c in results:
        movie_list = []
        for movie in c['movies']:
            movie_list.append(movie['name'])
        
        ans += "{} is currently showing the following movies:\n".format(c['name']) + "\n".join(movie_list)

    return ans

def search_movie(movie_name):

    r = requests.get('http://127.0.0.1:5001/v1/Cinema')
    results=r.json()

    print(results)

    ans = ""

    cinema_list = []
    for c in results:
        movie_list = [m['name'] for m in c['movies']]
        if movie_name in movie_list:
            cinema_list.append(c['name'])
        
        ans = "{} is currently showing the following cinemas:\n".format(movie_name) + "\n".join(cinema_list)

    return ans


def get_cinema_info(cinema_name):
    print(cinema_name)
    c_results = requests.get('http://127.0.0.1:5001/v1/Cinema/{}'.format(cinema_name))
    print(c_results)
    dets = c_results.json()
    movie_list = []
    if(dets == None):
        return ""

    ans = "This is all the information we could find about {}:\n".format(cinema_name)
    ans += "Cinema Name: {}\n".format(cinema_name)
    ans += "Address: {}\n".format(dets['address'])
    ans += "Phone Number: {}\n".format(dets['phone'])
    ans += "Available Snacks: \n" + "\n".join(dets['snacks']) + '\n'
    for m in dets['movies']:
        movie_list.append(m['name'])
    ans += "Movies Now Showing: \n" + "\n".join(movie_list) + '\n'

    return ans

def search_description(desc):

    r = requests.get('http://127.0.0.1:5001/v1/Cinema')
    results=r.json()

    print(results)

    ans = ""
    desc = desc.replace("\"", "").lower()
    full_movie_list = []
    for c in results:
        movie_list = [m for m in c['movies']]

        for m in movie_list:
            m_description = m['description'].lower()
            if desc in m_description:
                full_movie_list.append(m['name'])
    
    #remove all duplicates in list
    full_movie_list = list(dict.fromkeys(full_movie_list))

    if(len(full_movie_list) > 0):
        ans = "The following movies matches your description:\n" + "\n".join(full_movie_list)


    return ans
