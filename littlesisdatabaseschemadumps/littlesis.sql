-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: littlesis
-- ------------------------------------------------------
-- Server version	5.5.41-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity_id` bigint(20) NOT NULL,
  `street1` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `street2` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `street3` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `city` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `county` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `state_id` bigint(20) NOT NULL,
  `country_id` bigint(20) NOT NULL DEFAULT '1',
  `postal` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `latitude` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `longitude` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `category_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `state_id_idx` (`state_id`),
  KEY `country_id_idx` (`country_id`),
  KEY `category_id_idx` (`category_id`),
  KEY `entity_id_idx` (`entity_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `address_ibfk_10` FOREIGN KEY (`category_id`) REFERENCES `address_category` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `address_ibfk_1` FOREIGN KEY (`state_id`) REFERENCES `address_state` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `address_ibfk_2` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `address_ibfk_3` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `address_ibfk_4` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `address_ibfk_5` FOREIGN KEY (`category_id`) REFERENCES `address_category` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `address_ibfk_6` FOREIGN KEY (`state_id`) REFERENCES `address_state` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `address_ibfk_7` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `address_ibfk_8` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `address_ibfk_9` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address_category`
--

DROP TABLE IF EXISTS `address_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address_category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_category`
--

LOCK TABLES `address_category` WRITE;
/*!40000 ALTER TABLE `address_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `address_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address_country`
--

DROP TABLE IF EXISTS `address_country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address_country` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_country`
--

LOCK TABLES `address_country` WRITE;
/*!40000 ALTER TABLE `address_country` DISABLE KEYS */;
/*!40000 ALTER TABLE `address_country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address_state`
--

DROP TABLE IF EXISTS `address_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address_state` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `abbreviation` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `country_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`name`),
  KEY `country_id_idx` (`country_id`),
  CONSTRAINT `address_state_ibfk_2` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `address_state_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `address_country` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_state`
--

LOCK TABLES `address_state` WRITE;
/*!40000 ALTER TABLE `address_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `address_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alias`
--

DROP TABLE IF EXISTS `alias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alias` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity_id` bigint(20) NOT NULL,
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `context` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_primary` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`entity_id`,`name`,`context`),
  KEY `entity_id_idx` (`entity_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `alias_ibfk_4` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `alias_ibfk_1` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `alias_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `alias_ibfk_3` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alias`
--

LOCK TABLES `alias` WRITE;
/*!40000 ALTER TABLE `alias` DISABLE KEYS */;
/*!40000 ALTER TABLE `alias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_request`
--

DROP TABLE IF EXISTS `api_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_request` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `api_key` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `resource` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `ip_address` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_key_idx` (`api_key`),
  CONSTRAINT `api_request_ibfk_2` FOREIGN KEY (`api_key`) REFERENCES `api_user` (`api_key`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `api_request_ibfk_1` FOREIGN KEY (`api_key`) REFERENCES `api_user` (`api_key`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_request`
--

LOCK TABLES `api_request` WRITE;
/*!40000 ALTER TABLE `api_request` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_user`
--

DROP TABLE IF EXISTS `api_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `api_key` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `name_first` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `name_last` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `reason` longtext COLLATE utf8_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '0',
  `request_limit` int(11) NOT NULL DEFAULT '10000',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_key_unique_idx` (`api_key`),
  UNIQUE KEY `email_unique_idx` (`email`),
  KEY `api_key_idx` (`api_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_user`
--

LOCK TABLES `api_user` WRITE;
/*!40000 ALTER TABLE `api_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business`
--

DROP TABLE IF EXISTS `business`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `annual_profit` bigint(20) DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `business_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `business_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business`
--

LOCK TABLES `business` WRITE;
/*!40000 ALTER TABLE `business` DISABLE KEYS */;
/*!40000 ALTER TABLE `business` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_industry`
--

DROP TABLE IF EXISTS `business_industry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_industry` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `business_id` bigint(20) NOT NULL,
  `industry_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `business_id_idx` (`business_id`),
  KEY `industry_id_idx` (`industry_id`),
  CONSTRAINT `business_industry_ibfk_4` FOREIGN KEY (`business_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `business_industry_ibfk_1` FOREIGN KEY (`industry_id`) REFERENCES `industry` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `business_industry_ibfk_2` FOREIGN KEY (`business_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `business_industry_ibfk_3` FOREIGN KEY (`industry_id`) REFERENCES `industry` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_industry`
--

LOCK TABLES `business_industry` WRITE;
/*!40000 ALTER TABLE `business_industry` DISABLE KEYS */;
/*!40000 ALTER TABLE `business_industry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_person`
--

DROP TABLE IF EXISTS `business_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_person` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sec_cik` bigint(20) DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `business_person_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `business_person_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_person`
--

LOCK TABLES `business_person` WRITE;
/*!40000 ALTER TABLE `business_person` DISABLE KEYS */;
/*!40000 ALTER TABLE `business_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidate_district`
--

DROP TABLE IF EXISTS `candidate_district`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate_district` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `candidate_id` bigint(20) NOT NULL,
  `district_id` bigint(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`candidate_id`,`district_id`),
  KEY `candidate_id_idx` (`candidate_id`),
  KEY `district_id_idx` (`district_id`),
  CONSTRAINT `candidate_district_ibfk_4` FOREIGN KEY (`candidate_id`) REFERENCES `political_candidate` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `candidate_district_ibfk_1` FOREIGN KEY (`district_id`) REFERENCES `political_district` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `candidate_district_ibfk_2` FOREIGN KEY (`candidate_id`) REFERENCES `political_candidate` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `candidate_district_ibfk_3` FOREIGN KEY (`district_id`) REFERENCES `political_district` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidate_district`
--

LOCK TABLES `candidate_district` WRITE;
/*!40000 ALTER TABLE `candidate_district` DISABLE KEYS */;
/*!40000 ALTER TABLE `candidate_district` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_user`
--

DROP TABLE IF EXISTS `chat_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `room` bigint(20) NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `chat_user_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chat_user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_user`
--

LOCK TABLES `chat_user` WRITE;
/*!40000 ALTER TABLE `chat_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custom_key`
--

DROP TABLE IF EXISTS `custom_key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custom_key` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `value` longtext COLLATE utf8_unicode_ci,
  `description` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `object_model` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `object_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `object_idx` (`object_model`,`object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_key`
--

LOCK TABLES `custom_key` WRITE;
/*!40000 ALTER TABLE `custom_key` DISABLE KEYS */;
/*!40000 ALTER TABLE `custom_key` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `degree`
--

DROP TABLE IF EXISTS `degree`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `degree` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `abbreviation` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `degree`
--

LOCK TABLES `degree` WRITE;
/*!40000 ALTER TABLE `degree` DISABLE KEYS */;
/*!40000 ALTER TABLE `degree` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domain`
--

DROP TABLE IF EXISTS `domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `url` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domain`
--

LOCK TABLES `domain` WRITE;
/*!40000 ALTER TABLE `domain` DISABLE KEYS */;
INSERT INTO `domain` VALUES (1,'Twitter','http://twitter.com'),(2,'NyTimes','http://nytimes.com'),(3,'SourceWatch','http://sourcewatch.org'),(4,'MapLight','http://maplight.org');
/*!40000 ALTER TABLE `domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donation`
--

DROP TABLE IF EXISTS `donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `bundler_id` bigint(20) DEFAULT NULL,
  `relationship_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bundler_id_idx` (`bundler_id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `donation_ibfk_4` FOREIGN KEY (`bundler_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `donation_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `donation_ibfk_2` FOREIGN KEY (`bundler_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `donation_ibfk_3` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donation`
--

LOCK TABLES `donation` WRITE;
/*!40000 ALTER TABLE `donation` DISABLE KEYS */;
/*!40000 ALTER TABLE `donation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `education`
--

DROP TABLE IF EXISTS `education`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `education` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `degree_id` bigint(20) DEFAULT NULL,
  `field` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_dropout` tinyint(1) DEFAULT NULL,
  `relationship_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `degree_id_idx` (`degree_id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `education_ibfk_4` FOREIGN KEY (`degree_id`) REFERENCES `degree` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `education_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `education_ibfk_2` FOREIGN KEY (`degree_id`) REFERENCES `degree` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `education_ibfk_3` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `education`
--

LOCK TABLES `education` WRITE;
/*!40000 ALTER TABLE `education` DISABLE KEYS */;
/*!40000 ALTER TABLE `education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elected_representative`
--

DROP TABLE IF EXISTS `elected_representative`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elected_representative` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `bioguide_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `govtrack_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `crp_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pvs_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `watchdog_id` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `elected_representative_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `elected_representative_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elected_representative`
--

LOCK TABLES `elected_representative` WRITE;
/*!40000 ALTER TABLE `elected_representative` DISABLE KEYS */;
/*!40000 ALTER TABLE `elected_representative` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `email`
--

DROP TABLE IF EXISTS `email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `email` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity_id` bigint(20) NOT NULL,
  `address` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `email_ibfk_4` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `email_ibfk_1` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `email_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `email_ibfk_3` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `email`
--

LOCK TABLES `email` WRITE;
/*!40000 ALTER TABLE `email` DISABLE KEYS */;
/*!40000 ALTER TABLE `email` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entity`
--

DROP TABLE IF EXISTS `entity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entity` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `blurb` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `summary` longtext COLLATE utf8_unicode_ci,
  `notes` longtext COLLATE utf8_unicode_ci,
  `website` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `parent_id` bigint(20) DEFAULT NULL,
  `primary_ext` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `merged_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `start_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `end_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_current` tinyint(1) DEFAULT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `parent_id_idx` (`parent_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `entity_ibfk_4` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `entity_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `entity_ibfk_2` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `entity_ibfk_3` FOREIGN KEY (`parent_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entity`
--

LOCK TABLES `entity` WRITE;
/*!40000 ALTER TABLE `entity` DISABLE KEYS */;
/*!40000 ALTER TABLE `entity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `extension_definition`
--

DROP TABLE IF EXISTS `extension_definition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `extension_definition` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `display_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `has_fields` tinyint(1) NOT NULL DEFAULT '0',
  `parent_id` bigint(20) DEFAULT NULL,
  `tier` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent_id_idx` (`parent_id`),
  CONSTRAINT `extension_definition_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `extension_definition` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `extension_definition_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `extension_definition` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `extension_definition`
--

LOCK TABLES `extension_definition` WRITE;
/*!40000 ALTER TABLE `extension_definition` DISABLE KEYS */;
INSERT INTO `extension_definition` VALUES (1,'Person','Person',1,NULL,1),(2,'Org','Organization',1,NULL,1),(3,'PoliticalCandidate','Political Candidate',1,1,2),(4,'ElectedRepresentative','Elected Representative',1,1,2),(5,'Business','Business',1,2,2),(6,'GovernmentBody','Government Body',1,2,2),(7,'School','School',1,2,2),(8,'MembershipOrg','Membership Organization',0,2,2),(9,'Philanthropy','Philanthropy',0,2,2),(10,'NonProfit','Other Not-for-Profit',0,2,2),(11,'PoliticalFundraising','Political Fundraising Committee',1,2,2),(12,'PrivateCompany','Private Company',0,2,3),(13,'PublicCompany','Public Company',1,2,3),(14,'IndustryTrade','Industry/Trade Association',0,2,3),(15,'LawFirm','Law Firm',0,2,3),(16,'LobbyingFirm','Lobbying Firm',0,2,3),(17,'PublicRelationsFirm','Public Relations Firm',0,2,3),(18,'IndividualCampaignCommittee','Individual Campaign Committee',0,2,3),(19,'Pac','PAC',0,2,3),(20,'OtherCampaignCommittee','Other Campaign Committee',0,2,3),(21,'MediaOrg','Media Organization',0,2,3),(22,'ThinkTank','Policy/Think Tank',0,2,3),(23,'Cultural','Cultural/Arts',0,2,3),(24,'SocialClub','Social Club',0,2,3),(25,'ProfessionalAssociation','Professional Association',0,2,3),(26,'PoliticalParty','Political Party',0,2,3),(27,'LaborUnion','Labor Union',0,2,3),(28,'Gse','Government-Sponsored Enterprise',0,2,3),(29,'BusinessPerson','Business Person',1,1,2),(30,'Lobbyist','Lobbyist',1,1,2),(31,'Academic','Academic',0,1,2),(32,'MediaPersonality','Media Personality',0,1,3),(33,'ConsultingFirm','Consulting Firm',0,2,3),(34,'PublicIntellectual','Public Intellectual',0,1,3),(35,'PublicOfficial','Public Official',0,1,2),(36,'Lawyer','Lawyer',0,1,2);
/*!40000 ALTER TABLE `extension_definition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `extension_record`
--

DROP TABLE IF EXISTS `extension_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `extension_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity_id` bigint(20) NOT NULL,
  `definition_id` bigint(20) NOT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  KEY `definition_id_idx` (`definition_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `extension_record_ibfk_6` FOREIGN KEY (`definition_id`) REFERENCES `extension_definition` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `extension_record_ibfk_1` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `extension_record_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `extension_record_ibfk_3` FOREIGN KEY (`definition_id`) REFERENCES `extension_definition` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `extension_record_ibfk_4` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `extension_record_ibfk_5` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `extension_record`
--

LOCK TABLES `extension_record` WRITE;
/*!40000 ALTER TABLE `extension_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `extension_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `external_key`
--

DROP TABLE IF EXISTS `external_key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `external_key` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity_id` bigint(20) NOT NULL,
  `external_id` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `domain_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`external_id`,`domain_id`),
  KEY `entity_id_idx` (`entity_id`),
  KEY `domain_id_idx` (`domain_id`),
  CONSTRAINT `external_key_ibfk_4` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`),
  CONSTRAINT `external_key_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `external_key_ibfk_2` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`),
  CONSTRAINT `external_key_ibfk_3` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `external_key`
--

LOCK TABLES `external_key` WRITE;
/*!40000 ALTER TABLE `external_key` DISABLE KEYS */;
/*!40000 ALTER TABLE `external_key` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `family`
--

DROP TABLE IF EXISTS `family`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `family` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `is_nonbiological` tinyint(1) DEFAULT NULL,
  `relationship_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `family_ibfk_2` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `family_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `family`
--

LOCK TABLES `family` WRITE;
/*!40000 ALTER TABLE `family` DISABLE KEYS */;
/*!40000 ALTER TABLE `family` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fec_filing`
--

DROP TABLE IF EXISTS `fec_filing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fec_filing` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `relationship_id` bigint(20) DEFAULT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `fec_filing_id` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `crp_cycle` bigint(20) DEFAULT NULL,
  `crp_id` varchar(7) COLLATE utf8_unicode_ci DEFAULT NULL,
  `start_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `end_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_current` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `fec_filing_ibfk_2` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fec_filing_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fec_filing`
--

LOCK TABLES `fec_filing` WRITE;
/*!40000 ALTER TABLE `fec_filing` DISABLE KEYS */;
/*!40000 ALTER TABLE `fec_filing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fedspending_filing`
--

DROP TABLE IF EXISTS `fedspending_filing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fedspending_filing` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `relationship_id` bigint(20) DEFAULT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `goods` longtext COLLATE utf8_unicode_ci,
  `district_id` bigint(20) DEFAULT NULL,
  `fedspending_id` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `start_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `end_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_current` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_id_idx` (`relationship_id`),
  KEY `district_id_idx` (`district_id`),
  CONSTRAINT `fedspending_filing_ibfk_4` FOREIGN KEY (`district_id`) REFERENCES `political_district` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fedspending_filing_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fedspending_filing_ibfk_2` FOREIGN KEY (`district_id`) REFERENCES `political_district` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fedspending_filing_ibfk_3` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fedspending_filing`
--

LOCK TABLES `fedspending_filing` WRITE;
/*!40000 ALTER TABLE `fedspending_filing` DISABLE KEYS */;
/*!40000 ALTER TABLE `fedspending_filing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gender`
--

DROP TABLE IF EXISTS `gender`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gender` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gender`
--

LOCK TABLES `gender` WRITE;
/*!40000 ALTER TABLE `gender` DISABLE KEYS */;
/*!40000 ALTER TABLE `gender` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `government_body`
--

DROP TABLE IF EXISTS `government_body`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `government_body` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `is_federal` tinyint(1) DEFAULT NULL,
  `state_id` bigint(20) DEFAULT NULL,
  `city` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `county` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `state_id_idx` (`state_id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `government_body_ibfk_4` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `government_body_ibfk_1` FOREIGN KEY (`state_id`) REFERENCES `address_state` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `government_body_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `government_body_ibfk_3` FOREIGN KEY (`state_id`) REFERENCES `address_state` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `government_body`
--

LOCK TABLES `government_body` WRITE;
/*!40000 ALTER TABLE `government_body` DISABLE KEYS */;
/*!40000 ALTER TABLE `government_body` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity_id` bigint(20) NOT NULL,
  `filename` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `title` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `caption` longtext COLLATE utf8_unicode_ci,
  `is_featured` tinyint(1) NOT NULL DEFAULT '0',
  `is_free` tinyint(1) DEFAULT NULL,
  `url` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `width` bigint(20) DEFAULT NULL,
  `height` bigint(20) DEFAULT NULL,
  `has_square` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `image_ibfk_4` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `image_ibfk_1` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `image_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `image_ibfk_3` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
/*!40000 ALTER TABLE `image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `industry`
--

DROP TABLE IF EXISTS `industry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `industry` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `context` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `code` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `industry`
--

LOCK TABLES `industry` WRITE;
/*!40000 ALTER TABLE `industry` DISABLE KEYS */;
/*!40000 ALTER TABLE `industry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `link`
--

DROP TABLE IF EXISTS `link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `link` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity1_id` bigint(20) NOT NULL,
  `entity2_id` bigint(20) NOT NULL,
  `category_id` bigint(20) NOT NULL,
  `relationship_id` bigint(20) NOT NULL,
  `is_reverse` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `entity1_id_idx` (`entity1_id`),
  KEY `entity2_id_idx` (`entity2_id`),
  KEY `category_id_idx` (`category_id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `link_ibfk_8` FOREIGN KEY (`category_id`) REFERENCES `relationship_category` (`id`),
  CONSTRAINT `link_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`),
  CONSTRAINT `link_ibfk_2` FOREIGN KEY (`entity2_id`) REFERENCES `entity` (`id`),
  CONSTRAINT `link_ibfk_3` FOREIGN KEY (`entity1_id`) REFERENCES `entity` (`id`),
  CONSTRAINT `link_ibfk_4` FOREIGN KEY (`category_id`) REFERENCES `relationship_category` (`id`),
  CONSTRAINT `link_ibfk_5` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`),
  CONSTRAINT `link_ibfk_6` FOREIGN KEY (`entity2_id`) REFERENCES `entity` (`id`),
  CONSTRAINT `link_ibfk_7` FOREIGN KEY (`entity1_id`) REFERENCES `entity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `link`
--

LOCK TABLES `link` WRITE;
/*!40000 ALTER TABLE `link` DISABLE KEYS */;
/*!40000 ALTER TABLE `link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lobby_filing`
--

DROP TABLE IF EXISTS `lobby_filing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lobby_filing` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `federal_filing_id` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `year` bigint(20) DEFAULT NULL,
  `period` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `report_type` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `start_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `end_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_current` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lobby_filing`
--

LOCK TABLES `lobby_filing` WRITE;
/*!40000 ALTER TABLE `lobby_filing` DISABLE KEYS */;
/*!40000 ALTER TABLE `lobby_filing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lobby_filing_lobby_issue`
--

DROP TABLE IF EXISTS `lobby_filing_lobby_issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lobby_filing_lobby_issue` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `issue_id` bigint(20) NOT NULL,
  `lobby_filing_id` bigint(20) NOT NULL,
  `specific_issue` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `issue_id_idx` (`issue_id`),
  KEY `lobby_filing_id_idx` (`lobby_filing_id`),
  CONSTRAINT `lobby_filing_lobby_issue_ibfk_4` FOREIGN KEY (`issue_id`) REFERENCES `lobby_issue` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lobby_filing_lobby_issue_ibfk_1` FOREIGN KEY (`lobby_filing_id`) REFERENCES `lobby_filing` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lobby_filing_lobby_issue_ibfk_2` FOREIGN KEY (`issue_id`) REFERENCES `lobby_issue` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lobby_filing_lobby_issue_ibfk_3` FOREIGN KEY (`lobby_filing_id`) REFERENCES `lobby_filing` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lobby_filing_lobby_issue`
--

LOCK TABLES `lobby_filing_lobby_issue` WRITE;
/*!40000 ALTER TABLE `lobby_filing_lobby_issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `lobby_filing_lobby_issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lobby_filing_lobbyist`
--

DROP TABLE IF EXISTS `lobby_filing_lobbyist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lobby_filing_lobbyist` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `lobbyist_id` bigint(20) NOT NULL,
  `lobby_filing_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lobbyist_id_idx` (`lobbyist_id`),
  KEY `lobby_filing_id_idx` (`lobby_filing_id`),
  CONSTRAINT `lobby_filing_lobbyist_ibfk_4` FOREIGN KEY (`lobby_filing_id`) REFERENCES `lobby_filing` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lobby_filing_lobbyist_ibfk_1` FOREIGN KEY (`lobbyist_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lobby_filing_lobbyist_ibfk_2` FOREIGN KEY (`lobby_filing_id`) REFERENCES `lobby_filing` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lobby_filing_lobbyist_ibfk_3` FOREIGN KEY (`lobbyist_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lobby_filing_lobbyist`
--

LOCK TABLES `lobby_filing_lobbyist` WRITE;
/*!40000 ALTER TABLE `lobby_filing_lobbyist` DISABLE KEYS */;
/*!40000 ALTER TABLE `lobby_filing_lobbyist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lobby_filing_relationship`
--

DROP TABLE IF EXISTS `lobby_filing_relationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lobby_filing_relationship` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `relationship_id` bigint(20) NOT NULL,
  `lobby_filing_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_id_idx` (`relationship_id`),
  KEY `lobby_filing_id_idx` (`lobby_filing_id`),
  CONSTRAINT `lobby_filing_relationship_ibfk_4` FOREIGN KEY (`lobby_filing_id`) REFERENCES `lobby_filing` (`id`),
  CONSTRAINT `lobby_filing_relationship_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`),
  CONSTRAINT `lobby_filing_relationship_ibfk_2` FOREIGN KEY (`lobby_filing_id`) REFERENCES `lobby_filing` (`id`),
  CONSTRAINT `lobby_filing_relationship_ibfk_3` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lobby_filing_relationship`
--

LOCK TABLES `lobby_filing_relationship` WRITE;
/*!40000 ALTER TABLE `lobby_filing_relationship` DISABLE KEYS */;
/*!40000 ALTER TABLE `lobby_filing_relationship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lobby_issue`
--

DROP TABLE IF EXISTS `lobby_issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lobby_issue` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lobby_issue`
--

LOCK TABLES `lobby_issue` WRITE;
/*!40000 ALTER TABLE `lobby_issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `lobby_issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lobbying`
--

DROP TABLE IF EXISTS `lobbying`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lobbying` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `relationship_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `lobbying_ibfk_2` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lobbying_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lobbying`
--

LOCK TABLES `lobbying` WRITE;
/*!40000 ALTER TABLE `lobbying` DISABLE KEYS */;
/*!40000 ALTER TABLE `lobbying` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lobbyist`
--

DROP TABLE IF EXISTS `lobbyist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lobbyist` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `lda_registrant_id` bigint(20) DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `lobbyist_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `lobbyist_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lobbyist`
--

LOCK TABLES `lobbyist` WRITE;
/*!40000 ALTER TABLE `lobbyist` DISABLE KEYS */;
/*!40000 ALTER TABLE `lobbyist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ls_list`
--

DROP TABLE IF EXISTS `ls_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ls_list` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci,
  `is_ranked` tinyint(1) NOT NULL DEFAULT '0',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  `is_featured` tinyint(1) NOT NULL DEFAULT '0',
  `is_network` tinyint(1) NOT NULL DEFAULT '0',
  `display_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `featured_list_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`name`),
  KEY `featured_list_id_idx` (`featured_list_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `ls_list_ibfk_4` FOREIGN KEY (`featured_list_id`) REFERENCES `ls_list` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `ls_list_ibfk_1` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `ls_list_ibfk_2` FOREIGN KEY (`featured_list_id`) REFERENCES `ls_list` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `ls_list_ibfk_3` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ls_list`
--

LOCK TABLES `ls_list` WRITE;
/*!40000 ALTER TABLE `ls_list` DISABLE KEYS */;
INSERT INTO `ls_list` VALUES (79,'United States','People and organizations with significant influence on the policies of the United States.',0,0,0,1,'us',NULL,'2010-01-25 22:11:12','2011-06-21 16:05:13',1,1);
/*!40000 ALTER TABLE `ls_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ls_list_entity`
--

DROP TABLE IF EXISTS `ls_list_entity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ls_list_entity` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `list_id` bigint(20) NOT NULL,
  `entity_id` bigint(20) NOT NULL,
  `rank` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_uniqueness_idx` (`list_id`,`entity_id`),
  KEY `list_id_idx` (`list_id`),
  KEY `entity_id_idx` (`entity_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `ls_list_entity_ibfk_6` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ls_list_entity_ibfk_1` FOREIGN KEY (`list_id`) REFERENCES `ls_list` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ls_list_entity_ibfk_2` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `ls_list_entity_ibfk_3` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ls_list_entity_ibfk_4` FOREIGN KEY (`list_id`) REFERENCES `ls_list` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ls_list_entity_ibfk_5` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ls_list_entity`
--

LOCK TABLES `ls_list_entity` WRITE;
/*!40000 ALTER TABLE `ls_list_entity` DISABLE KEYS */;
/*!40000 ALTER TABLE `ls_list_entity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membership`
--

DROP TABLE IF EXISTS `membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `membership` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `dues` bigint(20) DEFAULT NULL,
  `relationship_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `membership_ibfk_2` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `membership_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membership`
--

LOCK TABLES `membership` WRITE;
/*!40000 ALTER TABLE `membership` DISABLE KEYS */;
/*!40000 ALTER TABLE `membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modification`
--

DROP TABLE IF EXISTS `modification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modification` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `object_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_id` bigint(20) NOT NULL DEFAULT '1',
  `is_create` tinyint(1) NOT NULL DEFAULT '0',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0',
  `is_merge` tinyint(1) NOT NULL DEFAULT '0',
  `merge_object_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `object_model` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `object_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `object_idx` (`object_model`,`object_id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `modification_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `modification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modification`
--

LOCK TABLES `modification` WRITE;
/*!40000 ALTER TABLE `modification` DISABLE KEYS */;
INSERT INTO `modification` VALUES (1,'United States',1,1,0,0,NULL,'2015-03-01 21:33:46','2015-03-01 21:33:46','LsList',79);
/*!40000 ALTER TABLE `modification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modification_field`
--

DROP TABLE IF EXISTS `modification_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modification_field` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `modification_id` bigint(20) NOT NULL,
  `field_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `old_value` longtext COLLATE utf8_unicode_ci,
  `new_value` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `modification_id_idx` (`modification_id`),
  CONSTRAINT `modification_field_ibfk_2` FOREIGN KEY (`modification_id`) REFERENCES `modification` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `modification_field_ibfk_1` FOREIGN KEY (`modification_id`) REFERENCES `modification` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modification_field`
--

LOCK TABLES `modification_field` WRITE;
/*!40000 ALTER TABLE `modification_field` DISABLE KEYS */;
INSERT INTO `modification_field` VALUES (1,1,'name',NULL,'United States'),(2,1,'description',NULL,'People and organizations with significant influence on the policies of the United States.'),(3,1,'is_ranked',NULL,'0'),(4,1,'is_admin',NULL,'0'),(5,1,'is_featured',NULL,'0'),(6,1,'is_network',NULL,'1'),(7,1,'display_name',NULL,'us');
/*!40000 ALTER TABLE `modification_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `network_map`
--

DROP TABLE IF EXISTS `network_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `network_map` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `entity_ids` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rel_ids` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8_unicode_ci,
  `width` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `network_map_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `network_map_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `network_map`
--

LOCK TABLES `network_map` WRITE;
/*!40000 ALTER TABLE `network_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `network_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `note`
--

DROP TABLE IF EXISTS `note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `note` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `title` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `body` text COLLATE utf8_unicode_ci NOT NULL,
  `body_raw` text COLLATE utf8_unicode_ci NOT NULL,
  `alerted_user_names` text COLLATE utf8_unicode_ci,
  `alerted_user_ids` text COLLATE utf8_unicode_ci,
  `entity_ids` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `relationship_ids` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `lslist_ids` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sfguardgroup_ids` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `network_ids` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_private` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `note_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `note_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `note`
--

LOCK TABLES `note` WRITE;
/*!40000 ALTER TABLE `note` DISABLE KEYS */;
/*!40000 ALTER TABLE `note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object_tag`
--

DROP TABLE IF EXISTS `object_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `object_tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `tag_id` bigint(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `object_model` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `object_id` bigint(20) NOT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`object_model`,`object_id`,`tag_id`),
  KEY `object_idx` (`object_model`,`object_id`),
  KEY `tag_id_idx` (`tag_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `object_tag_ibfk_4` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `object_tag_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `object_tag_ibfk_2` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `object_tag_ibfk_3` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object_tag`
--

LOCK TABLES `object_tag` WRITE;
/*!40000 ALTER TABLE `object_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `object_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `org`
--

DROP TABLE IF EXISTS `org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `org` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `name_nick` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `employees` bigint(20) DEFAULT NULL,
  `revenue` bigint(20) DEFAULT NULL,
  `fedspending_id` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `lda_registrant_id` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `org_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `org_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `org`
--

LOCK TABLES `org` WRITE;
/*!40000 ALTER TABLE `org` DISABLE KEYS */;
/*!40000 ALTER TABLE `org` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_category`
--

DROP TABLE IF EXISTS `os_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `category_id` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `category_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `industry_id` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `industry_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `sector_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_id_idx` (`category_id`),
  UNIQUE KEY `unique_name_idx` (`category_name`),
  KEY `category_id_idx` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_category`
--

LOCK TABLES `os_category` WRITE;
/*!40000 ALTER TABLE `os_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_entity_category`
--

DROP TABLE IF EXISTS `os_entity_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_entity_category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity_id` bigint(20) NOT NULL,
  `category_id` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `source` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`entity_id`,`category_id`),
  KEY `entity_id_idx` (`entity_id`),
  KEY `category_id_idx` (`category_id`),
  CONSTRAINT `os_entity_category_ibfk_4` FOREIGN KEY (`category_id`) REFERENCES `os_category` (`category_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `os_entity_category_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `os_entity_category_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `os_category` (`category_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `os_entity_category_ibfk_3` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_entity_category`
--

LOCK TABLES `os_entity_category` WRITE;
/*!40000 ALTER TABLE `os_entity_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_entity_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_entity_donor`
--

DROP TABLE IF EXISTS `os_entity_donor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_entity_donor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity_id` bigint(20) NOT NULL,
  `donor_id` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `match_code` bigint(20) DEFAULT NULL,
  `is_verified` tinyint(1) NOT NULL DEFAULT '0',
  `is_processed` tinyint(1) NOT NULL DEFAULT '0',
  `is_synced` tinyint(1) NOT NULL DEFAULT '1',
  `reviewed_by_user_id` bigint(20) DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `locked_by_user_id` bigint(20) DEFAULT NULL,
  `locked_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_entity_donor`
--

LOCK TABLES `os_entity_donor` WRITE;
/*!40000 ALTER TABLE `os_entity_donor` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_entity_donor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_entity_preprocess`
--

DROP TABLE IF EXISTS `os_entity_preprocess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_entity_preprocess` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity_id` bigint(20) NOT NULL,
  `cycle` varchar(4) COLLATE utf8_unicode_ci NOT NULL,
  `processed_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_entity_preprocess`
--

LOCK TABLES `os_entity_preprocess` WRITE;
/*!40000 ALTER TABLE `os_entity_preprocess` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_entity_preprocess` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_entity_transaction`
--

DROP TABLE IF EXISTS `os_entity_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_entity_transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entity_id` int(11) NOT NULL,
  `cycle` varchar(4) COLLATE utf8_unicode_ci NOT NULL,
  `transaction_id` varchar(7) COLLATE utf8_unicode_ci NOT NULL,
  `match_code` bigint(20) DEFAULT NULL,
  `is_verified` tinyint(1) NOT NULL DEFAULT '0',
  `is_processed` tinyint(1) NOT NULL DEFAULT '0',
  `is_synced` tinyint(1) NOT NULL DEFAULT '1',
  `reviewed_by_user_id` bigint(20) DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `locked_by_user_id` bigint(20) DEFAULT NULL,
  `locked_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_entity_transaction`
--

LOCK TABLES `os_entity_transaction` WRITE;
/*!40000 ALTER TABLE `os_entity_transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_entity_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ownership`
--

DROP TABLE IF EXISTS `ownership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ownership` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `percent_stake` bigint(20) DEFAULT NULL,
  `shares` bigint(20) DEFAULT NULL,
  `relationship_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `ownership_ibfk_2` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ownership_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ownership`
--

LOCK TABLES `ownership` WRITE;
/*!40000 ALTER TABLE `ownership` DISABLE KEYS */;
/*!40000 ALTER TABLE `ownership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name_last` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `name_first` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `name_middle` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_prefix` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_suffix` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_nick` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `birthplace` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gender_id` bigint(20) DEFAULT NULL,
  `party_id` bigint(20) DEFAULT NULL,
  `is_independent` tinyint(1) DEFAULT NULL,
  `net_worth` bigint(20) DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gender_id_idx` (`gender_id`),
  KEY `party_id_idx` (`party_id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `person_ibfk_6` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `person_ibfk_1` FOREIGN KEY (`party_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `person_ibfk_2` FOREIGN KEY (`gender_id`) REFERENCES `gender` (`id`),
  CONSTRAINT `person_ibfk_3` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `person_ibfk_4` FOREIGN KEY (`party_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `person_ibfk_5` FOREIGN KEY (`gender_id`) REFERENCES `gender` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phone`
--

DROP TABLE IF EXISTS `phone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phone` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity_id` bigint(20) NOT NULL,
  `number` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `phone_ibfk_4` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `phone_ibfk_1` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `phone_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `phone_ibfk_3` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phone`
--

LOCK TABLES `phone` WRITE;
/*!40000 ALTER TABLE `phone` DISABLE KEYS */;
/*!40000 ALTER TABLE `phone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `political_candidate`
--

DROP TABLE IF EXISTS `political_candidate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_candidate` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `is_federal` tinyint(1) DEFAULT NULL,
  `is_state` tinyint(1) DEFAULT NULL,
  `is_local` tinyint(1) DEFAULT NULL,
  `pres_fec_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `senate_fec_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `house_fec_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `crp_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `political_candidate_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `political_candidate_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `political_candidate`
--

LOCK TABLES `political_candidate` WRITE;
/*!40000 ALTER TABLE `political_candidate` DISABLE KEYS */;
/*!40000 ALTER TABLE `political_candidate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `political_district`
--

DROP TABLE IF EXISTS `political_district`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_district` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `state_id` bigint(20) DEFAULT NULL,
  `federal_district` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `state_district` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `local_district` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `state_id_idx` (`state_id`),
  CONSTRAINT `political_district_ibfk_2` FOREIGN KEY (`state_id`) REFERENCES `address_state` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `political_district_ibfk_1` FOREIGN KEY (`state_id`) REFERENCES `address_state` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `political_district`
--

LOCK TABLES `political_district` WRITE;
/*!40000 ALTER TABLE `political_district` DISABLE KEYS */;
/*!40000 ALTER TABLE `political_district` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `political_fundraising`
--

DROP TABLE IF EXISTS `political_fundraising`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_fundraising` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fec_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type_id` bigint(20) DEFAULT NULL,
  `state_id` bigint(20) DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `state_id_idx` (`state_id`),
  KEY `type_id_idx` (`type_id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `political_fundraising_ibfk_6` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `political_fundraising_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `political_fundraising_type` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `political_fundraising_ibfk_2` FOREIGN KEY (`state_id`) REFERENCES `address_state` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `political_fundraising_ibfk_3` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `political_fundraising_ibfk_4` FOREIGN KEY (`type_id`) REFERENCES `political_fundraising_type` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `political_fundraising_ibfk_5` FOREIGN KEY (`state_id`) REFERENCES `address_state` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `political_fundraising`
--

LOCK TABLES `political_fundraising` WRITE;
/*!40000 ALTER TABLE `political_fundraising` DISABLE KEYS */;
/*!40000 ALTER TABLE `political_fundraising` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `political_fundraising_type`
--

DROP TABLE IF EXISTS `political_fundraising_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_fundraising_type` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `political_fundraising_type`
--

LOCK TABLES `political_fundraising_type` WRITE;
/*!40000 ALTER TABLE `political_fundraising_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `political_fundraising_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `position`
--

DROP TABLE IF EXISTS `position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `position` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `is_board` tinyint(1) DEFAULT NULL,
  `is_executive` tinyint(1) DEFAULT NULL,
  `is_employee` tinyint(1) DEFAULT NULL,
  `compensation` bigint(20) DEFAULT NULL,
  `boss_id` bigint(20) DEFAULT NULL,
  `relationship_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `boss_id_idx` (`boss_id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `position_ibfk_4` FOREIGN KEY (`boss_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `position_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `position_ibfk_2` FOREIGN KEY (`boss_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `position_ibfk_3` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `position`
--

LOCK TABLES `position` WRITE;
/*!40000 ALTER TABLE `position` DISABLE KEYS */;
/*!40000 ALTER TABLE `position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professional`
--

DROP TABLE IF EXISTS `professional`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `professional` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `relationship_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `professional_ibfk_2` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `professional_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professional`
--

LOCK TABLES `professional` WRITE;
/*!40000 ALTER TABLE `professional` DISABLE KEYS */;
/*!40000 ALTER TABLE `professional` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `public_company`
--

DROP TABLE IF EXISTS `public_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `public_company` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ticker` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sec_cik` bigint(20) DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `public_company_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `public_company_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `public_company`
--

LOCK TABLES `public_company` WRITE;
/*!40000 ALTER TABLE `public_company` DISABLE KEYS */;
/*!40000 ALTER TABLE `public_company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reference`
--

DROP TABLE IF EXISTS `reference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reference` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fields` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `source_detail` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `publication_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `object_model` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `object_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `object_idx` (`object_model`,`object_id`),
  KEY `object_id_idx` (`object_id`),
  CONSTRAINT `reference_ibfk_2` FOREIGN KEY (`object_id`) REFERENCES `relationship` (`id`),
  CONSTRAINT `reference_ibfk_1` FOREIGN KEY (`object_id`) REFERENCES `relationship` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reference`
--

LOCK TABLES `reference` WRITE;
/*!40000 ALTER TABLE `reference` DISABLE KEYS */;
/*!40000 ALTER TABLE `reference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reference_excerpt`
--

DROP TABLE IF EXISTS `reference_excerpt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reference_excerpt` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `reference_id` bigint(20) NOT NULL,
  `body` longtext COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reference_id_idx` (`reference_id`),
  CONSTRAINT `reference_excerpt_ibfk_2` FOREIGN KEY (`reference_id`) REFERENCES `reference` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reference_excerpt_ibfk_1` FOREIGN KEY (`reference_id`) REFERENCES `reference` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reference_excerpt`
--

LOCK TABLES `reference_excerpt` WRITE;
/*!40000 ALTER TABLE `reference_excerpt` DISABLE KEYS */;
/*!40000 ALTER TABLE `reference_excerpt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relationship`
--

DROP TABLE IF EXISTS `relationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relationship` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `entity1_id` bigint(20) NOT NULL,
  `entity2_id` bigint(20) NOT NULL,
  `category_id` bigint(20) NOT NULL,
  `description1` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description2` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `goods` longtext COLLATE utf8_unicode_ci,
  `filings` bigint(20) DEFAULT NULL,
  `notes` longtext COLLATE utf8_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `start_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `end_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_current` tinyint(1) DEFAULT NULL,
  `last_user_id` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `entity1_id_idx` (`entity1_id`),
  KEY `entity2_id_idx` (`entity2_id`),
  KEY `category_id_idx` (`category_id`),
  KEY `last_user_id_idx` (`last_user_id`),
  CONSTRAINT `relationship_ibfk_8` FOREIGN KEY (`category_id`) REFERENCES `relationship_category` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `relationship_ibfk_1` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `relationship_ibfk_2` FOREIGN KEY (`entity2_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relationship_ibfk_3` FOREIGN KEY (`entity1_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relationship_ibfk_4` FOREIGN KEY (`category_id`) REFERENCES `relationship_category` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `relationship_ibfk_5` FOREIGN KEY (`last_user_id`) REFERENCES `sf_guard_user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `relationship_ibfk_6` FOREIGN KEY (`entity2_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relationship_ibfk_7` FOREIGN KEY (`entity1_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationship`
--

LOCK TABLES `relationship` WRITE;
/*!40000 ALTER TABLE `relationship` DISABLE KEYS */;
/*!40000 ALTER TABLE `relationship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relationship_category`
--

DROP TABLE IF EXISTS `relationship_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relationship_category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `display_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `default_description` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `entity1_requirements` text COLLATE utf8_unicode_ci,
  `entity2_requirements` text COLLATE utf8_unicode_ci,
  `has_fields` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationship_category`
--

LOCK TABLES `relationship_category` WRITE;
/*!40000 ALTER TABLE `relationship_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `relationship_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `representative`
--

DROP TABLE IF EXISTS `representative`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `representative` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `bioguide_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `representative_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `representative_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `representative`
--

LOCK TABLES `representative` WRITE;
/*!40000 ALTER TABLE `representative` DISABLE KEYS */;
/*!40000 ALTER TABLE `representative` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `representative_district`
--

DROP TABLE IF EXISTS `representative_district`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `representative_district` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `representative_id` bigint(20) NOT NULL,
  `district_id` bigint(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`representative_id`,`district_id`),
  KEY `representative_id_idx` (`representative_id`),
  KEY `district_id_idx` (`district_id`),
  CONSTRAINT `representative_district_ibfk_4` FOREIGN KEY (`district_id`) REFERENCES `political_district` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `representative_district_ibfk_1` FOREIGN KEY (`representative_id`) REFERENCES `elected_representative` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `representative_district_ibfk_2` FOREIGN KEY (`district_id`) REFERENCES `political_district` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `representative_district_ibfk_3` FOREIGN KEY (`representative_id`) REFERENCES `elected_representative` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `representative_district`
--

LOCK TABLES `representative_district` WRITE;
/*!40000 ALTER TABLE `representative_district` DISABLE KEYS */;
/*!40000 ALTER TABLE `representative_district` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduled_email`
--

DROP TABLE IF EXISTS `scheduled_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduled_email` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `from_email` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `from_name` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `to_email` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `to_name` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `subject` text COLLATE utf8_unicode_ci,
  `body_text` longtext COLLATE utf8_unicode_ci,
  `body_html` longtext COLLATE utf8_unicode_ci,
  `is_sent` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduled_email`
--

LOCK TABLES `scheduled_email` WRITE;
/*!40000 ALTER TABLE `scheduled_email` DISABLE KEYS */;
/*!40000 ALTER TABLE `scheduled_email` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school`
--

DROP TABLE IF EXISTS `school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `endowment` bigint(20) DEFAULT NULL,
  `students` bigint(20) DEFAULT NULL,
  `faculty` bigint(20) DEFAULT NULL,
  `tuition` bigint(20) DEFAULT NULL,
  `is_private` tinyint(1) DEFAULT NULL,
  `entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `entity_id_idx` (`entity_id`),
  CONSTRAINT `school_ibfk_2` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `school_ibfk_1` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school`
--

LOCK TABLES `school` WRITE;
/*!40000 ALTER TABLE `school` DISABLE KEYS */;
/*!40000 ALTER TABLE `school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scraper_meta`
--

DROP TABLE IF EXISTS `scraper_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scraper_meta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `scraper` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `namespace` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `predicate` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `value` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`scraper`,`namespace`,`predicate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scraper_meta`
--

LOCK TABLES `scraper_meta` WRITE;
/*!40000 ALTER TABLE `scraper_meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `scraper_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sf_guard_group`
--

DROP TABLE IF EXISTS `sf_guard_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sf_guard_group` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `blurb` varchar(255) DEFAULT NULL,
  `description` text,
  `contest` text,
  `is_working` tinyint(1) NOT NULL DEFAULT '0',
  `is_private` tinyint(1) NOT NULL DEFAULT '0',
  `display_name` varchar(255) NOT NULL,
  `home_network_id` bigint(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sf_guard_group`
--

LOCK TABLES `sf_guard_group` WRITE;
/*!40000 ALTER TABLE `sf_guard_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sf_guard_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sf_guard_group_list`
--

DROP TABLE IF EXISTS `sf_guard_group_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sf_guard_group_list` (
  `group_id` bigint(20) NOT NULL DEFAULT '0',
  `list_id` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`group_id`,`list_id`),
  KEY `list_id` (`list_id`),
  CONSTRAINT `sf_guard_group_list_ibfk_4` FOREIGN KEY (`group_id`) REFERENCES `sf_guard_group` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sf_guard_group_list_ibfk_1` FOREIGN KEY (`list_id`) REFERENCES `ls_list` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sf_guard_group_list_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `sf_guard_group` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sf_guard_group_list_ibfk_3` FOREIGN KEY (`list_id`) REFERENCES `ls_list` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sf_guard_group_list`
--

LOCK TABLES `sf_guard_group_list` WRITE;
/*!40000 ALTER TABLE `sf_guard_group_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `sf_guard_group_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sf_guard_group_permission`
--

DROP TABLE IF EXISTS `sf_guard_group_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sf_guard_group_permission` (
  `group_id` bigint(20) NOT NULL DEFAULT '0',
  `permission_id` bigint(20) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`group_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `sf_guard_group_permission_ibfk_4` FOREIGN KEY (`group_id`) REFERENCES `sf_guard_group` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sf_guard_group_permission_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `sf_guard_permission` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sf_guard_group_permission_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `sf_guard_group` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sf_guard_group_permission_ibfk_3` FOREIGN KEY (`permission_id`) REFERENCES `sf_guard_permission` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sf_guard_group_permission`
--

LOCK TABLES `sf_guard_group_permission` WRITE;
/*!40000 ALTER TABLE `sf_guard_group_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `sf_guard_group_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sf_guard_permission`
--

DROP TABLE IF EXISTS `sf_guard_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sf_guard_permission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sf_guard_permission`
--

LOCK TABLES `sf_guard_permission` WRITE;
/*!40000 ALTER TABLE `sf_guard_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `sf_guard_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sf_guard_remember_key`
--

DROP TABLE IF EXISTS `sf_guard_remember_key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sf_guard_remember_key` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) DEFAULT NULL,
  `remember_key` varchar(32) DEFAULT NULL,
  `ip_address` varchar(50) NOT NULL DEFAULT '',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`ip_address`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `sf_guard_remember_key_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sf_guard_remember_key_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sf_guard_remember_key`
--

LOCK TABLES `sf_guard_remember_key` WRITE;
/*!40000 ALTER TABLE `sf_guard_remember_key` DISABLE KEYS */;
/*!40000 ALTER TABLE `sf_guard_remember_key` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sf_guard_user`
--

DROP TABLE IF EXISTS `sf_guard_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sf_guard_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `algorithm` varchar(128) NOT NULL DEFAULT 'sha1',
  `salt` varchar(128) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `is_super_admin` tinyint(1) DEFAULT '0',
  `last_login` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `is_active_idx_idx` (`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sf_guard_user`
--

LOCK TABLES `sf_guard_user` WRITE;
/*!40000 ALTER TABLE `sf_guard_user` DISABLE KEYS */;
INSERT INTO `sf_guard_user` VALUES (1,'system@example.org','sha1','32b041ee39125300e436f1e6fd8f8d19','c6443c37850166c568105849441e78063cf0532a',1,1,NULL,'2008-11-05 15:22:45','2011-06-21 16:27:27',1),(2,'bot@example.org','sha1','45eb9a24b767c6ccead8474d2ba89c65','151a2241aadd10ae849bcb46606dc0d45834ab85',1,1,NULL,'2008-11-05 15:22:45','2011-06-21 16:27:54',1),(3,'admin@example.org','sha1','a0cc3515c1dfc054218382b24a1b88eb','40482f58ef92afaacd298090f2cc10ee5562d3a7',1,1,'2011-06-21 01:31:01','2008-11-05 15:22:45','2011-06-21 13:31:01',1);
/*!40000 ALTER TABLE `sf_guard_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sf_guard_user_group`
--

DROP TABLE IF EXISTS `sf_guard_user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sf_guard_user_group` (
  `user_id` bigint(20) NOT NULL DEFAULT '0',
  `group_id` bigint(20) NOT NULL DEFAULT '0',
  `is_owner` tinyint(1) NOT NULL DEFAULT '0',
  `score` bigint(20) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`group_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `sf_guard_user_group_ibfk_4` FOREIGN KEY (`group_id`) REFERENCES `sf_guard_group` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sf_guard_user_group_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sf_guard_user_group_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `sf_guard_group` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sf_guard_user_group_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sf_guard_user_group`
--

LOCK TABLES `sf_guard_user_group` WRITE;
/*!40000 ALTER TABLE `sf_guard_user_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `sf_guard_user_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sf_guard_user_permission`
--

DROP TABLE IF EXISTS `sf_guard_user_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sf_guard_user_permission` (
  `user_id` bigint(20) NOT NULL DEFAULT '0',
  `permission_id` bigint(20) NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `sf_guard_user_permission_ibfk_4` FOREIGN KEY (`permission_id`) REFERENCES `sf_guard_permission` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sf_guard_user_permission_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sf_guard_user_permission_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `sf_guard_permission` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sf_guard_user_permission_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sf_guard_user_permission`
--

LOCK TABLES `sf_guard_user_permission` WRITE;
/*!40000 ALTER TABLE `sf_guard_user_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `sf_guard_user_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sf_guard_user_profile`
--

DROP TABLE IF EXISTS `sf_guard_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sf_guard_user_profile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `name_first` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `name_last` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `reason` longtext COLLATE utf8_unicode_ci,
  `analyst_reason` longtext COLLATE utf8_unicode_ci,
  `is_visible` tinyint(1) NOT NULL DEFAULT '1',
  `invitation_code` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `enable_html_editor` tinyint(1) NOT NULL DEFAULT '1',
  `enable_recent_views` tinyint(1) NOT NULL DEFAULT '1',
  `enable_favorites` tinyint(1) NOT NULL DEFAULT '1',
  `enable_pointers` tinyint(1) NOT NULL DEFAULT '1',
  `public_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `bio` longtext COLLATE utf8_unicode_ci,
  `is_confirmed` tinyint(1) NOT NULL DEFAULT '0',
  `confirmation_code` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `filename` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ranking_opt_out` tinyint(1) NOT NULL DEFAULT '0',
  `watching_opt_out` tinyint(1) NOT NULL DEFAULT '0',
  `enable_notes_list` tinyint(1) NOT NULL DEFAULT '1',
  `enable_announcements` tinyint(1) NOT NULL DEFAULT '1',
  `enable_notes_notifications` tinyint(1) NOT NULL DEFAULT '1',
  `score` bigint(20) DEFAULT NULL,
  `show_full_name` tinyint(1) NOT NULL DEFAULT '0',
  `unread_notes` int(11) NOT NULL DEFAULT '0',
  `home_network_id` bigint(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_idx` (`user_id`),
  UNIQUE KEY `unique_email_idx` (`email`),
  CONSTRAINT `sf_guard_user_profile_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sf_guard_user_profile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sf_guard_user_profile`
--

LOCK TABLES `sf_guard_user_profile` WRITE;
/*!40000 ALTER TABLE `sf_guard_user_profile` DISABLE KEYS */;
/*!40000 ALTER TABLE `sf_guard_user_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social`
--

DROP TABLE IF EXISTS `social`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `relationship_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `social_ibfk_2` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `social_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social`
--

LOCK TABLES `social` WRITE;
/*!40000 ALTER TABLE `social` DISABLE KEYS */;
/*!40000 ALTER TABLE `social` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sphinx_index`
--

DROP TABLE IF EXISTS `sphinx_index`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sphinx_index` (
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sphinx_index`
--

LOCK TABLES `sphinx_index` WRITE;
/*!40000 ALTER TABLE `sphinx_index` DISABLE KEYS */;
/*!40000 ALTER TABLE `sphinx_index` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_visible` tinyint(1) NOT NULL DEFAULT '1',
  `triple_namespace` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `triple_predicate` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `triple_value` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_meta`
--

DROP TABLE IF EXISTS `task_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task_meta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `task` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `namespace` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `predicate` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `value` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`task`,`namespace`,`predicate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_meta`
--

LOCK TABLES `task_meta` WRITE;
/*!40000 ALTER TABLE `task_meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `contact1_id` bigint(20) DEFAULT NULL,
  `contact2_id` bigint(20) DEFAULT NULL,
  `district_id` bigint(20) DEFAULT NULL,
  `is_lobbying` tinyint(1) DEFAULT NULL,
  `relationship_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contact1_id_idx` (`contact1_id`),
  KEY `contact2_id_idx` (`contact2_id`),
  KEY `relationship_id_idx` (`relationship_id`),
  CONSTRAINT `transaction_ibfk_6` FOREIGN KEY (`contact1_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`contact2_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `transaction_ibfk_3` FOREIGN KEY (`contact1_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `transaction_ibfk_4` FOREIGN KEY (`relationship_id`) REFERENCES `relationship` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `transaction_ibfk_5` FOREIGN KEY (`contact2_id`) REFERENCES `entity` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_favorite`
--

DROP TABLE IF EXISTS `user_favorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_favorite` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `object_model` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `object_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueness_idx` (`user_id`,`object_model`,`object_id`),
  KEY `object_idx` (`object_model`,`object_id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `user_favorite_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_favorite_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_favorite`
--

LOCK TABLES `user_favorite` WRITE;
/*!40000 ALTER TABLE `user_favorite` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_favorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_form_post`
--

DROP TABLE IF EXISTS `user_form_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_form_post` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `module` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `action` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `params` text COLLATE utf8_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `object_model` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `object_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `object_idx` (`object_model`,`object_id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `user_form_post_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_form_post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_form_post`
--

LOCK TABLES `user_form_post` WRITE;
/*!40000 ALTER TABLE `user_form_post` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_form_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_view`
--

DROP TABLE IF EXISTS `user_view`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_view` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `is_visible` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `object_model` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `object_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `object_idx` (`object_model`,`object_id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `user_view_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_view_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sf_guard_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_view`
--

LOCK TABLES `user_view` WRITE;
/*!40000 ALTER TABLE `user_view` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_view` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-03-02  0:21:18
