import requests

class Configuration():
    def __init__(self, session_id: str):
        self.host = 'https://leetcode.com/'
        self.session_id = session_id
        
        self._csrf_cookie: str = self.csrf_cookie
        
        self._headers: dict = {'x-csrftoken': self._csrf_cookie,
                               'Referer': self.host}
        self._cookies: dict = {'csrftoken': self._csrf_cookie,
                               'LEETCODE_SESSION': self.session_id}       
    
    @property
    def csrf_cookie(self) -> str:
        response = requests.get(url=self.host,
                                cookies={"LEETCODE_SESSION": self.session_id})
        return response.cookies["csrftoken"]
    
    @csrf_cookie.setter
    def csrf_cookie(self, value: str):
        self._csrf_cookie = value
        
    @property
    def headers(self) -> dict:
        return self._headers
    
    @property
    def cookies(self) -> dict:
        return self._cookies