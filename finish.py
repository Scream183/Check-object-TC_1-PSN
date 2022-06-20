#!/usr/bin/env python
# coding: utf-8

# In[7]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[10]:



import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pandas as pd
from datetime import datetime
import re
from sqlalchemy import create_engine


root = tk.Tk()
root.title('Проверка на уведомления и патенты')
root.resizable(False, False)
root.geometry('500x200')

def OKTMO(oktmo):
    op = pd.read_csv("Z:\\ТС\\Сбор информации\\Сотрудники\\Андрей Ю\\python\\lists\\OKTMO.csv", index_col = 0, dtype = str).rename(columns={'0':'region_name','1':'kod'}).set_index('region_name')
    return op.loc[oktmo][0]

def has_type_street(adres):
    type_street = pd.read_csv("Z:\\ТС\\Сбор информации\\Сотрудники\\Андрей Ю\\python\\lists\\type_street_list.csv", index_col = 0, dtype = str)
    for index, row in type_street.iterrows():
        if row[0] in adres:
            return True
    return False

def has_type_street1(adres):
    type_street = pd.read_csv("Z:\\ТС\\Сбор информации\\Сотрудники\\Андрей Ю\\python\\lists\\type_street_list.csv", index_col = 0, dtype = str)
    for index, row in type_street.iterrows():
        if row[0] in adres:
            return row[0]
    return False
    
    
def clean_house(house):
    result = re.search(r'\d+', house)
    return result.group(0)

def street_in_Mkad(row):
    
    #convert street
    addr = row['Адрес ТО']#ищем улицу
    type_TO = row['Тип ТО']
    square_shop = str(row['Площадь ТО, м2'])
    idd = row['Системный идентификатор объекта']
    kind_of_object = row['Вид объекта']
    placement_scheme = row['Схема размещения НТО']
    street_with_number = pd.read_csv("Z:\\ТС\\Сбор информации\\Сотрудники\\Андрей Ю\\python\\lists\\street_with_number.csv")
    street_with_number = [[street_with_number.loc[i][1], str(street_with_number.loc[i][2])] for i in range(len(street_with_number))]
    for p in street_with_number:
        addr = addr.replace(p[0], p[1])
    if has_type_street1(addr):
        type_street = has_type_street1(addr) # find type street, if type street contains addr
        index_street = addr.find(type_street) #find index type street in addr
        street = addr[index_street:].split(' ')[1].strip(',')
    elif 'МКАД' in addr.upper():
        street = 'МКАД'
    else:
        street = None
        
        
    #convert house
    index_house = addr.find('дом ')
    if index_house == -1:
        house = None
    elif type_TO == 'Нестационарные торговые объекты' and kind_of_object != 'Вендинговый автомат':
        house = None
    elif kind_of_object == 'Вендинговый автомат' and (placement_scheme == 'Метрополитен' or placement_scheme =='ДТиУ'):
        house = None
    else:
        addr1 = addr[index_house:].split(' ')
        house = addr1[1].strip(',')
        house = clean_house(house)    
    


    #convert building
    building = None
    
    #convert status BP
    status = row['Статус для целей обложения ТС']
    if 'Недостоверные' in status:
        nc = status
    else:
        nc = None
    
    #convert octmo
    oktmo = row['Муниципальный район']
    if type_TO == 'Нестационарные торговые объекты' or (street == None and house == None):
        oktmo = OKTMO(oktmo)
    else:
        oktmo = None
        
    if type_TO == 'Нестационарные торговые объекты':
        type_to = '2'
    elif square_shop == 'nan' and type_TO != 'Нестационарные торговые объекты':
        type_to = '1'
    else:
        type_to = '3'
        
    return street, house, building, nc, oktmo, type_to
               

      

