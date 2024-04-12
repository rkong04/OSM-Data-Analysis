import pandas as pd
import sys
import matplotlib.pyplot as plt
from scipy import stats

# Add counts on top of each bar
def addCountsOnBars(bars):
    for bar in bars.patches:
        plt.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f'{int(bar.get_height())}',
                ha='center', va='bottom', fontsize=10)

def main():

    chain = pd.read_csv('./datasets/chain_restaurants.csv')
    indep = pd.read_csv('./datasets/independent_restaurants.csv')

    # HISTOGRAM 1: Top 10 Chains by Count in the Greater Vancouver Area

    # Group by the chain restaurants by name, count, and sort
    chain_grouped = chain.groupby('chain_name')
    chain_grouped_count = chain_grouped.size()
    chain_grouped_count_sorted = chain_grouped_count.sort_values(ascending=False)

    # Plotting:
    top_ten_chains = chain_grouped_count_sorted.head(10)
    plt.figure(figsize=(10, 6))
    bars = top_ten_chains.plot(kind='bar', width= 0.80)
    plt.title('Top 10 Chains by Count in Greater Vancouver')
    plt.xlabel('Chain Name')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.1, zorder=0)
    addCountsOnBars(bars)
    plt.tight_layout()
    plt.savefig('./Images/plotOfChainCounts.jpg')


    # HISTOGRAM 2: Number of Chains by in each specific city in the Greater Vancouver Area, showing top 14 results

    chain = chain.drop(chain.index[chain['city'] == 'Electoral Area A']) # remove Electporal Area A, it's where the mountains are
    chainsGroupedByCity = chain.groupby('city')
    chainsGroupedByCityCount = chainsGroupedByCity.size().sort_values(ascending=False)
    chainsGroupedByCityCount = pd.DataFrame({'City': chainsGroupedByCityCount.index, 'Count': chainsGroupedByCityCount.values})
    top_cities = chainsGroupedByCityCount.head(14)
    bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896']

    # Plotting:
    plt.figure(figsize=(10, 6))
    bars = plt.bar(top_cities['City'], top_cities['Count'], color=bar_colors[:len(top_cities)])
    plt.title('Number of Chains in Greater Vancouver Regions')
    plt.xlabel('City Name')
    plt.ylabel('Number of Chains')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.1, zorder=0)
    addCountsOnBars(bars)
    plt.tight_layout()
    plt.savefig('./Images/plotOfChainsPerCity.jpg')

    # GRAPH 3: ScatterPlot:
    # Note: All Population data gathered from the 2021 Census database https://www12.statcan.gc.ca/census-recensement/index-eng.cfm
    populationsOfEachCity = {'City': ['Vancouver', 'Surrey', 'Burnaby', 'Abbotsford', 'Richmond', 'Coquitlam', 'Delta', 'New Westminster', 'City of Langley', 'Port Coquitlam', 'Maple Ridge', 'West Vancouver', 'North Vancouver', 'Port Moody'], 
                             'Population': [662248, 568322, 249125, 153524, 209937, 148625, 108455, 78916, 28963, 61498, 90990, 44122, 58120, 33535]}
    populationsOfEachCityDf = pd.DataFrame(populationsOfEachCity)

    # Add the population data into the chain counts by city dataframe
    chainCountsWithPopulation = chainsGroupedByCityCount.merge(populationsOfEachCityDf, how='inner', on='City')
    # Perform Regression
    fit = stats.linregress(chainCountsWithPopulation["Population"]/100000, chainCountsWithPopulation["Count"])
    chainCountsWithPopulation['Prediction'] = chainCountsWithPopulation['Population']/100000 * fit.slope + fit.intercept
    print('The correlation coefficient is:', fit.rvalue) # Check that chain count in that city is correlated to the population in that city
    
    # Plot the scatter plot with the regression line
    plt.figure(figsize=(10,6))
    for i, txt in enumerate(chainCountsWithPopulation['City']):
        plt.scatter(chainCountsWithPopulation["Population"][i]/100000, chainCountsWithPopulation["Count"][i], color=bar_colors[i], label=txt)
    plt.plot(chainCountsWithPopulation["Population"]/100000, chainCountsWithPopulation['Prediction'], color='black', linewidth=2, label='Linear Regression')

    plt.xlabel("Population in 2021 (x 100,000)")
    plt.ylabel("Number of Chains")
    plt.title("Number of Chains vs Population")
    plt.legend()
    plt.savefig('./Images/numOfChainsVsPopulation.jpg')
    chainCountsWithPopulation.to_csv('./datasets/city_population_chain_count.csv')


if __name__ == '__main__':
    main()