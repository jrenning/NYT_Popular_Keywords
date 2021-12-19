import config 
import json
import requests 
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import re

url = f'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={config.API_KEY}'
response1 = requests.get(url).json()


popular_titles = []

for i in range(len(response1['results'])):
    popular_titles.append(response1['results'][i]['title'])


'''for i in range(len(popular_titles)):
    print(f'{i+1}. {popular_titles[i]}')'''


'''print(response1['results'][1].keys())
    print(response1['results'][1]['adx_keywords'])'''


popular_keywords = []

for i in range(len(response1['results'])):
    popular_keywords.append(response1['results'][i]['adx_keywords'])


'''for i in range(len(popular_keywords)):
        print(f'{i+1}. {popular_keywords[i]}')'''

popular_keywords_list = []
popular_keywords_list2 = []
popular_keywords_list3 = []


# seperate keywords 
for i in range(len(popular_keywords)):
    popular_keywords_list.append(popular_keywords[i].split(';'))

# flatten lists 
for lists in popular_keywords_list:
    for items in lists:
        popular_keywords_list2.append(items)

for i in range(len(popular_keywords_list2)):
    popular_keywords_list3 += (popular_keywords_list2[i].split())
    
popular_keywords_list3 = (sorted(popular_keywords_list3))
keyword_count = dict(Counter(popular_keywords_list3))

keyword_count2 = dict(sorted(keyword_count.items(),key=lambda item: item[1]))

# matching that gets rid of special characters and common keywords 
for key in keyword_count2.copy():
    if re.search("^\W",key):
        keyword_count2.pop(key)
    elif key == 'and' or key == 'of':
        keyword_count2.pop(key)


keys = list(keyword_count2)[-10:]
values = list(keyword_count2.values())[-10:]

for i in range(len(keys)):
    print(f'{i+1}. {keys[-(i+1)]} was a keyword {values[-(i+1)]} times in the popular NYT articles today')

figure(figsize=(12,9), dpi=80)
bar = plt.bar(keys,values)
plt.xlabel('Key Words')
plt.ylabel('Occurances of Word')
plt.title('Most Popular Keywords in Top 20 NYT Articles')



plt.show()




    


