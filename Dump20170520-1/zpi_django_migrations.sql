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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-04-19 16:09:37'),(2,'auth','0001_initial','2017-04-19 16:09:37'),(3,'admin','0001_initial','2017-04-19 16:09:37'),(4,'admin','0002_logentry_remove_auto_add','2017-04-19 16:09:37'),(5,'contenttypes','0002_remove_content_type_name','2017-04-19 16:09:37'),(6,'auth','0002_alter_permission_name_max_length','2017-04-19 16:09:37'),(7,'auth','0003_alter_user_email_max_length','2017-04-19 16:09:37'),(8,'auth','0004_alter_user_username_opts','2017-04-19 16:09:37'),(9,'auth','0005_alter_user_last_login_null','2017-04-19 16:09:37'),(10,'auth','0006_require_contenttypes_0002','2017-04-19 16:09:37'),(11,'auth','0007_alter_validators_add_error_messages','2017-04-19 16:09:37'),(12,'auth','0008_alter_user_username_max_length','2017-04-19 16:09:37'),(13,'sessions','0001_initial','2017-04-19 16:09:37'),(14,'wnioski','0001_initial','2017-04-19 16:15:17'),(15,'wnioski','0002_auto_20170420_0921','2017-04-20 09:21:33'),(16,'wnioski','0003_auto_20170420_1746','2017-04-20 15:46:51'),(17,'wnioski','0004_auto_20170423_1831','2017-04-23 16:31:53'),(18,'wnioski','0005_auto_20170423_1854','2017-04-23 16:54:47'),(19,'wnioski','0006_auto_20170423_1904','2017-04-23 17:04:06'),(20,'wnioski','0007_remove_wniosek_data_zlo','2017-04-24 08:47:02'),(21,'wnioski','0008_auto_20170424_0858','2017-04-24 08:59:09');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-20 22:51:57
