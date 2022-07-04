import config 
import requests 
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import re



def sort_data(response,response_key,delimter=None):
    response_list = []
    for i,_ in enumerate(response['results']):
        response_list.append(response['results'][i][response_key])
    # split on specified delimter and then on whitespace to get every word
    if response_key == 'adx_keywords':
        response_string_list = str(response_list).split(delimter)
        response_string_list = str(response_string_list).split()
        return response_string_list
    
    return response_list
    

def clean_data(response_string_list):
    
    keyword_count = dict(Counter(response_string_list))
    
    # sorts by number of occurances 
    sorted_keyword_count = dict(sorted(keyword_count.items(),key=lambda item: item[1],reverse=True))
    
    
    # remove stop words and non-alphanumeric words ie just symbols 
    for key in sorted_keyword_count.copy():
        if re.search("^\W",key):
            sorted_keyword_count.pop(key)
        elif key == 'and' or key == 'of' or key=='the':
            sorted_keyword_count.pop(key)
        # remove samll keys 
        elif len(key) < 3:
            sorted_keyword_count.pop(key)
                
    return sorted_keyword_count

def get_popular_titles(base_response):
    # print popular titles 
    title_response_string_list = sort_data(base_response,'title')
    print('Popular Titles')
    for i,_ in enumerate(title_response_string_list):
        print(f'{i+1}. {title_response_string_list[i]}')


def get_keywords(base_response):
    # split by semicolons and then spaces 
    keyword_response_string_list = sort_data(base_response,'adx_keywords',';')
    sorted_keyword_count = clean_data(keyword_response_string_list)
    return sorted_keyword_count

def get_top_keywords(sorted_keyword_count,top_number):
    # get last ten entries as list is sorted in reverse
    top_keywords = list(sorted_keyword_count)[:top_number]
    # remove symbols and other non-alphanumeric
    top_keywords = [re.sub(r'\W','',key) for key in top_keywords]   
    # get top counts 
    top_counts = list(sorted_keyword_count.values())[:top_number]
    
    return top_keywords,top_counts


def summarize_keywords(top_keywords,top_counts):

    print('\n')
    for i,_ in enumerate(top_keywords):
        print(f'{i+1}. {top_keywords[i]} was a keyword {top_counts[i]} times in the popular NYT articles today')


def plot_keywords(top_keywords,top_counts,top_number):

    figure(figsize=(12,9), dpi=80)
    bar = plt.bar(top_keywords,top_counts)
    # make labels vertical so they don't overlap
    plt.xticks(top_keywords,rotation='vertical')
    plt.xlabel('Key Words')
    plt.ylabel('Occurances of Word')
    plt.title(f'Most Popular Keywords in the top {top_number} NYT Articles Today')
    plt.show()

def main():
    TOP_NUMBER = 20
    
    url = f'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={config.API_KEY}'
    
    base_response = requests.get(url).json()
    get_popular_titles(base_response)
    sorted_keyword_count = get_keywords(base_response)
    top_keywords,top_counts = get_top_keywords(sorted_keyword_count,TOP_NUMBER)
    summarize_keywords(top_keywords,top_counts)
    plot_keywords(top_keywords,top_counts,TOP_NUMBER)


if __name__ == "__main__":
    main()
    




    



    




    


