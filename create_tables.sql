drop table if exists skillplant_data;

ALTER USER postgres PASSWORD 'changeme';

create table IF NOT EXISTS skillplant_data
(
    id            serial
        constraint skillplant_data_pk
            primary key,
    position      varchar   not null,
    company       varchar   not null,
    date_updated  date      not null,
    region        varchar,
    country       varchar,
    description   text,
    remote        varchar,
    job_type      varchar,
    seniority     varchar,
    date_gathered timestamp,
    hard_skill_1   varchar,
    hard_skill_2   varchar,
    hard_skill_3   varchar,
    hard_skill_4   varchar,
    hard_skill_5   varchar,
    soft_skill_1   varchar,
    soft_skill_2   varchar,
    soft_skill_3   varchar,
    soft_skill_4   varchar,
    soft_skill_5   varchar
);

alter table skillplant_data
    owner to postgres;

