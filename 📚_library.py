import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud 

# Streamlit is a cool library that allows you to create web apps with python
# It support matplotlib.pyplot which wordcloud uses

# This app is hosted and available at : 

# See other project : https://mathisdrn-fuel-consumption-app---main-langb4.streamlit.app/
# To run locally : 
# > pip install streamlit
# > streamlit run 📚_library.py

st.title('📚 Library')

def display_res(result):
    # Wordcloud for 1st result
    word_list = result['keywords'][0].split()
    word_list = [w for w in word_list if w not in stopwords]     
    wordcloud = WordCloud(max_font_size=40).generate(' '.join(word_list))
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    st.pyplot(fig=fig, clear_figure=True)
    
    for i in range(result.shape[0]):
        st.markdown(f'### {i+1}. {result.iloc[i]["title"]}')
        st.markdown(f'> {result.iloc[i]["description"][0:200]}...')
        
        # price stock category
        col1, col2, col3 = st.columns(3)
        col1.metric("Category", result.iloc[i]["category"])
        col2.metric("Price", result.iloc[i]["price"])
        col3.metric("Stock", result.iloc[i]["stock"])
        
        # Separator 
        st.markdown('---')


# Loading books 
df = pd.read_csv('books.csv')
df['description'] = df['description'].fillna('')

# Loading stopwords as list
with open('stopwords.txt', 'r') as file:
    stopwords = [line.strip() for line in file.readlines()]
    # Efficiency purposes
    stopwords = set(stopwords)
    
# Creating a Counter object for each book : Counter(title + description)
df['keywords'] = (df['description'] + ' ' + df['title']).str.lower()
# Replace !?.,() and digits by a space
df['keywords'] = df['keywords'].str.replace(pat = r'[!?,.\d()*-]+', repl = ' ', regex = True)
# Replace double quotes when preceded or followed by a space
df['keywords'] = df['keywords'].str.replace(pat = r"(\s)'|'(\s)", repl = r"\1 \2", regex = True)
df['counter'] = df['keywords'].str.split().apply(lambda x: Counter(x))

# Input search
input = st.text_input('Search for a book 👀')
input = input.lower().split()
search_input = [w for w in input if w not in stopwords]

# Searching process 
# On each row, sum the number of occurences of search_input (this could potentially be vectorized)
df['score'] = df['counter'].apply(lambda x: sum([x[word] for word in input if word in x]))
# # Getting the top 10 result by frequency of occurence
result = df.sort_values(by = 'score', ascending=False)[0:10]
result = result[result['score'] > 0]
result.reset_index(drop=True, inplace=True)

if input == []:
    pass
elif result.shape[0] == 0 or search_input == []:
    st.markdown('### No result found 🔍')
else: 
    st.markdown(f"""#### Your search returned {result.shape[0]} result(s) :""")
    display_res(result)