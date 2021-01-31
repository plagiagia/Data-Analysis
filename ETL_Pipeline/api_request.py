# Import libraries
import os

import pandas as pd
import requests

# Set basic params and URL for api
api_url = "https://api.yelp.com/v3/businesses/search"
params = {"term": "restaurants",
          "location": "berlin"}

# Set the API key and headers
# This line of code will catch the API key from the environment variables
api_key = os.environ.get("API_KEY", "the actual API KEY")
headers = {"Authorization": "Bearer {}".format(api_key)}


def get_response(url=api_url, params=params, headers=headers, offset=[0]):
    """
    Get a response from an API URL with predefined parameters and headers. Also runs for different number of
    iterations, in case the API returns chunks of data.

    INFO: This API returns only 20 businesses when it is called

    VARIABLES
    ----------
    url: str, API URL, see the documentation for further usage
    params: dict, predefined parameters in dictionary format
    headers: dict,  the header for the API, see documentation of the API
    offset: list,  takes only integers, how many entries to skip after the next call

    RETURN:
    --------
    data_list: list with all JSON responses
    """

    data_list = []

    for each in offset:
        params['offset'] = each
        response = requests.get(api_url, params=params, headers=headers)
        data = response.json()
        data_list.append(data)

    return(data_list)


if __name__ == "__main__":

    print("Recieve data...")
    data = get_response(url=api_url, params=params, headers=headers,
                        offset=list(range(0, 100, 10)))
    print("All data recieved...")
