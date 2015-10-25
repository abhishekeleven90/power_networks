-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 25, 2015 at 05:27 PM
-- Server version: 5.5.41-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `flasktemp`
--

-- --------------------------------------------------------

--
-- Table structure for table `person`
--

CREATE TABLE IF NOT EXISTS `person` (
  `name` varchar(200) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=34 ;

--
-- Dumping data for table `person`
--

INSERT INTO `person` (`name`, `id`) VALUES
('nayaperson', 5),
('nayaperson', 6),
('nayaperson', 7),
('nayaperson', 8),
('nayaperson', 9),
('nayaperson', 10),
('nayaperson', 11),
('nayaperson', 12),
('nayaperson', 13),
('nayaperson', 14),
('nayaperson', 15),
('nayaperson', 16),
('nayaperson', 17),
('nayaperson', 18),
('nayaperson', 19),
('nayaperson', 20),
('nayaperson', 21),
('nayaperson', 22),
('nayaperson', 23),
('nayaperson', 24),
('nayaperson', 25),
('nayaperson', 26),
('nayaperson', 27),
('nayaperson', 28),
('nayaperson', 29),
('nayaperson', 30),
('nayaperson', 31),
('nayaperson', 32),
('nayaperson', 33);

-- --------------------------------------------------------

--
-- Table structure for table `pet`
--

CREATE TABLE IF NOT EXISTS `pet` (
  `type` varchar(20) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ownerid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ownerid` (`ownerid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

--
-- Dumping data for table `pet`
--

INSERT INTO `pet` (`type`, `id`, `ownerid`) VALUES
('cat', 3, 9),
('cat', 4, 10),
('cat', 5, 11),
('cat', 6, 12),
('cat', 7, 13),
('cat', 8, 14),
('cat', 9, 15),
('cat', 10, 16),
('cat', 11, 17),
('cat', 12, 18),
('cat', 13, 19),
('cat', 14, 20),
('cat', 15, 21),
('cat', 16, 22),
('cat', 17, 23),
('cat', 18, 24),
('cat', 19, 25),
('cat', 20, 26),
('cat', 21, 27),
('cat', 22, 28),
('cat', 23, 29),
('cat', 24, 30),
('cat', 25, 31),
('cat', 26, 32),
('cat', 27, 33);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `userid` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userid`, `password`, `role`) VALUES
('abhiagar90@gmail.com', '48dc8d29308eb256edc76f25def07251', 3),
('abhijhs11@gmail.com', '48dc8d29308eb256edc76f25def07251', 7),
('mcs142114@iitd.ac.in', '48dc8d29308eb256edc76f25def07251', 1);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pet`
--
ALTER TABLE `pet`
  ADD CONSTRAINT `personcons` FOREIGN KEY (`ownerid`) REFERENCES `person` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;