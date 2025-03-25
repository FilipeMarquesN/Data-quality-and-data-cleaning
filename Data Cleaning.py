import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def loadData(countryDataFile, leadershipDataFile, sportDataFile):
    """
    Receives:
    - countryDataFile (str): Path to the country data Excel file.
    - leadershipDataFile (str): Path to the leadership data CSV file.
    - sportDataFile (str): Path to the sports data CSV file.

    Returns:
    - countryData (DataFrame): Loaded country data.
    - leadershipData (DataFrame): Loaded leadership data.
    - sportData (DataFrame): Loaded sports data.
    """
    leadershipData = pd.read_csv(leadershipDataFile)
    sportData = pd.read_csv(sportDataFile)
    countryData = pd.read_excel(countryDataFile, sheet_name="Data")
    return countryData, leadershipData, sportData

def clipYears(countryData, leadershipData, sportData):
    """
    Used with the objetive of just using data that its availeble in all the datasets.
    Receives:
    - countryData (DataFrame): Country data containing a 'year' column.
    - leadershipData (DataFrame): Leadership data containing a 'year' column.
    - sportData (DataFrame): Sports data containing a 'Year' column.

    Returns:
    - countryData (DataFrame): Country data with 'year' values clipped at a maximum of 2016.
    - leadershipData (DataFrame): Leadership data with 'year' values clipped between 1950 and 2016.
    - sportData (DataFrame): Sports data with 'Year' values clipped at a minimum of 1950.
    """
    countryData['year'] = countryData['year'].clip(upper=2016)
    leadershipData['year'] = leadershipData['year'].clip(upper=2016, lower=1950)
    sportData['Year'] = sportData['Year'].clip(lower=1950)
    return countryData, leadershipData, sportData

def removeUnwantedColumns(leadershipData, countryData, sportData):
    """
    Receives:
    - leadershipData (DataFrame): Leadership data containing unnecessary columns.
    - countryData (DataFrame): Country data containing unnecessary columns.
    - sportData (DataFrame): Sports data containing unnecessary columns.

    Returns:
    - leadershipData (DataFrame): Cleaned leadership data with specific columns removed.
    - countryData (DataFrame): Cleaned country data with specific columns removed.
    - sportData (DataFrame): Cleaned sports data with specific columns removed.
    """
    leadershipColsToDrop = [
        'country_code_cow', "hog_ideology_num_full", "hog_ideology_num_redux", "hog_right", 
        "hog_left", "hog_center", "hog_noideo", "hog_noinfo", "hog_ideomiss", "hog_party",
        "hog_party_abbr", "hog_party_eng", "hog_party_id", "hog_title", "leader",
        "leader_ideology", "leader_ideology_num_full", "leader_ideology_num_redux",
        "leader_right", "leader_left", "leader_center", "leader_noideo", "leader_noinfo",
        "leader_ideomiss", "leader_party", "leader_party_abbr"
    ]
    countryColsToDrop = ['i_cig', 'i_xm', 'i_xr', 'i_outlier', 'i_irr', 'cor_exp', 'statcap',"pl_c","pl_i","pl_g","pl_x","pl_m","pl_n","pl_k","csh_x","csh_m","csh_r","rdana","rkna"
    ,"rwtfpna","labsh","irr","delta"]
    sportColsToDrop = ['NOC']

    leadershipData = leadershipData.drop(columns=leadershipColsToDrop)
    countryData = countryData.drop(columns=countryColsToDrop)
    sportData = sportData.drop(columns=sportColsToDrop)

    return leadershipData, countryData, sportData

def standardizeCountryNames(sportData, leadershipData):
    """
    Used to stantertize the data, it the objetive of solving problem like coutries with different names.

    Receives:
    - sportData (DataFrame): Sports data with inconsistent country/team names.
    - leadershipData (DataFrame): Leadership data with inconsistent country names.

    Returns:
    - sportData (DataFrame): Sports data with standardized country/team names.
    - leadershipData (DataFrame): Leadership data with standardized country names.
    """
    sportTeamMapping = {
        "Congo (Brazzaville)": "Republic of the Congo",
        "Congo (Kinshasa)": "Democratic Republic of the Congo",
        "United States": "United States of America",
        "Viet Nam": "Vietnam"
    }
    leadershipCountryMapping = {
        "Burma/Myanmar": "Myanmar",
        "Timor-Leste": "Timor Leste",
        "The Gambia": "Gambia",
        "Republic of Vietnam": "Vietnam",
        "North Macedonia": "Macedonia",
        "United Kingdom": "Great Britain",
        "German Democratic Republic": "Germany"
    }

    sportData["Team"] = sportData["Team"].replace(sportTeamMapping)
    leadershipData["country_name"] = leadershipData["country_name"].replace(leadershipCountryMapping)

    return sportData, leadershipData

