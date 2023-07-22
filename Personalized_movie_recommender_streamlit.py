import streamlit as st
 
st.title("Recommender Chatbot")
 
st.write("""
### Tell us your User Id, and we tell you what you like
 
""")
import pandas as pd



path = 'C:/Users/rahma/OneDrive/Desktop/Bootcamp/Section 8 - Recommender System/ml-latest-small/movies.csv'
movies = pd.read_csv(path)

path = 'C:/Users/rahma/OneDrive/Desktop/Bootcamp/Section 8 - Recommender System/ml-latest-small/ratings.csv'
ratings = pd.read_csv(path)


from sklearn.metrics.pairwise import cosine_similarity


users_items = pd.pivot_table(data=ratings, 
                                 values='rating', 
                                 index='userId', 
                                 columns='movieId')


users_items.fillna(0, inplace=True)


user_similarities = pd.DataFrame(cosine_similarity(users_items),
                                 columns=users_items.index, 
                                 index=users_items.index)

def weighted_user_rec(user_id, n):
  weights = (user_similarities.query("userId!=@user_id")[user_id] / sum(user_similarities.query("userId!=@user_id")[user_id]))
  not_seen_movies = users_items.loc[users_items.index!=user_id, users_items.loc[user_id,:]==0]
  weighted_averages = pd.DataFrame(not_seen_movies.T.dot(weights), columns=["predicted_rating"])
  recommendations = weighted_averages.merge(movies, left_index=True, right_on="movieId")
  top_recommendations = recommendations.sort_values("predicted_rating", ascending=False)[:n]
  return top_recommendations

import re

def rearrange_title(title):
    pattern = ", The"
    match = re.search(pattern, title)
    if match:
        extracted = match.group().lstrip(', ').strip()
        rearranged = extracted + ' ' + title.replace(pattern, '', 1).strip()
        return rearranged
    else:
        return title
    
    
def chat_bot(user_id,n):
  try:
    recom = weighted_user_rec(int(user_id), 1)
  except Exception:
    return_string = "Sorry, you have probably entered an invalid userID"
    return return_string

  try:
    recom = weighted_user_rec(1, int(n))
  except Exception:
    return_string = "Sorry, you have probably entered an invalid number of movies"
    return return_string

  recom_list = list(weighted_user_rec(int(user_id), int(n))['title'])

  for i in range(len(recom_list)):
    recom_list[i] = rearrange_title(recom_list[i])
  
  recom_unpacked='<br>'.join(recom_list)
  return_string = f"You will probably like the following movie(s):<br>{recom_unpacked}"
  return return_string


user_id = st.text_input("Please type your User Id here:")
n = st.text_input("How many movies would you like to get recommended?")

if st.button("Recommend"):
    recomm = chat_bot(user_id,n)
    st.markdown(recomm,unsafe_allow_html=True)