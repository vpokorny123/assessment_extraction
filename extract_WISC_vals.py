#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 09:39:48 2021

@author: victorpokorny
"""
def num(s):
    """ 3.0 -> 3, 3.001000 -> 3.001 otherwise return s """
    s = str(s)
    try:
        int(float(s))
        return s.rstrip('0').rstrip('.')
    except ValueError:
        return s

filename = '/put/path/then/filenamehere'
import textract
import pandas as pd
text = textract.process(filename+'.pdf', encoding='ascii')
text = text.decode()

# get composite scores first
pattern = 'Composite Score Summary' 
idx = text.find(pattern)

smol_text = text[idx+len(pattern):idx+len(pattern)+2000]
no_n = smol_text.split('\n')
scores = list(filter(lambda x: x.isalnum(), no_n))
#there are 18 fields
comp_scores = scores[17:23]
comp_percentiles = scores[23:29]
comp_classify = [x for x in no_n if x in ["Average", "Low Average","Extremely Low", "High Average", "Very Low"]]

# then get subtest scores
pattern = 'Age\nEquivalent' 
idx = text.find(pattern)
smol_text = text[idx+len(pattern):idx+len(pattern)+500]
no_n = smol_text.split('\n')

res = []
nope = []
for ele in no_n:
    try:
        res.append(float(ele))
    except ValueError:
        nope.append(ele)
        
#scores = list(filter(lambda x: x.isdigit(), no_n))
scores = res
subtest_scores = scores[10:20]
subtest_percentiles = scores[20:30]
subtest_classify = [' '] * 10


# stack em on top of each other
all_scores = comp_scores + [int(x) for x in subtest_scores]
all_percentiles = [num(float(i)) for i in comp_percentiles] + [num(i) for i in subtest_percentiles]
all_classify = comp_classify + subtest_classify
  
labels = ['Verbal Comprehension',
          'Visual Spatial',
          'Fluid Reasoning',
          'Working Memory',
          'Processing Speed',
          'FSIQ',
          'Similarities',
          'Vocabulary',
          'Block Design',
          'Visual Puzzles',
          'Matrix Reasoning',
          'Figure Weights',
          'Digit Span',
          'Picture Span',
          'Coding',
          'Symbol Search'
          ]

d = {'Subtest/Index':labels, 'Scaled and Index Scores': all_scores, 
     'Percentile Rank': all_percentiles, 'Classification': all_classify }

final = pd.DataFrame(d)
#reorganize to fit template
final = final.reindex([0,6,7,
                       1,8,9,
                       2,10,11,
                       3,12,13,
                       4,14,15,
                       5])
final.to_csv(filename+'.csv')



