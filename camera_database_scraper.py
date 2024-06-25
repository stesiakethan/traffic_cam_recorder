from string import Template
import requests
import json
import time
import http.client

default_request_string = "/List/GetData/Cameras?query=%7B%22columns%22%3A%5B%7B%22data%22%3Anull%2C%22name%22%3A%22%22%7D%2C%7B%22name%22%3A%22sortId%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22region%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22county%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22roadway%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22description1%22%7D%2C%7B%22name%22%3A%22direction%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22blocked%22%2C%22s%22%3Atrue%7D%2C%7B%22data%22%3A8%2C%22name%22%3A%22%22%7D%5D%2C%22order%22%3A%5B%7B%22column%22%3A1%2C%22dir%22%3A%22asc%22%7D%2C%7B%22column%22%3A2%2C%22dir%22%3A%22asc%22%7D%5D%2C%22start%22%3A0%2C%22length%22%3A100%2C%22search%22%3A%7B%22value%22%3A%22%22%7D%7D&lang=en-US""/List/GetData/Cameras?query=%7B%22columns%22%3A%5B%7B%22data%22%3Anull%2C%22name%22%3A%22%22%7D%2C%7B%22name%22%3A%22sortId%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22region%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22county%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22roadway%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22description1%22%7D%2C%7B%22name%22%3A%22direction%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22blocked%22%2C%22s%22%3Atrue%7D%2C%7B%22data%22%3A8%2C%22name%22%3A%22%22%7D%5D%2C%22order%22%3A%5B%7B%22column%22%3A1%2C%22dir%22%3A%22asc%22%7D%2C%7B%22column%22%3A2%2C%22dir%22%3A%22asc%22%7D%5D%2C%22start%22%3A0%2C%22length%22%3A100%2C%22search%22%3A%7B%22value%22%3A%22%22%7D%7D&lang=en-US"
templatized_request_string = Template("https://fl511.com/List/GetData/Cameras?query=%7B%22columns%22%3A%5B%7B%22data%22%3Anull%2C%22name%22%3A%22%22%7D%2C%7B%22name%22%3A%22sortId%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22region%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22county%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22roadway%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22description1%22%7D%2C%7B%22name%22%3A%22direction%22%2C%22s%22%3Atrue%7D%2C%7B%22name%22%3A%22blocked%22%2C%22s%22%3Atrue%7D%2C%7B%22data%22%3A8%2C%22name%22%3A%22%22%7D%5D%2C%22order%22%3A%5B%7B%22column%22%3A1%2C%22dir%22%3A%22asc%22%7D%2C%7B%22column%22%3A2%2C%22dir%22%3A%22asc%22%7D%5D%2C%22start%22%3A$start_value%2C%22length%22%3A100%2C%22search%22%3A%7B%22value%22%3A%22%22%7D%7D&lang=en-US")

#Pulls raw camera list from fl511's hidden API in JSON format
def pull_json(request_string=default_request_string):
    conn = http.client.HTTPSConnection("fl511.com")
    payload = ""
    headers = {
        'cookie': "session-id=CD9C06D37D75D121286E215B7FDF91476D55B2FD3D69D7B811576D8FE95CBD4F1B65A6BA9F86F601B19EAE58AE4350E53D8823EA4C847D0BB834E18430A4A7F89D57FCD2B55A1A311A94489CE138F71725EEB6DE4AFAE935D1BA8F279BBDE636DB383CB9B470A5622DA848CA19E23594FDDB00015C60A667DED2C2D0F1FA816F; _culture=en-US; session=session",
        'User-Agent': "insomnia/8.5.1"
        }

    conn.request("GET", request_string, payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data

#Used in construct_request_list
def get_pagination_limit():
    #Using default_request_string as set in pull_json's default parameters, as we're only looking for the recordsTotal variable in the response
    data = pull_json()
    obj = json.loads(data)
    #Stores recordsTotal as an integer in order to use floor division on it to get the pagination limit
    total_records = int((obj["recordsTotal"]))

    pagination_limit = (total_records // 100) * 100
    return pagination_limit



#Returns link_list, a list of request strings to iterate on in order to extract all data from the camera database as the number of records per request is limited to 100
#Pagination_limit will be the total number of records floor divided to the nearest 100, for example 4200 if the total number of records is 4231
def construct_request_list():
    pagination_limit = get_pagination_limit()
    request_string = templatized_request_string

    request_list = []
    start_value = 0
    while start_value <= pagination_limit:
        formatted_request_string = request_string.substitute(start_value=str(start_value))
        start_value = start_value + 100
        request_list.append(formatted_request_string)

    return request_list

#Main function, iterates through request list to pull each page of json data and constructs it into one file
def full_camera_list_constructor(file_name="camera_list"):
    request_list = construct_request_list()

    json_list = []
    for i in request_list:
        data = json.loads(pull_json(request_string=i))
        json_list.extend(data["data"])

    with open("Resources/" + file_name + ".json", "w") as f:
        encoded_json_list = json.dumps(json_list)
        f.write(encoded_json_list)

#Uncomment this command and run the script to update camera list
#full_camera_list_constructor()