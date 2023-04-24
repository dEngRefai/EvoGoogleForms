import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import  HttpError
import json
from apiclient import errors
import webbrowser
import time
import random

CLIENT_FILE = 'client.json'
SCOPES = ['https://www.googleapis.com/auth/forms', 'https://www.googleapis.com/auth/drive']

creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('forms', 'v1', credentials=creds) 
service_drive = build('drive', 'v2', credentials=creds) 

# Define the list of questions

questions = [
    "Are you excited to explore the unique and iconic archaeological site of Petra?",
    "Curious to know more about the rich history and culture of the ancient Nabatean civilization at Petra?",
    "Ready to discover the fascinating structures and monuments that await you at Petra?",
    "Interested in learning about ancient engineering and architectural techniques while exploring Petra?",
    "Eager to witness the breathtaking Treasury (Al-Khazneh) and its mesmerizing facade at Petra?",
    "Want to trace the footsteps of ancient traders along the Silk Road trade route through Petra?",
    "Ready for an adventure through the narrow siq (canyon) entrance of Petra that leads to its wonders?",
    "Excited to capture the stunning natural landscapes and panoramic views of Petra in your photographs?",
    "Looking forward to exploring the rock-cut tombs and caves of Petra for insights into the Nabatean way of life?",
    "Ready for an unforgettable experience on foot or by camel, horse, or donkey while exploring Petra's ancient wonders?"
]

# Define the list of urls

Images = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Treasury_petra_crop.jpeg/1200px-Treasury_petra_crop.jpeg",
    "https://lp-cms-production.imgix.net/2019-06/f27a1f10a618448d65e6ac16c9270e56-petra.jpg",
    "https://cdn.britannica.com/88/189788-050-9B5DB3A4/Al-Dayr-Petra-Jordan.jpg",
    "https://i0.wp.com/www.touristjordan.com/wp-content/uploads/2022/05/shutterstock_1030695895-scaled.jpg?fit=2560%2C1707&ssl=1",
    "https://upload.travelawaits.com/ta/uploads/2021/04/6774bc9a0dad571855fb28138b8a46774bc.jpg",
    "https://i.natgeofe.com/n/69e2cf60-ad59-4d20-bdd1-dc96f40ab4e8/petra-world-heritage-jordan.jpg",
    "https://select.jo/wp-content/uploads/2019/07/The-Nabatean-city-of-Petra-Jordania_51.jpg.pagespeed.ce_.l8Akg6N3mb.jpg",
    "https://www.kevinandamanda.com/wp-content/uploads/2019/09/Petra-Jordan-01-720x900.jpg",
    "https://cdn.kimkim.com/files/a/content_articles/featured_photos/3139f160593f5df5287ef0b599873b83a563a8c2/big-d31dd33032d7c38fe0e3f5b253f23ff2.jpg",
    "https://media.cnn.com/api/v1/images/stellar/prod/160914152344-jordan-petra-83259680.jpg?q=w_1900,h_1069,x_0,y_0,c_fill/w_1280"
]

# Define the number of iterations, the size of each Images set and the size of each question set
num_iterations = 3
set_size_Image = 1
set_size_Question = 2

# Initialize the best Image set, the best question set and the fitness score
best_Image_set = ["https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Treasury_petra_crop.jpeg/1200px-Treasury_petra_crop.jpeg"]
best_question_set = []

best_fitness_score = 0





# Define the fitness function
def fitness_function():
   
    # Retrieve  the response of the form
    try:
     response = service.forms().responses().list(formId=createResult["formId"]).execute()
    except errors.HttpError as error: 
        print( f'An error occurred: %s' % error)
    
    # import json

    my_dict = response
    my_text = json.dumps(my_dict)
    

    # initializing string
    test_str = my_text

    # initializing substrings
    sub1 = "{\"value\": \""
    sub2 = "\"}]}}}}"

   # find the indices of the substrings
    idx1 = test_str.find(sub1)

    idx2 = test_str.find(sub2)

   # extract the string between the substrings
    res = test_str[idx1+len(sub1):idx2].strip()
   
    res_Number = int(res)

    return res_Number





