# Try entering the following in the search box:
#  3 or 1=1

import bottle
from datetime import datetime
from mysql.connector import connect

con = connect(user='root', password='passw0rd', database='simpledb')
cursor = con.cursor()

@bottle.route('/')
def hello():
    qty = 0
    if 'qty' in bottle.request.params:
        qty = bottle.request.params['qty']

    # SQL Injection vulnerability here:
    cursor.execute("""
    select ProdId, ProdName, Quantity, ProdNextShipDate
    from product
    where Quantity < {0}
    """.format(qty))  # Also try   ProdName = '{0}'

    # Retrieve results
    result = cursor.fetchall()

    table = """
        <table>
        <tr>
            <td>Product ID`
            <td>Product Name
            <td>Quantity
            <td>Next Ship Date
        </tr>
        """

    for row in result:
        (prodId, prodName, quantity, shipDate) = row
        tableRow = """
        <tr>
            <td>{0}
            <td>{1}
            <td>{2}
            <td>{3}
        </tr>
        """.format(prodId, prodName, quantity, shipDate)
        table += tableRow

    table += "</table>"
    return HTML_DOC.format(
            table)

HTML_DOC = """<html><body>
        <form>
          Show products with quantity less than: <input type='text' name='qty' value=''>
          <input type='submit' value='Go!'>
        </form>
        {0}</body></html>"""

# Launch the BottlePy dev server
if __name__ == "__main__":
    bottle.run(host='localhost', debug=True)

