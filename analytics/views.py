import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt




@require_GET
def recent_top_spenders(request):
    sort_order = request.GET.get("sort", "desc").upper()   
    days = request.GET.get("days", "30")                   

    if sort_order not in ["ASC", "DESC"]:
        sort_order = "DESC"

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT
                c.name,
                c.email,
                SUM(o.total_amount) AS total_spent
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            WHERE o.created_at >= CURRENT_DATE - (%s * INTERVAL '1 day')
            GROUP BY c.id, c.name, c.email
            ORDER BY total_spent {sort_order};
        """, [days])
        rows = cursor.fetchall()

    data = []
    for r in rows:
        data.append({
            "name": r[0],
            "email": r[1],
            "total_spent": float(r[2])
        })

    return JsonResponse(data, safe=False)






@require_GET
def search_orders(request):
    customer_id = request.GET.get("customer_id")
    min_amount = request.GET.get("min_amount")
    status = request.GET.get("status")

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM search_orders(%s, %s, %s);"
            , [customer_id, min_amount, status]
        )


        row = cursor.fetchall()
    return JsonResponse(row, safe=False)










ALLOWED_VIEWS = {
    "sales_overview": {
        "table": "orders",
        "fields": {
            "region": "shipping_address",
            "status": "status",
            "amount": "total_amount"
        }
    }
}







@csrf_exempt
@require_POST
def generate_report(request):
    body = json.loads(request.body)
    view_name = body.get("view_name")
    filters = body.get("filters", [])




    if view_name not in ALLOWED_VIEWS:
        return JsonResponse({"error": "Invalid view name"}, status=400)
    
    view_config = ALLOWED_VIEWS[view_name]
    table = view_config["table"]
    allowed_fields = view_config["fields"]


    sql = f"SELECT * FROM {table} WHERE 1=1"
    params = []



    for filter in filters:
        field = filter["field"]
        value = filter["value"]
        operator = filter["op"]


        if field not in allowed_fields:
            return JsonResponse({"error": "Invalid field name"}, status=400)
        

        column = allowed_fields[field]  

        if operator == "eq":
            sql += f" AND {column} = %s"
            params.append(value)
        elif operator == "gt":
            sql += f" AND {column} > %s"
            params.append(value)
        else:
            return JsonResponse({"error": "Invalid operator"}, status=400)
        
    
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()

    return JsonResponse(rows, safe=False)