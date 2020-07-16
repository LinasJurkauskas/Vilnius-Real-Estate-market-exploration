import AruodasScrapper as ARS
import SQL_CONN as SQL 
import metadata as metadata

# Calls in action the other functions to scrape
#main test

scrapper = ARS.AruodasScrapper()
year_list = metadata.get_years()
#year_list = [2021]
state_list = metadata.get_state()
#type_list = ['butai']
type_list = metadata.get_types()

for type in type_list:
    for year in year_list:
        for state in state_list:
            data_list = scrapper.CollectData(year,state,type)
            scrapper.FormatData(data_list, type)
            if len(data_list) > 0:
                SQL.insert_to_sql(data_list, year,state,type)



