-- tabel article
update article set number_id = (select id from number where  article.parent = number.legacy_id);
update article set volume_id = (select id from volume where  article.parent = volume.legacy_id);

-- tabel volume
update volume set year_id = (select id from year where  volume.parent = year.legacy_id);

-- tabel year
update year set journal_id = (select id from journal where year.parent = journal.legacy_id);

-- tabel number
update number set volume_id = (select id from volume where  number.parent = volume.legacy_id);
update number set year_id = (select id from year where  number.parent = year.legacy_id);

-- table contributor
update article_contributor set par_id = (select id from article where article.legacy_id = article_contributor.parent);
update number_contributor set par_id = (select id from number where number.legacy_id = number_contributor.parent);
update volume_contributor set par_id = (select id from volume where volume.legacy_id = volume_contributor.parent);
update year_contributor set par_id = (select id from year where year.legacy_id = year_contributor.parent);
update journal_contributor set par_id = (select id from journal where journal.legacy_id = journal_contributor.parent);

-- table date
update article_date set par_id = (select id from article where article.legacy_id = article_date.parent);
-- update number_date set par_id = (select id from number where number.legacy_id = number_date.parent);
-- update volume_date set par_id = (select id from volume where volume.legacy_id = volume_date.parent);
update year_date set par_id = (select id from year where year.legacy_id = year_date.parent);
update journal_date set par_id = (select id from journal where journal.legacy_id = journal_date.parent);

-- table description
update article_description set par_id = (select id from article where article.legacy_id = article_description.parent);
-- update number_description set par_id = (select id from number where number.legacy_id = number_description.parent);
-- update volume_description set par_id = (select id from volume where volume.legacy_id = volume_description.parent);
-- update year_description set par_id = (select id from year where year.legacy_id = year_description.parent);
-- update journal_description set par_id = (select id from journal where journal.legacy_id = journal_description.parent);

-- table keywords
update article_keywords set par_id = (select id from article where article.legacy_id = article_keywords.parent);
-- update number_keywords set par_id = (select id from number where number.legacy_id = number_keywords.parent);
-- update volume_keywords set par_id = (select id from volume where volume.legacy_id = volume_keywords.parent);
-- update year_keywords set par_id = (select id from year where year.legacy_id = year_keywords.parent);
-- update journal_keywords set par_id = (select id from journal where journal.legacy_id = journal_keywords.parent);

-- table name
update article_name set par_id = (select id from article where article.legacy_id = article_name.parent);
update number_name set par_id = (select id from number where number.legacy_id = number_name.parent);
update volume_name set par_id = (select id from volume where volume.legacy_id = volume_name.parent);
update year_name set par_id = (select id from year where year.legacy_id = year_name.parent);
update journal_name set par_id = (select id from journal where journal.legacy_id = journal_name.parent);


-- table references
update article_references set par_id = (select id from article where article.legacy_id = article_references.parent);
-- update number_references set par_id = (select id from number where number.legacy_id = number_references.parent);
-- update volume_references set par_id = (select id from volume where volume.legacy_id = volume_references.parent);
-- update year_references set par_id = (select id from year where year.legacy_id = year_references.parent);
-- update journal_references set par_id = (select id from journal where journal.legacy_id = journal_references.parent);

-- table article_pages
update article_pages set par_id = (select id from article where article.legacy_id = article_pages.parent);
update article_review set par_id = (select id from article where article.legacy_id = article_review.parent);