def street_zelenog(row):
    addr = row['Адрес ТО']#ищем улицу
    type_TO = row['Тип ТО']
    square_shop = str(row['Площадь ТО, м2'])
    idd = row['Системный идентификатор объекта']
    index_building = addr.find('корпус')
    
    
    #convert building
    if index_building > 0:
        building = addr[index_building:].split(' ')[1].strip(',')
        if len(building) > 3:
            building = clean_house(building)
    else:
        building = None
        
    #convert street if has
    if building == None:
        if has_type_street1(addr):
            type_street = has_type_street1(addr) # find type street, if type street contains addr
            index_street = addr.find(type_street) #find index type street in addr
            street = addr[index_street:].split(' ')[1].strip(',')
            if len(street) <= 2:
                street = None
        else:
            street = None
    else:
        street = None
        
    #convert house
    if building == None:
        index_house = addr.find('дом ')
        if index_house > 0:
            house = addr[index_house:].split(' ')[1].strip(',')
            house = clean_house(house)
        else:
            house = None
    else:
        house = None
        
    #convert status BP
    status = row['Статус для целей обложения ТС']
    if 'Недостоверные' in status:
        nc = status
    else:
        nc = None
    
    #convert octmo
    oktmo = row['Муниципальный район']
    if type_TO == 'Нестационарные торговые объекты' or (street == None and house == None and building == None):
        oktmo = OKTMO(oktmo)
    else:
        oktmo = None
        
    if type_TO == 'Нестационарные торговые объекты':
        type_to = '2'
    elif square_shop == 'nan' and type_TO != 'Нестационарные торговые объекты':
        type_to = '1'
    else:
        type_to = '3'

    return street, house, building, nc, oktmo, type_to    

    

def street_new_moscow(row):
    
    #convert street
    addr = row['Адрес ТО']
    idd = row['Системный идентификатор объекта']
    type_TO = row['Тип ТО']
    square_shop = str(row['Площадь ТО, м2'])
    kind_of_object = row['Вид объекта']
    placement_scheme = row['Схема размещения НТО']
    if has_type_street1(addr):
        type_street = has_type_street1(addr) # find type street, if type street contains addr
        index_street = addr.find(type_street) #find index type street in addr
        addr1 = addr[index_street:] # cut addr from type street to ...
        street = addr1.split(' ')[1].strip(',')
        if 'км' in addr:
            addr2 = addr[:addr.find('км')].strip().split() #street befor 'шоссе' 
            street = addr2[-3]
            if 'шоссе' in street:
                street = addr1.split(' ')[1]    
        if len(street) < 5:
            street = None
    elif 'МКАД' in addr:
        street = 'МКАД'
    else:
        street = None
        
    #convert house  
    index_house = addr.find('дом ')
    if index_house == -1:
        house = None
    elif type_TO == 'Нестационарные торговые объекты' and kind_of_object != 'Вендинговый автомат':
        house = None
    elif kind_of_object == 'Вендинговый автомат' and (placement_scheme == 'Метрополитен' or placement_scheme =='ДТиУ'):
        house = None
    else:
        addr1 = addr[index_house:].split(' ')
        house = addr1[1].strip(',')
        house = clean_house(house)   
    
    #convert building
    building = None
    
    #convert status BP
    status = row['Статус для целей обложения ТС']
    if 'Недостоверные' in status:
        nc = status
    else:
        nc = None
    
    #convert octmo
    oktmo = row['Муниципальный район']
    if type_TO == 'Нестационарные торговые объекты' or (street == None and house == None):
        oktmo = OKTMO(oktmo)
    else:
        oktmo = None
        
    if type_TO == 'Нестационарные торговые объекты':
        type_to = '2'
    elif square_shop == 'nan' and type_TO != 'Нестационарные торговые объекты':
        type_to = '1'
    else:
        type_to = '3'
        
    return street, house, building, nc, oktmo, type_to

def file_AIC_OPN():
    global filename1
    filename1 = fd.askopenfilename()
    showinfo(title='Выбранный файл', message=filename1)
    

def file_ТС_1():
    with open('Z:\ТС\Сбор информации\Сотрудники\Андрей Ю\python\lists\login_pass_ip.txt', encoding='utf-8') as file:
        a = file.readlines()
    conn = create_engine(f"mysql+pymysql://{a[0].strip()}:{a[1].strip()}@{a[2].strip()}/yusupov_av")
    return conn


