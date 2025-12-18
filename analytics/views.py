from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_GET


@require_GET
def recent_top_spenders(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                c.name,
                c.email,
                SUM(o.total_amount) AS total_spent
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            WHERE o.created_at >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY c.id, c.name, c.email
            ORDER BY total_spent DESC;
        """)
        rows = cursor.fetchall()

    data = []
    for r in rows:
        data.append({
            "name": r[0],
            "email": r[1],
            "total_spent": float(r[2])
        })

    return JsonResponse(data, safe=False)
