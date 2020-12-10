# IND135-SoccerAnalytic-CodeReview
Code description and Review for the Soccer Analytic Team
#Soccer Analytics Project
Over the last few years, soccer has become increasingly data driven with teams hiring world class analytics teams or sending film to large sports analytics companies. Both of these are extremely expensive propositions hence why we see teams whose large investments in analytics run parallel with their success. A great example of this is Liverpool’s wildly successful squad that achieved runners up and a tournament win in consecutive UEFA Champions Leagues, the biggest club soccer competition in the world.
 
On the flip side, these advances in analytics have played a role in increasing the already large advantage that wealthier clubs have in each level of soccer competition. Whether it be college, club, or national team, wealthier teams already have access to the greatest players, coaching staff, and infrastructure. By investing heavily in this new crucial dimension of the game exacerbates the inequalities in the soccer world. 
 
Using Machine Learning techniques, our team has created a strategic tool for lower budget soccer clubs to predict the likelihood of a goal being scored given data regarding specific events at the time of a shot. This metric that we are calculating is commonly known in the soccer world as Expected Goal (xG). The model feeds a GUI which allows users to input data surrounding each shot of a game to output an xG value.
 
## Features
The features we used are as follows:
Distance 
Applied the distance formula from location of shot to center of goal post.
Shot Body Type
Head/Foot/Other
One hot encoded each type
Shot Angle 
Angle from the point of a player connecting both the left and right goal posts. 
Calculated using law of cosine
First Time?
Whether the shot was kicked directly from a pass or dribbled before.
One hot encoded no (0) , yes (1)
Obstructing Players
Opponent players lying inside the shot angle. Essentially players that lie in the triangle connecting the shot location and the 2 goal posts.
Applied techniques used in this video to calculated: https://www.youtube.com/watch?v=HYAgJN3x4GA
Distance to center
Distance from center of field.
 
 
## Model
We created a Logistic Regression model on the features listed above using the Scikit-Learn Library. Logistic Regression is a commonly used algorithm for xG models. Other commonly used models include XGBoost and Deep Neural Networks. We tested XGBoost but found that the model had slightly less predictive power than the Logistic Regression model. We adjusted the “class_weight” hyperparameter setting the smaller class to a 1.5 class weight. This basically duplicates the rows in which a goal occurred until the length is equal to 1.5 times its current length.
## Model Evaluation
Due to the large class imbalance, it was not effective to evaluate our model using accuracy, precision, and recall. Therefore, we decided to create an ROC curve as is often done for xG models. The ROC-AUC (Area under curve) score measures the degree to which the model is capable of separating the 2 classifications. The curve represents an aggregate measure of performance across different thresholds.
 
 
## Web Application Structure

The expected goals web application is built on Flask, Python, and Google App Engine. It is deployed in the cloud on google platform and uses the Google Datastore for persistent data. The file structure is as follows: 

The main folder is called xg-test, which is the root directory. This folder contains:
main.py: the main python file that ultimately runs the program.
soccer_analytics.pkl: expected goals model
requirements.txt: specifies the dependencies of our web application
app.yaml: defines our web application's settings for App Engine.
Xg-test-project-734003e4e35c.json: the ‘key’ to access the google datastore database if wanting to run it locally
Templates (folder): contains all the HTML files written in html code and JavaScript. Each file represents one page on the web application.
start.html: start webpage
competitions.html: where you select or create new competitions
competition-information: where you create, view, or edit matches within the selected competition
view-statistics.html: where you view the match statistics of a particular match
index.html: where you add shots to a match
Static (folder): images displayed on the website

The main.py file is the core component of the expected goals service. It imports Flask which is a framework to build web applications in python. The code is structured into two sections:
https request endpoints: 
executes service requests and returns html response. Calls helper functions to interact with database, and/or loads the trained model to calculate xG. 
Helper functions and data store communication functions: 
Stores and retrieves data objects in datastore (Competitions, Matches, and Shots). 

The GUI code folder further explains how to run and navigate the interface.
 
 
 
 
 
Sources 
 
https://www.nytimes.com/2019/05/22/magazine/soccer-data-liverpool.html
 
https://www.youtube.com/watch?v=310_eW0hUqQ&t=535s&ab_channel=FriendsofTracking
 
https://towardsdatascience.com/illustrating-predictive-models-with-the-roc-curve-67e7b3aa8914
