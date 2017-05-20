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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content_type_id` int(11) NOT NULL DEFAULT '0',
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`),
  CONSTRAINT `content_type_id_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (64,22,'add_uprawnienia','Can add uprawnienia'),(65,22,'change_uprawnienia','Can change uprawnienia'),(66,22,'delete_uprawnienia','Can delete uprawnienia'),(67,23,'add_jednorg','Can add jedn org'),(68,23,'change_jednorg','Can change jedn org'),(69,23,'delete_jednorg','Can delete jedn org'),(70,24,'add_typobiektu','Can add typ obiektu'),(71,24,'change_typobiektu','Can change typ obiektu'),(72,24,'delete_typobiektu','Can delete typ obiektu'),(73,25,'add_obiekt','Can add obiekt'),(74,25,'change_obiekt','Can change obiekt'),(75,25,'delete_obiekt','Can delete obiekt'),(76,26,'add_rodzajpracownika','Can add rodzaj pracownika'),(77,26,'change_rodzajpracownika','Can change rodzaj pracownika'),(78,26,'delete_rodzajpracownika','Can delete rodzaj pracownika'),(79,27,'add_pracownik','Can add pracownik'),(80,27,'change_pracownik','Can change pracownik'),(81,27,'delete_pracownik','Can delete pracownik'),(82,28,'add_wniosek','Can add wniosek'),(83,28,'change_wniosek','Can change wniosek'),(84,28,'delete_wniosek','Can delete wniosek'),(85,29,'add_status','Can add status'),(86,29,'change_status','Can change status'),(87,29,'delete_status','Can delete status'),(88,30,'add_historia','Can add historia'),(89,30,'change_historia','Can change historia'),(90,30,'delete_historia','Can delete historia'),(91,31,'add_logentry','Can add log entry'),(92,31,'change_logentry','Can change log entry'),(93,31,'delete_logentry','Can delete log entry'),(94,32,'add_permission','Can add permission'),(95,32,'change_permission','Can change permission'),(96,32,'delete_permission','Can delete permission'),(97,33,'add_group','Can add group'),(98,33,'change_group','Can change group'),(99,33,'delete_group','Can delete group'),(100,34,'add_user','Can add user'),(101,34,'change_user','Can change user'),(102,34,'delete_user','Can delete user'),(103,35,'add_contenttype','Can add content type'),(104,35,'change_contenttype','Can change content type'),(105,35,'delete_contenttype','Can delete content type'),(106,36,'add_session','Can add session'),(107,36,'change_session','Can change session'),(108,36,'delete_session','Can delete session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-20 22:51:55
