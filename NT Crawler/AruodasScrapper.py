import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import SQL_CONN as SQL


class AruodasScrapper:
    def __init__(self):
        """
        Purpose: scrape all apartments & houses available in Vilnius from Aruodas.lt
        """
        self.browser = webdriver.Chrome()
        self.browser.get("https://www.aruodas.lt/butai/vilniuje/")

    def GetMaxPage(self):
        pages_element = self.browser.find_elements_by_class_name("pagination")
        pages_nr = []
        for x in pages_element:
            pages_nr.append(x.text)
        pages_nr = pages_nr[0].split(' ')

        max_page = 0
        for number in pages_nr:
            if number.isnumeric() == True:
                if int(number) > max_page:
                    max_page = int(number)
        self.max_page = max_page 
        return max_page

    def CollectData(self, year, state, type):
        page_string = "https://www.aruodas.lt/"+str(type)+"/vilniuje/?FBuildYearMin="+str(year)+"&FBuildYearMax="+str(year)+"&detailed_search=1&FHouseState="+str(state)
       # page_string = "https://www.aruodas.lt/butai//vilniuje//""
        self.browser.get(page_string)
        try:
            error_element = self.browser.find_element_by_class_name("error2")
            data_list = []
            return data_list
    
        except:
            pages_element = self.browser.find_elements_by_class_name("pagination")
            pages_nr = []
            for x in pages_element:
                pages_nr.append(x.text)
            if len(pages_nr) != 0:
                pages_nr = pages_nr[0].split(' ')
                max_page = 0
                for number in pages_nr:
                    if number.isnumeric() == True:
                        if int(number) > max_page:
                            max_page = int(number)
                self.max_page = max_page
            else:
                max_page = 1
                self.max_page = 1

            data_list = []

            current_page = 1
            while current_page <= max_page:
                #print(current_page)
                items_element = self.browser.find_elements_by_class_name("list-row")
                items_found = []
                for item in items_element:
                    #print(item)
                    items_found.append(item.text)
                
                for item in items_found:
                    list_item = item.split("\n")
                    data_list.append(list_item)

                current_page += 1
                time.sleep(2)
                if current_page <= max_page:
                    page_change = self.browser.find_element_by_link_text(str(current_page))
                    #page_change.click()
                    self.browser.execute_script("arguments[0].click();", page_change)
            
            return data_list


    def FormatData(self, data_list, type):
        try:
            import_date = str(date.today())
            #remove dummy rows
            index = 0
            for item_list in data_list:
                if len(item_list) < 4:
                    data_list.pop(index)
                index += 1

            #add first column to where it is missing:
            for item_list in data_list:
                if item_list[0] != "Rezervuota":
                    item_list.insert(0, "0")
                else:
                    item_list[0] = "1"
            #Varžytynės
            for item_list in data_list:
                if  "Varžytynės" not in item_list[1]:
                    item_list.insert(1,"0")
                else:
                    item_list[1] = "1"   

            #add rezervuota column to where there is no price change
            for item_list in data_list:
                if "Naujas projektas" not in item_list[2]:
                    item_list.insert(2,"0")
                else:
                    item_list[2] = "1"

            #check if nr_stars exists:
            for item_list in data_list:
                if item_list[3].isdigit() == False:
                    item_list.insert(3,0)

            #add two unknown columns
            for item_list in data_list:
                if item_list[4] != "":
                    item_list.insert(4,"")

            for item_list in data_list:
                if item_list[5] != "":
                    item_list.insert(5,"")

            #if street does not exist add blank one
            for item_list in data_list:
                if item_list[7][0].isdigit() == True:
                    item_list.insert(7,"no street")

            #add posted column to where there is none
            for item_list in data_list:
                if "Prie" not in item_list[8]:
                    item_list.insert(8,"")

            #add price change column to where there is no price change
            for item_list in data_list:
                if "Kaina" not in item_list[9]:
                    item_list.insert(9,"0")
            #print(item_list)

            # add two last columns if they are missing:
            for item_list in data_list:
                if len(item_list) <15:
                    item_list.append('')

            for item_list in data_list:
                if len(item_list) <15:
                    item_list.append('')
            id = 1
            for item_list in data_list:
                item_list.append(id)
                item_list.append(import_date)
                id += 1

            for item_list in data_list:
                #price columns
                letter_index = 0
                while letter_index < len(item_list[10]):
                    if item_list[10][letter_index] == "€":
                        object_price = item_list[10][:letter_index].replace(" ","")
                        object_sqm_price = item_list[10][letter_index:].replace("€/m²","")
                        object_sqm_price = object_sqm_price.replace("€","")
                        object_sqm_price = object_sqm_price.replace(" ","")
                        break   
                    letter_index += 1
                item_list.append(object_price)
                item_list.append(object_sqm_price)

            if type == "butai" or type == "butu-nuoma":
            #building space columns
                for item_list in data_list:      
                    space_split = item_list[11].split()
                    item_list.append(space_split[0])
                    item_list.append(space_split[1])
                    item_list.append(space_split[2])
            else:
                for item_list in data_list:  
                    item_list.append(0)
                    space_split = item_list[11].split()
                    item_list.append(space_split[0])
                    item_list.append(0)


            #floor_split
            if type == "butai" or type =="butu-nuoma":
                for item_list in data_list:
                    space_split = item_list[21].split("/")
                    item_list.append(space_split[0])
                    item_list.append(space_split[1])
            else:
                for item_list in data_list:
                    item_list.append(0)
                    item_list.append(0)
 

            for item_list in data_list:
                item_list.append(item_list[13]+" "+item_list[14])
                print(item_list)
        except:
            print(data_list)







        
        






