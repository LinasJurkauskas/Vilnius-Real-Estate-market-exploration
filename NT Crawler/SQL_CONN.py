import pyodbc as sql

# def connect_to_sql():
#     conn = sql.connect('Driver={SQL Server};'
#                         'Server=LAPTOP-VIMAFH9F\SQLEXPRESS;'
#                         'Database=Politics;'
#                         'Trusted_Connection=yes;')


def insert_to_sql(data_list, year, state, type):
    conn = sql.connect('Driver={SQL Server};'
                        'Server=LAPTOP-VIMAFH9F\SQLEXPRESS;'
                        'Database=Politics;'
                        'Trusted_Connection=yes;')
    cursor = conn.cursor()
    for item_list in data_list:
        reserved = item_list[0]
        auction = item_list[1]
        is_new_project = item_list[2]
        nr_stars = item_list[3] 
        unknown1 = item_list[4]
        unknown2 = item_list[5]
        district = item_list[6]
        street = item_list[7]
        discount = item_list[9]
        id = item_list[15]
        log_date = item_list[16]
        total_price = item_list[17]
        price_sq_m = item_list[18].replace(',', '.')
        nr_rooms = item_list[19]
        space_sq_m = item_list[20]
        floor_obj = item_list[21]
        floor = item_list[22]
        nr_floors = item_list[23]
        comments = item_list[24]
        raw_data = str(item_list)
        if type == 'butai':
            type_int = 1
        elif type == 'namai':
            type_int = 2
        elif type == 'butu-nuoma':
            type_int = 3

        cursor.execute('''
                    INSERT INTO Politics.[dbo].ARUODAS_DATA (is_new_project, auction,  reserved, nr_stars, unknown1, unknown2, 
                                                            district, street, discount, id, log_date,  total_price,price_sq_m,
                                                            nr_rooms, space_sq_m, floor_obj,  floor, nr_floors, comments, year,
                                                               raw_data , state , type )
                    VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?)
                    ''',
                    (is_new_project,auction, reserved, nr_stars, unknown1, unknown2, 
                    district, street,  discount , id, log_date, total_price,price_sq_m,
                    nr_rooms, space_sq_m, floor_obj,  floor, nr_floors, comments, year, raw_data , state, type_int )
                    )
        conn.commit()                       

# def insert_to_sql_test(data_list):
#     conn = sql.connect('Driver={SQL Server};'
#                         'Server=LAPTOP-VIMAFH9F\SQLEXPRESS;'
#                         'Database=Politics;'
#                         'Trusted_Connection=yes;')
#     cursor = conn.cursor()
#     for item_list in data_list:
#         raw_data = str(item_list)

#         cursor.execute('''
#                     INSERT INTO Politics.[dbo].ARUODAS_DATA (raw_data   )
#                     VALUES
#                     (?)
#                     ''',
#                     (raw_data)
#                     )
#         conn.commit() 

#insert_to_sql()
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM Politics.[dbo].ARUODAS_DATA')

    # for row in cursor:
    #     print(row)


    