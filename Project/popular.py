import config 
import requests 
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import re

url = f'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={config.API_KEY}'
response1 = requests.get(url).json()


def sort_data(response,response_key,delimter=None):
    response_list = []
    for i,_ in enumerate(response['results']):
        response_list.append(response['results'][i][response_key])
       
    if response_key == 'adx_keywords':
        response_string_list = str(response_list).split(delimter)
        response_string_list = str(response_string_list).split()
        return response_string_list
    
    return response_list
    

def clean_data(response_string_list):
    
    keyword_count = dict(Counter(response_string_list))
    
    sorted_keyword_count = dict(sorted(keyword_count.items(),key=lambda item: item[1]))
    
    for key in sorted_keyword_count.copy():
        if re.search("^\W",key):
            sorted_keyword_count.pop(key)
        elif key == 'and' or key == 'of' or key=='the':
            sorted_keyword_count.pop(key)
                
    return sorted_keyword_count


title_response_string_list = sort_data(response1,'title')
print('Popular Titles')
for i,_ in enumerate(title_response_string_list):
    print(f'{i+1}. {title_response_string_list[i]}')

keyword_response_string_list = sort_data(response1,'adx_keywords',';')
sorted_keyword_count = clean_data(keyword_response_string_list)


keys = list(sorted_keyword_count)[-10:]
keys = [re.sub(r'\W','',key) for key in keys]   

    
values = list(sorted_keyword_count.values())[-10:]

print('\n')
for i,_ in enumerate(keys):
    print(f'{i+1}. {keys[-(i+1)]} was a keyword {values[-(i+1)]} times in the popular NYT articles today')

figure(figsize=(12,9), dpi=80)
bar = plt.bar(keys,values)
plt.xlabel('Key Words')
plt.ylabel('Occurances of Word')
plt.title('Most Popular Keywords in Top 20 NYT Articles Today')



plt.show()




    


