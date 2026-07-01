CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'learner'))
);

CREATE TABLE IF NOT EXISTS quiz_results (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    question_id INT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS eval_scores (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL,
    model TEXT NOT NULL,
    accuracy FLOAT NOT NULL,
    groundedness FLOAT NOT NULL,
    latency_ms INT NOT NULL,
    run_at TIMESTAMPTZ DEFAULT NOW()
);
