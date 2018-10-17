-- MySQL dump 10.13  Distrib 5.7.19, for Win64 (x86_64)
--
-- Host: localhost    Database: db_web
-- ------------------------------------------------------
-- Server version	5.7.19-log

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('56907ee8ecfe');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boards`
--

DROP TABLE IF EXISTS `boards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `admin_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  CONSTRAINT `boards_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boards`
--

LOCK TABLES `boards` WRITE;
/*!40000 ALTER TABLE `boards` DISABLE KEYS */;
INSERT INTO `boards` VALUES (1,'意见与建议',1),(2,'新闻',1),(3,'影视',1),(4,'音乐',1),(5,'历史',1),(6,'游戏',1),(7,'生活',1),(8,'校园',3),(9,'体育',1),(10,'交易',12),(11,'科技',1),(12,'教育',2),(14,'闲聊',4);
/*!40000 ALTER TABLE `boards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `author_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `floor` int(11) NOT NULL,
  `parent` int(11) DEFAULT NULL,
  `com_time` datetime NOT NULL,
  `like_num` int(11) NOT NULL,
  `status` enum('normal','blocked','hot') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,'你哈',2,1,1,0,'2017-12-25 18:15:39',6,'normal'),(2,'你好',2,1,2,0,'2017-12-25 18:16:35',1,'normal'),(3,'前排围观',2,1,3,0,'2017-12-25 18:26:13',1,'blocked'),(4,'你好，我是bob',3,1,4,0,'2017-12-25 20:25:36',0,'normal'),(5,'很高兴认识你',3,1,5,0,'2017-12-25 22:05:19',4,'normal');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `favorites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
INSERT INTO `favorites` VALUES (1,2,4),(2,2,1),(3,1,1);
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `post_day` date NOT NULL,
  `author_id` int(11) NOT NULL,
  `board_id` int(11) NOT NULL,
  `com_num` int(11) NOT NULL,
  `reward` int(11) NOT NULL,
  `status` enum('reviewing','normal','blocked','hot') NOT NULL,
  `favor_num` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `board_id` (`board_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `posts_ibfk_2` FOREIGN KEY (`board_id`) REFERENCES `boards` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES (1,'大家好','大家好，我是alice','2017-12-11',2,1,5,0,'normal',2),(2,'如何学习SQL','我超想学数据库的，大家有没有什么学习建议？','2017-12-11',2,1,0,0,'normal',0),(3,'求大家帮我出奇招','考试快到了，学不会，怎么作弊？','2017-12-30',8,12,0,0,'normal',0),(4,'数据库考试通知','26日，开卷考试，四或五道大题','2018-01-10',3,1,0,0,'normal',1),(5,'2018年第二学期开学通知','2018.3.5开始上课','2018-01-10',3,1,0,0,'normal',0),(6,'快放假了','回家路上注意安全','2018-01-10',3,8,0,0,'normal',0),(7,'文明发帖','请文明发帖','2018-01-10',1,1,0,0,'normal',0),(8,'文明评论','请文明评论','2018-01-10',1,3,0,0,'normal',0),(9,'构建和谐论坛','请大家共同努力，构建和谐论坛','2018-01-10',1,3,0,0,'normal',0),(10,'宿舍严禁使用违章电器','宿舍严禁使用违章电器','2018-01-10',1,8,0,0,'normal',0),(11,'数据库课程设计答辩时间','1月20日，周六，在此之前提交作业','2018-01-12',2,12,0,0,'reviewing',0),(12,'水一贴','水经验','2018-01-15',23,1,0,0,'normal',0),(14,'低价出售数据库教材','二手教材，无破损，半价出售','2018-01-19',23,10,0,0,'normal',0);
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_c`
--

DROP TABLE IF EXISTS `reports_c`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reports_c` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `comt_id` int(11) NOT NULL,
  `handle` int(11) NOT NULL,
  `report_time` datetime NOT NULL,
  `handle_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comt_id` (`comt_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reports_c_ibfk_1` FOREIGN KEY (`comt_id`) REFERENCES `comments` (`id`),
  CONSTRAINT `reports_c_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_c`
--

LOCK TABLES `reports_c` WRITE;
/*!40000 ALTER TABLE `reports_c` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports_c` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_p`
--

DROP TABLE IF EXISTS `reports_p`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reports_p` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `handle` int(11) NOT NULL,
  `report_time` datetime NOT NULL,
  `handle_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reports_p_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  CONSTRAINT `reports_p_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_p`
--

LOCK TABLES `reports_p` WRITE;
/*!40000 ALTER TABLE `reports_p` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports_p` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `password` varchar(100) NOT NULL,
  `gender` enum('M','N','F') NOT NULL,
  `birthday` date DEFAULT NULL,
  `recognition` varchar(20) DEFAULT NULL,
  `is_admin` enum('Y','N') NOT NULL,
  `level` int(11) NOT NULL,
  `exp` int(11) NOT NULL,
  `pic` varchar(100) NOT NULL,
  `balance` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Superman','wsz970801','N','2014-07-27','Developer','Y',0,0,'images/userdefault.png',-1),(2,'alice','alice123','F','1999-02-19',NULL,'Y',1,1,'images/userdefault.png',0),(3,'bob','bob123','N',NULL,NULL,'Y',1,3,'images/userdefault.png',0),(4,'charlie','charlie123','N',NULL,NULL,'Y',1,0,'images/userdefault.png',0),(5,'david','david123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(6,'emma','emma123','N',NULL,NULL,'Y',1,0,'images/userdefault.png',0),(7,'frank','frank123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(8,'george','george123','M',NULL,NULL,'N',-1,0,'images/userdefault.png',0),(9,'howard','howard123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(10,'isaac','isaac123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(11,'jordan','jordan123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(12,'kevin','kevin123','N',NULL,NULL,'Y',1,0,'images/userdefault.png',0),(13,'lora','lora123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(14,'maria','maria123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(15,'nolan','nolan123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(16,'oliver','oliver123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(17,'paul','paul123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(18,'queen','queen123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(19,'rose','rose123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(20,'sophie','sophie123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(21,'taylor','taylor123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(22,'ulysses','ulysses123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(23,'versace','versace123','F',NULL,NULL,'N',1,0,'images/userdefault.png',0),(24,'watson','watson123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(25,'xenia','xenia123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(26,'young','young123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0),(27,'zoey','zoey123','N',NULL,NULL,'N',1,0,'images/userdefault.png',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-02 22:03:40
