-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 03, 2016 at 03:24 PM
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

DELIMITER $$
--
-- Functions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `jaro_winkler_similarity`(
  in1 VARCHAR(255),
  in2 VARCHAR(255)
) RETURNS float
    DETERMINISTIC
BEGIN
#finestra:= search window, curString:= scanning cursor for the original string, curSub:= scanning cursor for the compared string
    DECLARE finestra, curString, curSub, maxSub, trasposizioni, prefixlen, maxPrefix INT;
    DECLARE char1, char2 CHAR(1);
    DECLARE common1, common2, old1, old2 VARCHAR(255);
    DECLARE trovato BOOLEAN;
    DECLARE returnValue, jaro FLOAT;
    SET maxPrefix = 6;
#from the original jaro - winkler algorithm
    SET common1 = "";
    SET common2 = "";
    SET finestra = (length(in1) + length(in2) - abs(length(in1) - length(in2))) DIV 4
                   + ((length(in1) + length(in2) - abs(length(in1) - length(in2))) / 2) MOD 2;
    SET old1 = in1;
    SET old2 = in2;

#calculating common letters vectors
    SET curString = 1;
    WHILE curString <= length(in1) AND (curString <= (length(in2) + finestra)) DO
      SET curSub = curstring - finestra;
      IF (curSub) < 1
      THEN
        SET curSub = 1;
      END IF;
      SET maxSub = curstring + finestra;
      IF (maxSub) > length(in2)
      THEN
        SET maxSub = length(in2);
      END IF;
      SET trovato = FALSE;
      WHILE curSub <= maxSub AND trovato = FALSE DO
        IF substr(in1, curString, 1) = substr(in2, curSub, 1)
        THEN
          SET common1 = concat(common1, substr(in1, curString, 1));
          SET in2 = concat(substr(in2, 1, curSub - 1), concat("0", substr(in2, curSub + 1, length(in2) - curSub + 1)));
          SET trovato = TRUE;
        END IF;
        SET curSub = curSub + 1;
      END WHILE;
      SET curString = curString + 1;
    END WHILE;
#back to the original string
    SET in2 = old2;
    SET curString = 1;
    WHILE curString <= length(in2) AND (curString <= (length(in1) + finestra)) DO
      SET curSub = curstring - finestra;
      IF (curSub) < 1
      THEN
        SET curSub = 1;
      END IF;
      SET maxSub = curstring + finestra;
      IF (maxSub) > length(in1)
      THEN
        SET maxSub = length(in1);
      END IF;
      SET trovato = FALSE;
      WHILE curSub <= maxSub AND trovato = FALSE DO
        IF substr(in2, curString, 1) = substr(in1, curSub, 1)
        THEN
          SET common2 = concat(common2, substr(in2, curString, 1));
          SET in1 = concat(substr(in1, 1, curSub - 1), concat("0", substr(in1, curSub + 1, length(in1) - curSub + 1)));
          SET trovato = TRUE;
        END IF;
        SET curSub = curSub + 1;
      END WHILE;
      SET curString = curString + 1;
    END WHILE;
#back to the original string
    SET in1 = old1;

#calculating jaro metric
    IF length(common1) <> length(common2)
    THEN SET jaro = 0;
    ELSEIF length(common1) = 0 OR length(common2) = 0
      THEN SET jaro = 0;
    ELSE
#calcolo la distanza di winkler
#passo 1: calcolo le trasposizioni
      SET trasposizioni = 0;
      SET curString = 1;
      WHILE curString <= length(common1) DO
        IF (substr(common1, curString, 1) <> substr(common2, curString, 1))
        THEN
          SET trasposizioni = trasposizioni + 1;
        END IF;
        SET curString = curString + 1;
      END WHILE;
      SET jaro =
      (
        length(common1) / length(in1) +
        length(common2) / length(in2) +
        (length(common1) - trasposizioni / 2) / length(common1)
      ) / 3;

    END IF;
#end if for jaro metric

#calculating common prefix for winkler metric
    SET prefixlen = 0;
    WHILE (substring(in1, prefixlen + 1, 1) = substring(in2, prefixlen + 1, 1)) AND (prefixlen < 6) DO
      SET prefixlen = prefixlen + 1;
    END WHILE;


#calculate jaro-winkler metric
    RETURN jaro + (prefixlen * 0.1 * (1 - jaro));
  END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `relidtable`
--

CREATE TABLE IF NOT EXISTS `relidtable` (
  `relid` int(11) NOT NULL,
  `reltype` varchar(1000) DEFAULT NULL,
  `startuuid` int(11) DEFAULT NULL,
  `enduuid` int(11) DEFAULT NULL,
  PRIMARY KEY (`relid`),
  KEY `startuuid` (`startuuid`),
  KEY `enduuid` (`enduuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
('abhi1@gmail.com', '48dc8d29308eb256edc76f25def07251', 1),
('abhi2@gmail.com', '48dc8d29308eb256edc76f25def07251', 2),
('abhi3@gmail.com', '48dc8d29308eb256edc76f25def07251', 3),
('abhi4@gmail.com', '48dc8d29308eb256edc76f25def07251', 4),
('abhi5@gmail.com', '48dc8d29308eb256edc76f25def07251', 5),
('abhi6@gmail.com', '48dc8d29308eb256edc76f25def07251', 6),
('abhi7@gmail.com', '48dc8d29308eb256edc76f25def07251', 7);

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
-- Constraints for table `relidtable`
--
ALTER TABLE `relidtable`
  ADD CONSTRAINT `relidtable_ibfk_1` FOREIGN KEY (`startuuid`) REFERENCES `uuidtable` (`uuid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `relidtable_ibfk_2` FOREIGN KEY (`enduuid`) REFERENCES `uuidtable` (`uuid`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
