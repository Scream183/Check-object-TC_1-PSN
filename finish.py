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

def clean_house(r):
    for v in r:
        if v.upper() in ",/ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ":
            r = r.replace(v,"").strip()
    return r

def street_in_Mkad(row):
    replace_list = [['Тысяча Девятьсот', '1905'], ['Десятилетия', '10'], ['10-летия', '10'], ['Восьмисотлетия', '800'], ['800-летия', '800'], ['Двадцати Шести', '26'], ['26-ти', '26'], ['Тысяча Восемьсот', '1812'], ['1 Мая', '1'], ['Сорок', '40'], ['Пятьдесят', '50'], ['60-летия', '60'], ['Шестидесятилетия', '60'], ['Восьмого', '8'], ['Девятого', '9']]
    replace_list2 = [[',',""], ['/','']]
    addr = row['Адрес ТО'] #ищем улицу
    for p in replace_list:
        addr = addr.replace(p[0], p[1])
    street = addr.split(',')[1]
    _p = street.split(' ')
    if 'квартал 113А' in addr or 'квартал 114А' in addr:
        g = 'ВОЛЖСКИЙ'
    elif 'МКАД' in addr:
        g = 'МКАД'
    elif not has_type_street(addr):
        g = _p[1].upper()
    else:
        g = _p[2].upper()
    nto = row['Тип ТО']
    if addr.find('дом') == -1 and nto == 'Стационарные торговые объекты': # ищем дом
        r = addr.split(',')[2].strip()
    elif nto == 'Нестационарные торговые объекты':
        r = None
    elif addr.find('дом') > 0:
        house = addr.find('дом') + 4
        r = addr[house:house+2].strip()
        if r.isdigit() == False:
            r = clean_house(r)
    if 'Волжский' in addr:
        r = None
    building = None 
    status = row['Статус для целей обложения ТС']
    if 'Недостоверные' in status:
        nc = status
    else:
        nc = None
    oktmo = row['Муниципальный район']
    if nto == 'Нестационарные торговые объекты':
        oktmo = OKTMO(oktmo)
    return g, r, building, nc, oktmo
def street_zelenog(row):
    state = row['Административный округ']
    state_list1 = ['ЗелАО']
    addr = row['Адрес ТО'] #ищем улицу
    if (state in state_list1) and ('Зеленоград' in addr) and (not 'корпус' in addr):
        street = addr.split(',')[2]
        _p = street.split(' ')
        t = _p[2].upper()
    elif 'ж.д.' in addr:
        street = addr.split(',')[2]
        _p = street.split(' ')
        t = _p[0].upper()
    elif (state in state_list1) and (not 'Зеленоград' in addr):
        street = addr.split(',')[1]
        _p = street.split(' ')
        t = _p[2].upper()
    else:
        t = None
    nto = row['Тип ТО']
    house = addr.find('дом') # ищем дом
    if house == -1 or nto == 'Нестационарные торговые объекты':
        v = None
    else:
        house = addr.find('дом')+4 
        v = addr[house:house+2]
        if v.isdigit() == False:
            v = clean_house(v)
    building = addr.find('корпус')
    if building == -1 or house > 0: #ищем корпус
        h = None 
    else:
        building = addr.find('корпус')+7
        h = addr[building:building+4]
        if h.isdigit() == False:
            h = clean_house(h)
    status = row['Статус для целей обложения ТС']
    if 'Недостоверные' in status:
        nc = status
    else:
        nc = None
    oktmo = row['Муниципальный район']
    if nto == 'Нестационарные торговые объекты':
        oktmo = OKTMO(oktmo)
            
    return t, v, h, nc, oktmo #возвращаем улицу, дом, корпус
