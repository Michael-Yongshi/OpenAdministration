# Administration_Ledger

## Todo

0
on launch, check if database exists in root:
- supplier
- clients
- purchase_invoices
- sale-invoices

1
- add single invoice, purchase or sale, add respective supplier / client
- add single supplier / client (asking if you also want to add an invoice)
show total vat per quarter (to pay or to receive)

2
- import list of sale invoices
- add another invoice based on the last added (if you need to add multiple similar invoices)

3
- add transaction database
- way to import transactions
- map transactions to invoices
- give invoices a 'isPaid' field
- set invoice 'isPaid' to 1 if mapped to transactions totalling the amount
- set invoice 'isPaid' manually and ask to add a new transaction (if paid in cash for example)

4
- make profit/loss statement

5
- make balance sheet at certain point in time


## Templates

### ABN AMRO
omschrijving:
if left(column 8 / H / omschrijving; 4 characters)
/TRT -> split it in forward slashes, iban is 4th string and name 8th string.
BEA -> split it in spaces, name is 4th but spanning multiple spaces until a comma
SEPA
ABN

## License

Licensed under GPL-3.0-or-later, see LICENSE file for details.

Copyright © 2020 WAM-Desktop contributors.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.