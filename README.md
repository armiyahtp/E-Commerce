## Setup

1. Open the \E_commerce_analytic_engin\src\project> folder in vscode

2. Activate the venv
    - ../../venv/bin/activate
        OR
    - ../../venv/scripts/activate

3. Install dependencies
    - pip install django psycopg2-binary

4. Configure PostgreSQL in settings.py

5. Run schema.sql in database

6. Run server
    - python manage.py runserver

7. Use postman to test API
    - Select GET method, http://127.0.0.1:8000/api/customers/recent-top-spenders for recent top spenders
    - Select GET method, http://127.0.0.1:8000/api/orders/search for search orders
    - Select POST method, http://127.0.0.1:8000/api/reports/generate for generate reports\
        1️⃣ Click Body tab
        2️⃣ Select raw
        3️⃣ Select JSON (right dropdown)
        - input the json like this: 
            {
                "view_name": "sales_overview",
                "filters": [
                    { "field": "region", "op": "eq", "value": "Kochi" }
                ]
            }


