#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 09:39:48 2021
NOTE THAT THERE ARE CHILD AND ADOLESCENT VERSIONS OF THE TEST! MAKE SURE YOU ARE RUNNING THE RIGHT SCRIPT

@author: victorpokorny
"""
filename = '/put/path/then/filenamehere' # 
import textract
import pandas as pd
text = textract.process(filename+'.pdf', encoding='ascii')
text = text.decode()
pattern = '\n\ns\nr\ne\nh\nc\na\ne\nT\no\n\n \n\nt\n \n\ne\nd\nu\n\nt\ni\nt\nt\n\nA\n'
idx = text.find(pattern)
if idx == -1:
    pattern = '\nA\n\nj\n\nl\n\na\nn\no\ns\nr\ne\nP'
    idx = text.find(pattern)
smol_text = text[idx+len(pattern):idx+len(pattern)+800]
no_n = smol_text.split('\n')
scores = list(filter(lambda x: x.isnumeric(), no_n))
#there are 18 fields
t_scores = scores[0:21]

#switched first two around because the decoding got messed up
labels = ['Attitude to School',
           'Attitude to Teachers',
           'Sensation Seeking',
           'School Problems',
           'Atypicality',
           'Locus of Control',
           'Social Stress',
           'Anxiety',
           'Depression',
           'Sense of Inadequacy',
           'Somatization',
           'Internalizing Problems',
           'Attention Problems',
           'Hyperactivity',
           'Inattention/Hyperactivity',
           'Emotional Symptom Index',
           'Relations with Parents',
           'Interpersonal Relations',
           'Self-Esteem',
           'Self-Reliance',
           'Personal Adjustment']

sig = []
i = 0
for scor in t_scores:
    if i < 15 and int(scor) > 70:
        sig.append('Clinically Significant**')
    elif i<15 and int(scor) <71 and int(scor) > 59: 
        sig.append('At-Risk*')
    elif i<15 and int(scor) <60:
        sig.append('Normal')
    elif i>14 and int(scor) <31:
        sig.append('Clinically Significant**')
    elif i>14 and int(scor) >30 and int(scor) < 41:
        sig.append('At-Risk*')
    elif i>14 and int(scor) >40:
        sig.append('Normal')
    else:
        print('something is wrong')
    i = i+1

d = {'Composite Scales':labels, 'Rating': t_scores, 'Description': sig }
d1 = {'Composite Scales':'Scale Score Summary', 'Rating': '', 'Description': '' }
d2 = {'Composite Scales':'Adaptive Scales', 'Rating': '', 'Description': '' }


final = pd.DataFrame(d)
final = final.append(d1, ignore_index = True)
final = final.append(d2, ignore_index = True)
#reorganize to fit template
final = final.reindex([3,11,14,15,20,21,0,1,4,5,6,7,8,9,10,12,13,2,22,16,17,18,19])
final.to_csv(filename+'.csv')



