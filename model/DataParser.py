
class DataParser:


    __LOCATIONS_FILE_PATH = "data/geotargets.csv"
    __LANGUAGES_FILE_PATH = "data/languagecodes.csv"

    __main_locations = {} #KEY: Location Name, VALUE: Location ID
    __sub_locations = {} #KEY: Location Name, VALUE: Location ID
    __main_sub_location_connector = {} #KEY: Location ID, VALUE: [sub_location_ids]

    __languages = {} #KEY: Language Name, VALUE: Language ID


    def __init__(self):
        self.__parse_languages()
        self.__parse_locations()


    def __parse_languages(self):
        file_str = self.__read_data_from_file(self.__LANGUAGES_FILE_PATH)
        lines = file_str.split('\n')[1:-1] #First line has column names, last line is empty
        for line in lines:
            language_name = line.split(',')[0]
            language_code = line.split(',')[2]
            self.__languages[language_name] = language_code


    def __parse_locations(self):
        file_str = self.__read_data_from_file(self.__LOCATIONS_FILE_PATH)
        lines = file_str.split('\n')[1:-1] #First line has column names, last line is empty
        for line in lines:
            splitted = line.split('\",')
            for i in range(len(splitted)):
                if splitted[i][0] == '\"':
                    splitted[i] = splitted[i][1:]
            location_id = splitted[0]
            location_name = splitted[1]
            parent_location_id = splitted[3]

            try: #Main Location
                parent_location_id = str(int(parent_location_id))
                self.__sub_locations[location_name] = location_id
                try:
                    self.__main_sub_location_connector[parent_location_id] += [location_id]
                except KeyError:
                    self.__main_sub_location_connector[parent_location_id] = [location_id]
            except ValueError: #Sub-location
                self.__main_locations[location_name] = location_id



    @staticmethod
    def __read_data_from_file(file_path):
        f = open(file_path, 'r')
        file_text = f.read()
        f.close()
        return file_text


    def get_parent_locations(self):
        return list(self.__main_locations.keys())


    def get_sub_locations_by_parent_location_id(self, parent_location_id):
        return list(self.__main_sub_location_connector[parent_location_id])


    def get_languages(self):
        return list(self.__languages.keys())


    def get_location_id(self, location):
        try:
            return self.__main_locations[location]
        except:
            try:
                return self.__sub_locations[location]
            except:
                return

    def get_parent_location_ids(self, locations):
        location_ids = []
        for location in locations:
            location_ids.append(self.__main_locations[location])
        return location_ids


    def get_language_id(self, language):
        return self.__languages[language]
