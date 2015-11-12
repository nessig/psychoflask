drop table if exists messages;
CREATE TABLE messages (
    title       text,
    body        text,
    tsv         tsvector
);

-- CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
-- ON messages FOR EACH ROW EXECUTE PROCEDURE
-- tsvector_update_trigger(tsv, 'pg_catalog.english', title, body);

CREATE FUNCTION messages_trigger() RETURNS trigger AS $$
begin
  new.tsv :=
     setweight(to_tsvector('pg_catalog.english', coalesce(new.title,'')), 'A') ||
     setweight(to_tsvector('pg_catalog.english', coalesce(new.body,'')), 'D');
  return new;
end
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
    ON messages FOR EACH ROW EXECUTE PROCEDURE messages_trigger();

INSERT INTO messages VALUES('title here1', 'the body text is here1');
INSERT INTO messages VALUES('title here2', 'the body text is here2');
INSERT INTO messages VALUES('title here3', 'the body text is here3');
