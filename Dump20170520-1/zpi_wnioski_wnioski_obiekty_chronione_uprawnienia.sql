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
-- Table structure for table `wnioski_wnioski_obiekty_chronione_uprawnienia`
--

DROP TABLE IF EXISTS `wnioski_wnioski_obiekty_chronione_uprawnienia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wnioski_wnioski_obiekty_chronione_uprawnienia` (
  `id_wniosku` int(11) NOT NULL,
  `id_obiektu` int(11) NOT NULL,
  `id_uprawnienia` int(11) NOT NULL,
  KEY `fk_WNIOSKI_id_wniosku_idx` (`id_wniosku`),
  KEY `fk_OBIEKTY_CHRONIONE_id_obiektu_idx` (`id_obiektu`),
  KEY `fk_UPRAWNIENIA_id_uprawnienia_idx` (`id_uprawnienia`),
  CONSTRAINT `fk2_OBIEKTY_CHRONIONE_id_obiektu` FOREIGN KEY (`id_obiektu`) REFERENCES `wnioski_obiekty_chronione` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk2_UPRAWNIENIA_id_uprawnienia` FOREIGN KEY (`id_uprawnienia`) REFERENCES `wnioski_uprawnienia` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk2_WNIOSKI_id_wniosku` FOREIGN KEY (`id_wniosku`) REFERENCES `wnioski_wnioski` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wnioski_wnioski_obiekty_chronione_uprawnienia`
--

LOCK TABLES `wnioski_wnioski_obiekty_chronione_uprawnienia` WRITE;
/*!40000 ALTER TABLE `wnioski_wnioski_obiekty_chronione_uprawnienia` DISABLE KEYS */;
/*!40000 ALTER TABLE `wnioski_wnioski_obiekty_chronione_uprawnienia` ENABLE KEYS */;
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
