Credit_Card_Databases-API/schema.sql
-- USERS TABLE
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TRANSACTIONS TABLE
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    time BIGINT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    class BOOLEAN,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TRANSACTION_FEATURES TABLE
CREATE TABLE transaction_features (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    V1 DECIMAL(10,6),
    V2 DECIMAL(10,6),
    V3 DECIMAL(10,6),
    V4 DECIMAL(10,6),
    V5 DECIMAL(10,6),
    V6 DECIMAL(10,6),
    V7 DECIMAL(10,6),
    V8 DECIMAL(10,6),
    V9 DECIMAL(10,6),
    V10 DECIMAL(10,6),
    V11 DECIMAL(10,6),
    V12 DECIMAL(10,6),
    V13 DECIMAL(10,6),
    V14 DECIMAL(10,6),
    V15 DECIMAL(10,6),
    V16 DECIMAL(10,6),
    V17 DECIMAL(10,6),
    V18 DECIMAL(10,6),
    V19 DECIMAL(10,6),
    V20 DECIMAL(10,6),
    V21 DECIMAL(10,6),
    V22 DECIMAL(10,6),
    V23 DECIMAL(10,6),
    V24 DECIMAL(10,6),
    V25 DECIMAL(10,6),
    V26 DECIMAL(10,6),
    V27 DECIMAL(10,6),
    V28 DECIMAL(10,6)
);

-- TRANSACTION_LOGS TABLE
CREATE TABLE transaction_logs (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL,
    message TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ML_MODELS TABLE
CREATE TABLE ml_models (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) NOT NULL,
    description TEXT,
    trained_on TIMESTAMP,
    accuracy DECIMAL(5,4)
);

-- MODEL_PREDICTIONS TABLE
CREATE TABLE model_predictions (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    model_id INTEGER NOT NULL REFERENCES ml_models(id) ON DELETE CASCADE,
    predicted_class BOOLEAN,
    probability DECIMAL(5,4),
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- STORED PROCEDURE: Insert a transaction with validation
CREATE OR REPLACE FUNCTION insert_transaction(
    p_user_id INTEGER,
    p_time BIGINT,
    p_amount DECIMAL,
    p_class BOOLEAN,
    p_status VARCHAR
) RETURNS INTEGER AS $$
DECLARE
    new_id INTEGER;
BEGIN
    -- Validate user exists
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = p_user_id) THEN
        RAISE EXCEPTION 'User ID % does not exist', p_user_id;
    END IF;

    -- Validate amount
    IF p_amount <= 0 THEN
        RAISE EXCEPTION 'Amount must be positive';
    END IF;

    -- Insert transaction
    INSERT INTO transactions(user_id, time, amount, class, status)
    VALUES (p_user_id, p_time, p_amount, p_class, p_status)
    RETURNING id INTO new_id;

    RETURN new_id;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER FUNCTION: Log changes to transactions
CREATE OR REPLACE FUNCTION log_transaction_change() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO transaction_logs(transaction_id, action, message)
        VALUES (NEW.id, 'INSERT', 'Transaction created');
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO transaction_logs(transaction_id, action, message)
        VALUES (NEW.id, 'UPDATE', 'Transaction updated');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER: Attach to transactions table
CREATE TRIGGER trg_log_transaction_change
AFTER INSERT OR UPDATE ON transactions
FOR EACH ROW EXECUTE FUNCTION log_transaction_change();
