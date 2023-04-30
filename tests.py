import datetime

from src.templates import (
    template_column_headers,
    get_fieldnames_from_template,
)

from src.methods import (
    open_csv_to_dict,
    open_xls_to_dict,
    write_dict_to_csv,
    write_dict_to_xls,
    add_dict_to_csv,
)

# def didi_test():
#     # import triodos mutations
#     infile = 'mutations20200630082802.csv'
#     template = template_column_headers["TRIONL2U"]
#     csv_dict = open_csv_to_dict(infile, template)

#     # save to didi xls format
#     outfile = 'Finances_didi.xls'
#     template = template_column_headers["Didi Format"]
#     write_dict_to_xls(csv_dict, outfile, template)


def test_triodos():
    # import triodos mutations
    infile = 'mutations20200531101607.csv'
    template = template_column_headers["TRIONL2U"]
    csv_dict = open_csv_to_dict(infile, template)

    # Write mutations to their own csv file uniform format 
    outfile = "Finances_first.csv"
    template = template_column_headers["Uniform Format"]
    write_dict_to_csv(csv_dict, outfile, template)

    # import new triodos mutations
    infile = 'mutations20200630082802.csv'
    template = template_column_headers["TRIONL2U"]
    csv_dict = open_csv_to_dict(infile, template)

    # add to current uniform csv
    infile = 'Finances_first.csv'
    outfile = 'Finances_added.csv'
    template = template_column_headers["Uniform Format"]
    add_dict_to_csv(csv_dict, infile, outfile, template)

    # reopen finance file
    infile = 'Finances_added.csv'
    template = template_column_headers["Uniform Format"]
    csv_dict = open_csv_to_dict(infile, template)

    # make some changes
    # print(f"{csv_dict[1]}")
    # csv_dict[1]["TxnDate"] = datetime.datetime.strptime("05-09-1999", "%d-%m-%Y")
    # csv_dict[1]["SignedAmount"] += 1
    
    # resave it
    outfile = 'Finances_reloaded.csv'
    write_dict_to_csv(csv_dict, outfile, template)

    # save to xls
    outfile = 'Finances_reloaded.xls'
    write_dict_to_xls(csv_dict, outfile, template)


def test_abnamro():
    infile = 'XLS200624131731.xls'
    template = template_column_headers["ABNANL2A"]
    csv_dict = open_xls_to_dict(infile, template)

    outfile = "ABNAMRO.csv"
    template = template_column_headers["Uniform Format"]
    write_dict_to_csv(csv_dict, outfile, template)


if __name__ == "__main__":

    didi_test()

    test_triodos()

    test_abnamro()