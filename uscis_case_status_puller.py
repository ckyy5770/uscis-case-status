import requests
from bs4 import BeautifulSoup
from datetime import date

URL = 'https://egov.uscis.gov/casestatus/mycasestatus.do'

def MakeRequest(case_id):
    return requests.post(URL, data = {'appReceiptNum': case_id})

# return [case_status, case_detail]
def GetStatus(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return [str(soup.findAll('h1')[0]), str(soup.findAll('p')[0])]

def GetReceivedDate(case_detail):
    year = int(case_detail.split(',')[1].strip())

    month_day = case_detail.split(',')[0][6:].split(' ')
    month = ParseMonth(month_day[0])
    day = int(month_day[1])

    return date(year, month, day)

def ParseMonth(word):
    word = word.lower()
    if word == 'january' or word == 'jan':
        return 1
    elif word == 'february' or word == 'feb':
        return 2
    elif word == 'march' or word == 'mar':
        return 3
    elif word == 'april' or word == 'apr':
        return 4
    elif word == 'may':
        return 5
    elif word == 'june' or word == 'jun':
        return 6
    elif word == 'july' or word == 'jul':
        return 7
    elif word == 'august' or word == 'aug':
        return 8
    elif word == 'september' or word == 'sep':
        return 9
    elif word == 'october' or word == 'oct':
        return 10
    elif word == 'november' or word == 'nov':
        return 11
    elif word == 'december' or word == 'dec':
        return 12
    else:
        return 0

def main():
    raw_html = MakeRequest('YSC1890142200').text
    [case_status, case_detail] = GetStatus(raw_html)

    print(case_status)
    print(case_detail)

    received_date = GetReceivedDate(case_detail)
    print(received_date)

if __name__ == "__main__":
    main()
