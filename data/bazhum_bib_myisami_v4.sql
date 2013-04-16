-- phpMyAdmin SQL Dump
-- version 3.5.5
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Czas wygenerowania: 04 Kwi 2013, 16:53
-- Wersja serwera: 5.1.66
-- Wersja PHP: 5.3.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Baza danych: `bazhum_bib`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `article`
--

DROP TABLE IF EXISTS `article`;
CREATE TABLE IF NOT EXISTS `article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number_id` int(11) DEFAULT NULL,
  `volume_id` int(11) DEFAULT NULL,
  `legacy_id` varchar(255) DEFAULT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `notes` text,
  `bibliographical_description` varchar(255) DEFAULT NULL,
  `mht_typ_form` varchar(255) DEFAULT NULL,
  `mht_typ_rodz` varchar(255) DEFAULT NULL,
  `title_nonexplicit` text,
  `mph_reference` varchar(255) DEFAULT NULL,
  `baztech_author_email` varchar(512) DEFAULT NULL,
  `keywords` text,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `legacy_id` (`legacy_id`),
  KEY `number_id` (`number_id`),
  KEY `volume_id` (`volume_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `article_contributor`
--

DROP TABLE IF EXISTS `article_contributor`;
CREATE TABLE IF NOT EXISTS `article_contributor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `role` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `surname` varchar(512) DEFAULT NULL,
  `firstname` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `article_review`
--

DROP TABLE IF EXISTS `article_review`;
CREATE TABLE IF NOT EXISTS `article_review` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `place` varchar(512) DEFAULT NULL,
  `year` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `article_date`
--

DROP TABLE IF EXISTS `article_date`;
CREATE TABLE IF NOT EXISTS `article_date` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `text` text,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `article_description`
--

DROP TABLE IF EXISTS `article_description`;
CREATE TABLE IF NOT EXISTS `article_description` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) NOT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `lang` varchar(255) NOT NULL,
  `text` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `article_keywords`
--

DROP TABLE IF EXISTS `article_keywords`;
CREATE TABLE IF NOT EXISTS `article_keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) NOT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `lang` varchar(20) NOT NULL,
  `kw` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `article_name`
--

DROP TABLE IF EXISTS `article_name`;
CREATE TABLE IF NOT EXISTS `article_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `name` varchar(1500) DEFAULT NULL,
  `nameClean` varchar(1500) DEFAULT NULL,
  `lang` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`),
  KEY `name` (`name`(333))
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla  `article_pages`
--

DROP TABLE IF EXISTS `article_pages`;
CREATE TABLE IF NOT EXISTS `article_pages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `page_from` varchar(255) DEFAULT NULL,
  `page_to` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `article_references`
--

DROP TABLE IF EXISTS `article_references`;
CREATE TABLE IF NOT EXISTS `article_references` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `index` varchar(20) DEFAULT NULL,
  `text` text,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `journal`
--

DROP TABLE IF EXISTS `journal`;
CREATE TABLE IF NOT EXISTS `journal` (
  `jid` int(11) NOT NULL AUTO_INCREMENT,
  `legacy_id` varchar(255) DEFAULT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `notes` text,
  `id` varchar(255) DEFAULT NULL,
  `continuate` varchar(255) DEFAULT NULL,
  `continuatedBy` varchar(255) DEFAULT NULL,
  `frequency` varchar(255) DEFAULT NULL,
  `www` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`jid`),
  KEY `legacy_id` (`legacy_id`),
  KEY `parent` (`parent`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `journal_contributor`
--

DROP TABLE IF EXISTS `journal_contributor`;
CREATE TABLE IF NOT EXISTS `journal_contributor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `role` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `surname` varchar(512) DEFAULT NULL,
  `firstname` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `journal_date`
--

DROP TABLE IF EXISTS `journal_date`;
CREATE TABLE IF NOT EXISTS `journal_date` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `text` text,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `journal_name`
--

DROP TABLE IF EXISTS `journal_name`;
CREATE TABLE IF NOT EXISTS `journal_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `name` text,
  `lang` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `number`
--

DROP TABLE IF EXISTS `number`;
CREATE TABLE IF NOT EXISTS `number` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `volume_id` int(11) DEFAULT NULL,
  `year_id` int(11) DEFAULT NULL,
  `legacy_id` varchar(255) DEFAULT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  KEY `legacy_id` (`legacy_id`),
  KEY `parent` (`parent`),
  KEY `volume_id` (`volume_id`),
  KEY `year_id` (`year_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `number_contributor`
--

DROP TABLE IF EXISTS `number_contributor`;
CREATE TABLE IF NOT EXISTS `number_contributor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `role` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `surname` varchar(512) DEFAULT NULL,
  `firstname` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `number_name`
--

DROP TABLE IF EXISTS `number_name`;
CREATE TABLE IF NOT EXISTS `number_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `name` text,
  `lang` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `volume`
--

DROP TABLE IF EXISTS `volume`;
CREATE TABLE IF NOT EXISTS `volume` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year_id` int(11) DEFAULT NULL,
  `legacy_id` varchar(255) DEFAULT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `notes` text,
  `bibliographical_description` varchar(255) DEFAULT NULL,
  `mht_typ_form` varchar(255) DEFAULT NULL,
  `mht_typ_rodz` varchar(255) DEFAULT NULL,
  `title_nonexplicit` text,
  `mph_reference` varchar(255) DEFAULT NULL,
  `baztech_author_email` varchar(512) DEFAULT NULL,
  `title` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `legacy_id` (`legacy_id`),
  KEY `year_id` (`year_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `volume_contributor`
--

DROP TABLE IF EXISTS `volume_contributor`;
CREATE TABLE IF NOT EXISTS `volume_contributor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `role` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `surname` varchar(512) DEFAULT NULL,
  `firstname` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `volume_name`
--

DROP TABLE IF EXISTS `volume_name`;
CREATE TABLE IF NOT EXISTS `volume_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `name` text,
  `lang` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `year`
--

DROP TABLE IF EXISTS `year`;
CREATE TABLE IF NOT EXISTS `year` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `journal_id` int(11) DEFAULT NULL,
  `legacy_id` varchar(255) DEFAULT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  KEY `legacy_id` (`legacy_id`),
  KEY `parent` (`parent`),
  KEY `journal_id` (`journal_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `year_contributor`
--

DROP TABLE IF EXISTS `year_contributor`;
CREATE TABLE IF NOT EXISTS `year_contributor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `role` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `surname` varchar(512) DEFAULT NULL,
  `firstname` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `year_date`
--

DROP TABLE IF EXISTS `year_date`;
CREATE TABLE IF NOT EXISTS `year_date` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `text` text,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `year_name`
--

DROP TABLE IF EXISTS `year_name`;
CREATE TABLE IF NOT EXISTS `year_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `par_id` int(11) DEFAULT NULL,
  `parent` varchar(255) NOT NULL,
  `name` text,
  `lang` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent` (`parent`),
  KEY `par_id` (`par_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
