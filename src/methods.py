import os
import collections
import json
import csv
import math
import datetime

import xlrd
import xlwt

from src.templates import (
    template_column_headers,
    get_fieldnames_from_template,
    )

def open_csv_to_strings(infile):
    # open headerrow as strings to check amount of columns and headers found in file
    with open(os.path.join("data", infile)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

    return csv_reader

def open_csv_to_dict(infile, template):
    # file.csv without headers import as dict

    print(f"infile used {infile}")
    csv_dict = collections.OrderedDict()
    with open(os.path.join("data", infile), mode='r') as csv_file:

        if template != None:
            fieldnames = get_fieldnames_from_template(template)
            csv_reader = csv.DictReader(f = csv_file, fieldnames = fieldnames, delimiter = template["Delimiter"])

        else:
            csv_reader = csv.DictReader(f = csv_file)

        # If there are headers in the csv file, skip the first row with the next statement
        if template["HeadersPresent"] == True:
            next(csv_reader, None)

        i = 0
        for row in csv_reader:
            i += 1
            csv_dict.update({i: row})
        print(f"rows imported: {i}")

    # convert the format of the imported csv to the uniform format
    csv_dict = convert_to_uniform(csv_dict, template)

    # convert known accounts to certain categories
    csv_dict = convert_to_category(csv_dict)

    return csv_dict

def open_xls_to_dict(infile, template):

    csv_dict = {}
    with xlrd.open_workbook(os.path.join("data", infile)) as wb:
        sh = wb.sheet_by_index(0)

        i = 0
        for rownum in range(sh.nrows):
            if template["HeadersPresent"] == True and i == 0:
                pass
            else:
                fieldnames = []
                for column in template["Headers"]:
                    fieldnames.append(template["Headers"][column]["Header"])

                rowdict = collections.OrderedDict()
                n = 0
                for fieldname in fieldnames:
                    rowdict.update({fieldname: sh.row_values(rownum)[n]})
                    n += 1
                # print(f"rowdict = {rowdict}")

                csv_dict.update({i:rowdict})
                # print(f"contents are: {sh.row_values(rownum)}")
            i += 1
    
    # print(csv_dict)
    return csv_dict

def write_dict_to_csv(csv_dict, outfile, template):

    with open(os.path.join("data", outfile), 'w', newline='') as csvfile:
        csvwriter = csv.writer(
            csvfile, 
            delimiter='|', 
            quotechar='"', 
            quoting=csv.QUOTE_MINIMAL
            )

        # write headerrow first
        fieldnames = get_fieldnames_from_template(template)
        rowtowrite = fieldnames
        csvwriter.writerow(rowtowrite)

        # Iterate over csv_dict to write the rows to the csv writer
        i = 0
        for rownum in csv_dict:
            i += 1
            rowtowrite = []

            # Build the row by iterating over the columns
            for column in fieldnames:
                try:
                    rowtowrite.append(csv_dict[rownum][column])
                except:
                    rowtowrite.append("")

            csvwriter.writerow(rowtowrite)
       
        print(f"rows written to {outfile}: {i}")

def write_dict_to_xls(csv_dict, outfile, template):

    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('My Worksheet')

    # get template headers
    template_headers = get_fieldnames_from_template(template)
    # print(f"template headers: {template_headers}")

    data_headers = []
    for item in csv_dict[1].items():
        data_headers.append(item[0])
    # print(f"data headers: {data_headers}")

    # Create a data column to template column mapping table
    header_dict = {}
    template_c = 0
    for template_header in template_headers:
        template_c += 1

        data_c = 0
        for data_header in data_headers:
            # print(f"matching: {template_c}:{template_header} with {data_c}:{data_header}")
            data_c += 1
            if template_header == data_header:
                header_dict.update({data_c: template_c})
                break
    # print(header_dict)

    # Write header row
    c = 0
    for template_header in template_headers:
        worksheet.write(0, c, label = template_header)
        c += 1

    # Write data
    r = 1
    for row in csv_dict:
        c = 1
        for column in csv_dict[row]:
            # write column to the spot determined by the template (header_dict mapping table)
            try:
                template_c = header_dict[c]
                # print(f"c = {c}, template_c = {template_c}")

                if template["Headers"][template_c]["Convert"] == "Date":
                    date_format = xlwt.XFStyle()
                    date_format.num_format_str = 'dd/mm/yyyy'
                    worksheet.write(r, template_c-1, label = csv_dict[row][column], style = date_format)
                else:
                    worksheet.write(r, template_c-1, label = csv_dict[row][column])
                    # print(csv_dict[row][column])

            except:
                # If column does not exist in template, skip it
                pass
            c += 1
        r += 1
    
    # Saving workbook
    workbook.save(os.path.join("data", outfile))
    print(f"written {r-1} rows to {outfile}")

def add_dict_to_csv(csv_dict, infile, outfile, template = template_column_headers["Uniform Format"]):
    """
    Adds the new data to an existing csv file
    Could use a check if the earliest dates are already existing in the current file to prevent duplicates
    """

    current_dict = open_csv_to_dict(infile, template)

    fieldnames = []
    for column in template["Headers"]:
        fieldnames.append(template["Headers"][column]["Header"])

    count = 1
    for row in current_dict:
        count += 1

    for row in csv_dict:
        rowdict = collections.OrderedDict()
        for fieldname in fieldnames:
            try:
                rowdict.update({fieldname: csv_dict[row][fieldname]})
            except:
                rowdict.update({fieldname: ""})
        # print(rowdict)
        current_dict.update({count: rowdict})
        # print(current_dict)
        count += 1

    # print(current_csv)
    write_dict_to_csv(current_dict, outfile, template)

def convert_to_uniform(csv_dict, template):
    
    if template["Template"] == "Uniform Format":
        for row in csv_dict:
            # convert date values
            date_time_str = csv_dict[row]["TxnDate"]
            date_time_obj = datetime.datetime.strptime(date_time_str[0:10], "%Y-%m-%d")
            csv_dict[row]["TxnDate"] = date_time_obj

            # convert string to float
            value = float(csv_dict[row]["SignedAmount"])
            csv_dict[row].update({"SignedAmount": value})
            
    elif template["Template"] == "TRIONL2U":
        for row in csv_dict:
            
            # convert unsigned value to signed value using a sign column
            nothousands = csv_dict[row]["UnsignedAmount"].replace('.', '')
            value = float(nothousands.replace(',', '.'))
            signedvalue = math.copysign(value, -1) if csv_dict[row]["Sign"] == "Debet" else value
            csv_dict[row].update({"SignedAmount": signedvalue})

            # convert OriginAccount
            try:
                # print(csv_dict[row]["OriginAccount"])
                split = csv_dict[row]["OriginAccount"].split(" ", 1)
                # print(split)
                csv_dict[row]["OriginAccount"] = split[1]

            except:
                pass

            # convert date values
            date_time_str = csv_dict[row]["TxnDate"]
            date_time_obj = datetime.datetime.strptime(date_time_str, "%d-%m-%Y")
            csv_dict[row]["TxnDate"] = date_time_obj

    elif template["Template"] == "ABNANL2A":
        for row in csv_dict:
            pass
            # convert date values

    return csv_dict

def convert_to_category(csv_dict):
    
    with open("src/known_accounts.json", "r") as infile:
        known_accounts = json.load(infile)
    
        # print(known_accounts)
        for row in csv_dict:
            csv_dict[row]["Category"] = ""

            for account in known_accounts:
                if csv_dict[row]["OriginAccount"] == account:
                    csv_dict[row]["Category"] = known_accounts[account]
                    break

    with open("src/known_accounts_simple.json", "r") as infile:
        known_accounts = json.load(infile)
        # print(known_accounts)
        for row in csv_dict:
            csv_dict[row]["Categorie"] = ""

            for account in known_accounts:
                if csv_dict[row]["OriginAccount"] == account:
                    csv_dict[row]["Categorie"] = known_accounts[account]
                    break

    return csv_dict