CREATE DATABASE  IF NOT EXISTS `Warcraft` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `Warcraft`;
-- MySQL dump 10.13  Distrib 5.6.13, for osx10.6 (i386)
--
-- Host: forge-warehouse.cwlbtoxvbcev.us-west-1.rds.amazonaws.com    Database: Warcraft
-- ------------------------------------------------------
-- Server version	5.6.13-log

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
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item` (
  `id` int(10) unsigned NOT NULL,
  `subId` smallint(6) NOT NULL DEFAULT '0',
  `allowableClasses` set('1','2','3','4','5','6','7','8','9','10','11') DEFAULT NULL,
  `allowableRaces` set('1','2','3','4','5','6','7','8','9','10','11','22','25','26') DEFAULT NULL,
  `boundZone` smallint(5) unsigned NOT NULL DEFAULT '0',
  `buyPrice` int(10) unsigned NOT NULL,
  `disenchantingSkillRank` smallint(5) unsigned NOT NULL DEFAULT '0',
  `displayInfoId` int(10) unsigned NOT NULL,
  `equippable` tinyint(1) unsigned NOT NULL,
  `icon` varchar(64) NOT NULL,
  `inventoryType` tinyint(3) unsigned NOT NULL,
  `isAuctionable` tinyint(1) unsigned NOT NULL,
  `itemBind` tinyint(3) unsigned NOT NULL,
  `itemClass` tinyint(3) unsigned NOT NULL,
  `itemLevel` smallint(5) unsigned NOT NULL,
  `itemSource` varchar(45) DEFAULT NULL,
  `itemSubClass` tinyint(3) unsigned NOT NULL,
  `maxCount` tinyint(3) unsigned NOT NULL,
  `minFactionId` smallint(5) unsigned NOT NULL,
  `minReputation` tinyint(3) unsigned NOT NULL,
  `quality` tinyint(3) unsigned NOT NULL,
  `randomEnchant` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `requiredAbility` smallint(5) unsigned NOT NULL DEFAULT '0',
  `requiredLevel` tinyint(3) unsigned NOT NULL,
  `requiredSkillRank` int(10) unsigned NOT NULL,
  `requiredSkill` smallint(5) unsigned NOT NULL,
  `sellPrice` int(10) unsigned NOT NULL,
  `stackable` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`,`subId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `equippable`
--

DROP TABLE IF EXISTS `equippable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equippable` (
  `id` int(10) unsigned NOT NULL,
  `subId` smallint(6) NOT NULL DEFAULT '0',
  `armor` int(10) unsigned NOT NULL DEFAULT '0',
  `baseArmor` int(10) unsigned NOT NULL DEFAULT '0',
  `hasSockets` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `sockets` varchar(8) DEFAULT NULL,
  `socketBonus` varchar(24) DEFAULT NULL,
  `maxDurability` smallint(5) unsigned NOT NULL DEFAULT '0',
  `damageMin` smallint(5) unsigned NOT NULL DEFAULT '0',
  `damageMax` int(10) unsigned NOT NULL DEFAULT '0',
  `weaponSpeed` float unsigned DEFAULT '0',
  `dps` float unsigned DEFAULT '0',
  `statAgility` mediumint(9) NOT NULL DEFAULT '0',
  `statCritical` mediumint(9) NOT NULL DEFAULT '0',
  `statDodge` mediumint(9) NOT NULL DEFAULT '0',
  `statExpertise` mediumint(9) NOT NULL DEFAULT '0',
  `statHaste` mediumint(9) NOT NULL DEFAULT '0',
  `statHit` mediumint(9) NOT NULL DEFAULT '0',
  `statIntellect` mediumint(9) NOT NULL DEFAULT '0',
  `statMastery` mediumint(9) NOT NULL DEFAULT '0',
  `statPVPPower` mediumint(9) NOT NULL DEFAULT '0',
  `statParry` mediumint(9) NOT NULL DEFAULT '0',
  `statResilience` mediumint(9) NOT NULL DEFAULT '0',
  `statSpellPower` mediumint(9) NOT NULL DEFAULT '0',
  `statSpirit` mediumint(9) NOT NULL DEFAULT '0',
  `statStamina` mediumint(9) NOT NULL DEFAULT '0',
  `statStrength` mediumint(9) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`,`subId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `item_name`
--

DROP TABLE IF EXISTS `item_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_name` (
  `id` int(10) unsigned NOT NULL,
  `subId` smallint(6) NOT NULL DEFAULT '0',
  `name` varchar(64) CHARACTER SET utf8 NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `nameDescription` varchar(45) DEFAULT NULL,
  `nameDescriptionColor` char(6) DEFAULT '0',
  `language` char(5) NOT NULL DEFAULT 'en_US',
  PRIMARY KEY (`id`,`subId`,`language`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-26 12:24:26
