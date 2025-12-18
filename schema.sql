CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);






CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    shipping_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);






CREATE TABLE order_item (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);




 

CREATE OR REPLACE FUNCTION search_orders(
    p_customer_id INT DEFAULT NULL,
    p_min_amount DECIMAL DEFAULT NULL,
    p_status VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    order_id INT,
    customer_id INT,
    total_amount DECIMAL,
    status VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        o.id,
        o.customer_id,
        o.total_amount,
        o.status
    FROM orders o
    WHERE
        (p_customer_id IS NULL OR o.customer_id = p_customer_id)
        AND (p_min_amount IS NULL OR o.total_amount >= p_min_amount)
        AND (p_status IS NULL OR o.status = p_status);
END;
$$ LANGUAGE plpgsql;
