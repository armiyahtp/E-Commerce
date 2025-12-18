from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_GET


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