def start_TC_1():
    a = pd.read_excel(filename1, header = 1, dtype = str)
    state_list1 = ['ЗелАО']
    state_list2 = ['ТАО', 'НАО']
    state_list3 = ['ЦАО', 'САО', 'СВАО', 'ВАО', 'ЮВАО', 'ЮАО', 'ЮЗАО', 'ЗАО', 'СЗАО']
    c1,c2,c3,c4,c5,c6 = [], [], [], [], [],[]
    for index, row in a.iterrows():
        state = row['Административный округ']
        if state in state_list3:
            f = street_in_Mkad(row)
            c1.append(f[0])
            c2.append(f[1])
            c3.append(f[2])
            c4.append(f[3])
            c5.append(f[4])
            c6.append(f[5])
        if state in state_list1:
            g = street_zelenog(row)
            c1.append(g[0])
            c2.append(g[1])
            c3.append(g[2])
            c4.append(g[3])
            c5.append(g[4])
            c6.append(g[5])
        if state in state_list2:
            v = street_new_moscow(row)
            c1.append(v[0])
            c2.append(v[1])
            c3.append(v[2])
            c4.append(v[3])
            c5.append(v[4])
            c6.append(v[5])
    a['street'] = c1
    a['house'] = c2
    a['building'] = c3
    a['nc'] = c4
    a['oktmo'] = c5
    a['type_to'] = c6
    a['obxod'] = pd.to_datetime(a['Дата последнего обхода/АБО'],dayfirst = True) #переформатируем столбец из строки в дату
    a['street'] = a['street'].str.replace('Ё', 'Е').str.upper() #замена букв в улицах
    a['total'] = a['Сумма сбора, руб.'].str.replace(' ', '')
    y = filename1.strip('/')[:-5]+'_проверено на уведомления и патенты'+'.xlsx'


    b = pd.read_sql("SELECT `C_INN`, `C_OBJECT_TYPE`, `C_OBJECT_ID`, `C_MARK_NOTICE`, `C_TRADE_KIND`, `C_STREET`, `C_ADMINISTRATIVE_DISTRICT`, `C_ROOM`, `C_OKTMO`, `C_CITY`, `C_LOCALITY`, `C_REGION`, `C_HOUSE`, `C_BUILDING`, `C_IGNORING_TYPE`, `ACT_NUMBER`, `C_STOP_USING_DATE`, `C_USE_OBJECT_EMERGENCE_DATE`, `C_QUARTER_FEE`,`C_OBJECT_ID`, `C_OBJECT_ID` as `index`    from `tc_1`", con=file_ТС_1())
    t = []
    street_with_number = pd.read_csv("Z:\\ТС\\Сбор информации\\Сотрудники\\Андрей Ю\\python\\lists\\street_with_number.csv")
    street_with_number = [[street_with_number.loc[i][1], str(street_with_number.loc[i][2])] for i in range(len(street_with_number))]
    for index, row in b.iterrows():
        addr = row['C_STREET']
        for p in street_with_number:
            if not pd.isna(addr):      
                addr = addr.replace(p[0], p[1])
        t.append(addr)

    b['Улица'] = t
    street = []
    for index, row in b.iterrows():
        addr = str(row['Улица']) + '--'+ str(row['C_ADMINISTRATIVE_DISTRICT']) + '--' + str(row['C_ROOM'])+ '--' + str(row['C_CITY'])+ '--' + str(row['C_LOCALITY'])+ '--' + str(row['C_REGION'])+ '--'+ str(row['C_HOUSE'])+ '--' + str(row['C_BUILDING'])
        street.append(addr)
    b['Улица'] = street
    b['Улица'] = b['Улица'].str.upper() #замена маленьких букв на большие
    b['Улица'] = b['Улица'].str.replace('Ё', 'Е') #замена букв в улицах
    b['ANNULEMENT'] = b['C_IGNORING_TYPE'].str.len()
    b['АКТ'] = b['ACT_NUMBER'].str.len()
    b['date_stop'] = pd.to_datetime(b['C_STOP_USING_DATE'],dayfirst = True) #переформатируем столбец дата прекращения из строки в дату
    b['date_begin'] = pd.to_datetime(b['C_USE_OBJECT_EMERGENCE_DATE'], format='%d.%m.%Y', errors='coerce') #переформатируем столбец дата возникновения из строки в дату
    b = b[~b['date_begin'].isna()] # ~ работает как not"""
    b = b.set_index('index')


    s = pd.read_sql("SELECT `index`, `INN`, `STREET`, `DATE_STOP_PATENT`, `DATE_START_PATENT`, `DATE_LOSS_PATENT`, `DATE_CESSATION_PATENT`, `DATE_STOP_USE_PATENT`, `HOUSE`, `KORP` FROM PSN WHERE DATE_START_PATENT > '2021-12-31'", con=file_ТС_1())
    street_with_number = pd.read_csv("Z:\\ТС\\Сбор информации\\Сотрудники\\Андрей Ю\\python\\lists\\street_with_number.csv")
    street_with_number = [[street_with_number.loc[i][1], str(street_with_number.loc[i][2])] for i in range(len(street_with_number))]
    t_psn = []
    replace_list1 = [['Тысяча Девятьсот', '1905'], ['Десятилетия', '10'], ['10-летия', '10'], ['Восьмисотлетия', '800'], ['800-летия', '800'], ['Двадцати Шести', '26'], ['26-ти', '26'], ['Тысяча Восемьсот', '1812'], ['1 Мая', '1'], ['Сорок', '40'], ['Пятьдесят', '50'], ['60-летия', '60'], ['Шестидесятилетия', '60'], ['Восьмого', '8'], ['Девятого', '9']]
    for index, row in s.iterrows():
        addr = row['STREET']
        for p in street_with_number:
            if not pd.isna(addr):      
                addr = addr.replace(p[0], p[1])
        t_psn.append(addr)
    s['Улица'] = t_psn
    s['Улица'] = s['Улица'].str.upper() #замена маленьких букв на большие
    s['Улица'] = s['Улица'].str.replace('Ё', 'Е') #замена букв в улицах
    s = s.set_index('index')


    ecxn = pd.read_sql("SELECT `ИНН`, `ДатаНачЕСХН`, `ДатаКонЕСХН` FROM ESHN", con=file_ТС_1())
    
    new_col = []
    new_col1 = []
    new_col2 = []
    new_col3 = []
    for index, row in a.iterrows():
        inn = row['ИНН']
        if len(inn) == 11:
            inn = "0" + inn
        street = row['street']
        house = row['house']
        building = row['building']
        go = row['obxod']
        kvartal = row['obxod'].quarter
        status = row['nc']
        kind_obct = row['Вид объекта']
        type_obct = row['Тип ТО']
        total = row['total']
        total = str(int(total) - 1000)
        oktmo = row['oktmo']
        type_to = row['type_to']
        result = b[b['C_INN'] == inn]
        if street == None:
            pass
        else:
            result = result[result['Улица'].str.contains(street, na = False)]
        if house == None: 
            pass
        else:
            result = result[result['C_HOUSE'].str.contains(house, na = False)]
        if building == None:
            pass
        else:
            result = result[result['C_BUILDING'].str.contains(building, na = False)]

        if status == None:
            itog = result[result['C_MARK_NOTICE']=='2']
            if len(itog) == 0:
                itog = result[result['C_MARK_NOTICE']=='1']
        else:
            itog = result[result['C_MARK_NOTICE']=='2']
            itog = itog[itog['C_TRADE_KIND'].str.contains(type_to, na = False)]
            if len(itog) == 0:
                itog = result[result['C_MARK_NOTICE']=='1']
                itog = itog[itog['C_TRADE_KIND'].str.contains(type_to, na = False)]

        itog = itog[(itog['date_begin'] <= go) | ((itog['date_begin'].dt.year == go.year) & (itog['date_begin'].dt.quarter == go.quarter))] #смотрим, подходит ли дата возникновения объекта под обход
        itog = itog[(itog['date_stop'] >= go) | itog['date_stop'].isna() | ((itog['date_stop'].dt.year == go.year) & (itog['date_stop'].dt.quarter == go.quarter))] #смотрим, подходит ли дата снятия объекта под обход, если снятия нет то False
        itog = itog[itog['ANNULEMENT'].isna()] #если есть анулированные уведомления, то False


        #If not street, building, house - we are finding in oktmo
        if len(itog) == 0 and kind_obct != "Вендинговый автомат" and status == None and type_obct == "Нестационарные торговые объекты":
            okt = b[b['C_INN'] == inn]
            okt = okt[okt["C_OKTMO"] == oktmo]

            if status == None:
                result_oktmo = okt[okt['C_MARK_NOTICE']=='2']
                if len(result_oktmo) == 0:
                    result_oktmo = okt[okt['C_MARK_NOTICE']=='1']
            else:
                result_oktmo = okt[okt['C_MARK_NOTICE']=='2']
                result_oktmo = result_oktmo[result_oktmo['C_TRADE_KIND'].str.contains(type_to, na = False)]
                if len(result_oktmo) == 0:
                    result_oktmo = okt[okt['C_MARK_NOTICE']=='1']
                    result_oktmo = result_oktmo[result_oktmo['C_TRADE_KIND'].str.contains(type_to, na = False)]

            result_oktmo = result_oktmo[(result_oktmo['date_begin'] <= go) | ((result_oktmo['date_begin'].dt.year == go.year) & (result_oktmo['date_begin'].dt.quarter == go.quarter))] #смотрим, подходит ли дата возникновения объекта под обход
            result_oktmo = result_oktmo[(result_oktmo['date_stop'] >= go) | result_oktmo['date_stop'].isna() | ((result_oktmo['date_stop'].dt.year == go.year) & (result_oktmo['date_stop'].dt.quarter == go.quarter))] #смотрим, подходит ли дата снятия объекта под обход, если снятия нет то False
            result_oktmo = result_oktmo[result_oktmo['ANNULEMENT'].isna()] #если есть анулированные уведомления, то False
        else:
            result_oktmo = []


        result1 = s[s['INN'] == inn]
        if street == None: # ищем улицу, если пустое значение в графе улица (таблица а), то False
            pass
        else:
            result1 = result1[result1['Улица'].str.contains(street, na = False)]
        if house == None: # ищем дом, если пустое значение в графе дом (таблица а), то ничего не делаем
            pass
        else:
            result1 = result1[result1['HOUSE'].str.contains(house, na = False)]
        if building == None:
            pass
        else:
            result1 = result1[result1['KORP'].str.contains(building, na = False)]
        result1 = result1[(result1['DATE_START_PATENT'] <= go)]  #смотрим, подходит ли дата начала ТД объекта под обход
        result1 = result1[(result1['DATE_STOP_PATENT'] >= go)] #смотрим, подходит ли дата дата прекращения ТД под обход, если снятия нет то False
        result1 = result1[(result1['DATE_LOSS_PATENT'] > go) | result1['DATE_LOSS_PATENT'].isna()] #ищем дату потери, если есть
        result1 = result1[(result1['DATE_CESSATION_PATENT'] > go) | result1['DATE_CESSATION_PATENT'].isna()] #ищем дату прекращения, если есть
        result1 = result1[(result1['DATE_STOP_USE_PATENT'] > go) | result1['DATE_STOP_USE_PATENT'].isna()]

        result2 = ecxn[ecxn['ИНН'] == inn]
        result2 = result2[(result2['ДатаНачЕСХН'] <= go)]
        result2 = result2[(result2['ДатаКонЕСХН'] >= go) | result2['ДатаКонЕСХН'].isna()]

        if len(result1) != 0:
            new_col2.append("Да")
            result1['DATE_START_PATENT'].values[-1] = str(result1['DATE_START_PATENT'].values[-1])
            result1['DATE_STOP_PATENT'].values[-1] = str(result1['DATE_STOP_PATENT'].values[-1])
            new_col1.append('c ' + result1['DATE_START_PATENT'].values[-1] +' по '+ result1['DATE_STOP_PATENT'].values[-1])
        else:
            new_col2.append("Нет") 

        if len(result2) != 0:
            new_col3.append("Да")
        else:
            new_col3.append("Нет")


        if len(itog) != 0 or len(result_oktmo) != 0:
            print(inn, street,house,building)
            print(itog[['C_USE_OBJECT_EMERGENCE_DATE', 'C_STOP_USING_DATE']].rename({'C_USE_OBJECT_EMERGENCE_DATE':'ДатаВозникн','C_STOP_USING_DATE':'ДатаПрекр' }, axis='columns'))
            new_col.append('Есть уведомление')

            if new_col2[-1] == 'Да':
                continue
            else:
                if len(result_oktmo) == 0:
                    x = itog['C_USE_OBJECT_EMERGENCE_DATE'].values[-1]
                else:
                    x = result_oktmo['C_USE_OBJECT_EMERGENCE_DATE'].values[-1]
                new_col1.append('Действует с '+x)
        else:
            new_col.append('Нет уведомления')
            if len(new_col1) == int(index)+1:
                pass
            else:
                new_col1.append(' ')

        if len(itog) != 0:
            b = b.drop(itog.index[-1])
        if len(result_oktmo) != 0:
            b = b.drop(result_oktmo.index[-1])
        if len(result1) != 0:
            s = s.drop(result1.index[-1])
        else:
            pass




    a['Уведомление'] = new_col #cоздаем колонку в "а" и присваиваем рузульты списка new_col
    a['Патент'] = new_col2
    a['ЕСХН'] = new_col3
    a['Комментарий'] = new_col1
    cols = list(a)
    cols.insert(1, cols.pop(cols.index('Уведомление')))
    cols.insert(2, cols.pop(cols.index('Патент')))
    cols.insert(3, cols.pop(cols.index('ЕСХН')))
    cols.insert(4, cols.pop(cols.index('Комментарий')))
    a = a.loc[:, cols]
    a.to_excel(y, index=False)
    

open_button = ttk.Button(root, text='Загрузить Excel файл "Список проверяемых объектов"', command=file_AIC_OPN)
open_button.pack(expand=True)

open_button = ttk.Button(root, text= "Подключится к базе данных", command=file_ТС_1)
open_button.pack(expand=True)


open_button1 = ttk.Button(root, text='START', command=lambda:[start_TC_1()])
open_button1.pack(expand=True)



root.mainloop()

# In[ ]:
