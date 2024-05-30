-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: quytrinhsx
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `giaidoansanxuat`
--

DROP TABLE IF EXISTS `giaidoansanxuat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giaidoansanxuat` (
  `ID_GiaiDoan` int NOT NULL AUTO_INCREMENT,
  `ID_QuyTrinhSanXuat` int DEFAULT NULL,
  `ID_BangChuyen` int DEFAULT NULL,
  `SoNhanCongHienTai` int DEFAULT NULL,
  `SoNhanCongNangSuatLonNhat` int DEFAULT NULL,
  `ThoiGianXuLyToiThieu` int DEFAULT NULL,
  `la_giai_doan_cuoi` tinyint DEFAULT NULL,
  `ThuTu` int DEFAULT NULL,
  PRIMARY KEY (`ID_GiaiDoan`),
  KEY `ID_BangChuyen_idx` (`ID_BangChuyen`),
  KEY `ID_QuyTrinhSanXuat_idx` (`ID_QuyTrinhSanXuat`),
  CONSTRAINT `BangChuyen` FOREIGN KEY (`ID_BangChuyen`) REFERENCES `bangchuyen` (`ID_BangChuyen`),
  CONSTRAINT `QuyTrinhSanXuat` FOREIGN KEY (`ID_QuyTrinhSanXuat`) REFERENCES `quytrinhsanxuat` (`ID_QuyTrinhSanXuat`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giaidoansanxuat`
--

LOCK TABLES `giaidoansanxuat` WRITE;
/*!40000 ALTER TABLE `giaidoansanxuat` DISABLE KEYS */;
INSERT INTO `giaidoansanxuat` VALUES (1,1,1,0,10,10,0,1),(2,1,2,0,12,15,0,2),(3,1,3,20,14,20,1,3),(4,2,4,0,10,25,0,1),(5,2,5,0,15,20,0,2),(6,2,6,14,20,30,1,3),(7,3,7,0,10,30,0,1),(8,3,8,0,13,40,1,2);
/*!40000 ALTER TABLE `giaidoansanxuat` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-31  2:46:36