def dataImporting(countryDataFile, leadershipDataFile, sportDataFile):
    """
    Used to import the data using the files obtained and converting it to df from the pandas library
    Receives:
    - countryDataFile (str): Path to the country data Excel file.
    - leadershipDataFile (str): Path to the leadership data CSV file.
    - sportDataFile (str): Path to the sports data CSV file.

    Returns:
    - countryData (DataFrame): Processed country data.
    - leadershipData (DataFrame): Processed leadership data.
    - sportData (DataFrame): Processed sports data.
    """
    countryData, leadershipData, sportData = loadData(countryDataFile, leadershipDataFile, sportDataFile)
    countryData, leadershipData, sportData = clipYears(countryData, leadershipData, sportData)
    leadershipData, countryData, sportData = removeUnwantedColumns(leadershipData, countryData, sportData)
    sportData, leadershipData = standardizeCountryNames(sportData, leadershipData)

    return countryData, leadershipData, sportData

def removeNotOlympicCountries(sportData, leadershipData, countryData):  ## See how to make this
    countries = pd.unique(sportData['Team'])
    
    inLeadership = leadershipData[leadershipData['country_name'].isin(countries)]
    outleadership = leadershipData[~leadershipData['country_name'].isin(countries)]
    
    
    inCountry = countryData[countryData['country'].isin(countries)]
    outCountry = countryData[~countryData['country'].isin(countries)]  # Ver greatBritain (Verifiquei isto e o nome nos jogos olimpicos é Great Britain)

    return inLeadership, inCountry

def removeNotOlympicYear(sportData,leadershipData,coutryData):
    """
    Used to remove the years without data about OlympicYear (this can be problematic tho)

    Receive:
    - sportData (DataFrame): A DataFrame containing sports data, including a "Year" column.
    - leadershipData (DataFrame): A DataFrame containing leadership data with a "year" column.
    - coutryData (DataFrame): A DataFrame containing country data with a "year" column.

    Return:
    - leadershipData (DataFrame): Filtered leadership data containing only Olympic years.
    - coutryData (DataFrame): Filtered country data containing only Olympic years.
    """
    Year = pd.unique(sportData["Year"])
    leadershipData = leadershipData[leadershipData['year'].isin(Year)]
    coutryData = coutryData[coutryData['year'].isin(Year)]
    return leadershipData,coutryData

def start():
    """
    Receives:
    - No parameters.

    Executes:
    - Calls DataImporting to load and process country, leadership, and sports data.
    - Calls RemoveNotOlympicCountries to filter data based on Olympic participation.
    - Calls RemoveNotOlympicYear to filter data based on Olympic years.

    Returns:
    - No return value. The function executes data processing steps.
    """

    countryData, leadershipData, sportData = dataImporting("countryData.xlsx", "leadershipData.csv", "sportData.csv")
    leadershipData, countryData = removeNotOlympicCountries(sportData, leadershipData, countryData)
    leadershipData, countryData = removeNotOlympicYear(sportData, leadershipData, countryData)
    countriesWithMostMedals(sportData)




# Phase 2 
def countriesWithMostMedals(sportData):

    data_2016 = sportData[sportData['Year'] == 2016]  
    
    female_data = data_2016[data_2016['Sex'] == 'F']
    
    
    female_counts = female_data.groupby('Team').size().reset_index(name='Female Count')
    female_counts = female_counts[female_counts['Female Count'] > 10]
    female_counts = female_counts.sort_values(by='Female Count', ascending=False)
    sns.barplot(data=female_counts, x='Female Count', y='Team', orient='h')

    plt.yticks(fontsize=4)
    plt.show()

start()
