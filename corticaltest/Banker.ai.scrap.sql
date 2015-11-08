use test;
#drop table vctest;
#drop table startups;

select count(*) from vctest4 where length(text) > 0 and cortical_io is not null;
select count(*) from vctest4 where length(text) > 0 and cortical_io is null;
select count(*) from crunchbase_startups where text <>'' and cortical_io is not null;
select count(*) from crunchbase_startups where text <>'' and cortical_io is null;

select * from crunchbase_startups where text <>'' and cortical_io is not null;

create table vctest2 (text text, siteurl varchar(1000), pageurl varchar(1000), pagetitle varchar(1000) );

create table vctest (text text, siteurl varchar(255) PRIMARY KEY, pageurl varchar(1000), pagetitle varchar(1000), cortical_io text,watson text,opencalais text,cortical_io_keywords text,a1 text, a2 text, a3 text);

create table startups ( pagetitle varchar(1000), text text, pageurl varchar(1000), siteurl varchar(255) PRIMARY KEY, cortical_io text,watson text,opencalais text,cortical_io_keywords text,a1 text, a2 text, a3 text);


alter table vctest modify siteurl varchar(255);
SET GLOBAL max_connections = 500;

#alter table vctest add column cortical_io_keywords text;

#set innodb_lock_wait_timeout=100;
set global max_allowed_packet=67108864;
show open tables where in_use>0;
show full processlist;
kill 9184;
kill 9186;
kill 9188;
kill 3;


grant all on database.* to user@'%';
flush privileges;

#ALTER TABLE vctest4 ADD text text;
#ALTER TABLE vctest4 ADD cortical_io text;
#ALTER TABLE vctest4 ADD watson text;
#ALTER TABLE vctest4 ADD opencalais text;
#ALTER TABLE vctest4 ADD cortical_io_keywords text;
ALTER TABLE vctest4 ADD lang varchar(127);
ALTER TABLE crunchbase_startups ADD lang varchar(127);
#ALTER TABLE crunchbase_startups ADD text text;
#ALTER TABLE crunchbase_startups ADD cortical_io text;
#ALTER TABLE crunchbase_startups ADD watson text;
#ALTER TABLE crunchbase_startups ADD opencalais text;
#ALTER TABLE crunchbase_startups ADD cortical_io_keywords text;

#download complete
select * from vctest4 where length(text) = 0;

select count(*) from vctest4 where length(text) > 0 and cortical_io is not null;
select count(*) from vctest4 where length(text) > 0 and cortical_io is null;
select count(*) from crunchbase_startups where text <>'' and cortical_io is not null;
select count(*) from crunchbase_startups where text <>'' and cortical_io is null;


select * from crunchbase_startups where text <>'' and siteurl='8minutenergy.com';

#analysis complete
select * from vctest4 where length(text) > 0 and watson is not null;
select * from crunchbase_startups where length(text) > 0 and watson is not null and funding_total_usd > 10000000 and country_code='USA';

update vctest4 set text = null where text = '';
select * from vctest4 where siteurl like '%http:%';
select count(*) from vctest4 where siteurl not like '%.com%' and instr(siteurl, '/') <> 0;

delete from vctest4 where siteurl not like '%.com%' and instr(siteurl, '/') <> 0;

select * from vctest4 where siteurl not like '%.com%';

alter table vctest4 change column siteurl siteurl longtext;

-- run this on vc list
update crunchbase_startups set siteurl = replace(siteurl, 'http://', '');
update crunchbase_startups set siteurl = left(siteurl, instr(siteurl, '/') - 1) where instr(siteurl, '/') != 0;
update crunchbase_startups set text = '' where text is null;
-- end

select count(*) from crunchbase_startups where length(text) > 0;

select *, left(siteurl, instr(siteurl, '/') - 1), instr(siteurl, '/') from crunchbase_startups where instr(siteurl, '/') != 0;
#update vctest4 set text = '';
#update vctest4 set siteurl = '3g-capital.com' where siteurl like '%3g-cap%';
#update vctest4 set siteurl = left(siteurl, instr(siteurl, '.com')+3);

-- select *, left(siteurl, instr(siteurl, '.com')+3) from vctest4;
#create table vctest4_bk_siteurl (siteurl varchar(255)) as select siteurl from vctest4;

#ALTER TABLE `vctest4` CHANGE COLUMN `Web` `siteurl` VARCHAR(255) NOT NULL;
#ALTER TABLE `crunchbase_startups` CHANGE COLUMN `homepage_url` `siteurl` VARCHAR(255) NOT NULL;
SELECT homepage_url FROM crunchbase_startups where homepage_url <>'' and cortical_io is null ORDER BY RAND() LIMIT 10;