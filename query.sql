drop table if exists users cascade;
create table users (
       id serial primary key,
       username varchar(80) unique not null,
       email varchar(80) unique not null,
       password varchar(80) not null,
       about_me varchar(200),
       last_seen timestamp
);

drop table if exists posts;
create table posts (
       id serial primary key,
       title varchar(80) not null,
       body text not null,
       pub_date timestamp,
       author_id integer references users (id),
       tsv tsvector
);

drop table if exists followers;
create table followers (
       follower int references users (id),
       following int references users (id)
);

CREATE FUNCTION posts_trigger() RETURNS trigger AS $$
begin
  new.tsv :=
     setweight(to_tsvector('pg_catalog.english', coalesce(new.title,'')), 'A') ||
     setweight(to_tsvector('pg_catalog.english', coalesce(new.body,'')), 'D');
  return new;
end
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
    ON posts FOR EACH ROW EXECUTE PROCEDURE posts_trigger();

-- INSERT INTO posts VALUES('title here1', 'the body text is here1');
-- INSERT INTO posts VALUES('title here2', 'the body text is here2');
-- INSERT INTO posts VALUES('title here3', 'the body text is here3');

