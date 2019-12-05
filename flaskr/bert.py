
import pandas as pd
import numpy as np
from bert_embedding import BertEmbedding
from sklearn.metrics.pairwise import cosine_similarity
import string
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for , jsonify
)
from werkzeug.exceptions import abort  
from datetime import datetime
#from flaskr.auth import login_required

from flaskr.db import get_db, row2json_users, row2json_activities, row2json_registered,rowList2json_activities, bert_data
import click

def current_date() : 
    ans = ""
    count = 0 
    for i in (str(datetime.now())) : 
        if count < 12 : 
            if i not in ['-'," ",":"] : 
                ans += i 
                count += 1
        else : 
            break
    return int(ans)

bp = Blueprint('bert', __name__,url_prefix='/bert')

@bp.route("/")
def index() : 
    return "bert"

@bp.route("/predict/<username>")
def prediction(username) : 
    now = current_date() 
    final_past = []
    final_future = []
    activity_ids = []
    db = get_db()
    posts = db.execute(
        "SELECT * FROM registered WHERE username = ?" ,(username,)
    ).fetchall()

    for row in posts : 
        activity_ids.append(row[1])

    for id in activity_ids : 
        answer = db.execute(
            "SELECT * FROM activities WHERE date_activity < ? AND unq_id = ? ",(now,id,)
        ).fetchall()
        final_past.append(answer)
        answer = db.execute(
            "SELECT * FROM activities WHERE date_activity > ? AND unq_id = ? ",(now,id,)
        ).fetchall()
        final_future.append(answer)
    print(bert_data(final_past))
    print(bert_data(final_future))
    print("########################33")

    attended_listdict = bert_data(final_past)
    upcoming_listdict = bert_data(final_future)

    upcoming=[]

    upcoming_ids=[]

    attended=[]

    for dic in upcoming_listdict:
        upcoming.append(dic["description"])
        upcoming_ids.append(dic["unq_id"])

    for dic in attended_listdict:
        attended.append(dic["description"])



    b = bert_instance()
    print(1)
    enquiry_para = text_preprocess(attended)
    print(2)
    recommendation_matrix=b.matrix(upcoming,enquiry_para)
    #recommended_ids=upcoming_ids[get_top10_indexes(recommendation_matrix)]

    recommended_indices=get_top10_indexes(recommendation_matrix)

    #these are the recommended unique ids 
    upcoming_ids=np.array(upcoming_ids)

    ids_list = list(upcoming_ids[recommended_indices])

    print("these are the final ids!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(ids_list)

    final_ids=[]
    for ide in ids_list:
        final_ids.append(int(ide))


    return jsonify({"ids_list" : final_ids})

"""
Pipeline:
1. API gives Frequencies of all past events, use that to select the 2 event types thats most popular
2. In the ratio of event types, display the UPCOMING recently posted events from those types, that have the highest % cosine similarity(using BERT)(max of 10 recommendations)
"""

#takes username as input

#API will calculate the 2 most frequently attended types of events

#API will send the ATTENDED past 25 event descps of both types

#API will send 100 UPCOMING event descriptions(of both types), with their unique ids

#combine all the 25 event descriptions, remove junk words. Then find matrix for
#for similarity bw this enquiry and events posted. Get the top 10 enquiries and return
# IDS for recommended events from the 100


class bert_instance():
    bert_embedding = BertEmbedding()
    def matrix(self,processed_texts,enquiry):
        all_vectors=[]
        enquiry_vector=[]
        enquiry_vector.append(self.return_vector(enquiry))
        enquiry_vector=np.array(enquiry_vector)
        for text in processed_texts:
            all_vectors.append(self.return_vector(text))
        all_vectors=np.array(all_vectors)
        print(all_vectors)
        print(all_vectors.shape)
        matrix=cosine_similarity(all_vectors,enquiry_vector)
        return(matrix)
    def return_vector(self,text):
        vectorfile=self.bert_embedding([text]) 
        print(len(vectorfile))
        #for i in range(len(vectorfile)):
        vectorlist=vectorfile[0][1]
        #print(vectorlist)
        sum_vector=np.empty(shape=vectorlist[0].shape)
        sum_amt=0
        for vector in vectorlist:
            sum_amt+=(vector[0])
            sum_vector+=vector
        sum_vector/=len(vectorlist)
        sum_vector=np.nan_to_num(sum_vector)
        return(sum_vector)

def text_preprocess(all_texts):
    tokenizer = RegexpTokenizer(r'\w+') #tokenize words
    textstring=""
    #This is the list of some common words in the dataset that dont add predictive value. Your new dataset may have other words, check the most frequent words and add to this list
    stoplist_events=[
                     'ang', 'mo', 'kio', 'bedok', 'bishan', #locations to remove
                     'boon', 'lay', 'bukit', 'batok', 'bukit', 
                     'merah', 'bukit', 'panjang', 'bukit', 'timah', 
                     'central', 'water', 'catchment', 'changi', 
                     'changi', 'bay', 'choa', 'chu', 'kang', 
                     'clementi', 'downtown', 'core', 'geylang', 
                     'hougang', 'jurong', 'east', 'jurong', 'west', 
                     'kallang', 'lim', 'chu', 'kang', 'mandai', 'marina', 
                     'east', 'marina', 'south', 'marine', 'parade', 'museum', 
                     'newton', 'north-eastern', 'islands', 'novena', 'orchard', 
                     'outram', 'pasir', 'ris', 'paya', 'lebar', 'pioneer', 'punggol'
                     , 'queenstown', 'river', 'valley', 'rochor', 'seletar', 
                     'sembawang', 'sengkang', 'serangoon', 'simpang', 'singapore', 
                     'river', 'southern', 'islands', 'straits', 'view', 'sungei', 
                     'kadut', 'tampines', 'tanglin', 'tengah', 'toa', 'payoh', 
                     'tuas', 'western', 'islands', 'western', 'water', 'catchment', 
                     'woodlands', 'yishun', #end of locations
                     
                     "join","us","at","singapore", #other words
                     'am', 'pm', 'shy','all','welcome',
                     #days of the week
                     'monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    stoplist = set(stoplist_events) #like a list, but can use hash table
    punctuation = list(string.punctuation)
    
    for text in all_texts:
        text=str(text)
        text = text.lower()
        tokens = tokenizer.tokenize(text)
        tokens = [WordNetLemmatizer().lemmatize(token) for token in tokens] #lemmatize all tokens
        tokens = [w for w in tokens if not w.isdigit()]  #remove digits
        tokens = [w for w in tokens if len(w)>2]  #remove words having 2 or less chars
        tokens = [w for w in tokens if not w in punctuation] #remove punctuations 
        tokens = [w for w in tokens if not w in stoplist] #remove stopwords
        textstring+=(" ".join(tokens))+" "
    
    return (textstring) #remove large sentence with all purified words

def get_top10_indexes(matrix):
    lis=matrix.flatten()
    top10=lis.argsort()[-4:][::-1]
    return(top10)
 
    