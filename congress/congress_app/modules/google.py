import requests
import os
import re

API_KEY = os.environ["GOOGLE_API_KEY"]
GOOGLE_CIVIC_API = "https://www.googleapis.com/civicinfo/v2"
REPS_BY_ADDRESS_ENDPT = "/representatives"

def addressToDistricts(address):
    params = {"key": API_KEY, "address" : address, "includeOffices" : False}
    response = requests.get(GOOGLE_CIVIC_API + REPS_BY_ADDRESS_ENDPT, params=params)

    response = response.json()

    print(response)
    divisions = response["divisions"]

    state = None
    cong_district = None

    district_pattern = r'^ocd-division/country:us/state:([a-z]{2})/cd:(.+)$'
    for key, value in divisions.items():
        m = re.match(district_pattern, key)
        if m != None:
            print("Key", key)
            state = m.group(1)
            cong_district = m.group(2)
            break

    if state == None or cong_district == None:
        # TODO: Implement error_reps
        raise DistrictInfoNotFoundError

    return state.upper(), cong_district
