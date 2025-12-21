-- Создание таблицы scraping_tasks
CREATE TABLE IF NOT EXISTS scraping_tasks (
    id VARCHAR(36) PRIMARY KEY,
    url TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    result JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

-- Добавление колонок если они отсутствуют (для существующей таблицы)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'scraping_tasks' AND column_name = 'completed_at') THEN
        ALTER TABLE scraping_tasks ADD COLUMN completed_at TIMESTAMP;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'scraping_tasks' AND column_name = 'result') THEN
        ALTER TABLE scraping_tasks ADD COLUMN result JSONB;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'scraping_tasks' AND column_name = 'error_message') THEN
        ALTER TABLE scraping_tasks ADD COLUMN error_message TEXT;
    END IF;
END $$;