def street_new_moscow(row):
    addr = row['Адрес ТО']
    state = row['Административный округ']
    street = addr.split(',')[1]
    street2 = addr.split(',')[2]
    if has_type_street(street):
        _p = street.split(' ')
        g = _p[2].upper()
        if 'Киевское' in addr and  'Московский' in addr:
            g = 'КИЕВСКОЕ'
        elif 'Калужское' in addr:
            g = 'КАЛУЖСКОЕ'
    elif has_type_street(street2):
        _p = street2.split(' ')
        g = _p[2].upper()
        if 'Калужское' in addr:
            g = 'КАЛУЖСКОЕ'
        elif 'Киевское' in addr:
            g = 'КИЕВСКОЕ'
        elif ('1-й Микрорайон' in addr and 'Московский' in addr): #or ('микрорайон 1-й' in addr and 'Московский' in addr) :
            g = '1'
    elif 'Микрорайон' in street2: #or 'микрорайон' in street2:
        g = 'МИКРОРАЙОН'
    elif 'Киевское' in addr and  'Московский' in addr:
        g = 'КИЕВСКОЕ'
    elif not has_type_street(addr):
        g = None
        if 'МКАД' in addr:
            g = 'МКАД'
    street = addr.find('дом')
    nto = row['Тип ТО']
    if street == -1 or nto == 'Нестационарные торговые объекты':
        house = None
    else:
        street = addr.find('дом')+4
        house = addr[street:street+4]
        if house.isdigit() == False:
            house = clean_house(house)
    building = None
    status = row['Статус для целей обложения ТС']
    if 'Недостоверные' in status:
        nc = status
    else:
        nc = None
    oktmo = row['Муниципальный район']
    if nto == 'Нестационарные торговые объекты':
        oktmo = OKTMO(oktmo)
    return g, house, building, nc, oktmo

def file_AIC_OPN():
    global filename1
    filename1 = fd.askopenfilename()
    showinfo(title='Выбранный файл', message=filename1)
    

def file_ТС_1():
    global filename2
    filename2 = fd.askopenfilename()
    showinfo(title='Выбранный файл', message=filename2)

def file_PSN():
    global filename7
    filename7 = fd.askopenfilename()
    showinfo(title='Выбранный файл', message=filename7)
   
def file_ecxn():
    global filename3
    filename3 = fd.askopenfilename()
    showinfo(title='Выбранный файл', message=filename3)

