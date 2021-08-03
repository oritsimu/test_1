import pyrebase

class Network:

    __FIREBASE_EMAIL = "orit.mutznik@gmail.com"
    __FIREBASE_PASS = "SDF4+^4ferv"

    __firebase_config = {
        "apiKey": "AIzaSyDRJAX_mHlGCvtDfdzDDzkv6KIEwMG4Tuk",
        "authDomain": "kwrautomator.firebaseapp.com",
        "databaseURL": "https://kwrautomator-default-rtdb.firebaseio.com/",
        "projectId": "kwrautomator",
        "storageBucket": "kwrautomator.appspot.com",
        "messagingSenderId": "228133074635",
        "appId": "1:228133074635:web:2025cf78e2f1365af04d4e",
        "measurementId": "G-MQN268LK4Q"
        }

    __user = None
    __firebase = None
    __auth = None
    __db = None


    def __init__(self):
        self.__firebase = pyrebase.pyrebase.initialize_app(self.__firebase_config)
        self.__auth = self.__firebase.auth()
        self.__db = self.__firebase.database()
        self.__authenticate_to_firebase()

    def __authenticate_to_firebase(self):
        email = self.__FIREBASE_EMAIL
        password = self.__FIREBASE_PASS
        self.__user = self.__auth.sign_in_with_email_and_password(email, password)

    def getRefreshTokenForGoogleAdsAPI(self):
        refresh_token_response = self.__db.child("refresh_token").get(token=self.__user['idToken']).val()
        return str(refresh_token_response)

    def getKeywordLimit(self):
        keyword_limit = self.__db.child("keyword_limit").get(token=self.__user['idToken']).val()
        return int(keyword_limit)

    def getLoginCustomerID(self):
        login_customer_id = self.__db.child("login-customer-id").get(token=self.__user['idToken']).val()
        return str(login_customer_id)

    def getDeveloperToken(self):
        developer_token = self.__db.child("developer_token").get(token=self.__user['idToken']).val()
        return str(developer_token)

    def getClientID(self):
        client_id = self.__db.child("client_id").get(token=self.__user['idToken']).val()
        return str(client_id)

    def getClienSecret(self):
        client_secret = self.__db.child("client_secret").get(token=self.__user['idToken']).val()
        return str(client_secret)

    def getTestMCCID(self):
        test_mcc_id = self.__db.child("test_mcc_id").get(token=self.__user['idToken']).val()
        return str(test_mcc_id)









#END
