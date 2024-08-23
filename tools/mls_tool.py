import os

import pandas as pd
import requests


def create_request_to_mls(total_area: int, address: str, total_bedrooms: int, total_bathrooms: int):
    """
    Creates a request to Multiple listing service with given information about the estates and returns the average,
    highest and lowest prices per square foot

    Example call:

    create_request_to_mls(250, '4211 Elevator Dr, Austin, TX 78731', 2)
    Args:
        total_area (int): the total area of the estate
        address (str): the address of the estate
        total_bedrooms (int): the number of bedrooms of the estate
        total_bathrooms (int): the number of bathrooms of the estate
    Returns:
        str: Return should contain the total number of found estates,
        average with the highest and the lowest asking prices per square foot
    """
    url = (f'https://api.bridgedataoutput.com/api/v2/actris_ref/listings?access_token'
           f'=8498c7a46296394a3a8d179018034a65&limit=50&near={address}&radius=1mi&LivingArea.gte={total_area}&LivingArea'
           f'.lte={total_area * 1.3}&PropertyType=Residential&BedroomsTotal={total_bedrooms}&BathroomsTotalInteger={total_bathrooms}')

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = pd.DataFrame(response.json().get("bundle"))
        if data.shape[0] != 0:
            features_data = data[
                ['ListingId', 'ListPrice', 'LivingArea', 'Flooring', 'ExteriorFeatures', 'SecurityFeatures',
                 'ParkingFeatures', 'Appliances',
                 'Heating']].astype(str)
            features_data['PricePerSqFoot'] = round(features_data['ListPrice'].apply(int) /
                                                    features_data['LivingArea'].apply(int), 3)
            return features_data.to_dict('records')
        else:
            return 'Sorry, no estates found.'
    except requests.exceptions.RequestException as e:
        # Handle the exception (e.g., log it, return a default value, etc.)
        print(f"An error occurred: {e}")
        return "An error occurred while fetching data."

