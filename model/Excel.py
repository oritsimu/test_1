import pandas as pd

class Excel:


    @staticmethod
    def get_data_frame(py_list, columns):
        list_excel = []
        for x in range(len(py_list)):
            list_months = []
            list_searches = []
            for y in py_list[x].keyword_idea_metrics.monthly_search_volumes:
                list_months.append(str(y.month)[12::] + " - " + str(y.year))
                list_searches.append(y.monthly_searches)

            list_excel.append([py_list[x].text, py_list[x].keyword_idea_metrics.avg_monthly_searches, str(py_list[x].keyword_idea_metrics.competition)[28::], py_list[x].keyword_idea_metrics.competition_index, list_searches, list_months ])

        return pd.DataFrame(list_excel, columns = columns)

    @staticmethod
    def dataframe_to_excel(towrite, dataframe):
        return dataframe.to_excel(towrite, encoding='utf-8', header=True, index=False)