#best_aruodas_offers = {}
#time.sleep(3)
#COLLECTING DATA
# items_element = browser.find_elements_by_class_name("list-row")
# items_found = []
# for x in items_element:
#     items_found.append(x.text)

# list_of_lists = []
# id = 1
# for item in items_found:
#     list_item = item.split("\n")
#     list_item.append(id)
#     list_of_lists.append(list_item)
#     id += 1

# print(list_of_lists)


#driver.get("https://www.aruodas.lt/butai/vilniuje/")
#assert "Python" in driver.title
#elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source

#elem = driver.find_element_by_id("input_FPriceMin")
#print(elem)

#def adjust_choices(min_price, max_price, min_size, max_size):
#elem = driver.find_element_by_id("input_FPriceMin")
#print(elem)

# best_aruodas_offers = {}
# time.sleep(3)
# items_element = driver.find_elements_by_class_name("list-row")
# items_found = []
# for x in items_element:
#     items_found.append(x.text)
# counter = 4
# rating = 0
# select = Select(driver.find_element_by_id("changeListOrder"))
# select.select_by_value("Price")
# time.sleep(3)
# for x in items_found:
#     counter -= 1
#     rating += 1
#     if counter > 0:
#         x.strip()
#         if x != "":
#             x = x[1:]
#             x.strip()
#             best_aruodas_offers["#" + str(rating)] = x
#         else:
#             continue
# print(best_aruodas_offers)
# #return best_aruodas_offers

# #driver.close()


#browser = webdriver.Chrome()

#browser.get('http://www.seleniumhq.org/')
#elem = browser.find_element_by_link_text('Download')

#browser.get("https://www.aruodas.lt/butai/vilniuje/")
#elem = browser.find_element_by_id("input_FPriceMin")
#print(elem.text)

# #GETTING THE NUMBER OF PAGES
# pages_element = browser.find_elements_by_class_name("pagination")
# pages_nr = []
# for x in pages_element:
#     pages_nr.append(x.text)
# pages_nr = pages_nr[0].split(' ')

# max_page = 0
# for number in pages_nr:
#     if number.isnumeric() == True:
#         if int(number) > max_page:
#             max_page = int(number)
    
# print(max_page)
