-- SELECT title,body FROM (
--   SELECT title, body, tsv
--     FROM messages, plainto_tsquery('YOUR QUERY') AS q
--       WHERE (tsv @@ q)
      
-- ) AS t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('YOUR QUERY')) DESC LIMIT 5;


-- SELECT title, body FROM(
-- select title,body,tsv
-- from messages, plainto_tsquery('cheese') as q
-- WHERE (tsv @@ q)
-- ) as t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('cheese')) DESC LIMIT 5;

-- SELECT ts_headline(title, q), ts_headline(body,q) FROM(
-- select title,body,tsv
-- from messages, plainto_tsquery('cheese') as q
-- WHERE (tsv @@ q)
-- ) as t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('cheese')) DESC LIMIT 5;

-- select ts_headline(body, query)
--   from messages, to_tsquery('wonderful & thing')  query, 
--   where query @@ tsv;


-- select ts_headline(body, query) ,ts_rank(tsv, query)
--   from messages, to_tsquery('title') as query
--     where tsv @@ query and body ilike '%the body%';

-- SELECT title, ts_headline(body, q), rank
-- FROM (SELECT title, body, q, ts_rank_cd(tsv, q) AS rank
--       FROM messages, to_tsquery('cheese') q
--       WHERE tsv @@ q
--       ORDER BY rank DESC
--       LIMIT 10) AS foo;

-- insert into messages (title,body) values ('cheesey title text', 'body title elephants');

-- SELECT ts_headline(title, q), ts_headline(body, q), rank
-- FROM (SELECT title, body, q, ts_rank_cd(tsv, q) AS rank
--       FROM messages, to_tsquery('body | text') q
--       WHERE tsv @@ q
--       ORDER BY rank DESC
--       LIMIT 10) AS foo;

-- SELECT ts_headline(title, q), ts_headline(body,q) FROM(
-- select title,body,tsv,q
-- from messages, plainto_tsquery('body') as q
-- WHERE (tsv @@ q)
-- ) as t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('body')) DESC LIMIT 5;

-- select users.username,body_headline,title_headline
-- from users
-- inner join (SELECT author_id,
-- ts_headline(title, q) as title_headline,
-- ts_headline(body,q) as body_headline
-- FROM(
-- select author_id,title,body,tsv,q
-- from posts, plainto_tsquery('body') as q
-- WHERE (tsv @@ q)
-- ) as t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('body')) DESC LIMIT 5)
-- on (users.id=author_id);

-- select users.username,posts.title,posts.body,posts.pub_date from users
-- inner join posts
-- on (users.id=author_id)
-- order by pub_date desc;

-- select users.username,body_headline,title_headline
-- from users
-- inner join (SELECT author_id,
-- ts_headline(title, q) as title_headline,
-- ts_headline(body,q) as body_headline
-- FROM(
-- select pub_date,author_id,title,body,tsv,q
-- from posts, plainto_tsquery('body') as q
-- WHERE (tsv @@ q)
-- ) as t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('body')) DESC LIMIT 5) as foo
-- on (users.id=author_id);

-- SELECT author_id,pub_date,
-- ts_headline(title, q) as title_headline,
-- ts_headline(body,q) as body_headline
-- FROM(
-- select author_id,title,body,tsv,q,pub_date
-- from posts, plainto_tsquery('body') as q
-- WHERE (tsv @@ q)
-- ) as t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('body')) DESC LIMIT 5;


