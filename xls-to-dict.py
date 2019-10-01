import os
import pandas as pd


class XlsToDict:
    def __init__(self, file_path):
        self._response_dict = dict()
        self._user_dict = dict()
        self._interest_list = list()
        self._file_path = file_path

    def get_output_dict(self):
        df = self._get_data_frame()
        self._set_response(df)
        return self._response_dict

    def _get_data_frame(self):
        return pd.read_excel(os.getcwd() + self._file_path)

    def _set_response(self, df):
        for nick_name in df['User Handle'].dropna().tolist():
            self._set_user_dict(df, nick_name)
            self._response_dict.update({
                nick_name: self._user_dict
            })

    def _prepare_interests_list(self, df_link, index):
        df_t = df_link.drop(columns=['Post Link', 'User Handle']).T
        self._interest_list = df_t[index].dropna().tolist()

    def _set_interests_to_dict(self):
        for interest in self._interest_list:
            if interest not in self._user_dict['interests']:
                self._user_dict['interests'].append(interest)

    def _set_user_dict(self, df, nick_name):
        self._user_dict_structure()
        df['User Handle'] = df['User Handle'].fillna(method='ffill')
        df = df[df['User Handle'] == nick_name]
        index = df.index[0]
        for link in df['Post Link']:
            df_link = df[df['Post Link'] == link]
            self._prepare_interests_list(df_link, index)
            self._set_interests_to_dict()
            index += 1
            self._user_dict['images'].update({link: self._interest_list})

    def _user_dict_structure(self):
        self._user_dict = {
            'images': {},
            'interests': []
        }


xls_to_dict = XlsToDict('/Testing Data by Insta Accounts.xlsx')
print(xls_to_dict.get_output_dict())
