drop table if exists skillplant_data;

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
    date_gathered timestamp
);

alter table skillplant_data
    owner to postgres;

