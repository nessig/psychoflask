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
       title varchar(30) not null,
       body varchar(400) not null,
       author_id integer references users (id)
);

drop table if exists followers;
create table followers (
       follower int references users (id),
       following int references users (id)
);
