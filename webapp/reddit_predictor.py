import pandas as pd
import numpy as np
import pickle
import math
import re

def df_format(df):
    if "title" in df.columns:
        df["title"]=  df["title"].map(lambda x: x.lower())
        df["title"] = df["title"].map(lambda x: re.sub('[^a-zA-Z ]', '', x))
        df["title"] = df["title"].map(lambda x: x.split())
        df["title"] = df["title"].map(lambda x: [i for i in x if (len(i)>3 and len(i)<10)])
        from nltk.corpus import stopwords
        stop = stopwords.words('english')
        df["title"] = df["title"].map(lambda x: [i for i in x if i not in stop])
        df["title"] = df["title"].map(lambda x: [str(i) for i in x])
    if "domain" in df.columns:
        df["domain"] = df["domain"].map(lambda x: "domain_"+str(x))
    if "subreddit" in df.columns:
        df["subreddit"] = df["subreddit"].map(lambda x: "subreddit_"+str(x))
    return df

input_dict = {
    "title" : "where the hell is matt",
    "subreddit" : "where",
    "domain" : "youtube.com"
}


#loading the training_df_column_names.pkl and tfidf_dict.pkl
with open("training_df_column_names.pkl","rb") as f:
    training_df_column_names = pickle.load(f)
with open("tfidf_dict.pkl","rb") as f:
    tfidf_dict = pickle.load(f)
# loading the model pkl file
with open("trained_model.pkl","rb") as f:
    model = pickle.load(f)

def get_prediction(input_dict):
    d = pd.DataFrame(input_dict, index=np.arange(1))
    training_df = pd.DataFrame(0, index=np.arange(d.shape[0]), columns = training_df_column_names)
    #training_df.drop("pk_id", axis=1, inplace=True)
    d = df_format(d)
    for index, row in d.iterrows():
        if str(row["domain"]) in training_df_column_names:
            training_df[row["domain"]].loc[index] = training_df[row["domain"]].loc[index] + 1
        if str(row["subreddit"]) in training_df_column_names:
            training_df[row["subreddit"]].loc[index] = training_df[row["subreddit"]].loc[index] + 1
        for w in row["title"]:
            if w in training_df_column_names:
                training_df[w].loc[index] = training_df[w].loc[index] * tfidf_dict[w]

    # prediction will contain the predicted value
    prediction= np.exp(model.predict(training_df.as_matrix())).astype(int)
    return prediction[0]
