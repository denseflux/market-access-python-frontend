import base64

import requests

from companies_house.dataclasses import CompanyHouseCompany, CompanyHouseSearchResult

DEFAULT_API_ENDPOINT = "https://api.companieshouse.gov.uk"


class CompaniesHouseAPIClient(object):
    api_key: str

    def __init__(self, api_key: str, api_endpoint: str = DEFAULT_API_ENDPOINT):
        self.api_key = api_key
        self.api_endpoint = api_endpoint

    def get_company_from_id(self, company_id: str):
        """
        Get company house data from the API
        """
        url = f"{self.api_endpoint}/company/{company_id}"
        headers = {
            "Authorization": "Basic " + base64.b64encode(self.api_key.encode()).decode()
        }
        response = requests.get(url, headers=headers)
        return CompanyHouseCompany(**response.json())

    def search_companies(self, query: str, page: int = 1, limit: int = 20):
        """
        Search company house companies
        """
        url = f"{self.api_endpoint}/search/companies"
        headers = {
            "Authorization": "Basic " + base64.b64encode(self.api_key.encode()).decode()
        }
        params = {"q": query, "page": page, "limit": limit}
        response = requests.get(url, params=params, headers=headers)
        results = CompanyHouseSearchResult(**response.json())
        return results
