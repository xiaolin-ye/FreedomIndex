# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 20:30:41 2022

@author: xy
"""

import numpy as np
import pandas as pd
import collections as col
import re
import csv
import random

data = pd.read_excel(r'C:\Users\xy\Desktop\A9\HFI2021.xlsx', header=3, na_values=['-','nan'])

#%%
column_names = data.columns


r_parenthesis = re.compile('\(.*\)')
replaced = [re.sub(r_parenthesis, '', s) for s in column_names]

r_parenthesis = re.compile('\)')
replaced = [re.sub(r_parenthesis, '', s) for s in replaced]


replaced[0:4] = ''

r_indexes = re.compile('^[A-Z]{1}[a-z]*[\s\.]')
titles = [re.sub(r_indexes, '', s) for s in replaced]

titles = [re.sub('[,:/]', ' ', s) for s in titles]

words = [word.capitalize() for line in titles for word in line.split()]

words_count = col.Counter(words)

ignore = ['Of','From','&','And','To', 'In', 'A', 'The','For']
for word in ignore:
    if word in words_count:
        del words_count[word]

with open('word_counter.csv','w') as csvfile:
    writer=csv.writer(csvfile)
    for key, value in words_count.items():
        writer.writerow([key] + [value] + list(str(random.randrange(10))))

 
#%%

last_year_summary = data[data['Year'] == 2019][
    ['Countries','ISO', 'Region','HUMAN FREEDOM',
     'HUMAN FREEDOM (QUARTILE)', 'PERSONAL FREEDOM (SCORE)',
     'ECONOMIC FREEDOM (SCORE)'
     ]]

last_year_summary.to_csv('last_year_summary.csv')

#%%

yearly_summary = data[
    ['Year', 'Countries', 'Region','HUMAN FREEDOM',]]

yearly_summary = yearly_summary.pivot_table('HUMAN FREEDOM', ['Countries', 'Region'], 'Year')

yearly_summary.to_csv('yearly_summary.csv')


#%%

yearly_evolution_3metrics = data[['Year', 'Countries',
                                  'HUMAN FREEDOM','PERSONAL FREEDOM (SCORE)',
                                  'ECONOMIC FREEDOM (SCORE)' ]]


yearly_evolution_3metrics.to_csv('yearly_evolution_3metrics.csv')

#%%

r_maincategories = re.compile('^[A-Z]{1}[\s]{1}')
titles = [s for s in replaced if re.match(r_maincategories, s)]

country_titles = ['Year', 'Countries']

personal_freedom_socres = data[country_titles + titles[0:7]]
personal_freedom_socres['Category'] = 'Personal Freedom'

economic_freedom_scores =data[country_titles + titles[7:]]
economic_freedom_scores['Category'] = 'Economic Freedom'

personal_freedom_socres.to_csv('personal_freedom_scores.csv')
economic_freedom_scores.to_csv('economic_freedom_scores.csv')



