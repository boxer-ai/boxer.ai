use test;
#drop table vctest;
#drop table startups;

create table vctest2 (text text, siteurl varchar(1000), pageurl varchar(1000), pagetitle varchar(1000) );

create table vctest (text text, siteurl varchar(255) PRIMARY KEY, pageurl varchar(1000), pagetitle varchar(1000), cortical_io text,watson text,opencalais text,cortical_io_keywords text,a1 text, a2 text, a3 text);

create table startups ( pagetitle varchar(1000), text text, pageurl varchar(1000), siteurl varchar(255) PRIMARY KEY, cortical_io text,watson text,opencalais text,cortical_io_keywords text,a1 text, a2 text, a3 text);


alter table vctest modify siteurl varchar(255);
SET GLOBAL max_connections = 500;

#alter table vctest add column cortical_io_keywords text;

#set innodb_lock_wait_timeout=100;
show open tables where in_use>0;
show full processlist;
kill 66895;

#ALTER TABLE vctest4 ADD text text;
#ALTER TABLE vctest4 ADD cortical_io text;
#ALTER TABLE vctest4 ADD watson text;
#ALTER TABLE vctest4 ADD opencalais text;
#ALTER TABLE vctest4 ADD cortical_io_keywords text;

#ALTER TABLE crunchbase_startups ADD text text;
#ALTER TABLE crunchbase_startups ADD cortical_io text;
#ALTER TABLE crunchbase_startups ADD watson text;
#ALTER TABLE crunchbase_startups ADD opencalais text;
#ALTER TABLE crunchbase_startups ADD cortical_io_keywords text;

select *, ROW_NUMBER()  from vctest;

select * from vctest4 where length(text) > 0;
ALTER IGNORE TABLE vctest4 ADD UNIQUE (siteurl)

#select count(*) from vctest4;
#delete from vctest4 where length(siteurl) = 0;

#update vctest4 set text = '';
#update vctest4 set siteurl = '3g-capital.com' where siteurl like '%3g-cap%';
#update vctest4 set siteurl = left(siteurl, instr(siteurl, '.com')+3);

-- select *, left(siteurl, instr(siteurl, '.com')+3) from vctest4;
create table vctest4_bk_siteurl (siteurl varchar(255)) as select siteurl from vctest4;

SELECT Web FROM vctest4 where Web <>'' and cortical_io is null ORDER BY RAND() LIMIT 10;

ALTER TABLE `vctest4` CHANGE COLUMN `Web` `siteurl` VARCHAR(255) NOT NULL;
ALTER TABLE `crunchbase_startups` CHANGE COLUMN `homepage_url` `siteurl` VARCHAR(255) NOT NULL;

select * from crunchbase_startups;
SELECT homepage_url FROM crunchbase_startups where homepage_url <>'' and cortical_io is null ORDER BY RAND() LIMIT 10;


select * from vctest WHERE siteurl = 'ahl.com';
#select siteurl, text from vctest where cortical_io is null limit 1;

UPDATE vctest SET cortical_io_keywords = '' WHERE siteurl = 'divcowest.com';
