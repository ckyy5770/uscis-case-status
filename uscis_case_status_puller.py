import requests
from bs4 import BeautifulSoup

URL = 'https://egov.uscis.gov/casestatus/mycasestatus.do'

def MakeRequest(case_id):
    return requests.post(, data = {'appReceiptNum': case_id})

# return [status, detail]
def GetStatus(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return [soup.h1(), soup.p()]

def main():
    raw_html = MakeRequest('YSC1890142200').text
    [status, status_detail] = GetStatus(raw_html)

if __name__ == "__main__":
    main()
