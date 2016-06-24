-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 24, 2016 at 04:12 PM
-- Server version: 5.5.49-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `nexus`
--

-- --------------------------------------------------------

--
-- Table structure for table `changetable`
--

CREATE TABLE IF NOT EXISTS `changetable` (
  `changeid` bigint(20) NOT NULL AUTO_INCREMENT,
  `taskid` int(11) NOT NULL,
  `pushedby` varchar(255) NOT NULL,
  `verifiedby` varchar(255) NOT NULL,
  `verifydate` datetime NOT NULL,
  `pushdate` datetime NOT NULL,
  `fetchdate` datetime NOT NULL,
  `source_url` varchar(1000) NOT NULL,
  PRIMARY KEY (`changeid`),
  KEY `taskid` (`taskid`,`pushedby`),
  KEY `verifiedby` (`verifiedby`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `relidlabels`
--

CREATE TABLE IF NOT EXISTS `relidlabels` (
  `changeid` bigint(20) NOT NULL,
  `relid` int(11) NOT NULL,
  `label` varchar(100) NOT NULL,
  `changetype` int(11) NOT NULL,
  UNIQUE KEY `changeid` (`changeid`,`relid`,`label`),
  KEY `relid` (`relid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `relidprops`
--

CREATE TABLE IF NOT EXISTS `relidprops` (
  `changeid` bigint(20) NOT NULL,
  `relid` int(11) NOT NULL,
  `propname` varchar(100) NOT NULL,
  `oldpropvalue` text,
  `newpropvalue` text,
  `changetype` int(11) NOT NULL,
  UNIQUE KEY `changeid` (`changeid`,`relid`,`propname`),
  KEY `relid` (`relid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `relidtable`
--

CREATE TABLE IF NOT EXISTS `relidtable` (
  `relid` int(11) NOT NULL,
  `reltype` varchar(1000) NOT NULL,
  `startuuid` int(11) NOT NULL,
  `enduuid` int(11) NOT NULL,
  PRIMARY KEY (`relid`),
  KEY `startuuid` (`startuuid`),
  KEY `enduuid` (`enduuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tasklog`
--

CREATE TABLE IF NOT EXISTS `tasklog` (
  `taskid` int(11) NOT NULL,
  `userid` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `jsondump` mediumtext NOT NULL,
  `dumpdate` datetime NOT NULL,
  KEY `taskid` (`taskid`,`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

CREATE TABLE IF NOT EXISTS `tasks` (
  `taskid` int(11) NOT NULL AUTO_INCREMENT,
  `ownerid` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `createdate` datetime NOT NULL,
  `iscrawled` int(11) NOT NULL,
  PRIMARY KEY (`taskid`),
  KEY `ownerid` (`ownerid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Triggers `tasks`
--
DROP TRIGGER IF EXISTS `after_tasks_insert`;
DELIMITER //
CREATE TRIGGER `after_tasks_insert` AFTER INSERT ON `tasks`
 FOR EACH ROW INSERT INTO taskusers(userid, taskid)
VALUES (NEW.ownerid, NEW.taskid)
//
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `taskusers`
--

CREATE TABLE IF NOT EXISTS `taskusers` (
  `taskid` int(11) NOT NULL,
  `userid` varchar(255) NOT NULL,
  PRIMARY KEY (`taskid`,`userid`),
  KEY `userid` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `userid` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` int(11) NOT NULL,
  `apikey` varchar(255) NOT NULL,
  `keyenabled` int(11) NOT NULL,
  `lastlogin` datetime NOT NULL,
  `lastpwdchange` datetime NOT NULL,
  `name` varchar(1000) NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `apikey` (`apikey`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Triggers `users`
--
DROP TRIGGER IF EXISTS `after_users_insert`;
DELIMITER //
CREATE TRIGGER `after_users_insert` AFTER INSERT ON `users`
 FOR EACH ROW INSERT INTO tasks(name, ownerid, description, createdate, iscrawled)
VALUES ('Wiki Task For User', NEW.userid,  'Default task of the user', NOW(), 0)
//
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `uuidlabels`
--

CREATE TABLE IF NOT EXISTS `uuidlabels` (
  `changeid` bigint(20) NOT NULL,
  `uuid` int(11) NOT NULL,
  `label` varchar(100) NOT NULL,
  `changetype` int(11) NOT NULL,
  UNIQUE KEY `changeid` (`changeid`,`uuid`,`label`),
  KEY `uuid` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `uuidprops`
--

CREATE TABLE IF NOT EXISTS `uuidprops` (
  `changeid` bigint(20) NOT NULL,
  `uuid` int(11) NOT NULL,
  `propname` varchar(100) NOT NULL,
  `oldpropvalue` text,
  `newpropvalue` text,
  `changetype` int(11) NOT NULL,
  KEY `changeid` (`changeid`),
  KEY `uuid` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `uuidtable`
--

CREATE TABLE IF NOT EXISTS `uuidtable` (
  `uuid` int(11) NOT NULL,
  `name` varchar(3000) DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `changetable`
--
ALTER TABLE `changetable`
  ADD CONSTRAINT `changetable_ibfk_1` FOREIGN KEY (`taskid`, `pushedby`) REFERENCES `taskusers` (`taskid`, `userid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `changetable_ibfk_2` FOREIGN KEY (`verifiedby`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `relidlabels`
--
ALTER TABLE `relidlabels`
  ADD CONSTRAINT `relidlabels_ibfk_1` FOREIGN KEY (`changeid`) REFERENCES `changetable` (`changeid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `relidlabels_ibfk_2` FOREIGN KEY (`relid`) REFERENCES `relidtable` (`relid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `relidprops`
--
ALTER TABLE `relidprops`
  ADD CONSTRAINT `relidprops_ibfk_1` FOREIGN KEY (`changeid`) REFERENCES `changetable` (`changeid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `relidprops_ibfk_2` FOREIGN KEY (`relid`) REFERENCES `relidtable` (`relid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `relidtable`
--
ALTER TABLE `relidtable`
  ADD CONSTRAINT `relidtable_ibfk_1` FOREIGN KEY (`startuuid`) REFERENCES `uuidtable` (`uuid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `relidtable_ibfk_2` FOREIGN KEY (`enduuid`) REFERENCES `uuidtable` (`uuid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tasklog`
--
ALTER TABLE `tasklog`
  ADD CONSTRAINT `tasklog_ibfk_1` FOREIGN KEY (`taskid`, `userid`) REFERENCES `taskusers` (`taskid`, `userid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tasks`
--
ALTER TABLE `tasks`
  ADD CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`ownerid`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `taskusers`
--
ALTER TABLE `taskusers`
  ADD CONSTRAINT `taskusers_ibfk_1` FOREIGN KEY (`taskid`) REFERENCES `tasks` (`taskid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `taskusers_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `uuidlabels`
--
ALTER TABLE `uuidlabels`
  ADD CONSTRAINT `uuidlabels_ibfk_1` FOREIGN KEY (`changeid`) REFERENCES `changetable` (`changeid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `uuidlabels_ibfk_2` FOREIGN KEY (`uuid`) REFERENCES `uuidtable` (`uuid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `uuidprops`
--
ALTER TABLE `uuidprops`
  ADD CONSTRAINT `uuidprops_ibfk_1` FOREIGN KEY (`changeid`) REFERENCES `changetable` (`changeid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `uuidprops_ibfk_2` FOREIGN KEY (`uuid`) REFERENCES `uuidtable` (`uuid`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
