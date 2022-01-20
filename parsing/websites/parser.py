from typing import Optional

from bs4 import BeautifulSoup
from requests import Session, Response
from requests.cookies import RequestsCookieJar

from data.config import default_headers


class Parser:
    def parse(self, url: str) -> int:
        raise NotImplemented

    def _get_soup(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None, cookies: Optional[RequestsCookieJar] = None) -> BeautifulSoup:
        response = self._send_get_request(url, params, headers, cookies)
        return BeautifulSoup(response.content, "html.parser")

    def _send_get_request(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None, cookies: Optional[RequestsCookieJar] = None) -> Response:
        session = self._session

        if headers is not None:
            session.headers.update(headers)
        if cookies is not None:
            session.cookies = cookies

        resp = session.get(url, params=params)
        if resp.status_code != 200:
            raise ConnectionError(resp)
        return resp

    @property
    def _session(self) -> Session:
        session = Session()
        session.headers = default_headers
        return session

