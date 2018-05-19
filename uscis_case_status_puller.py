import requests
from bs4 import BeautifulSoup
from datetime import date
from multiprocessing import Pool

URL = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
RECEIPT_NUM_RANGE = range(1890142000, 1890142500)


def MakeRequest(case_id):
    return requests.post(URL, data = {'appReceiptNum': case_id})

# return [case_status, case_detail]
def GetStatusContentFromHtml(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return [str(soup.findAll('h1')[0]).lstrip('<h1>').rstrip('</h1>'), str(soup.findAll('p')[0])]

def GetChangeDateFromCaseDetail(case_detail):
    year = int(case_detail.split(',')[1].strip())

    month_day = case_detail.split(',')[0][6:].split(' ')
    month = ParseMonth(month_day[0])
    day = int(month_day[1])

    return date(year, month, day)

def GetCaseNumberFromCaseDetail(case_detail):
    start = case_detail.find('YSC')
    return case_detail[start:(start+13)]


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

def GetCaseStatus(receipt):
    raw_html = MakeRequest(receipt).text
    [case_status, case_detail] = GetStatusContentFromHtml(raw_html)
    change_date = GetChangeDateFromCaseDetail(case_detail)
    case_number = GetCaseNumberFromCaseDetail(case_detail)
    return [case_number, case_status, change_date]

def UpdateCaseStatus(num_range):
    file_name = 'case_status_' + date.today().isoformat()
    with open(file_name, 'w') as of:
        print('receipt_num,case_status,change_date')
        for case in num_range:
            receipt = 'YSC' + str(case)
            print('Fetching Case Status: ' + receipt)
            [case_number, case_status, change_date] = GetCaseStatus(receipt)
            print(case_number + ',' + case_status + ',' + change_date.isoformat())
            print(case_number + ',' + case_status + ',' + change_date.isoformat(), file=of)

def UpdateCaseStatusAsync(num_range):
    pool = Pool()
    futures = []
    index = 0
    for case in num_range:
        receipt = 'YSC' + str(case)
        print('Fetching Case Status: ' + receipt)
        futures.append(pool.apply_async(GetCaseStatus, [receipt]))
        index += 1

    file_name = 'case_status_' + date.today().isoformat()
    with open(file_name, 'w') as of:
        for future in futures:
            res = future.get(timeout=10)
            print(res[0] + ',' + res[1] + ',' + res[2].isoformat())
            print(res[0] + ',' + res[1] + ',' + res[2].isoformat(), file=of)

def main():
    UpdateCaseStatusAsync(RECEIPT_NUM_RANGE)

if __name__ == "__main__":
    main()
