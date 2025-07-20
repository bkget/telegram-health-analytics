select
  id as message_id,
  source_file,
  date,
  text,
  views,
  replies,
  forwards
from {{ ref('stg_telegram_messages') }}
where date is not null
