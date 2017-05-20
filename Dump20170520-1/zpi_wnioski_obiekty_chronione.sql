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
-- Table structure for table `wnioski_obiekty_chronione`
--

DROP TABLE IF EXISTS `wnioski_obiekty_chronione`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wnioski_obiekty_chronione` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `opis` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `jedn_org_id` int(11) NOT NULL DEFAULT '0',
  `typ_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `wnioski_obiekt_jedn_org_id_7c179283` (`jedn_org_id`),
  KEY `wnioski_obiekt_typ_id_0b42be68` (`typ_id`),
  CONSTRAINT `fk_typ` FOREIGN KEY (`typ_id`) REFERENCES `wnioski_typy_obiektow_chronionych` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wnioski_obiekty_chronione`
--

LOCK TABLES `wnioski_obiekty_chronione` WRITE;
/*!40000 ALTER TABLE `wnioski_obiekty_chronione` DISABLE KEYS */;
INSERT INTO `wnioski_obiekty_chronione` VALUES (1,'Lista studentów','Lista studentów obecnie studiujących',3,1),(2,'Dokument praw studenta','Dokument świadczący o prawach studenta',3,2),(3,'Dysk z obrazami systemów','Dysk z obrazami systemów',3,3);
/*!40000 ALTER TABLE `wnioski_obiekty_chronione` ENABLE KEYS */;
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
