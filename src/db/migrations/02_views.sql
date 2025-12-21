CREATE OR REPLACE VIEW task_stats AS
SELECT
    status,
    COUNT(*) as count,
    AVG(EXTRACT(EPOCH FROM (completed_at - created_at))) as avg_duration
FROM scraping_tasks
GROUP BY status;

CREATE OR REPLACE VIEW daily_activity AS
SELECT
    DATE_TRUNC('day', created_at) as day,
    COUNT(*) as total_tasks
FROM scraping_tasks
GROUP BY 1;
