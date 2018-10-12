from csv import DictWriter

def exportToExcel(listOfDictionaries):


    with open('spreadsheet.csv', 'w') as outfile:
        writer = DictWriter(outfile, ('Date', 'From', 'To', 'Gender', 'Age', 'Province', 'Community', 'Community Other'))
        writer.writeheader()
        writer.writerows(listOfDictionaries)

