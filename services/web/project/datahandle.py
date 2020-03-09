import csv


def save_in_db(stream):
    return None


def leading_digit(word):
    word = str(word)
    try:
        number = float(word)
        if number < 0:
            number = -number
        number = int(number)
        while number >= 10:
            number = number // 10
        return number
        
    except ValueError: # not a number
        return 'NaN'

IS_NUMBER_THRESHOLD = .9

def count_by_leading_digit(stream, delimiter):
    reader = csv.DictReader(stream, delimiter=delimiter)

    table = {} # table[columnName][digit] = number of occurrences; table[colName]['nan'] = number of non numbers

    linecount = 0

    for line in reader:
        print('LINELINE', line)
        linecount += 1
        for column, value in line.items():
            leaddig = leading_digit(value)

            if column not in table:
                table[column] = {}
            if leaddig not in table[column]:
                table[column][leaddig] = 0
            
            table[column][leaddig] += 1
    
    numcolumnscount = 0
    numcolumn = ""
    for column, digitcount in table.items():
        nums = 0
        total = 0
        for digit, count in digitcount.items():
            nums += count if digit != 'NaN' else 0
        total = nums
        if 'NaN' in digitcount:
            total += digitcount['NaN']
        
        if nums / total > IS_NUMBER_THRESHOLD:
            numcolumnscount += 1
            numcolumn = column

    if numcolumnscount == 0 or numcolumnscount >= 2:
        return None
    print('THE THING', table[numcolumn])
    return {column: value for column, value in table[numcolumn].items() if column != 'NaN'}
