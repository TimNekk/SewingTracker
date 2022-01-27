import json
from typing import Optional, List

from bs4 import BeautifulSoup
from requests import Session, Response
from requests.cookies import RequestsCookieJar

from data.config import default_headers


class Parser:
    def parse_model(self, url: str) -> int:
        raise ParseException("No parser configured")

    def parse_search(self, search: str) -> dict[str, str]:
        raise ParseException("No parser configured")

    def _get_soup(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None, cookies: Optional[RequestsCookieJar] = None) -> BeautifulSoup:
        response = self._send_get_request(url, params, headers, cookies)
        soup = BeautifulSoup(response.content, "html.parser")
        if not soup:
            raise ConnectionError("Soup not created")
        return soup

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

    def _send_post_request(self, url: str, data: Optional[dict] = None, headers: Optional[dict] = None, cookies: Optional[RequestsCookieJar] = None) -> Response:
        session = self._session

        if headers is not None:
            session.headers.update(headers)
        if cookies is not None:
            session.cookies = cookies

        resp = session.post(url, data=json.dumps(data))
        if resp.status_code != 200:
            raise ConnectionError(resp)
        return resp

    @property
    def _session(self) -> Session:
        session = Session()
        session.headers = default_headers
        return session


class ParseException(Exception):
    pass
