from django.shortcuts import render
import pandas as pd
import requests


def home(request):
    """ 
    Home page
    """
    df = pd.read_excel('data/municipality_list.xlsx')
    for p in ['TL', 'TM', 'TH', 'PL', 'PM', 'PH']:
        df[p] = ''
    muns = [i for i in range(1, 5)]
    trees = [606, 607]
    df['Tree'] = ''
    response = []
    for tree in trees:
        for mun in muns:
            df.iloc[mun-1,8] = tree
            resp = requests.get(f"https://virkesborsen.se/price-api/avg-price?municipality={mun}&tree={tree}", headers={"Authorization": "Basic YW1hcmUudGVzdEB2aXJrZXNib3JzZW4uc2U6c3R3STB6NExONTlTc1dSR3htYWM="}).json()
            response.append(resp)
            df.iloc[mun-1,2] = resp['timber_low']
            df.iloc[mun-1,3] = resp['timber_medium']
            df.iloc[mun-1,4] = resp['timber_high']
            df.iloc[mun-1,5] = resp['pulp_low']
            df.iloc[mun-1,6] = resp['pulp_medium']
            df.iloc[mun-1,7] = resp['pulp_high']
    df.to_csv('data/price_data.csv')
    return render(request, 'prices/home.html', {'df':df})
