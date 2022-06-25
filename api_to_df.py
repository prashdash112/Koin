import requests
import pprint
import json
import numpy as np
import pandas as pd 

# mkt = 'USD'
# smb = 'ETH'
#url = "https://alpha-vantage.p.rapidapi.com/query"

def extractor(smb,mkt):
    '''

    Extracts the crypto data at several levels from alpha vantage api address.
    Able to request data 5 times in 1 minute
    url = "https://alpha-vantage.p.rapidapi.com/query"

    '''
    url = "https://alpha-vantage.p.rapidapi.com/query"
    querystring = {"function":"DIGITAL_CURRENCY_WEEKLY","market": mkt,"symbol":smb}
    headers = {
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com",
        "X-RapidAPI-Key": "36afc09399mshfb59776274c13d9p1a0ac8jsnf27c88101ebc"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    resp_txt = response.text
    response = json.loads(resp_txt)
    global api_request
    api_request = response['Time Series (Digital Currency Weekly)']
    return api_request

def api_df(response):

    '''

    Unpacks the JSON object to multiple arrays

    '''
    open_tck=[]
    high=[]
    low=[]
    close=[]
    volume=[]
    mkt_cap=[]
    
    for i in response.keys():
        
        open_tck.append(response[i]['1a. open (USD)'])
        high.append(response[i]['2a. high (USD)'])
        low.append(response[i]['3a. low (USD)'])
        close.append(response[i]['4a. close (USD)'])
        volume.append(response[i]['5. volume'])
        mkt_cap.append(response[i]['6. market cap (USD)'])
    
    # Data processing 
    
    open_tck = np.asarray(list(map(float, open_tck))[::-1])
    high = np.asarray(list(map(float, high))[::-1])
    low = np.asarray(list(map(float, low))[::-1])
    close = np.asarray(list(map(float, close))[::-1])
    volume = np.asarray(list(map(float, volume))[::-1])
    mkt_cap = np.asarray(list(map(float, mkt_cap))[::-1])
    keys = np.asarray(list(api_request)[::-1]) #able to use api_request variable to store dates since it is global
    
    # data dictionaries 
    open_dict = {'date':keys,'open':open_tck}
    high_dict = {'date':keys,'high':high}
    low_dict = {'date':keys,'low':low}
    close_dict = {'date':keys,'close':close}
    volume_dict = {'date':keys,'volume':volume}
    mkt_cap_dict = {'date':keys,'mkt_cap':mkt_cap}
    
    # final dataframes
    global open_df
    open_df = pd.DataFrame(data = open_dict)
    global high_df
    high_df = pd.DataFrame(data = high_dict)
    global low_df
    low_df = pd.DataFrame(data = low_dict)
    global close_df
    close_df = pd.DataFrame(data = close_dict)
    global volume_df
    volume_df = pd.DataFrame(data = volume_dict)
    global mkt_cap_df
    mkt_cap_df = pd.DataFrame(data = mkt_cap_dict)
    merged_df = pd.concat([open_df,high_df['high'],low_df['low'],close_df['close'],volume_df['volume'],mkt_cap_df['mkt_cap']],axis=1)
    return merged_df

    

    # strategy is to return a merged dataset of all data type datasets & use it to filter in update graph func in main file - 5/6/22::16:30Hrs
#api_df(extractor(smb,mkt))

#extractor(smb,mkt,url)
#api_df(extractor(mkt,smb))
#dataframes = api_df(extractor(mkt,smb,url))

##################################### THE END ##############################################################
###################################################################################################
###################################################################################################
###################################################################################################


# mkt = 'USD'
# smb = 'ETH'
# url = "https://alpha-vantage.p.rapidapi.com/query"

# def extractor(mkt,smb,url):
#     '''

#     Extracts the crypto data at several levels from alpha vantage api address.
#     Able to request data 5 times in 1 minute
#     url = "https://alpha-vantage.p.rapidapi.com/query"

#     '''
    
#     querystring = {"function":"DIGITAL_CURRENCY_WEEKLY","market": mkt,"symbol":smb}
#     headers = {
#         "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com",
#         "X-RapidAPI-Key": "36afc09399mshfb59776274c13d9p1a0ac8jsnf27c88101ebc"
#         }
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     return(response.text)

# k = extractor(mkt,smb,url)
# k = json.loads(k) # deserialised dictionary from a string 
# api_request = k['Time Series (Digital Currency Weekly)']

# open_tck=[]
# high=[]
# low=[]
# close=[]
# volume=[]
# mkt_cap=[]

# def api_df(response):
#     '''

#     Unpacks the JSON object to multiple arrays

#     '''
#     for i in response.keys():
#         open_tck.append(response[i]['1a. open (USD)'])
#         high.append(response[i]['2a. high (USD)'])
#         low.append(response[i]['3a. low (USD)'])
#         close.append(response[i]['4a. close (USD)'])
#         volume.append(response[i]['5. volume'])
#         mkt_cap.append(response[i]['6. market cap (USD)'])

# dataframes =   api_df(api_request)  

# # Data processing 
# open_tck = np.asarray(list(map(float, open_tck))[::-1])
# high = np.asarray(list(map(float, high))[::-1])
# low = np.asarray(list(map(float, low))[::-1])
# close = np.asarray(list(map(float, close))[::-1])
# volume = np.asarray(list(map(float, volume))[::-1])
# mkt_cap = np.asarray(list(map(float, mkt_cap))[::-1])
# keys = np.asarray(list(k['Time Series (Digital Currency Weekly)'].keys())[::-1])

# open_dict = {'date':keys,'open':open_tck}
# high_dict = {'date':keys,'high':high}
# low_dict = {'date':keys,'low':low}
# close_dict = {'date':keys,'close':close}
# volume_dict = {'date':keys,'volume':volume}
# mkt_cap_dict = {'date':keys,'mkt_cap':mkt_cap}

# # final dataframes 
# open_df = pd.DataFrame(data = open_dict)
# high_df = pd.DataFrame(data = high_dict)
# low_df = pd.DataFrame(data = low_dict)
# close_df = pd.DataFrame(data = close_dict)
# volume_df = pd.DataFrame(data = volume_dict)
# mkt_cap_df = pd.DataFrame(data = mkt_cap_dict)
