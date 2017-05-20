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
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` longtext COLLATE utf8_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (15,'1','Uprawnienia object',1,'[{\"added\": {}}]',22,4,'2017-04-23 17:04:58.825200'),(16,'2','Uprawnienia object',1,'[{\"added\": {}}]',22,4,'2017-04-23 17:05:02.765425'),(17,'3','Uprawnienia object',1,'[{\"added\": {}}]',22,4,'2017-04-23 17:05:07.242681'),(18,'1','JednOrg object',1,'[{\"added\": {}}]',23,4,'2017-04-23 17:17:08.432931'),(19,'2','JednOrg object',1,'[{\"added\": {}}]',23,4,'2017-04-23 17:17:13.560224'),(20,'1','RodzajPracownika object',1,'[{\"added\": {}}]',26,4,'2017-04-23 17:20:08.482229'),(21,'2','RodzajPracownika object',1,'[{\"added\": {}}]',26,4,'2017-04-23 17:20:12.335449'),(22,'3','RodzajPracownika object',1,'[{\"added\": {}}]',26,4,'2017-04-23 17:20:16.550691'),(23,'1','Database',1,'[{\"added\": {}}]',24,4,'2017-04-23 17:22:48.441378'),(24,'2','Document',1,'[{\"added\": {}}]',24,4,'2017-04-23 17:22:57.224881'),(25,'3','Hard drive',1,'[{\"added\": {}}]',24,4,'2017-04-23 17:23:36.493127'),(26,'1','Przyjęty',1,'[{\"added\": {}}]',29,4,'2017-04-23 17:24:24.901895'),(27,'2','Odrzucony',1,'[{\"added\": {}}]',29,4,'2017-04-23 17:24:29.195141'),(28,'3','Przetwarzanie',1,'[{\"added\": {}}]',29,4,'2017-04-23 17:24:55.637653'),(29,'1','Michał Kędzierski',1,'[{\"added\": {}}]',27,4,'2017-04-23 17:25:54.047994'),(30,'2','Kamil Trąbka',1,'[{\"added\": {}}]',27,4,'2017-04-23 17:26:23.716691'),(31,'3','Patryk Skibiński',1,'[{\"added\": {}}]',27,4,'2017-04-23 17:26:55.093486'),(32,'3','WMI',1,'[{\"added\": {}}]',23,4,'2017-04-23 17:30:48.857856'),(33,'1','Lista studentów',1,'[{\"added\": {}}]',25,4,'2017-04-23 17:31:14.052297'),(34,'2','Dokument praw studenta',1,'[{\"added\": {}}]',25,4,'2017-04-23 17:32:49.181739'),(35,'3','Dysk z obrazami systemów',1,'[{\"added\": {}}]',25,4,'2017-04-23 17:33:04.879636'),(36,'1','typ1 Kamil Trąbka, API, Jednostka 1 Patryk Skibiński, Zwykły, Jednostka 2 Lista studentów',1,'',28,4,'2017-04-24 08:48:34.242552'),(37,'2','typ1 2017-04-24 09:01:25+00:00 Michał Kędzierski, LABI, Jednostka 1 Kamil Trąbka, API, Jednostka 1, Dysk z obrazami systemów',1,'',28,4,'2017-04-24 09:01:37.163415'),(38,'3','typ2 2017-04-24 09:18:15+00:00 Kamil Trąbka, API, Jednostka 1 Michał Kędzierski, LABI, Jednostka 1, Dysk z obrazami systemów',1,'',28,4,'2017-04-24 09:18:24.774282'),(39,'5','michal',1,'[{\"added\": {}}]',34,4,'2017-05-14 14:17:07.611865'),(40,'6','kamil',1,'[{\"added\": {}}]',34,4,'2017-05-14 14:44:53.465146'),(41,'6','kamil',2,'[{\"changed\": {\"fields\": [\"is_staff\"]}}]',34,4,'2017-05-14 14:55:10.943464'),(42,'9','habababa',3,'',34,4,'2017-05-14 15:17:04.348587'),(43,'6','kamil',3,'',34,4,'2017-05-14 15:17:04.356587'),(44,'5','michal',3,'',34,4,'2017-05-14 15:17:04.364587'),(45,'8','patryk',3,'',34,4,'2017-05-14 15:17:04.372588'),(46,'7','test',3,'',34,4,'2017-05-14 15:17:04.380588'),(47,'10','uzytkownik',3,'',34,4,'2017-05-14 15:17:04.388589');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
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
