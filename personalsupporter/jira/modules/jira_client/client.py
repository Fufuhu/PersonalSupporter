import requests
from requests import RequestException

class JIRAClient(object):

    def __init__(self, *args, **kwargs):
        """
        : param user: ユーザ名
        : param password: パスワード
        : param protocol: プロトコル(デフォルトはhttps://)
        : param host: リクエスト先ホスト
        : param context: コンテキストパス
        """
        self._user = kwargs.get('user')
        self._password = kwargs.get('password')
        protocol = kwargs.get('protocol', 'https://')
        host = kwargs.get('host')
        context = kwargs.get('context')
        self._base_path = protocol + host + context

    __CREATE_USER_PATH = "/rest/api/2/user"

    def create_user(self, fullname, user, mail):
        """
        : param fullname: フルネーム
        : param user: ユーザID
        : param mail: メールアドレス
        """

        request_path = self._base_path + self.__CREATE_USER_PATH

        # リクエストボディの構築
        request_body = self.__construct_body_for_create_user(
            fullname=fullname,
            user=user,
            mail=mail)

        # 認証情報の準備
        credential = (self._user, self._password)

        try:
            response = requests.post(request_path, auth=credential, json=request_body)
        except RequestException as err:
            print(str(err))
        print(str(response))

    def __construct_body_for_create_user(self, fullname, user, mail):
        request_body = {
            "name": user,
            "emailAddress": mail,
            "displayName": fullname,
            "applicationKeys": [
                "jira-software",
            ],
        }
        return request_body

    def __construct_body_for_add_user_to_group(self, user):
        request_body = {
            "name": user,
        }
        return request_body


    __ADD_USER_TO_GROUP_PATH = "/rest/api/2/group/user"
    def add_user_to_group(self, user, group):
        """
        特定のユーザを特定のグループに所属させる
        """
        # 詳細は
        # https://docs.atlassian.com/jira/REST/server/#api/2/group-addUserToGroup
        # を参照。
        # POST /rest/api/2/group/user
        # クエリパラメータ: groupname (グループ名)
        # リクエストボディ
        # {
        #   "name": "ユーザID"
        # }
        #
        request_path = self._base_path + self.__ADD_USER_TO_GROUP_PATH
        credential = (self._user, self._password)

        request_body = self.__construct_body_for_add_user_to_group(user=user)
        query_string = {
            'groupname' : group, 
        }

        try:
            response = requests.post(request_path, auth=credential, json=request_body, params=query_string)
        except RequestException as err:
            print(str(err))
        print(str(response)) 
        # print(str(response.json()))

    def __construct_query_for_searching_issues(self, jql, start=1, max_results=20):
        request_query = {
            "jql": jql,
            "startAt": start,
            "maxResults": max_results,
            "fields": [
                "summary"
            ]
        }
        return request_query

    __SEARCH_ISSUES_PATH = "/rest/api/2/search"
    def get_summaries(self, jql, start, max_results):
        """
        issueを検索する
        """
        # 詳細は
        # https://docs.atlassian.com/jira/REST/7.1.8/#api/2/search-search
        # を参照。
        request_path = self._base_path + self.__SEARCH_ISSUES_PATH
        credential = (self._user, self._password)
        query = self.__construct_query_for_searching_issues(jql, start, max_results)

        response = requests.post(url=request_path, auth=credential, json=query)

        print(str(response.status_code))
        print(str(response.content))
        print(response.json())

        return response.json()
    
    __ADD_COMMENT_PATH = "/rest/api/2/issue/{}/comment"
    def add_comment(self, issue_id, comment):

        request_path = self._base_path + self.__ADD_COMMENT_PATH.format(issue_id)
        credential = (self._user, self._password)

        query = {
            "body": comment,
            "visility": {
                "type": "role",
                "value": "Administrator",
            }
        }

        response = requests.post(url=request_path, auth=credential, json=query)
        print(str(response.status_code))
        print(str(response.content))
        print(response.json())

        return response.json()
        
