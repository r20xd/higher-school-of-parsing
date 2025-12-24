CREATE TABLE IF NOT EXISTS scraping_tasks (
    id TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    result JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);
