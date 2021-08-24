import streamlit as st
import base64
import io
import pandas as pd
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import time
from model.Ads import Ads
from model.Excel import Excel
from model.Helpers import Helpers
from view.DownloadButtonView import DownloadButtonView
from model.DataParser import DataParser
from model.Network import Network


network = Network()
refresh_token = network.getRefreshTokenForGoogleAdsAPI()
client_secret = network.getClienSecret()
client_id = network.getClientID()
developer_token = network.getDeveloperToken()
login_customer_id = network.getLoginCustomerID()
Helpers.updateCredentials(refresh_token, client_secret, client_id, developer_token, login_customer_id)
__KEYWORD_LIMIT = network.getKeywordLimit()

st.set_page_config(layout="wide")
st.title("The Meta Description Briefing Tool:snake::fire:")
text = st.text_area("Input your search term (one per line, max {}) and hit Get Keywords to get the most relevant keywords to use on your meta description with their respective search volume. You’ll get a sample of your top 5 keywords, and you can hit Download Results for the complete dataset ⬇️".format(str(__KEYWORD_LIMIT)), height=150, key=1)


lines = text.split("\n")  # A list of lines
keywords = Helpers.removeRestrictedCharactersAndWhiteSpaces(lines)


data_parser = DataParser() #TODO save lists as binary to speed up the process
parent_locations = data_parser.get_parent_locations()
languages = data_parser.get_languages()


selected_countries = st.multiselect('Country', parent_locations, default=["United States"])
selected_language = st.selectbox('Language', languages)


location_ids = data_parser.get_parent_location_ids(selected_countries)
language_id = data_parser.get_language_id(selected_language)

print(location_ids)


include_volume = st.checkbox('Include search volume per keyword')


start_execution = st.button("Get Keywords! 🤘")

if start_execution:


    if len(keywords) == 0:

        st.warning("Please enter at least 1 keyword.")

    elif len(keywords) > __KEYWORD_LIMIT:

        st.warning("Please enter at most {} keywords.".format(str(__KEYWORD_LIMIT)))

    else:

        error_flag = False #If there is an unexpected error with the API, the rest of the code won't be processed and a warning message will appear.

        if include_volume:
            columns = ["Main KW", "Search Volume main", "Keyword 1", "Search Volume 1", "Keyword 2", "Search Volume 2", "Keyword 3", "Search Volume 3", "Keyword 4", "Search Volume 4", "Keyword 5", "Search Volume 5"]
        else:
            columns = ["Main KW", "Keyword 1", "Keyword 2", "Keyword 3", "Keyword 4", "Keyword 5"]


        rows = []
        
        ads = Ads(location_ids = location_ids, language_id = language_id)
        
        saved_time = 0
        
        counter = 1

        for keyword in keywords:
            
            current_time = time.time()
            diff_time = current_time - saved_time
            sleep_time = 1 - diff_time
            if sleep_time > 0:
                time.sleep(sleep_time) #API Limitations https://developers.google.com/google-ads/api/docs/best-practices/quotas
            saved_time = time.time()

            keyword = [keyword]


            #try:

            ideas = ads.run(keyword)

            row = []

            for i in range(len(ideas)):
                if include_volume:
                    row += [ideas[i].text, ideas[i].keyword_idea_metrics.avg_monthly_searches]
                else:
                    row += [ideas[i].text]

            rows.append(row)

            #except:
                #st.warning("Service is currently unavailable because of the high traffic :(")
                #error_flag = True
            
            if counter < len(keywords):
                st.warning("Getting keywords... {}/{}".format(str(counter), str(len(keywords))))
            else:
                st.success("Getting keywords... {}/{}".format(str(counter), str(len(keywords))))
            counter += 1


        if not error_flag:

            dataframe = pd.DataFrame(rows, columns = columns)

            st.write(dataframe)


            copy_button = Button(label="Copy to Clipboard")
            copy_button.js_on_event("button_click", CustomJS(args=dict(df=dataframe.to_csv(sep='\t')), code="""
            navigator.clipboard.writeText(df);
            """))

            no_event = streamlit_bokeh_events(
                copy_button,
                events="GET_TEXT",
                key="get_text",
                refresh_on_update=True,
                override_height=40,
                debounce_time=0)


            towrite = io.BytesIO()
            downloaded_file = dataframe.to_excel(towrite, encoding='utf-8', header=True, index=False)
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode()  # some strings
            custom_css, button_id = DownloadButtonView.getCustomCSS()
            linko = custom_css + f'<a id="{button_id}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="results.xlsx">Download KWs Excel</a>'


            st.markdown(linko, unsafe_allow_html=True)
            st.write("#")
