-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 28, 2016 at 05:26 PM
-- Server version: 5.5.41-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `crawldb`
--

-- --------------------------------------------------------

--
-- Table structure for table `political_crawl_jan`
--

CREATE TABLE IF NOT EXISTS `political_crawl_jan` (
  `id` int(11) DEFAULT NULL,
  `mynetaid` varchar(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `contact` varchar(15) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `resolved` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `political_crawl_jan`
--

INSERT INTO `political_crawl_jan` (`id`, `mynetaid`, `name`, `email`, `contact`, `address`, `resolved`) VALUES
(1, '23', 'Naveen Jindal', 'something@someone.com', '55467878', 'Andhra etc', 0),
(2, '25', 'Narendra Modi', 'narendra@narendra.com', '8375956404', 'Gujarat', 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
