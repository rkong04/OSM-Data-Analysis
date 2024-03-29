import pandas as pd


def main():

    # Store the json file into a dataframe
    data_relative_path = './osm/amenities-vancouver.json'
    rawdata = pd.read_json(data_relative_path, lines=True) # lines = True specifies that each line is a separate JSON object

    # Replace rawdata['tags'] with the flattenedTags
    flattenedTags = pd.json_normalize(rawdata['tags'])
    rawdata = pd.concat([rawdata.drop(columns='tags'), flattenedTags], axis=1)

    # Data Set 1: Get the rows with the "wikipedia" key in the tag object
    wikipedia_key_data = rawdata.dropna(subset=['wikipedia'])
    # Remove the columns with NaN
    wikipedia_key_data = wikipedia_key_data.dropna(axis=1)
    wikipedia_key_data.to_csv('wikipedia_key_data.csv')

    # Data Set 2: Get the rows with the "tourism":"attraction" in the tags (only 3 rows) or, just get all of the rows with the "tourism" key in the tags

    # Data Set 3: 





if __name__=='__main__':
    main()