# Perform random search
for i in range(num_iterations):
    # Generate a random Image set
    Image_set = random.sample(Images, set_size_Image)
    question_set = random.sample(questions, set_size_Question)

    Image_set_copy = Image_set.copy()
    question_set_copy = question_set.copy()

    # Create the form
    form = {
    "info": {
        "title": "Visit Petra!",
    }
    }

    try:
    # Creates the initial Form
     createResult = service.forms().create(body=form).execute()
    
    except errors.HttpError as error:
        print( f'An error occurred: %s' % error)

    myList = question_set_copy
    myString = ' '.join(myList)

    # Request body to add description to a Form
    update = {
    "requests": [{
        "updateFormInfo": {
            "info": {
                "description": myString
            },
            "updateMask": "description"
        }
    }]
    }

    try:
        question_setting = service.forms().batchUpdate(
        formId=createResult["formId"], body=update).execute()
    except errors.HttpError as error:
     print( f'An error occurred: %s' % error)

    myList_Image = Image_set_copy
    myString_Image = ''.join(myList_Image)

     #imageItem
    update = {
    "requests": [{
        "createItem": {
            "item": {
                #"title": "Petra",
                "imageItem": {
                    "image": {
                        'sourceUri': myString_Image
                    }
                }
            },
            "location": {
                "index": 0
            }
        }
    }
    ]
        }
    try:
        question_setting = service.forms().batchUpdate(
        formId=createResult["formId"], body=update).execute()
    except errors.HttpError as error:
     print( f'An error occurred: %s' % error)

    update = {
    "requests": [{
        "createItem": {
            "item": {
                "title": "How likely are you visiting Petra?",
                
                "questionItem": {
                    "question": {
                        'scaleQuestion': {'low': 1,
                                                'high': 5,
                                                 'lowLabel': 'Never',
                                                    'highLabel': 'Book my flight now!'
                        }
                    }
                }
            },
            "location": {
                "index": 1
            }
        }
    }
    ]
    }

    try:
        question_setting = service.forms().batchUpdate(formId=createResult["formId"], body=update).execute()
    except errors.HttpError as error:
            print( f'An error occurred: %s' % error)

    # prompt the form  
    url = createResult["responderUri"]
    webbrowser.open(url)

    # Wait for users to submit the form
    time.sleep(40)

    # Evaluate the fitness score of the question set
    
    fitness_score = fitness_function()

    # Delete the form
    try:
         service_drive.files().delete(fileId=createResult["formId"]).execute()
    except errors.HttpError as error:
     print( f'An error occurred: %s' % error)
    
    # Update the best question set and its fitness score if necessary
    if fitness_score > best_fitness_score:
        best_question_set = question_set_copy
        best_fitness_score = fitness_score
        best_Image_set = Image_set_copy

# Print the best question set, best Image set and the fitness score
print("Best question set:", best_question_set)
print("Best Image score:", best_Image_set)
print("Best fitness score:", best_fitness_score)

# Create the form
form = {
    "info": {
        "title": "Visit Petra!",
    }
    }

try:
    # Creates the initial Form
     createResult = service.forms().create(body=form).execute()
    
except errors.HttpError as error:
        print( f'An error occurred: %s' % error)

myList = best_question_set
myString = ' '.join(myList)

# Request body to add description to a Form
update = {
    "requests": [{
        "updateFormInfo": {
            "info": {
                "description": myString
            },
            "updateMask": "description"
        }
    }]
    }

try:
        question_setting = service.forms().batchUpdate(
        formId=createResult["formId"], body=update).execute()
except errors.HttpError as error:
     print( f'An error occurred: %s' % error)

myList_Image = best_Image_set
myString_Image = ''.join(myList_Image)

     #imageItem
update = {
    "requests": [{
        "createItem": {
            "item": {
                #"title": "Petra",
                "imageItem": {
                    "image": {
                        'sourceUri': myString_Image
                    }
                }
            },
            "location": {
                "index": 0
            }
        }
    }
    ]
        }
try:
        question_setting = service.forms().batchUpdate(
        formId=createResult["formId"], body=update).execute()
except errors.HttpError as error:
     print( f'An error occurred: %s' % error)

update = {
    "requests": [{
        "createItem": {
            "item": {
                "title": "How likely are you visiting Petra?",
                
                "questionItem": {
                    "question": {
                        'scaleQuestion': {'low': 1,
                                                'high': 5,
                                                 'lowLabel': 'Never',
                                                    'highLabel': 'Book my flight now!'
                        }
                    }
                }
            },
            "location": {
                "index": 1
            }
        }
    }
    ]
    }

try:
        question_setting = service.forms().batchUpdate(formId=createResult["formId"], body=update).execute()
except errors.HttpError as error:
            print( f'An error occurred: %s' % error)

    # prompt the form  
url = createResult["responderUri"]
webbrowser.open(url)
