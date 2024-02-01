import json
from datetime import datetime
from src.utils.DataframeProcessing import DataFrameProcessing


class UserProfile(DataFrameProcessing):
    def __init__(self, profile_decoded, ageinfo_decoded, account_decoded, tweets_decoded):
        self.tweets_info = self.filecontent_to_df(tweets_decoded)
        self.profile_info = self.obtain_dict_info(profile_decoded, ageinfo_decoded, account_decoded)
        # self.build_dataframe_wres()

    def build_dataframe_wres(self):
        pass

    def get_dataframe_wres(self):
        return self.profile_info, self.tweets_info

    def obtain_dict_info(self, profile_decoded, ageinfo_decoded, account_decoded):
        # Info de account.js
        js_code_ac = account_decoded.replace('window.YTD.account.part0 = ', '')
        json_dat_ac = json.loads(js_code_ac)

        # Info de profile.js
        js_code_fi = profile_decoded.replace('window.YTD.profile.part0 = ', '')
        json_dat_fi = json.loads(js_code_fi)

        # Info de ageinfo.js
        js_code_ag = ageinfo_decoded.replace('window.YTD.ageinfo.part0 = ', '')
        json_dat_ag = json.loads(js_code_ag)

        profile_data = {'profile': {}, 'age': {}, 'description': {}, 'pictures': {}}

        fecha_hora_obj = datetime.strptime(json_dat_ac[0]['account']['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
        fecha_crec = fecha_hora_obj.strftime("%d/%m/%Y %H:%M:%S")

        fecha_nac = datetime.strptime(json_dat_ag[0]['ageMeta']['ageInfo']['birthDate'], "%Y-%m-%d")
        fecha_nac_obj = fecha_nac.strftime("%d/%m/%Y")

        # Datos de profile
        profile_data['profile']['username'] = '@' + json_dat_ac[0]['account']['username']
        profile_data['profile']['email'] = json_dat_ac[0]['account']['email']
        profile_data['profile']['accountDisplayName'] = json_dat_ac[0]['account']['accountDisplayName']
        profile_data['profile']['createdAt'] = fecha_crec

        # Datos de age
        profile_data['age']['age'] = json_dat_ag[0]['ageMeta']['ageInfo']['age'][0]
        profile_data['age']['birthDate'] = fecha_nac_obj

        # Datos de la descripción
        profile_data['description']['bio'] = json_dat_fi[0]['profile']['description']['bio']
        profile_data['description']['website'] = 'www.miweb.com'  # json_dat_fi[0]['profile']['description']['website']
        profile_data['description']['location'] = json_dat_fi[0]['profile']['description']['location']

        # Imágenes
        profile_data['pictures']['header'] = json_dat_fi[0]['profile']['headerMediaUrl']
        profile_data['pictures']['prof_pic'] = json_dat_fi[0]['profile']['avatarMediaUrl']

        return profile_data
