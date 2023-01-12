#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 09:39:48 2021

@author: victorpokorny
"""
filename = '/put/path/then/filenamehere'
import textract
import pandas as pd
text = textract.process(filename+'.pdf', encoding='ascii')
text = text.decode()
pattern = '\ny\n\nl\ni\n\na\nD\n\ns\n\nl\nl\ni\n\n \n\nk\nS\ne\nv\ni\nt\n\np\na\nd\nA'
idx = text.find(pattern)
smol_text = text[idx+len(pattern):idx+len(pattern)+200]
no_n = smol_text.split('\n')
scores = list(filter(lambda x: x.isalnum(), no_n))
#there are 18 fields
t_scores = scores[0:18]

labels = ['Hyperactivity',
           'Aggression',
           'Conduct Problems',
           'Externalizing Problems',
           'Anxiety',
           'Depression',
           'Somatization',
           'Internalizing Problems',
           'Attention Problems',
           'Atypicality',
           'Withdrawal',
           'Behavior Symptoms Index',
           'Adaptability',
           'Social Skills',
           'Leadership',
           'Functional Communication',
           'Activities of Daily Living',
           'Adaptive Skills']

sig = []
i = 0
for scor in t_scores:
    if i < 14 and int(scor) > 69:
        sig.append('Clinically Significant**')
    elif i<14 and int(scor) <70 and int(scor) > 59:
        sig.append('At-Risk*')
    elif i<14 and int(scor) <60:
        sig.append('Normal')
    elif i>13 and int(scor) <31:
        sig.append('Clinically Significant**')
    elif i>13 and int(scor) >30 and int(scor) < 41:
        sig.append('At-Risk*')
    elif i>13 and int(scor) >40:
        sig.append('Normal')
    i = i+1

d = {'Composite Scales':labels, 'Rating': t_scores, 'Description': sig }
d1 = {'Composite Scales':'Scale Score Summary', 'Rating': '', 'Description': '' }
d2 = {'Composite Scales':'Adaptive Scales', 'Rating': '', 'Description': '' }


final = pd.DataFrame(d)
final = final.append(d1, ignore_index = True)
final = final.append(d2, ignore_index = True)
#reorganize to fit template
final = final.reindex([3,7,11,17,18,0,1,2,4,5,6,9,10,8,19,12,13,14,16,15])
final.to_csv(filename+'.csv')



