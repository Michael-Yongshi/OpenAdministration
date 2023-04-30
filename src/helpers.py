from sqlitemanager import handler
from sqlitemanager.objects import Database

def check_tables(db):

    tablename = "purchase_categories"

    try:
        handler.get_tables(db=db, table_selection=tablename)
    except:
        # add a table
        handler.create_table(
        db=db,
        config_dict = {tablename: {
        "id": {"column_type": "int", "primary_key": True, "autonumber": True},
        "name": {"column_type": "str"},
        }},
        record_dict = {tablename:[
        {"name":"Inventory"},
        {"name":"Equipment"},
        {"name":"Office Supplies"},
        {"name":"Administration"},
        {"name":"Communication"},
        {"name":"Transportation"},
        {"name":"Representation"},
        {"name":"Marketing"},
        {"name":"Finance and Insurance"},
        ]}
        )

    tablename = "purchases"
    try:
        handler.get_tables(db=db, table_selection=tablename)
    except:
        # add a table
        handler.create_table(
        db=db,
        config_dict = {tablename: {
        "id": {"column_type": "int", "primary_key": True, "autonumber": True},
        "cat_id": {"column_type": "int", "foreign_key": {"purchase_categories":"id"}},
        "supplier": {"column_type": "str"},
        "date": {"column_type": "dt"},
        "amount": {"column_type": "int",},
        "vat_id": {"column_type": "int", "foreign_key": {"vat_categories":"id"}},
        "vat": {"column_type": "int"},
        "isPaid": {"column_type": "Bool"},
        }}
        )

    tablename = "sales"
    try:
        handler.get_tables(db=db, table_selection=tablename)
    except:
        # add a table
        handler.create_table(
        db=db,
        config_dict = {tablename: {
            "id": {"column_type": "int", "primary_key": True, "autonumber": True},
            "client": {"column_type": "str"}, # "customer_id": {"column_type": "int", "foreign_key": {"customers":"id"}},
            "category": {"column_type": "str"}, # "cat_id": {"column_type": "int", "foreign_key": {"customer_categories":"id"}},
            "date": {"column_type": "dt"},
            "amount": {"column_type": "int",},
            "vat_id": {"column_type": "int", "foreign_key": {"vat_categories":"id"}},
            "vat": {"column_type": "int"}, 
            "isPaid": {"column_type": "Bool"},
        }}
        )

    tablename = "transactions"
    try:
        handler.get_tables(db=db, table_selection=tablename)
    except:
        # add a table
        handler.create_table(
        db=db,
        config_dict = {tablename: {
            "id": {"column_type": "int", "primary_key": True, "autonumber": True},
            "account": {"column_type": "str"},
            "account_counterparty": {"column_type": "str"},
            "date": {"column_type": "dt"},
            "amount": {"column_type": "int",},
        }}
        )

    # tablename = "suppliers"

    # try:
    #     handler.get_tables(db=db, table_selection=tablename)
    # except:
    #     # add a table
    #     handler.create_table(
        # db=db,
    #     tablename=tablename,
    #         column_names = [],
    #         column_types = [],
    #     )

    # tablename = "clients"

    # try:
    #     handler.get_tables(db=db, table_selection=tablename)
    # except:
    #     # add a table
    #     handler.create_table(
        # db=db,
    #     tablename=tablename,
    #         column_names = [],
    #         column_types = [],
    #     )

def get_database_info(db):

    tablelist = ""
    tables_dict = handler.get_tables(db=db)
    print(tables_dict)
    for tablename in tables_dict:
        table_object = tables_dict[tablename]
        print(table_object)
        tablelist += f"{tablename}\n"
        tablelist += f"{table_object.metadata}\n\n"

    return tablelist

def get_columns(handler, tablename):

    column_names = handler.database.read_column_names(tablename)

    return column_names

def get_records(handler, tablename):

    records = handler.table_read_records(tablename=tablename)

    return records

def create_records(handler, tablename, values):
    """expects multiple a list of list of values for multiple rows
    [
    [1, "Hawking", 68, 2],
    [2, "Marie Curie", 20, 2],
    [3, "Einstein", 100, 1],
    [4, "Rosenburg", 78, 1],
    [5, "Neil dGrasse Tyson", 57, True],
    ]
    """

    # TODO
    max_order = 1

    handler.table_create_add_records(tablename=tablename, recordsvalues=values)

# helper functions

def calc_invoice_vat(vatpercentage_float, amount_float):
    # TODO
    # check comma, dot

    try:
        vatamount = vatpercentage_float / 100 * amount_float
        total = vatamount + amount_float
        return vatamount

    except:
        return 0

def calc_invoice_total(vatpercentage_float, amount_float):
    # TODO
    # check comma, dot

    try:
        vatamount = calc_invoice_vat(vatpercentage_float, amount_float)
        total = vatamount + amount_float
        return total

    except:
        return 0

def get_date_range(year, quarter):

    if quarter in ["", None, "All"]:
        low = year + '0101'
        high = year + '1231'
    elif quarter == "Q1":
        low = year + '0101'
        high = year + '0331'
    elif quarter == "Q2":
        low = year + '0401'
        high = year + '0631'
    elif quarter == "Q3":
        low = year + '0701'
        high = year + '0931'
    elif quarter == "Q4":
        low = year + '1001'
        high = year + '1231'
    else:
        low = 0
        high = 99991231
    return [low, high]