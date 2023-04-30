
# set headers from template
# maps BIC codes of bank and gives the ordered columns usable names

def get_fieldnames_from_template(template):
    fieldnames = []
    for column in template["Headers"]:
        fieldnames.append(template["Headers"][column]["Header"])

    return fieldnames
    
template_column_headers = {
    "TRIONL2U": {
        "Template": "TRIONL2U",
        "Filetype": "CSV",
        "HeadersPresent": False,
        "Delimiter": ",",
        "Headers": {
            1: {
                "Header": "TxnDate",
                "Format": "String",
                "Convert": "Date",
            },
            2: {
                "Header": "TargetAccount",
                "Format": "String",
                "Convert": "String",
            },
            3: {
                "Header": "UnsignedAmount",
                "Format": "String",
                "Convert": "Float",
            },
            4: {
                "Header": "Sign",
                "Format": "String",
                "Convert": "String",
            },
            5: {
                "Header": "OriginName",
                "Format": "String",
                "Convert": "String",
            },
            6: {
                "Header": "OriginAccount",
                "Format": "String",
                "Convert": "String",
            },
            7: {
                "Header": "TxnType",
                "Format": "String",
                "Convert": "String",
            },
            8: {
                "Header": "Description",
                "Format": "String",
                "Convert": "String",
            },
        },
    },
    "ABNANL2A": {
        "Template": "ABNANL2A",
        "Filetype": "XLS",
        "HeadersPresent": True,
        "Delimiter": ",",
        "Headers": {
            1: {
                "Header": "TargetAccount",
                "Format": "String",
                "Convert": "String",
            },
            2: {
                "Header": "Currency",
                "Format": "String",
                "Convert": "String",
            },
            3: {
                "Header": "TxnDate",
                "Format": "String",
                "Convert": "Date",
            },
            4: {
                "Header": "ValueDate",
                "Format": "String",
                "Convert": "Date",
            },
            5: {
                "Header": "BalanceBefore",
                "Format": "String",
                "Convert": "Float",
            },
            6: {
                "Header": "BalanceAfter",
                "Format": "String",
                "Convert": "Float",
            },
            7: {
                "Header": "SignedAmount",
                "Format": "String",
                "Convert": "Float",
            },
            8: {
                "Header": "Description",
                "Format": "String",
                "Convert": "String",
            },
        },
    },
    "Uniform Format": {
        "Template": "Uniform Format",
        "Filetype": "CSV",
        "HeadersPresent": True,
        "Delimiter": "|",
        "Headers": {
            1: {
                "Header": "Category",
                "Format": "String",
                "Convert": "String",
            },
            2: {
                "Header": "TargetAccount",
                "Format": "String",
                "Convert": "String",
            },
            3: {
                "Header": "TxnDate",
                "Format": "Date",
                "Convert": "Date",
            },
            4: {
                "Header": "SignedAmount",
                "Format": "Float",
                "Convert": "Float",
            },
            5: {
                "Header": "OriginAccount",
                "Format": "String",
                "Convert": "String",
            },
            6: {
                "Header": "OriginName",
                "Format": "String",
                "Convert": "String",
            },
            7: {
                "Header": "Description",
                "Format": "String",
                "Convert": "String",
            },
        },
    },
        "Didi Format": {
        "Template": "Didi Format",
        "Filetype": "XLS",
        "HeadersPresent": True,
        "Delimiter": "|",
        "Headers": {
            1: {
                "Header": "Categorie",
                "Format": "String",
                "Convert": "String",
            },
            2: {
                "Header": "TxnDate",
                "Format": "Date",
                "Convert": "Date",
            },
            3: {
                "Header": "SignedAmount",
                "Format": "Float",
                "Convert": "Float",
            },
            4: {
                "Header": "Sign",
                "Format": "String",
                "Convert": "String",
            },
            5: {
                "Header": "OriginName",
                "Format": "String",
                "Convert": "String",
            },
            6: {
                "Header": "Description",
                "Format": "String",
                "Convert": "String",
            },
        },
    },
}

# build headers yourself (Triodos as example)
manual_column_headers = {}
manual_column_headers.update({1: "Date"})
manual_column_headers.update({2: "TargetAccount"})
manual_column_headers.update({3: "UnsignedAmount"})
manual_column_headers.update({4: "Sign"})
manual_column_headers.update({5: "OriginName"})
manual_column_headers.update({6: "OriginAccount"})
manual_column_headers.update({7: "TxnType"})
manual_column_headers.update({8: "Description"})

