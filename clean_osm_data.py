import pandas as pd
from fuzzywuzzy import fuzz

def getChainName(name, chainNames):
    for chainName in chainNames:
        similarity_score = fuzz.ratio(str(name), chainName)
        if(similarity_score > 80):
            return chainName
    else:
        return 'not_a_chain'

def fillMissingWikiInfo(chainName, chainsAndWikiDataDict):
    # figure out the key of the name
    for key, val in chainsAndWikiDataDict['name'].items():
        if (val == chainName):
            # then retrieve the value of the brand:wikidata from the key
            chain_key = key
            return chainsAndWikiDataDict['brand:wikidata'].get(chain_key)
    return None


def main():

    # Store the json file into a dataframe
    data_relative_path = './osm/amenities-vancouver.json'
    rawdata = pd.read_json(data_relative_path, lines=True) # lines = True specifies that each line is a separate JSON object

    # Replace rawdata['tags'] with the flattenedTags
    flattenedTags = pd.json_normalize(rawdata['tags'])
    rawdata = pd.concat([rawdata.drop(columns='tags'), flattenedTags], axis=1)

    # Data Set 1: Get the rows with the "brand:wikipedia" key in the tag object
    wikipedia_key_data = rawdata.dropna(subset=['brand:wikipedia'])
    # Remove the columns with NaN
    wikipedia_key_data = wikipedia_key_data.dropna(axis=1)
    #use to find amenities but can be subset with names for known locations
    wikipedia_key_data.to_csv('wikipedia_key_data.csv')

    #Data Set 2: Get the rows with "wikidata" key in the tag object
    wikidata_key_data = rawdata.dropna(subset=['brand:wikidata'])
    # Remove the columns where all entries are NaN
    wikidata_key_data = wikidata_key_data.dropna(axis=1, how='all')
    #use to find amenities but can be subset with names for known locations
    wikidata_key_data.to_csv('wikidata_key_data.csv')

    # Data Set 3: Get the rows with the "tourism" tags
    tourism = rawdata.dropna(subset=['name','tourism'])
    # Remove the columns with NaN
    tour_key_data = tourism.dropna(axis=1)
    tour_key_data = tour_key_data[tour_key_data['tourism'] != 'information']
    tour_key_data.to_csv("tourism.csv")

    # Data Set 3 Part 2: Tourism, but another version
    # tags: 'is_in:city', 'wikidata', 'ferry', 'tourism', 'wikipedia', 'guide'
    is_in_city = rawdata.dropna(subset=['is_in:city'])
    wikidata = rawdata.dropna(subset=['wikidata'])
    ferry = rawdata.dropna(subset=['ferry'])
    tourism = rawdata.dropna(subset=['tourism'])
    wikipedia = rawdata.dropna(subset=['wikipedia'])
    guide = rawdata.dropna(subset=['guide'])

    # combine these three data frames together
    tourism_test_df = is_in_city._append(wikidata, ignore_index=True)
    tourism_test_df = tourism_test_df._append(ferry, ignore_index=True)
    tourism_test_df = tourism_test_df._append(tourism, ignore_index=True)
    tourism_test_df = tourism_test_df._append(wikipedia, ignore_index=True)
    tourism_test_df = tourism_test_df._append(guide, ignore_index=True)
    tourism_test_df = tourism_test_df.drop_duplicates()
    tourism_test_df = tourism_test_df.dropna(how='all', axis=1)
    tourism_test_df.to_csv('tourismtwo.csv')

    # Data Set 4: get all chained and independently owned restaurants
    chain = rawdata.dropna(subset=['brand:wikidata','cuisine'])
    chain = chain.dropna(axis=1)

    indep = rawdata.dropna(subset=['cuisine'])
    indep = indep[indep['brand:wikidata'].isnull()]
    
    # get unique chains by dropping duplicates
    uniqueChains = chain.drop_duplicates(subset=['name'])
    uniqueChains = uniqueChains[['name', 'brand:wikidata']]
    uniqueChainNames = set(uniqueChains['name'])

    # check each row's name matches to one of the chains
    indep['chain_name'] = indep['name'].apply(getChainName, args=([uniqueChainNames]))
    # move the chains into new data frames
    chains_from_indep = indep[indep['chain_name'] != 'not_a_chain']
    indep = indep[indep['chain_name'] == 'not_a_chain']

    # Add the missing brand:wikidata into chains_from_indep dataframe
    chainsAndWikiDataDict = uniqueChains.to_dict()
    chains_from_indep['brand:wikidata'] = chains_from_indep['chain_name'].apply(fillMissingWikiInfo, args=([chainsAndWikiDataDict]))

    # keep only the necessary columns and append into chain df
    chains_from_indep = chains_from_indep[['lat','lon','timestamp','amenity','name','brand:wikidata','cuisine','brand']]
    chain = chain._append(chains_from_indep, ignore_index=True)

    indep.to_csv("independent_restaurant.csv")
    chain.to_csv("chain_restaurants.csv")
    # end of Data Set 4 --

if __name__=='__main__':
    main()