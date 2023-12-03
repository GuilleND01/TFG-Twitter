from abc import ABC, abstractmethod
import json
from pandas import json_normalize


class DataFrameProcessing(ABC):

    @abstractmethod
    def build_dataframe_wres(self):
        pass

    @abstractmethod
    def get_dataframe_wres(self):
        pass

    def filecontent_to_df(self, file_content):
        js_code = file_content.replace('window.YTD.tweets.part0 = ', '')

        # Read the json and obtain a df
        json_dat = json.loads(js_code)
        return json_normalize(json_dat)