with raw as (

  select
    id,
    -- Remove the '.json' extension from source_file
    regexp_replace(source_file, '\.json$', '') as source_file,
    -- Extract fields from JSON message
    (message->>'date')::timestamp as date,
    message->>'text' as text,
    (message->>'views')::int as views,
    (message->>'from_id')::int as from_id,
    (message->>'replies')::int as replies,
    (message->>'forwards')::int as forwards
  from public.raw_telegram_messages

)

select * from raw
