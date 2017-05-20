-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: zpi
-- ------------------------------------------------------
-- Server version	5.7.18-log

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
-- Table structure for table `wnioski_wnioski`
--

DROP TABLE IF EXISTS `wnioski_wnioski`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wnioski_wnioski` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `obiekt_id` int(11) NOT NULL,
  `prac_dot_id` int(11) NOT NULL,
  `prac_sklada_id` int(11) NOT NULL,
  `typ` varchar(9) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_zlo` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_prac_sklada_idx` (`prac_sklada_id`),
  KEY `fk_prac_dot_idx` (`prac_dot_id`),
  KEY `fk_obiekt_idx` (`obiekt_id`),
  CONSTRAINT `fk_obiekt` FOREIGN KEY (`obiekt_id`) REFERENCES `wnioski_obiekty_chronione` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_prac_dot` FOREIGN KEY (`prac_dot_id`) REFERENCES `wnioski_pracownicy` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_prac_sklada` FOREIGN KEY (`prac_sklada_id`) REFERENCES `wnioski_pracownicy` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wnioski_wnioski`
--

LOCK TABLES `wnioski_wnioski` WRITE;
/*!40000 ALTER TABLE `wnioski_wnioski` DISABLE KEYS */;
INSERT INTO `wnioski_wnioski` VALUES (1,1,3,2,'typ1','2017-04-24 08:59:09'),(2,3,2,1,'typ1','2017-04-24 09:01:25'),(3,3,1,2,'typ2','2017-04-24 09:18:15'),(4,1,1,1,'asd','2017-04-24 09:19:02'),(5,2,2,3,'dsad','2017-04-24 09:20:09'),(6,1,2,1,'hjk','2017-04-24 09:21:12'),(7,1,2,1,'hjk','2017-04-24 09:21:12'),(8,2,2,2,'DSG','2017-04-24 09:29:36'),(9,2,2,3,'afk','2017-04-24 09:34:25'),(10,3,2,1,'ddsd','2017-05-19 17:12:16'),(11,1,1,1,'test','2017-05-20 14:50:15'),(12,3,3,2,'test2','2017-05-20 22:49:45');
/*!40000 ALTER TABLE `wnioski_wnioski` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-20 22:51:56
