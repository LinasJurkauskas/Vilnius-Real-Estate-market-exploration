def get_years():
    '''
    generates the list of all years that will be used in scrapping.
    '''
    i = 1850
    years_list = []
    while i < 2022:
        years_list.append(i)
        i +=1
    
    return years_list


def get_state():
    '''
    '''
    state_list = ["full", "part","noteq","n_finished", "foundation", "none" ] 

    return state_list


def get_types():
    '''
    '''
    type_list = ['butai', 'butu-nuoma']

    return type_list
