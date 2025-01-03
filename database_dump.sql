-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: advertising
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `billboards`
--

DROP TABLE IF EXISTS `billboards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billboards` (
  `billboard_id` int unsigned NOT NULL AUTO_INCREMENT,
  `price_per_month` decimal(5,2) unsigned NOT NULL,
  `size` int unsigned NOT NULL,
  `billboard_address` varchar(100) NOT NULL,
  `mount_date` date NOT NULL,
  `quality` decimal(5,2) unsigned NOT NULL,
  `owner_id` int unsigned NOT NULL,
  PRIMARY KEY (`billboard_id`),
  UNIQUE KEY `UID_UNIQUE` (`billboard_id`),
  KEY `bil_own_idx` (`owner_id`),
  CONSTRAINT `bil_own` FOREIGN KEY (`owner_id`) REFERENCES `owners` (`owner_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `check_quality` CHECK ((`quality` between 0 and 100))
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billboards`
--

LOCK TABLES `billboards` WRITE;
/*!40000 ALTER TABLE `billboards` DISABLE KEYS */;
INSERT INTO `billboards` VALUES (1,100.00,200,'г. Омск, ул. Шоссейная, 15','2016-12-06',55.00,1),(2,883.72,25,'г. Омск, ул. Гоголя, 5','2016-06-26',35.29,17),(3,102.90,91,'г. Тольятти, ул. Гагарина, 1','2017-12-30',66.18,8),(4,684.54,61,'г. Казань, ул. Чкалова, 19','2017-12-19',93.92,9),(5,282.35,37,'г. Самара, ул. Садовая, 7','2015-06-30',97.59,7),(6,387.08,27,'г. Нижний Новгород, ул. Солнечная, 8','2020-04-30',17.75,7),(7,872.53,52,'г. Ижевск, ул. Красноармейская, 3','2016-11-25',49.79,7),(8,615.75,88,'г. Уфа, ул. Строителей, 50','2016-02-06',26.63,21),(9,814.68,45,'г. Краснодар, ул. Маяковского, 10','2017-08-01',87.77,14),(10,592.73,75,'г. Уфа, ул. Северная, 42','2015-12-28',39.20,21),(11,354.40,80,'г. Пермь, ул. Мичурина, 9','2016-02-05',12.96,19),(12,188.43,90,'г. Нижний Новгород, ул. Энергетиков, 2','2016-08-13',8.50,7),(13,598.70,54,'г. Москва, ул. Весенняя, 5','2017-12-08',58.27,6),(14,430.57,31,'г. Тольятти, ул. Пролетарская, 31','2015-06-27',24.80,5),(15,810.81,100,'г. Воронеж, ул. Западная, 27','2017-08-01',2.51,18),(16,891.37,73,'г. Москва, ул. Механизаторов, 9','2017-05-22',26.45,19),(17,158.03,42,'г. Ростов-на-Дону, ул. Октябрьская, 39','2015-03-19',23.50,15),(18,404.62,80,'г. Тольятти, ул. Дорожная, 23','2016-04-24',96.95,11),(19,281.02,47,'г. Красноярск, ул. Верхняя, 45','2016-05-29',75.52,6),(20,170.45,85,'г. Омск, ул. Некрасова, 35','2015-01-07',21.78,20),(21,345.11,36,'г. Пермь, ул. Степная, 41','2018-09-26',54.12,4),(22,287.74,48,'г. Уфа, ул. Береговая, 40','2017-06-16',47.44,2),(23,473.67,58,'г. Омск, ул. Лесная, 8','2017-01-08',81.39,3),(24,625.90,81,'г. Ижевск, ул. Вокзальная, 18','2018-07-03',47.51,10),(25,473.34,66,'г. Тюмень, ул. Юбилейная, 14','2020-03-15',66.23,12),(26,660.24,75,'г. Новосибирск, ул. Школьная, 12','2015-04-13',16.11,13),(27,370.60,58,'г. Екатеринбург, ул. Майская, 19','2015-09-15',33.43,16),(28,152.40,50,'г. Нижний Новгород, ул. Чкалова, 20','2024-02-23',50.53,3);
/*!40000 ALTER TABLE `billboards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `counts`
--

DROP TABLE IF EXISTS `counts`;
/*!50001 DROP VIEW IF EXISTS `counts`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `counts` AS SELECT 
 1 AS `renter`,
 1 AS `cnt`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `order_row`
--

DROP TABLE IF EXISTS `order_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_row` (
  `order_row_id` int NOT NULL AUTO_INCREMENT,
  `start_year` int NOT NULL,
  `start_month` int NOT NULL,
  `end_year` int NOT NULL,
  `end_month` int NOT NULL,
  `price` decimal(15,2) NOT NULL,
  `order_id` int unsigned NOT NULL,
  `billboard_id` int unsigned NOT NULL,
  PRIMARY KEY (`order_row_id`),
  UNIQUE KEY `uid_UNIQUE` (`order_row_id`),
  KEY `ord_id_order_idx` (`order_id`),
  KEY `ord_row_bil_idx` (`billboard_id`),
  CONSTRAINT `ord_row_bil` FOREIGN KEY (`billboard_id`) REFERENCES `billboards` (`billboard_id`),
  CONSTRAINT `ord_row_ord` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_row`
--

LOCK TABLES `order_row` WRITE;
/*!40000 ALTER TABLE `order_row` DISABLE KEYS */;
INSERT INTO `order_row` VALUES (1,2018,12,2022,11,13270.00,15,5),(2,2022,9,2023,11,8298.00,12,10),(3,2018,4,2022,10,43993.00,12,9),(4,2021,4,2024,1,19757.00,16,13),(5,2019,4,2022,10,4200.00,17,1),(7,2023,7,2023,10,474.00,18,17),(8,2015,5,2020,12,11420.00,16,20),(9,2018,8,2021,5,29163.00,4,2),(10,2023,7,2023,10,474.00,2,17),(11,2021,10,2022,6,1507.00,3,12),(12,2022,9,2023,11,5419.00,6,6),(13,2023,4,2023,12,3237.00,6,18),(14,2017,12,2021,12,38919.00,10,15),(15,2018,3,2021,3,15501.00,15,14),(16,2023,1,2024,6,4200.00,12,1),(19,2017,11,2020,10,30539.00,20,7),(21,2024,11,2024,12,200.00,32,1),(22,2024,3,2024,11,7953.48,32,2),(23,2024,6,2024,12,2014.18,33,22),(24,2024,5,2024,12,3096.64,33,6),(25,2024,6,2024,12,6107.71,33,7),(26,2024,1,2024,5,4362.65,34,7),(27,2024,1,2024,7,720.30,34,3),(28,2025,7,2026,12,5179.32,35,22),(29,2025,11,2025,12,1369.08,35,4),(30,2025,6,2025,12,4190.90,35,13),(32,2025,7,2025,12,948.18,36,17),(33,2025,11,2025,12,1621.62,36,15),(34,2025,6,2025,12,2415.77,37,21),(35,2025,1,2025,7,4310.25,38,8),(36,2025,2,2025,7,2427.72,38,18),(37,2025,1,2025,6,948.18,38,17),(38,2025,1,2025,11,1131.90,39,3),(39,2025,9,2025,12,1618.48,39,18),(40,2025,1,2025,7,2709.56,39,6),(41,2025,1,2025,5,1438.70,39,22);
/*!40000 ALTER TABLE `order_row` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `order_row_price_changed` AFTER UPDATE ON `order_row` FOR EACH ROW BEGIN

    UPDATE orders SET total_cost = total_cost + new.price WHERE order_id = new.order_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int unsigned NOT NULL AUTO_INCREMENT,
  `registration_date` date NOT NULL,
  `total_cost` decimal(15,2) NOT NULL,
  `renter_id` int unsigned NOT NULL,
  PRIMARY KEY (`order_id`),
  UNIQUE KEY `uid_UNIQUE` (`order_id`),
  KEY `ord_renter_idx` (`renter_id`),
  CONSTRAINT `ord_renter` FOREIGN KEY (`renter_id`) REFERENCES `renters` (`renter_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (2,'2017-08-28',474.00,19),(3,'2018-06-29',1507.00,19),(4,'2018-03-01',29163.00,15),(6,'2016-05-05',8656.00,15),(10,'2015-01-22',38919.00,11),(11,'2017-11-04',1341777.96,11),(12,'2015-07-17',60691.00,9),(15,'2017-01-23',28771.00,8),(16,'2015-03-13',75170.00,9),(17,'2018-08-05',4200.00,2),(18,'2018-04-20',4674.00,9),(20,'2016-12-19',43809.00,8),(21,'2020-03-05',0.00,1),(32,'2024-10-30',8153.48,1),(33,'2024-11-13',11218.53,1),(34,'2024-11-13',5082.95,3),(35,'2024-12-09',14479.92,1),(36,'2024-12-09',2569.80,1),(37,'2024-12-09',2415.77,1),(38,'2024-12-13',7686.15,3),(39,'2024-12-13',6898.64,1);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `owners`
--

DROP TABLE IF EXISTS `owners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `owners` (
  `owner_id` int unsigned NOT NULL AUTO_INCREMENT,
  `last_name` varchar(45) NOT NULL,
  `owner_address` varchar(100) NOT NULL,
  `birth_year` int unsigned NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`owner_id`),
  UNIQUE KEY `uid_UNIQUE` (`owner_id`),
  KEY `own_user_idx` (`user_id`),
  CONSTRAINT `own_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `owners`
--

LOCK TABLES `owners` WRITE;
/*!40000 ALTER TABLE `owners` DISABLE KEYS */;
INSERT INTO `owners` VALUES (1,'Панов','190641, г. Санкт-Петербург, ул. Восточная, 34, оф. 96',1972,'65(352)405-27-98',NULL),(2,'Харитонова','644292, г. Омск, ул. Заречная, 23, оф. 4',1965,'96(71)213-00-29',NULL),(3,'Селезнева','630221, г. Новосибирск, ул. Кооперативная, 20, оф. 98',1981,'436(36)925-42-19',NULL),(4,'Сидоров','620560, г. Екатеринбург, ул. Рабочая, 8, оф. 12',1983,'63(253)355-65-69',NULL),(5,'Малышева','190587, г. Санкт-Петербург, ул. Озерная, 45, оф. 48',1999,'44(0627)295-61-66',NULL),(6,'Александрова','620801, г. Екатеринбург, ул. Сосновая, 32, оф. 53',1980,'203(669)156-71-52',NULL),(7,'Яшин','603979, г. Нижний Новгород, ул. Свердлова, 34, оф. 96',1988,'92(6445)403-67-94',NULL),(8,'Демидов','445337, г. Тольятти, ул. Береговая, 5, оф. 33',1966,'975(445)013-16-67',NULL),(9,'Ильин','350699, г. Краснодар, ул. Зеленая, 31, оф. 11',1964,'943(880)948-64-25',NULL),(10,'Соколова','344044, г. Ростов-на-Дону, ул. Южная, 2, оф. 56',1998,'01(46)066-48-31',NULL),(11,'Дементьева','614658, г. Пермь, ул. Строителей, 18, оф. 41',1979,'00(34)251-19-07',NULL),(12,'Новиков','625124, г. Тюмень, ул. Комарова, 13, оф. 27',1996,'33(4488)496-14-54',NULL),(13,'Астафьева','443510, г. Самара, ул. Коммунистическая, 36, оф. 25',1957,'05(190)152-25-39',NULL),(14,'Петров','644499, г. Омск, ул. Луговая, 41, оф. 16',1954,'637(76)819-52-40',NULL),(15,'Иванов','644400, г. Омск, ул. Школьная, 6, оф. 85',1959,'913(226)325-57-85',NULL),(16,'Березин','445206, г. Тольятти, ул. Куйбышева, 36, оф. 23',1979,'59(661)525-04-90',NULL),(17,'Медведева','125672, г. Москва, ул. Пушкина, 3, оф. 63',1992,'9(55)727-04-26',NULL),(18,'Калачева','644354, г. Омск, ул. Набережная, 11, оф. 98',1988,'1(76)228-38-35',NULL),(19,'Петухов','630415, г. Новосибирск, ул. Кооперативная, 3, оф. 40',1973,'40(423)881-50-86',NULL),(20,'Соколов','190190, г. Санкт-Петербург, ул. Строителей, 6, оф. 57',1997,'13(364)862-69-00',NULL),(21,'Черкасова','450945, г. Уфа, ул. Горького, 38, оф. 23',1994,'44(898)670-73-16',NULL);
/*!40000 ALTER TABLE `owners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `renters`
--

DROP TABLE IF EXISTS `renters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `renters` (
  `renter_id` int unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `renter_address` varchar(100) NOT NULL,
  `business_sphere` varchar(45) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`renter_id`),
  UNIQUE KEY `uid_UNIQUE` (`renter_id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `ren_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `renters`
--

LOCK TABLES `renters` WRITE;
/*!40000 ALTER TABLE `renters` DISABLE KEYS */;
INSERT INTO `renters` VALUES (1,'Иван','Тимофеев','29(66)249-96-41','443945, г. Самара, ул. Луговая, 31, оф. 91','производство',5),(2,'Мирон','Шубин','57(2548)309-08-38','125643, г. Москва, ул. Энергетиков, 10, оф. 69','производство',6),(3,'Александр','Еремин','46(301)589-14-59','614656, г. Пермь, ул. Интернациональная, 26, оф. 17','финансы и страхование',7),(4,'Александр','Шишкин','903(193)771-68-90','443013, г. Самара, ул. Клубная, 23, оф. 29','транспорт',8),(5,'Дмитрий','Поздняков','443(84)600-52-50','344026, г. Ростов-на-Дону, ул. Нагорная, 28, оф. 69','торговля',9),(6,'Антонина','Киселева','6(76)004-87-55','644331, г. Омск, ул. Садовая, 27, оф. 86','производство',10),(7,'Ярослав','Максимов','45(907)912-51-31','630418, г. Новосибирск, ул. Спортивная, 2, оф. 32','торговля',11),(8,'Кирилл','Чижов','92(633)732-21-08','630670, г. Новосибирск, ул. Дружбы, 19, оф. 1','торговля',12),(9,'Мирон','Герасимов','62(92)731-96-70','344810, г. Ростов-на-Дону, ул. Свердлова, 25, оф. 35','туристическая сфера',13),(10,'Юрий','Петров','849(06)381-61-47','420843, г. Казань, ул. Дзержинского, 1, оф. 63','транспорт',14),(11,'Даниил','Гусев','2(855)785-10-47','190532, г. Санкт-Петербург, ул. Чкалова, 45, оф. 27','производство',15),(12,'Дмитрий','Смирнов','575(66)203-12-03','190454, г. Санкт-Петербург, ул. Дзержинского, 46, оф. 100','сельское хозяйство',16),(13,'Платон','Фомин','758(33)116-73-61','445777, г. Тольятти, ул. Карла Маркса, 18, оф. 2','сельское хозяйство',17),(14,'Анастасия','Беляева','3(7984)976-39-93','420609, г. Казань, ул. Рабочая, 24, оф. 23','производство',18),(15,'Арина','Никитина','5(74)080-20-79','454228, г. Челябинск, ул. Садовая, 30, оф. 99','транспорт',19),(16,'Марк','Николаев','31(791)762-63-89','445647, г. Тольятти, ул. Матросова, 13, оф. 79','сельское хозяйство',20),(17,'Дмитрий','Кондрашов','90(334)873-68-67','350404, г. Краснодар, ул. Майская, 47, оф. 16','транспорт',21),(18,'Анастасия','Кулешова','51(7566)243-41-63','350868, г. Краснодар, ул. Парковая, 14, оф. 81','транспорт',22),(19,'Эмилия','Сидорова','0(45)982-62-95','344229, г. Ростов-на-Дону, ул. Гагарина, 6, оф. 64','строительство',23),(20,'Елизавета','Севастьянова','714(0236)093-34-40','660430, г. Красноярск, ул. Рабочая, 12, оф. 6','туристическая сфера',24);
/*!40000 ALTER TABLE `renters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports` (
  `report_id` int unsigned NOT NULL AUTO_INCREMENT,
  `business_sphere` varchar(50) NOT NULL,
  `revenue` int NOT NULL,
  `count` int NOT NULL,
  `year` int NOT NULL,
  `month` int NOT NULL,
  PRIMARY KEY (`report_id`),
  UNIQUE KEY `report_id_UNIQUE` (`report_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports`
--

LOCK TABLES `reports` WRITE;
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
INSERT INTO `reports` VALUES (29,'производство',11219,1,2024,11),(30,'финансы и страхование',5083,1,2024,11);
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule` (
  `schedule_id` int NOT NULL,
  `start_year` int NOT NULL,
  `start_month` int NOT NULL,
  `end_year` int NOT NULL,
  `end_month` int NOT NULL,
  `billboard_id` int unsigned NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `sched_bil_idx` (`billboard_id`),
  CONSTRAINT `sched_bil` FOREIGN KEY (`billboard_id`) REFERENCES `billboards` (`billboard_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES (1,2019,1,2023,8,18),(2,2022,1,2023,2,13),(3,2023,5,2024,1,14),(4,2023,9,2023,10,16),(5,2019,12,2020,3,14),(6,2019,1,2020,6,4),(7,2022,3,2023,1,2),(8,2019,8,2019,12,11),(9,2016,8,2017,4,8),(10,2022,6,2023,8,24),(11,2015,10,2019,9,14),(12,2016,9,2022,3,12),(13,2016,10,2017,4,11),(14,2017,7,2018,11,8),(15,2016,7,2021,4,27),(16,2017,4,2021,7,1),(17,2018,4,2018,11,26),(18,2017,4,2017,9,26),(19,2018,11,2019,10,10),(20,2021,4,2022,2,5),(21,2022,1,2023,8,16),(22,2020,1,2022,4,8),(23,2017,5,2021,12,23),(24,2023,6,2024,1,26),(25,2021,7,2022,3,2),(26,2021,4,2022,2,7),(27,2017,9,2019,7,20),(28,2022,8,2023,11,7),(29,2017,9,2020,12,5),(30,2018,8,2021,8,13),(31,2022,2,2024,1,23),(32,2017,4,2017,9,20),(33,2021,10,2023,7,6),(34,2015,7,2016,9,5),(35,2018,12,2021,5,3),(36,2022,12,2023,6,20),(37,2022,2,2022,3,17),(38,2020,4,2021,1,20),(39,2022,9,2022,10,10),(40,2022,6,2022,9,17),(41,2015,4,2016,12,20),(42,2020,11,2024,1,11),(43,2019,6,2019,8,8),(44,2020,6,2021,5,4),(45,2021,7,2022,2,20),(46,2015,10,2018,3,17),(47,2016,1,2017,5,10),(48,2021,7,2022,12,1),(49,2019,2,2019,4,11),(50,2016,11,2018,12,18),(51,2018,5,2019,3,9),(52,2021,1,2022,12,15),(53,2016,9,2022,8,19),(54,2019,2,2020,1,21),(55,2017,7,2017,7,22),(56,2022,9,2023,7,25);
/*!40000 ALTER TABLE `schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(162) DEFAULT NULL,
  `role` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'man','scrypt:32768:8:1$HZ9rwJ7oLyADUPsg$b935db08bca17bbe6232da61c747446f0c08e44991180906953e0236684e147d6373c6979ed13e92c19b591e73f60a0b058520234d207b05672e0b6c0d7fdb80','manager'),(3,'dir','scrypt:32768:8:1$vNxACHc0lertbwrK$6130c51c1190d8706480821d33842f9a7fd72ad86be3558eb81cb9818628e8d1c383cbfe4d69084bd0b2a223cfb0f2f8b2a1a50f37ae88b7ccb34a38a6ad56cf','director'),(4,'sup','scrypt:32768:8:1$NG9Af9LgpPYy7JX3$bf39202a288ff0b407ed06c8ee86073a42194a41c35562a83343d968f67dde3e5c8cf583f05f8b035d8a2812be2148dd7fe08c687fdf650973a30dee96485ae1','support'),(5,'timofeev','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(6,'shubin','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(7,'eremin','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(8,'shishkin','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(9,'pozdnjakov','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(10,'kiseleva','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(11,'maksimov','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(12,'chizhov','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(13,'gerasimov','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(14,'petrov','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(15,'gusev','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(16,'smirnov','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(17,'fomin','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(18,'beljaeva','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(19,'nikitina','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(20,'nikolaev','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(21,'kondrashov','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(22,'kuleshova','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(23,'sidorova','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter'),(24,'sevast\'janova','scrypt:32768:8:1$Qsn1JPXm7hiKEV81$e5dea89ff8e8977258407d13ab0cdfa24972af9cf663c0eee6a1b33e135a7f43df87b123aec39ea32d000a76ae6299c44283f6a112120c16ed2aeb80a78d3756','renter');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `counts`
--

/*!50001 DROP VIEW IF EXISTS `counts`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `counts` (`renter`,`cnt`) AS select `orders`.`renter_id` AS `renter_id`,count(0) AS `COUNT(*)` from `orders` where (year(`orders`.`registration_date`) = 2020) group by `orders`.`renter_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-02 18:13:29
