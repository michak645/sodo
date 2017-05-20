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
-- Table structure for table `wnioski_pracownicy`
--

DROP TABLE IF EXISTS `wnioski_pracownicy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wnioski_pracownicy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `imie` varchar(90) COLLATE utf8_unicode_ci NOT NULL,
  `nazwisko` varchar(90) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_zatr` date DEFAULT NULL,
  `data_zwol` date DEFAULT NULL,
  `szkolenie` tinyint(4) NOT NULL,
  `login` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `haslo` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rodzaj_id` int(11) DEFAULT NULL,
  `jedn_org_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_id_rodzaju_idx` (`rodzaj_id`),
  CONSTRAINT `fk_id_rodzaju` FOREIGN KEY (`rodzaj_id`) REFERENCES `wnioski_rodzaje_pracownikow` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wnioski_pracownicy`
--

LOCK TABLES `wnioski_pracownicy` WRITE;
/*!40000 ALTER TABLE `wnioski_pracownicy` DISABLE KEYS */;
INSERT INTO `wnioski_pracownicy` VALUES (1,'Michał','Kędzierski','kedzierski@example.com','2016-01-01',NULL,0,'michal','michal',3,1),(2,'Kamil','Trąbka','trabka@example.com','2016-06-06',NULL,0,'kamil','kamil',2,1),(3,'Patryk','Skibiński','skibinski@example.com','2017-01-01',NULL,0,'patryk','patryk',1,2);
/*!40000 ALTER TABLE `wnioski_pracownicy` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-20 22:51:58
