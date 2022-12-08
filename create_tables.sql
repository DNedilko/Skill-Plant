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
    remote        boolean default false,
    job_type      real    default 0,
    seniority     integer
        constraint skillplant_data_seniority_types_type_id_fk
            references seniority_types,
    date_gathered timestamp not null
);

alter table skillplant_data
    owner to postgres;

create unique index skillplant_data_id_uindex
    on skillplant_data (id);

create table IF NOT EXISTS seniority_types
(
    type_id   serial
        constraint seniority_types_pk
            primary key,
    seniority varchar not null
);

alter table seniority_types
    owner to postgres;

create unique index seniority_types_seniority_uindex
    on seniority_types (seniority);