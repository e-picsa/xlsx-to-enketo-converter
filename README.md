### Enketo & XForm app convertors

This repository has endpoints that help convert an xlsx file to xForm and another that helps convert an xForm to an Enketo.

### How to run the app

1. Clone the repository
2. If you have docker running then just run `make start`
3. Otherwise, for the xform to enketo endpoint, run `cd xform-to-enketo` and then `npm install` to install dependencies.
   To run the app use `node server.js` and the `post` endpoint will be available at http://localhost:5261/api/xlsform-to-enketo

   For the xlsx to xform endpoint, run `cd xls-to-xform` and then `poetry install` to install dependencies. Run `poetry run python server.py`

   To run the app use node server.js and the endpoint will be available at `post` http://localhost:5262/api/convert_xls_to_xml"