def start_TC_1():
    a = pd.read_excel(filename1, header = 1, dtype = str)
    state_list1 = ['ЗелАО']
    state_list2 = ['ТАО', 'НАО']
    state_list3 = ['ЦАО', 'САО', 'СВАО', 'ВАО', 'ЮВАО', 'ЮАО', 'ЮЗАО', 'ЗАО', 'СЗАО']
    c1,c2,c3,c4,c5 = [], [], [], [], []
    for index, row in a.iterrows():
        state = row['Административный округ']
        if state in state_list3:
            f = street_in_Mkad(row)
            c1.append(f[0])
            c2.append(f[1])
            c3.append(f[2])
            c4.append(f[3])
            c5.append(f[4])
        if state in state_list1:
            g = street_zelenog(row)
            c1.append(g[0])
            c2.append(g[1])
            c3.append(g[2])
            c4.append(g[3])
            c5.append(g[4])
        if state in state_list2:
            v = street_new_moscow(row)
            c1.append(v[0])
            c2.append(v[1])
            c3.append(v[2])
            c4.append(v[3])
            c5.append(v[4])
    a['street'] = c1
    a['house'] = c2
    a['building'] = c3
    a['nc'] = c4
    a['oktmo'] = c5
    a['obxod'] = pd.to_datetime(a['Дата последнего обхода/АБО'],dayfirst = True) #переформатируем столбец из строки в дату
    a['street'] = a['street'].str.replace('Ё', 'Е') #замена букв в улицах
    a['total'] = a['Сумма сбора, руб.'].str.replace(' ', '')
    y = filename1.strip('/')[:-5]+'_проверено на уведомления и патенты'+'.xlsx'
    
    
    b = pd.read_excel(filename2, header = 0, dtype = str)
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
    	addr = str(row['Улица']) + str(row['C_ADMINISTRATIVE_DISTRICT']) + str(row['C_ROOM']) + str(row['C_CITY']) + str(row['C_LOCALITY']) + str(row['C_REGION'])+ str(row['C_HOUSE']) + str(row['C_BUILDING'])
    	street.append(addr)
    b['Улица'] = street
    b['Улица'] = b['Улица'].str.upper() #замена маленьких букв на большие
    b['Улица'] = b['Улица'].str.replace('Ё', 'Е') #замена букв в улицах
    b['ANNULEMENT'] = b['C_IGNORING_TYPE'].str.len()
    b['АКТ'] = b['ACT_NUMBER'].str.len()
    b['date_stop'] = pd.to_datetime(b['C_STOP_USING_DATE'],dayfirst = True) #переформатируем столбец дата прекращения из строки в дату
    b['date_begin'] = pd.to_datetime(b['C_USE_OBJECT_EMERGENCE_DATE'], format='%d.%m.%Y', errors='coerce') #переформатируем столбец дата возникновения из строки в дату
    b = b[~b['date_begin'].isna()] # ~ работает как not"""
    
    s = pd.read_excel(filename7, header = 0, dtype = str)
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
    s['date_finish'] = pd.to_datetime(s['DATE_STOP_PATENT'],dayfirst = True) #переформатируем столбец дата прекращения из строки в дату
    s['date_begin'] = pd.to_datetime(s['DATE_START_PATENT'],dayfirst = True)
    s['date_loss'] = pd.to_datetime(s['DATE_LOSS_PATENT'], dayfirst = True)
    s['date_cessation'] = pd.to_datetime(s['DATE_CESSATION_PATENT'], dayfirst = True)
    s['stop_use_day'] = pd.to_datetime(s['DATE_STOP_USE_PATENT'], dayfirst = True)
    
    ecxn = pd.read_excel(filename3, header = 0, dtype = str)
    ecxn['date_begin'] = pd.to_datetime(ecxn['ДатаНачЕСХН'], dayfirst = True)
    ecxn['date_stop'] = pd.to_datetime(ecxn['ДатаКонЕСХН'], dayfirst = True)
    
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
            result = result[result['C_MARK_NOTICE'].str.contains('1', na = False)]
        else:
            result = result[result['C_MARK_NOTICE'].str.contains('2', na = False)]
            if len(result) > 1:
                result = result[result['C_MARK_NOTICE'].str.contains('2', na = False)].iloc[-1]
                result = pd.DataFrame([result])
                result = result[result['C_QUARTER_FEE'] >= total]
            else:
                result = result[result['C_QUARTER_FEE'] >= total]
        result = result[(result['date_begin'] <= go) | ((result['date_begin'].dt.year == go.year) & (result['date_begin'].dt.quarter == go.quarter))] #смотрим, подходит ли дата возникновения объекта под обход
        result = result[(result['date_stop'] >= go) | result['date_stop'].isna() | ((result['date_stop'].dt.year == go.year) & (result['date_stop'].dt.quarter == go.quarter))] #смотрим, подходит ли дата снятия объекта под обход, если снятия нет то False
        result = result[result['ANNULEMENT'].isna()] #если есть анулированные уведомления, то False



        if len(result) == 0 and kind_obct != "Вендинговый автомат" and status == None and type_obct == "Нестационарные торговые объекты":
            okt = b[b['C_INN'] == inn]
            okt = okt[okt["C_OKTMO"] == oktmo]
            if status == None:
                okt = okt[okt['C_MARK_NOTICE'].str.contains('1', na = False)]
            else:
                okt = okt[okt['C_MARK_NOTICE'].str.contains('2', na = False)]
                if len(okt) > 1:
                    okt = okt[okt['C_MARK_NOTICE'].str.contains('2', na = False)].iloc[-1]
                    okt = pd.DataFrame([okt])
                    okt = okt[okt['C_QUARTER_FEE'] >= total]
                else:
                    okt = okt[okt['C_QUARTER_FEE'] >= total]
            okt = okt[(okt['date_begin'] <= go) | ((okt['date_begin'].dt.year == go.year) & (okt['date_begin'].dt.quarter == go.quarter))] #смотрим, подходит ли дата возникновения объекта под обход
            okt = okt[(okt['date_stop'] >= go) | okt['date_stop'].isna() | ((okt['date_stop'].dt.year == go.year) & (okt['date_stop'].dt.quarter == go.quarter))] #смотрим, подходит ли дата снятия объекта под обход, если снятия нет то False
            okt = okt[okt['ANNULEMENT'].isna()] #если есть анулированные уведомления, то False
        else:
            okt = []


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
        result1 = result1[(result1['date_begin'] <= go)]  #смотрим, подходит ли дата начала ТД объекта под обход
        result1 = result1[(result1['date_finish'] >= go)] #смотрим, подходит ли дата дата прекращения ТД под обход, если снятия нет то False
        result1 = result1[(result1['date_loss'] > go) | result1['date_loss'].isna()] #ищем дату потери, если есть
        result1 = result1[(result1['date_cessation'] > go) | result1['date_cessation'].isna()] #ищем дату прекращения, если есть
        result1 = result1[(result1['stop_use_day'] > go) | result1['stop_use_day'].isna()]
        
        result2 = ecxn[ecxn['ИНН'] == inn]
        result2 = result2[(result2['date_begin'] <= go)]
        result2 = result2[(result2['date_stop'] >= go) | result2['date_stop'].isna() | ((result2['date_stop'].dt.year == go.year) & (result2['date_stop'].dt.quarter == go.quarter))]
        result2['date_begin'] = result2['date_begin'].dt.strftime('%d.%m.%Y')
        
        if len(result1) != 0:
            new_col2.append("Да")
            new_col1.append('c ' + result1['DATE_START_PATENT'].values[-1] +' по '+ result1['DATE_STOP_PATENT'].values[-1])
        else:
            new_col2.append("Нет")
            
        if len(result2) != 0:
            new_col3.append('Да')
            new_col1.append('c '+ result2['date_begin'].values[-1])
        else:
            new_col3.append('Нет')


        if len(result) != 0 or len(okt) != 0:
            print(inn, street,house,building)
            print(result[['C_USE_OBJECT_EMERGENCE_DATE', 'C_STOP_USING_DATE']].rename({'C_USE_OBJECT_EMERGENCE_DATE':'ДатаВозникн','C_STOP_USING_DATE':'ДатаПрекр' }, axis='columns'))
            new_col.append('Есть уведомление')
            if new_col2[-1] == 'Да':
                continue
            else:
                if len(okt) == 0:
                    x = result['C_USE_OBJECT_EMERGENCE_DATE'].values[-1]
                else:
                    x = okt['C_USE_OBJECT_EMERGENCE_DATE'].values[-1]
                new_col1.append('Действует с '+x)
        else:
            new_col.append('Нет уведомления')
            if len(new_col1) == int(index)+1:
                pass
            else:
                new_col1.append(' ')
        
       



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
    a.to_excel(y)
    
open_button = ttk.Button(root, text='Загрузить Excel файл "Список проверяемых объектов"', command=file_AIC_OPN)
open_button.pack(expand=True)

open_button = ttk.Button(root, text='Загрузить Excel файл "Выгрузка по уведомлениям ТС"', command=file_ТС_1)
open_button.pack(expand=True)

open_button = ttk.Button(root, text='Загрузить Excel файл "Выгрузка по ПСН"', command=file_PSN)
open_button.pack(expand=True)

open_button = ttk.Button(root, text='Загрузить Excel файл "Выгрузка по ЕСХН"', command=file_ecxn)
open_button.pack(expand=True)

open_button1 = ttk.Button(root, text='START', command=lambda:[start_TC_1()])
open_button1.pack(expand=True)



root.mainloop()

   


# In[ ]:




