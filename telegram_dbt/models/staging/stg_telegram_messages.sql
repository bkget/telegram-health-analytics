{{ config (materialized = "table") }}

with raw as (

  select
    id,
    regexp_replace(source_file, '\.json$', '') as source_file,
    (message->>'date')::timestamp as date,
    message->>'text' as text,
    (message->>'views')::int as views,
    
    -- extracts only the digits from the from_id field before casting
    regexp_replace(message->>'from_id', '\D', '', 'g')::bigint as from_id,

    (message->>'replies')::int as replies,
    (message->>'forwards')::int as forwards

  from public.raw_telegram_messages

)

select * from raw
