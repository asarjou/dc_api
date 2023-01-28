import requests
import API.Constants as Constants
import json
def MakeRequest(url):

    response = requests.get(url, timeout=60) #If proxy in use would be included here - not used in this task

    if response.status_code == 200: 
        print('Successfully connected to API')
    else:
        print('Unsuccessful connection to API, status code: ' + str(response.status_code))   

    return response.json()

def NGESO_Request(resource_id, datetime): #Can look for any resource from NGESO datastore given a resourceID
    
    base_url = Constants.NGESO_BaseUrl

    url = base_url + resource_id + "&limit=1000&q=" + datetime #Gives Endpoint

    response = MakeRequest(url)

    final_response = get_all_records(Constants.NGESO_BaseUrl, response=response)
    return final_response

def get_all_records(base_url, response):

    # CKAN Limits the amount that we can pull in one request - after investigation the response we see that there is a link to the 'next' page included in the response
    ### briefly tested but there may be a bug in here due to how CKAN is querying the data with the offset? - unable to fully test due to time constraints ###
    first_response = response['result']['records']

    while "_links" in response['result'] and "next" in response['result']['_links']:
        
        next_url = base_url + str(response['result']['_links']['next'])

        response = MakeRequest(next_url) 
        #print(response)

        first_response.extend(response['result']['records'])
        #with open("data.json", "w") as outfile:
        #    json.dump(first_response, outfile)
        if len(response['result']['records']) < 1000: #limit set in url
            break
    return first_response

