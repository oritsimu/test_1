import pyrebase
import streamlit as st

class Network:

    __FIREBASE_EMAIL = "hidden"
    __FIREBASE_PASS = "hidden"

    __firebase_config = None

    __user = None
    __firebase = None
    __auth = None
    __db = None


    def __init__(self):
        self.__FIREBASE_EMAIL = st.secrets["FIREBASE_EMAIL"]
        self.__FIREBASE_PASS = st.secrets["FIREBASE_PASS"]
        self.__firebase_config = {
            "apiKey": st.secrets["apiKey"],
            "authDomain": st.secrets["authDomain"],
            "databaseURL": st.secrets["databaseURL"],
            "projectId": st.secrets["projectId"],
            "storageBucket": st.secrets["storageBucket"],
            "messagingSenderId": st.secrets["messagingSenderId"],
            "appId": st.secrets["appId"],
            "measurementId": st.secrets["measurementId"]
            }
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
        login_customer_id = self.__db.child("login-customer-id-test").get(token=self.__user['idToken']).val()
        return str(login_customer_id)

    def getDeveloperToken(self):
        developer_token = self.__db.child("developer_token_test").get(token=self.__user['idToken']).val()
        return str(developer_token)

    def getClientID(self):
        client_id = self.__db.child("client_id_test").get(token=self.__user['idToken']).val()
        return str(client_id)

    def getClienSecret(self):
        client_secret = self.__db.child("client_secret_test").get(token=self.__user['idToken']).val()
        return str(client_secret)

    def getTestMCCID(self):
        test_mcc_id = self.__db.child("test_mcc_id_test").get(token=self.__user['idToken']).val()
        return str(test_mcc_id)









#END
