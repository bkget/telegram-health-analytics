select
    date_trunc('day', date) as date_id,
    count(*) as total_messages,
    sum(views) as total_views,
    sum(replies) as total_replies,
    sum(forwards) as total_forwards
from {{ ref('stg_telegram_messages') }}
group by 1
