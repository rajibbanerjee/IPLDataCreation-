#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Uncoment the line below lines one by one to install the respective packages
#pip install pyyaml
#pip install pandas
#pip install numpy


# Global variable decleration

# In[3]:


# Change the DATA_PATH variable where you unzipped the files
DATA_PATH = "F:/workdir/IMP-INFO/AI/Final_Study_Plan/IITM-BSC/Hackathon/Data/ipl"

# Change the OUTPUT_PATH variable where you want to place the output file
OUTPUT_PATH = "F:/workdir/IMP-INFO/AI/Final_Study_Plan/IITM-BSC/Hackathon/Data/"


# import modules/packages

# In[4]:


import os
import yaml
import pandas as pd
import numpy as np


# Methods

# In[13]:


def get_score_card_template(num_cols=200):
    deliveries_template = list(np.round((np.linspace(0, 20, num_cols, endpoint=False)), 2))
    zero_runs_template = list(np.zeros(num_cols))
    score_card_template = dict(zip(deliveries_template, zero_runs_template))
    return score_card_template





def get_match_info_2(filtered_info, content, innings='1st innings'):
    match_info = {k:v for k,v in content['info'].items() if k in filtered_info}
    if innings == '1st innings':
        #match_info['Innings'] = 1
        match_info['Target'] = 0
    
    if innings =='2nd innings':
        deliveries = content['innings'][0]['1st innings']['deliveries']
        target = np.sum([v['runs']['total'] for delivery in deliveries for k,v in delivery.items()])
        match_info['Target'] = target
        
    return match_info

# Changed the arguement
def get_run_per_balls_2(content, innings='1st innings'):
    run_per_balls = {}
    if innings == '1st innings':
        list_of_deliveries = content['innings'][0][innings]['deliveries']
        run_per_balls = {k:v['runs']['batsman'] for delivery in list_of_deliveries for k,v in delivery.items() }
    
    if innings == '2nd innings' and len(content['innings']) > 1:
        list_of_deliveries = content['innings'][1][innings]['deliveries']
        run_per_balls = {k:v['runs']['batsman'] for delivery in list_of_deliveries for k,v in delivery.items() }
     
    return run_per_balls
        
    
    
def get_row_2(content):
    # Ist innings
    score_card_template_1 = get_score_card_template()
    filtered_info = ['city', 'dates', 'outcome', 'player_of_match', 'teams', 'toss', 'umpires', 'venue']
    match_info_1st = get_match_info_2(filtered_info, content)
    run_per_balls = get_run_per_balls_2(content)
    score_card_template_1.update(run_per_balls)
    match_info_1st.update(score_card_template_1)
    
    #2nd innings
    
    score_card_template_2 = get_score_card_template()
    match_info_2nd = get_match_info_2(filtered_info, content, innings='2nd innings')
    run_per_balls = get_run_per_balls_2(content, innings='2nd innings')
    score_card_template_2.update(run_per_balls)
    match_info_2nd.update(score_card_template_2)
    
    return [match_info_1st, match_info_2nd]

def get_dataframe_2(yaml_contents):
    L = []
    for c in yaml_contents:
        L = L + get_row_2(c)
    
    return pd.DataFrame(L)


# In[6]:


files = os.listdir(DATA_PATH)
yaml_contents = []
for file in files:
    with open(DATA_PATH+"/"+file, 'r') as f:
        #content = yaml.load(f)
        yaml_contents.append(yaml.load(f))
        print("Processing....."+f.name.split('/')[-1])
        
          
print("Total files processed: ".format(len(yaml_contents)))


# In[14]:


pd.set_option('display.max_columns', 209)
contents  = yaml_contents[:821]
df = get_dataframe_2(contents)
df.to_csv(OUTPUT_PATH+'/overall_score.csv')
df.tail(5)


# In[ ]:




