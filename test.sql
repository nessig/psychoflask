-- select username,
-- title_headline,
-- body_headline,
-- pub_date
-- from users
-- inner join (SELECT author_id,pub_date,
-- ts_headline(title, q) as title_headline,
-- ts_headline(body,q,'MaxWords=6, MinWords=3,MaxFragments=3, FragmentDelimiter=" ... "') as body_headline
-- FROM(
-- select author_id,title,body,tsv,q,pub_date
-- from posts, plainto_tsquery('elephants') as q
-- WHERE (tsv @@ q)
-- ) as t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery('elephants')) DESC LIMIT 5) as foo
-- on (users.id=author_id);

select comment_date,username,comment_text
from users
inner join comments
on (users.id=commenter_id)
where post_id=5;

