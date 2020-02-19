import requests
import math
import json
import pandas as pd

# IronMan WC 2019 id
eventId = 'AFAAC1DC-73BA-E811-A967-000D3A37468C'
limitPerPage = 100


def requestData(page):
    skip = page * limitPerPage
    url = f'https://data.competitor.com/result/subevent/{eventId}?%24limit={limitPerPage}&%24skip={skip}&%24sort%5BFinishRankOverall%5D=1'
    response = requests.get(url)
    content = json.loads(response.content)
    return content


def parseData(data):
    results = data
    for result in results:
        copy = result
        copy['FullName'] = result['Contact']['FullName']
        copy['Gender'] = result['Contact']['Gender']
        copy['Country'] = result['Country']['ISO2']
        del copy['Contact']
    return results


initialRequest = requestData(0)
totalPages = initialRequest['total']
data = initialRequest['data']
results = parseData(data)

for page in range(1, math.ceil(totalPages/limitPerPage)):
    requestResponse = requestData(page)
    results.extend(parseData(requestResponse['data']))

df = pd.DataFrame(results)[['AgeGroup', 'BikeTimeConverted', 'FullName', 'Gender', 'Country', 'EventStatus', 'FinishRankGender', 'FinishRankGroup',
                            'FinishRankOverall', 'FinishTimeConverted', 'RunTimeConverted', 'SwimTimeConverted', 'Transition1TimeConverted', 'Transition2TimeConverted']]
df.to_csv('results.csv')
