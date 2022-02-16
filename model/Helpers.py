
class Helpers:
    
    @staticmethod
    def clean(keyword):
        
        restricted_characters = ['-', ',', '\'', ')', '(', '[', ']', '{', '}', '.', '*', '?', '_', '@', '!', '$', '&', '#', '~', '%']
        
        clean_keyword = ""
        for char in keyword:
            if char not in restricted_characters:
                clean_keyword += char

        white_space_counter = 0

        for char in clean_keyword:
            if char == ' ':
                white_space_counter += 1
            else:
                break

        clean_keyword = clean_keyword[white_space_counter:]

        white_space_counter = 0

        for i in range(len(clean_keyword) - 1, 0, -1):
            if clean_keyword[i] == ' ':
                white_space_counter += 1
            else:
                break

        if white_space_counter != 0:
            clean_keyword = clean_keyword[:-white_space_counter]

        return clean_keyword

        
    @staticmethod
    def removeRestrictedCharactersAndWhiteSpaces(keywords):

        keywords = list(dict.fromkeys(keywords))  # Remove dupes
        keywords = list(filter(None, keywords))  # Remove empty

        preprocessed_list = []

        for keyword_geo in keywords:
            
            if "-" in keyword_geo:
                keyword = keyword_geo.split("-")[0]
                geos = keyword_geo.split("-")[1].split(" ")
                geos = [e for e in geos if e != " " and e != ""]
            
                keyword = Helpers.clean(keyword)
            
                for geo in geos:
                    geo = Helpers.clean(geo)
                    preprocessed_list.append(keyword + "-" + geo)
            else:
                keyword = Helpers.clean(keyword_geo)
                preprocessed_list.append(keyword)
            
        return preprocessed_list
            

    @staticmethod
    def updateCredentials(refresh_token, client_secret, client_id, developer_token, login_customer_id):
        f = open("auth/credentials.yaml", 'r')
        cred_data = f.read()
        f.close()
        cred_data_splitted = cred_data.split("\n")


        new_txt = ""

        for line in cred_data_splitted:
            if line[:17] == "login-customer-id":
                new_txt += "login-customer-id: " + login_customer_id + "\n"
            if line[:15] == "developer_token":
                new_txt += "developer_token: " + developer_token + "\n"
            if line[:9] == "client_id":
                new_txt += "client_id: " + client_id + "\n"
            if line[:13] == "client_secret":
                new_txt += "client_secret: " + client_secret + "\n"
            if line[:13] == "refresh_token":
                new_txt += "refresh_token: " + refresh_token + "\n"
            elif line == "":
                pass

        f = open("auth/credentials.yaml", 'w')
        f.write(new_txt)
        f.close()
