CREATE DATABASE  IF NOT EXISTS `Warcraft` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `Warcraft`;
-- MySQL dump 10.13  Distrib 5.6.13, for osx10.6 (i386)
--
-- Host: 127.0.0.1    Database: Warcraft
-- ------------------------------------------------------
-- Server version	5.6.15

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
-- Table structure for table `equippable`
--

DROP TABLE IF EXISTS `equippable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equippable` (
  `id` decimal(16,5) unsigned NOT NULL,
  `armor` int(10) unsigned zerofill NOT NULL DEFAULT '0000000000',
  `baseArmor` int(10) unsigned zerofill NOT NULL DEFAULT '0000000000',
  `hasSockets` tinyint(1) unsigned zerofill NOT NULL DEFAULT '0',
  `maxDurability` smallint(5) unsigned zerofill NOT NULL DEFAULT '00000',
  `statAgility` mediumint(9) NOT NULL DEFAULT '0',
  `statStrength` mediumint(9) NOT NULL DEFAULT '0',
  `statIntellect` mediumint(9) NOT NULL DEFAULT '0',
  `statSpirit` mediumint(9) NOT NULL DEFAULT '0',
  `statStamina` mediumint(9) NOT NULL DEFAULT '0',
  `sockets` varchar(8) DEFAULT NULL,
  `socketBonus` varchar(24) DEFAULT NULL,
  `damageMin` smallint(5) unsigned zerofill NOT NULL DEFAULT '00000',
  `damageMax` int(10) unsigned zerofill NOT NULL DEFAULT '0000000000',
  `dps` float unsigned zerofill DEFAULT '000000000000',
  `weaponSpeed` float unsigned zerofill DEFAULT '000000000000',
  `statCritical` mediumint(9) NOT NULL DEFAULT '0',
  `statHaste` mediumint(9) NOT NULL DEFAULT '0',
  `statMastery` mediumint(9) NOT NULL DEFAULT '0',
  `statResilience` mediumint(9) NOT NULL DEFAULT '0',
  `statHit` mediumint(9) NOT NULL DEFAULT '0',
  `statDodge` mediumint(9) NOT NULL DEFAULT '0',
  `statParry` mediumint(9) NOT NULL DEFAULT '0',
  `statSpellPower` mediumint(9) NOT NULL DEFAULT '0',
  `statPVPPower` mediumint(9) NOT NULL DEFAULT '0',
  `statExpertise` mediumint(9) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item` (
  `id` decimal(16,5) unsigned NOT NULL,
  `icon` varchar(64) NOT NULL,
  `buyPrice` int(10) unsigned zerofill NOT NULL,
  `itemClass` tinyint(3) unsigned zerofill NOT NULL,
  `itemSubClass` tinyint(3) unsigned zerofill NOT NULL,
  `inventoryType` tinyint(3) unsigned zerofill NOT NULL,
  `isAuctionable` tinyint(1) unsigned zerofill NOT NULL,
  `itemBind` tinyint(3) unsigned zerofill NOT NULL,
  `itemLevel` smallint(5) unsigned zerofill NOT NULL,
  `maxCount` tinyint(3) unsigned zerofill NOT NULL,
  `minFactionId` smallint(5) unsigned zerofill NOT NULL,
  `minReputation` tinyint(3) unsigned zerofill NOT NULL,
  `quality` tinyint(3) unsigned zerofill NOT NULL,
  `requiredLevel` tinyint(3) unsigned zerofill NOT NULL,
  `requiredSkill` smallint(5) unsigned zerofill NOT NULL,
  `requiredSkillRank` int(10) unsigned zerofill NOT NULL,
  `sellPrice` int(10) unsigned zerofill NOT NULL,
  `stackable` smallint(5) unsigned zerofill NOT NULL,
  `displayInfoId` int(10) unsigned zerofill NOT NULL,
  `equippable` tinyint(1) unsigned zerofill NOT NULL,
  `disenchantingSkillRank` smallint(5) unsigned zerofill NOT NULL DEFAULT '00000',
  `allowableClasses` set('1','2','3','4','5','6','7','8','9','10','11') DEFAULT NULL,
  `allowableRaces` set('1','2','3','4','5','6','7','8','9','10','11','22','25','26') DEFAULT NULL,
  `requiredAbility` smallint(5) unsigned zerofill NOT NULL DEFAULT '00000',
  `boundZone` smallint(5) unsigned zerofill NOT NULL DEFAULT '00000',
  `randomEnchant` tinyint(1) unsigned zerofill NOT NULL DEFAULT '0',
  `itemSource` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `item_name`
--

DROP TABLE IF EXISTS `item_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_name` (
  `id` decimal(16,5) unsigned NOT NULL,
  `name` varchar(64) CHARACTER SET utf8 NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `nameDescription` varchar(45) DEFAULT NULL,
  `nameDescriptionColor` char(6) DEFAULT '000000',
  `language` char(5) NOT NULL DEFAULT 'en_US',
  UNIQUE KEY `Id+Lang` (`id`,`language`),
  CONSTRAINT `id` FOREIGN KEY (`id`) REFERENCES `item` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `realmCharacter`
--

DROP TABLE IF EXISTS `realmCharacter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `realmCharacter` (
  `name` varchar(24) NOT NULL,
  `realm` varchar(24) DEFAULT NULL,
  `guild` varchar(24) DEFAULT NULL,
  `class` tinyint(3) unsigned DEFAULT NULL,
  `level` tinyint(3) unsigned DEFAULT NULL,
  `race` tinyint(3) unsigned DEFAULT NULL,
  `gender` tinyint(3) unsigned DEFAULT NULL,
  `specName` varchar(16) DEFAULT NULL,
  `lastModified` bigint(20) unsigned DEFAULT NULL,
  `head_id` int(11) DEFAULT NULL,
  `head_suffix` int(11) DEFAULT NULL,
  `head_seed` int(11) DEFAULT NULL,
  `head_enchant` int(11) DEFAULT NULL,
  `neck_id` int(11) DEFAULT NULL,
  `neck_suffix` int(11) DEFAULT NULL,
  `neck_seed` int(11) DEFAULT NULL,
  `neck_enchant` int(11) DEFAULT NULL,
  `shoulder_id` int(11) DEFAULT NULL,
  `shoulder_suffix` int(11) DEFAULT NULL,
  `shoulder_seed` int(11) DEFAULT NULL,
  `shoulder_enchant` int(11) DEFAULT NULL,
  `back_id` int(11) DEFAULT NULL,
  `back_suffix` int(11) DEFAULT NULL,
  `back_seed` int(11) DEFAULT NULL,
  `back_enchant` int(11) DEFAULT NULL,
  `chest_id` int(11) DEFAULT NULL,
  `chest_suffix` int(11) DEFAULT NULL,
  `chest_seed` int(11) DEFAULT NULL,
  `chest_enchant` int(11) DEFAULT NULL,
  `tabard_id` int(11) DEFAULT NULL,
  `tabard_suffix` int(11) DEFAULT NULL,
  `tabard_seed` int(11) DEFAULT NULL,
  `tabard_enchant` int(11) DEFAULT NULL,
  `wrist_id` int(11) DEFAULT NULL,
  `wrist_suffix` int(11) DEFAULT NULL,
  `wrist_seed` int(11) DEFAULT NULL,
  `wrist_enchant` int(11) DEFAULT NULL,
  `hands_id` int(11) DEFAULT NULL,
  `hands_suffix` int(11) DEFAULT NULL,
  `hands_seed` int(11) DEFAULT NULL,
  `hands_enchant` int(11) DEFAULT NULL,
  `waist_id` int(11) DEFAULT NULL,
  `waist_suffix` int(11) DEFAULT NULL,
  `waist_seed` int(11) DEFAULT NULL,
  `waist_enchant` int(11) DEFAULT NULL,
  `legs_id` int(11) DEFAULT NULL,
  `legs_suffix` int(11) DEFAULT NULL,
  `legs_seed` int(11) DEFAULT NULL,
  `legs_enchant` int(11) DEFAULT NULL,
  `feet_id` int(11) DEFAULT NULL,
  `feet_suffix` int(11) DEFAULT NULL,
  `feet_seed` int(11) DEFAULT NULL,
  `feet_enchant` int(11) DEFAULT NULL,
  `finger1_id` int(11) DEFAULT NULL,
  `finger1_suffix` int(11) DEFAULT NULL,
  `finger1_seed` int(11) DEFAULT NULL,
  `finger1_enchant` int(11) DEFAULT NULL,
  `finger2_id` int(11) DEFAULT NULL,
  `finger2_suffix` int(11) DEFAULT NULL,
  `finger2_seed` int(11) DEFAULT NULL,
  `finger2_enchant` int(11) DEFAULT NULL,
  `trinket1_id` int(11) DEFAULT NULL,
  `trinket1_suffix` int(11) DEFAULT NULL,
  `trinket1_seed` int(11) DEFAULT NULL,
  `trinket1_enchant` int(11) DEFAULT NULL,
  `trinket2_id` int(11) DEFAULT NULL,
  `trinket2_suffix` int(11) DEFAULT NULL,
  `trinket2_seed` int(11) DEFAULT NULL,
  `trinket2_enchant` int(11) DEFAULT NULL,
  `mainHand_id` int(11) DEFAULT NULL,
  `mainHand_suffix` int(11) DEFAULT NULL,
  `mainHand_seed` int(11) DEFAULT NULL,
  `mainHand_enchant` int(11) DEFAULT NULL,
  `offHand_id` int(11) DEFAULT NULL,
  `offHand_suffix` int(11) DEFAULT NULL,
  `offHand_seed` int(11) DEFAULT NULL,
  `offHand_enchant` int(11) DEFAULT NULL,
  `guildRealm` varchar(24) DEFAULT NULL,
  UNIQUE KEY `index1` (`name`,`realm`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `realmGuilds`
--

DROP TABLE IF EXISTS `realmGuilds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `realmGuilds` (
  `side` tinyint(4) NOT NULL,
  `realm` varchar(24) NOT NULL,
  `name` varchar(45) NOT NULL,
  `achievementPoints` int(11) NOT NULL,
  `lastScanned` int(10) unsigned zerofill NOT NULL,
  UNIQUE KEY `index1` (`realm`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `realmStatus`
--

DROP TABLE IF EXISTS `realmStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `realmStatus` (
  `name` varchar(24) NOT NULL,
  `slug` varchar(24) NOT NULL,
  `region` char(2) NOT NULL,
  `locale` varchar(8) NOT NULL,
  `population` varchar(12) NOT NULL,
  `siblings` varchar(45) DEFAULT NULL,
  UNIQUE KEY `index2` (`name`)
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

-- Dump completed on 2014-02-11  6:40:46
