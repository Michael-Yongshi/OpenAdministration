from sqlitemanager.handler import SQLiteHandler

def initialize_sqlitehandler():

    # connect to database
    handler = SQLiteHandler()
    handler.database_open(filename="administration")

    if handler.database == None:
        handler.database_new(filename="administration")

    check_tables(handler)

    return handler

def check_tables(handler):

    # tablename = "suppliers"

    # try:
    #     handler.database.tables[tablename]
    # except:
    #     # add a table
    #     handler.table_create(
    #     tablename=tablename,
    #         column_names = [],
    #         column_types = [],
    #     )

    # tablename = "clients"

    # try:
    #     handler.database.tables[tablename]
    # except:
    #     # add a table
    #     handler.table_create(
    #     tablename=tablename,
    #         column_names = [],
    #         column_types = [],
    #     )

    tablename = "purchase_categories"

    try:
        handler.database.tables[tablename]
    except:
        # add a table
        handler.table_create(
        tablename=tablename,
            column_names = [],
            column_types = [],
        )

        # add some records directly in the database
        handler.table_create_add_records(
            tablename=tablename,
            recordsvalues=[
                [1, "Inventory"],
                [2, "Equipment"],
                [3, "Office Supplies"],
                [4, "Administration"],
                [5, "Communication"],
                [6, "Transportation"],
                [7, "Representation"],
                [8, "Marketing"],
                [9, "Finance and Insurance"],
                ]
            )

    tablename = "purchases"
    try:
        handler.database.tables[tablename]
    except:
        # add a table
        handler.table_create(
        tablename=tablename,
            column_names = ["category", "supplier", "date", "amount", "vat", "isPaid"],
            # column_types = ["INTEGER REFERENCES purchase_categories(id)", "INTEGER REFERENCES suppliers(id)", "Text", "Integer", "Integer", "Bool"],
            column_types = ["Text", "Text", "Text", "Integer", "Integer", "Bool"],
        )

    tablename = "sales"
    try:
        handler.database.tables[tablename]
    except:
        # add a table
        handler.table_create(
        tablename=tablename,
            column_names = ["client", "date", "amount", "vat", "isPaid"],
            column_types = ["Text", "Integer", "Integer", "Integer", "Text"],
            # column_types = ["INTEGER REFERENCES clients(id)", "Integer", "Integer", "Integer", "Text"],
        )

    tablename = "transactions"
    try:
        handler.database.tables[tablename]
    except:
        # add a table
        handler.table_create(
        tablename=tablename,
            column_names = [],
            column_types = [],
        )

def get_tables(handler):

    # print(handler.database.tables)

    tablelist = ""
    for tablename in handler.database.tables:
        tablelist += f"{tablename}\n"
        tablelist += f"{handler.database.read_column_names(tablename)}\n\n"

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