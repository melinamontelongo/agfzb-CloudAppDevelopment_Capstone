import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    try:
        if "api_key" in kwargs:
            response = requests.post(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
        return
    status_code = response.status_code
    print("Status code: {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    json_review = json_payload["review"]
    try:
        response = requests.post(url, params=kwargs, json=json_review, headers={'Content-Type': 'application/json'})
    except:
        print("Error in POST")
    status_code = response.status_code
    print("Status code: {} ".format(status_code))
    if response.text == None or response.text == '':
        print('Null or empty string value for data')
    else:
        json_data = json.loads(response.text)
        return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review["dealership"], review=review["review"], name=review["name"],
                                    purchase=review["purchase"], purchase_date=review["purchase_date"],
                                   car_make=review["car_make"], car_model=review["car_model"],
                                   car_year=review["car_year"], sentiment=analyze_review_sentiments(review["review"]))
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/28339ce0-f864-4a65-ac9c-c7547fb9e8f3"
    api_key="7PLV-kcz2D7daTeKW_2pXzci6--GKXND2_A-yIkEAbFi"
# - Call get_request() with specified arguments
    #response = get_request(url, **params)
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
# - Get the returned sentiment label such as Positive or Negative
    response = natural_language_understanding.analyze(
        text=text,
        language="en",
        features= Features(sentiment= SentimentOptions()),
    ).get_result()
    sentiment = response["sentiment"]["document"]["label"]
    return sentiment
