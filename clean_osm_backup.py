import pandas as pd


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
    # Remove the columns with NaN
    wikidata_key_data = wikidata_key_data.dropna(axis=1)
    #use to find amenities but can be subset with names for known locations
    wikidata_key_data.to_csv('wikidata_key_data.csv')

    # Data Set 3: Get the rows with the "tourism" tags
    tourism = rawdata.dropna(subset=['name','tourism'])
    # Remove the columns with NaN
    tour_key_data = tourism.dropna(axis=1)
    tour_key_data = tour_key_data[tour_key_data['tourism'] != 'information']
    tour_key_data.to_csv("tourism.csv")

    # Data Set 4: get all chained and independently owned restaurants
    chain = rawdata.dropna(subset=['brand:wikidata','cuisine'])
    chain = chain.dropna(axis=1)

    indep = rawdata.dropna(subset=['cuisine'])
    indep = indep[indep['brand:wikidata'].isnull()]
    
    # get unique chains by dropping duplicates
    uniqueChains = chain.drop_duplicates(subset=['name'])
    uniqueChains = uniqueChains[['name', 'brand:wikidata']]

    # inner join the unique chains into the indep df
    chains_from_indep = pd.merge(indep, uniqueChains, on='name', how='inner')
    # after the join, the brand:wikidata from uniqueChains got added as a new series called brand:wikidata_y. Rename it to brand:wikidata.
    chains_from_indep = chains_from_indep.rename(columns={'brand:wikidata_y': 'brand:wikidata'})
    # keep only the necessary columns and append into chain df
    chains_from_indep = chains_from_indep[['lat','lon','timestamp','amenity','name','brand:wikidata','cuisine','brand']]
    chain = chain._append(chains_from_indep, ignore_index=True)

    # remove chains from the indep df
    uniqueChainNames = set(uniqueChains['name'])
    indep = indep[~indep['name'].isin(uniqueChainNames)]

    indep.to_csv("independent_restaurant.csv")
    chain.to_csv("chain_restaurants.csv")





if __name__=='__main__':
    main()