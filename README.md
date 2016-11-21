# Reddit Predictor DS Task

##Problem Statement
Can be found on this link https://quip.com/O8CTAVETCabm

##Solution

The webapp is built using the Python web microframework Flask.

There are three endpoints-  
1. Basic - This contains the basic level of the assignment. This contains the search feature.  
2. Intermediate - The intermediate level involves prediction of ups of a post from the subreddits already there in the database. These are the posts on a subset of which the model was trained.  
3. Advance - The advance level involves prediction of ups of a latest post fetched from the reddit API. The user can input a subreddit of his choice.  

+ The database used is sqlite3.   
+ The model is trained using [Stochastic Gradient Descent Regressor](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html#sklearn.linear_model.SGDRegressor)  
with alpha = 0.000050 and partial_fit() method for training the model iteratively in mini batches.    
+ The [Reddit Upvote Predictor Model Ipython Notebook](https://github.com/deepankarpal89/reddit-data-project/blob/master/Reddit_Upvote_Predictor_Model.ipynb) contains the steps used to train the model.  
  
The input fields considered while training the model are the domain, title and subreddit category.  
Due to limitation of computing power the model was trained only on 1 lakh posts. Training it on more posts will make the predictions more accurate.  
For testing, 3000 random posts were collected from the 1 lakh posts. These posts were kept separate and the difference between the actual upvote and the predicted values i.e. error is as follows

count | 3000.000000  
--- | ---
mean | 392.792667  
std | 2594.545617  
min | 0.000000  
25% | 22.000000  
50% | 51.000000  
75% | 137.000000  
max | 61412.000000  

##Ways to improve the result  
1.Training the model on more data.  
2. The words in title havnt been corrected, singularize and lemmatize in that order due to limitation of RAM and Processing power. By doing these three things the accuracy of predictions can be improved.  
