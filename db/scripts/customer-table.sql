CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS stripe_integration (
    id SERIAL PRIMARY KEY,
    customer_id INT UNIQUE,
    stripe_id varchar(255),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);