#AWPS: Backend
# Home of Login related Operations:
#   1) /(login)
#   2) /create_user
#   3) /forgot_password

import cypher
import random
import MessageFunctions



#system_collection = dbClient.APWS.Systems
 
def user_exists(username, dbClient):
    user_collection = dbClient.APWS.Users
    user = user_collection.find_one({'username': username})
    if user is not None:  
        return True
    else:
        return False

'''
For route /login
    Request format
    {
     "username": username,
     "password": passord,
} 
'''     
def sign_in(request, dbClient):  # Returns Json
    data = request.get_json()
    username = data['username'].lower()
    password = data['password']
    user_collection = dbClient.APWS.Users
    user = user_collection.find_one({'username': username})
    if user is not None:
        account_password = cypher.decrypt(user['password'])
        if user.get("OTP") is None:
            if password == account_password:
                return {'message': 'Authorized',
                        'access': True, }
            else:
                return {'message': 'Incorrect Username And/Or Password',
                        'access': False, }
        else:
            return {'message': 'Not Verified User',
                    'access': False, }
    else:
        return {'message': 'User Does Not Exist',
                'access':False, }


'''
For route /create_user
    Request format
    {
     "username": username,
     "password": passord,
} 
''' 

def sign_up(request, dbClient):  # Returns Json
    print('start')
    data = request.get_json()
    username = data['username'].lower()
    password = data['password']
    user_collection = dbClient.APWS.Users
    user = user_collection.find_one({'username': username})

    if user is None:
        OTP = 0000
        while user is None: 
            temp = random.randint(1000, 9999)
            if user_collection.find_one({'OTP': temp}) is None:      # Creates Unique OTPs 
                OTP = temp
                break
        newUser = {
            "username": username,
            "password": cypher.encrypt(password),
            "systems": [],
            "notifications": [],
            "OTP": OTP,
            "sys_invites": [],
        }
        user_collection.insert_one(newUser)
        subject = "MyAPWS Account Creation: Verify Email"            # Sends Email for New User to Verify Email
        MessageFunctions.send_email(subject, username, case=1, code=OTP)  # Parameter '1' = New User Email format to send
        return {'message': 'User added.',           # TODO Need Catch Block for emails that aren't valid!!
                'access': True }
    else:
        return {'message': 'Username exists already.', 
                'access': False}
    
def forgot_request(request, dbClient):          # Creates OTP for exisiting users
    data = request.get_json()
    user_collection = dbClient.APWS.Users

    username = data['username'].lower()
    user = user_collection.find_one({'username': username})

    if user_exists(username, dbClient):
        OTP = 0000
        while user:
            temp = random.randint(1000, 9999)
            if user_collection.find_one({'OTP': OTP}) is None:      # Generates unique OTP
                OTP = temp
                break
        update = {"$set": {"OTP": OTP}}
        user_collection.update_one(user, update)                    # Adds OTP to the user's document
        subject = "MyAPWS Password Reset"                           # Sends Forgot Password Email 
        MessageFunctions.send_email(subject, username, case=2, code=OTP) # Parameter '1' = New User Email format to send
        return {'access': True, 'message': 'Email has been sent'}
    else:
        return {'message': 'Username does not exist',
                'access': False, }
    
def otp_verify(request, dbClient):      # Checks to see input code matches the OTP
    data = request.get_json()
    user_collection = dbClient.APWS.Users
    username = data['username'].lower()
    input_otp = data['OTP']
    user = user_collection.find_one({'username': username})
    if int(user['OTP']) == int(input_otp):                            # Compares OTP from User input and Database
        remove = {"$unset": {"OTP": ""}}                    # Removes OTP from DB so it can't be used again
        user_collection.update_one(user, remove)
        return {'access': True, }
    else:
        return {'message': 'Incorrect Code', 
                'access': False, }
    
def reset_password(request, dbClient):      # Changes User Password
    data = request.get_json()
    user_collection = dbClient.APWS.Users
    username = data['username'].lower()

    user = user_collection.find_one({'username': username})
    new_password = data['password']

    update = {"$set": {"password": cypher.encrypt(new_password)}}
    user_collection.update_one(user, update)

    return {"access": True}
