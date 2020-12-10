
## Launching Web Application

Once invited to project:

1) If Google Cloud SDK is not installed, please follow these instructions to download. 
https://cloud.google.com/sdk/docs/quickstart
2) Start the SDK.
>> if you are prompted to choose a project choose xg-test-project
3) Connect to project
>> gcloud config set project xg-test-project (type this in the sdk terminal you just installed) 
4) In the SDK shell, cd to your project root (create a project folder where you want the project files to be located and cd to the folder in the terminal)
>> cd <project root>
5) Clone the git repository 
>> gcloud source repos clone xg-test (type this in terminal)
6) Step into to project directory
>> cd xg-test
7) run the following code to connect to the database:
>> pip install -r requirements.txt
8) Launch the web application
In any python shell environment:
>> python main.py
Then go to http://localhost:8080/ and web app should launch in browser



## Web application use

Start page
From the homepage, you click start to be brought to the competitions page.
Competition page
The competitions page allows you to either select from the competitions currently listed in the database, or create a new competition by filling in the parameters. 
Once you decide to view a competition or create a new one, you will be taken to the match page.
Match page
Here you can either select a match that exists in the database and view or edit the shots of the match, or you can create a new match by entering the parameters.
If editing a match or adding a new one, you will be taken to the shot page.
If viewing a match, you will be taken to the Match Statistics page.
Shot page 
Here you will be able to click on a location on the field, and fill in the parameters to add a shot taken during the match, and be given each shot's xG value. 
If you click view statistics, you will be taken to the match statistics page for that particular match.
Match Statistics page
Here you will be able to view all the shots inputted for a certain competition, and view a table displaying the number of shots, goals, and expected goals sum for each team. 
