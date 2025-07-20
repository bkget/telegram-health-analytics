select
  source_file,
  min(date) as first_message_at,
  max(date) as last_message_at,
  count(*) as total_messages,
  sum(views) as total_views,
  sum(replies) as total_replies,
  sum(forwards) as total_forwards
from {{ ref('stg_telegram_messages') }}
group by source_file
