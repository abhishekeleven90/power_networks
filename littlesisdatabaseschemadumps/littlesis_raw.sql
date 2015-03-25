-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: littlesis_raw
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
-- Table structure for table `os_candidate`
--

DROP TABLE IF EXISTS `os_candidate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_candidate` (
  `cycle` varchar(4) COLLATE utf8_unicode_ci NOT NULL,
  `fec_id` varchar(9) COLLATE utf8_unicode_ci NOT NULL,
  `candidate_id` varchar(9) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `party` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `district` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `district_current` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_current` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ran` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `recipient_code` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nopacs` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_last` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_first` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_middle` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_suffix` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_nick` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`candidate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_candidate`
--

LOCK TABLES `os_candidate` WRITE;
/*!40000 ALTER TABLE `os_candidate` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_candidate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_committee`
--

DROP TABLE IF EXISTS `os_committee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_committee` (
  `cycle` varchar(4) COLLATE utf8_unicode_ci NOT NULL,
  `committee_id` varchar(9) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `name` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `affiliate` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `parent` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `recipient_id` varchar(9) COLLATE utf8_unicode_ci DEFAULT NULL,
  `recipient_code` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `candidate_id` varchar(9) COLLATE utf8_unicode_ci DEFAULT NULL,
  `party` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `industry_id` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_sensitive` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_foreign` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`committee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_committee`
--

LOCK TABLES `os_committee` WRITE;
/*!40000 ALTER TABLE `os_committee` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_committee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_donation`
--

DROP TABLE IF EXISTS `os_donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_donation` (
  `cycle` varchar(4) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `row_id` varchar(30) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `donor_id` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `donor_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `recipient_id` varchar(9) COLLATE utf8_unicode_ci DEFAULT NULL,
  `employer_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `parent_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `industry_id` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `street` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `city` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `state` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `zip` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `recipient_code` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `transaction_type` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `committee_id` varchar(9) COLLATE utf8_unicode_ci DEFAULT NULL,
  `intermediate_id` varchar(9) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gender` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `employer_raw` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fec_id` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title_raw` varchar(38) COLLATE utf8_unicode_ci DEFAULT NULL,
  `org_raw` varchar(38) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `donor_name_last` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `donor_name_first` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `donor_name_middle` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `donor_name_suffix` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `donor_name_nick` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`cycle`,`row_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_donation`
--

LOCK TABLES `os_donation` WRITE;
/*!40000 ALTER TABLE `os_donation` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_donation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_lobbying`
--

DROP TABLE IF EXISTS `os_lobbying`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_lobbying` (
  `uniq_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `registrant_raw` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registrant` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `isfirm` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `client_raw` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `client` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ultorg` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `amount` decimal(15,2) DEFAULT NULL,
  `catcode` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `self` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `include_nsfs` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_used` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ind` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `year` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `typelong` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  `org_id` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `affiliate` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`uniq_id`),
  KEY `registrant_idx_idx` (`registrant`),
  KEY `ultorg_idx_idx` (`ultorg`),
  KEY `client_idx_idx` (`client`),
  KEY `catcode_idx_idx` (`catcode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_lobbying`
--

LOCK TABLES `os_lobbying` WRITE;
/*!40000 ALTER TABLE `os_lobbying` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_lobbying` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_lobbying_agency`
--

DROP TABLE IF EXISTS `os_lobbying_agency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_lobbying_agency` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `uniq_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `agency_id` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `agency` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uniq_id_idx_idx` (`uniq_id`),
  KEY `agency_id_idx_idx` (`agency_id`),
  KEY `agency_idx_idx` (`agency`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_lobbying_agency`
--

LOCK TABLES `os_lobbying_agency` WRITE;
/*!40000 ALTER TABLE `os_lobbying_agency` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_lobbying_agency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_lobbying_bill`
--

DROP TABLE IF EXISTS `os_lobbying_bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_lobbying_bill` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `b_id` int(11) DEFAULT NULL,
  `si_id` int(11) DEFAULT NULL,
  `cong_no` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bill_name` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `si_id_idx_idx` (`si_id`),
  KEY `bill_name_idx_idx` (`bill_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_lobbying_bill`
--

LOCK TABLES `os_lobbying_bill` WRITE;
/*!40000 ALTER TABLE `os_lobbying_bill` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_lobbying_bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_lobbying_industry`
--

DROP TABLE IF EXISTS `os_lobbying_industry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_lobbying_industry` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ultorg` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `client` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `total` decimal(15,2) DEFAULT NULL,
  `year` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `catcode` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `catcode_idx_idx` (`catcode`,`year`,`ultorg`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_lobbying_industry`
--

LOCK TABLES `os_lobbying_industry` WRITE;
/*!40000 ALTER TABLE `os_lobbying_industry` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_lobbying_industry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_lobbying_issue`
--

DROP TABLE IF EXISTS `os_lobbying_issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_lobbying_issue` (
  `si_id` int(11) NOT NULL DEFAULT '0',
  `uniq_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `issue_id` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `issue` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `specific_issue` longblob,
  `year` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`si_id`),
  KEY `uniq_id_idx_idx` (`uniq_id`),
  KEY `issue_id_idx_idx` (`uniq_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_lobbying_issue`
--

LOCK TABLES `os_lobbying_issue` WRITE;
/*!40000 ALTER TABLE `os_lobbying_issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_lobbying_issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_lobbyist`
--

DROP TABLE IF EXISTS `os_lobbyist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_lobbyist` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `uniq_id` varchar(36) COLLATE utf8_unicode_ci NOT NULL,
  `lobbyist_raw` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `lobbyist` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `lobbyist_id` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `year` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `official_position` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `cid` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `formercongmem` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_first` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_middle` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_last` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_suffix` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name_nick` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `uniq_id_idx_idx` (`uniq_id`),
  KEY `lobbyist_id_idx_idx` (`lobbyist_id`),
  KEY `name_idx_idx` (`name_last`,`name_middle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_lobbyist`
--

LOCK TABLES `os_lobbyist` WRITE;
/*!40000 ALTER TABLE `os_lobbyist` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_lobbyist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os_pac_donation`
--

DROP TABLE IF EXISTS `os_pac_donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `os_pac_donation` (
  `cycle` varchar(4) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `row_id` varchar(7) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `committee_id` varchar(9) COLLATE utf8_unicode_ci NOT NULL,
  `recipient_crp_id` varchar(9) COLLATE utf8_unicode_ci NOT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `industry_id` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `transaction_type` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `direct` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `recipient_fec_id` varchar(9) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`cycle`,`row_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os_pac_donation`
--

LOCK TABLES `os_pac_donation` WRITE;
/*!40000 ALTER TABLE `os_pac_donation` DISABLE KEYS */;
/*!40000 ALTER TABLE `os_pac_donation` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-03-02  0:21:28
