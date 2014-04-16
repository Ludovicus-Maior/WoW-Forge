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
  `lastModified` int(11) NOT NULL DEFAULT '0',
  `enqueueTime` int(11) NOT NULL DEFAULT '0',
  UNIQUE KEY `index2` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `realmStatus`
--

LOCK TABLES `realmStatus` WRITE;
/*!40000 ALTER TABLE `realmStatus` DISABLE KEYS */;
INSERT INTO `realmStatus` VALUES ('Aegwynn','aegwynn','EU','de_DE','high',NULL,0,0),('Aerie Peak','aerie-peak','EU','en_GB','medium',NULL,0,0),('Agamaggan','agamaggan','EU','en_GB','medium',NULL,0,0),('Aggra (Português)','aggra-portugues','EU','pt_BR','high',NULL,0,0),('Aggramar','aggramar','EU','en_GB','medium',NULL,0,0),('Ahn\'Qiraj','ahnqiraj','EU','en_GB','medium',NULL,0,0),('Akama','akama','US','en_US','medium',NULL,0,0),('Al\'Akir','alakir','EU','en_GB','medium',NULL,0,0),('Alexstrasza','alexstrasza','EU','de_DE','medium',NULL,0,0),('Alleria','alleria','EU','de_DE','medium',NULL,0,0),('Alonsus','alonsus','EU','en_GB','medium',NULL,0,0),('Altar of Storms','altar-of-storms','US','en_US','medium',NULL,0,0),('Alterac Mountains','alterac-mountains','US','en_US','low',NULL,0,0),('Aman\'Thul','amanthul','EU','de_DE','high',NULL,0,0),('Ambossar','ambossar','EU','de_DE','medium',NULL,0,0),('Anachronos','anachronos','EU','en_GB','medium',NULL,0,0),('Andorhal','andorhal','US','en_US','low',NULL,0,0),('Anetheron','anetheron','EU','de_DE','medium',NULL,0,0),('Antonidas','antonidas','EU','de_DE','high',NULL,0,0),('Anub\'arak','anubarak','EU','de_DE','low',NULL,0,0),('Anvilmar','anvilmar','US','en_US','medium',NULL,0,0),('Arak-arahm','arakarahm','EU','fr_FR','medium',NULL,0,0),('Arathi','arathi','EU','fr_FR','medium',NULL,0,0),('Arathor','arathor','EU','en_GB','medium',NULL,0,0),('Archimonde','archimonde','EU','fr_FR','high',NULL,0,0),('Area 52','area-52','EU','de_DE','medium',NULL,0,0),('Argent Dawn','argent-dawn','EU','en_GB','high',NULL,0,0),('Arthas','arthas','EU','de_DE','medium',NULL,0,0),('Arygos','arygos','EU','de_DE','medium',NULL,0,0),('Ashenvale','ashenvale','EU','ru_RU','high',NULL,0,0),('Aszune','aszune','EU','en_GB','medium',NULL,0,0),('Auchindoun','auchindoun','EU','en_GB','medium',NULL,0,0),('Azgalor','azgalor','US','en_US','medium',NULL,0,0),('Azjol-Nerub','azjolnerub','EU','en_GB','medium',NULL,0,0),('Azralon','azralon','US','pt_BR','high',NULL,0,0),('Azshara','azshara','EU','de_DE','medium',NULL,0,0),('Azuregos','azuregos','EU','ru_RU','high',NULL,0,0),('Azuremyst','azuremyst','EU','en_GB','medium',NULL,0,0),('Baelgun','baelgun','EU','de_DE','medium',NULL,0,0),('Balnazzar','balnazzar','EU','en_GB','low',NULL,0,0),('Barthilas','barthilas','US','en_US','low',NULL,0,0),('Black Dragonflight','black-dragonflight','US','en_US','medium',NULL,0,0),('Blackhand','blackhand','EU','de_DE','high',NULL,0,0),('Blackmoore','blackmoore','EU','de_DE','high',NULL,0,0),('Blackrock','blackrock','EU','de_DE','high',NULL,0,0),('Blackscar','blackscar','EU','ru_RU','high',NULL,0,0),('Blackwater Raiders','blackwater-raiders','US','en_US','low',NULL,0,0),('Blackwing Lair','blackwing-lair','US','en_US','medium',NULL,0,0),('Blade\'s Edge','blades-edge','EU','en_GB','medium',NULL,0,0),('Bladefist','bladefist','EU','en_GB','low',NULL,0,0),('Bleeding Hollow','bleeding-hollow','US','en_US','high',NULL,0,0),('Blood Furnace','blood-furnace','US','en_US','medium',NULL,0,0),('Bloodfeather','bloodfeather','EU','en_GB','low',NULL,0,0),('Bloodhoof','bloodhoof','EU','en_GB','medium',NULL,0,0),('Bloodscalp','bloodscalp','EU','en_GB','medium',NULL,0,0),('Blutkessel','blutkessel','EU','de_DE','low',NULL,0,0),('Bonechewer','bonechewer','US','en_US','medium',NULL,0,0),('Booty Bay','booty-bay','EU','ru_RU','medium',NULL,0,0),('Borean Tundra','borean-tundra','EU','ru_RU','high',NULL,0,0),('Boulderfist','boulderfist','EU','en_GB','medium',NULL,0,0),('Bronze Dragonflight','bronze-dragonflight','EU','en_GB','medium',NULL,0,0),('Bronzebeard','bronzebeard','EU','en_GB','medium',NULL,0,0),('Burning Blade','burning-blade','EU','en_GB','low',NULL,0,0),('Burning Legion','burning-legion','EU','en_GB','high',NULL,0,0),('Burning Steppes','burning-steppes','EU','en_GB','medium',NULL,0,0),('C\'Thun','cthun','EU','es_ES','medium',NULL,0,0),('Caelestrasz','caelestrasz','US','en_US','low',NULL,0,0),('Cairne','cairne','US','en_US','medium',NULL,0,0),('Cenarion Circle','cenarion-circle','US','en_US','medium',NULL,0,0),('Cenarius','cenarius','US','en_US','medium',NULL,0,0),('Chamber of Aspects','chamber-of-aspects','EU','en_GB','high',NULL,0,0),('Chants éternels','chants-eternels','EU','fr_FR','medium',NULL,0,0),('Cho\'gall','chogall','EU','fr_FR','medium',NULL,0,0),('Chromaggus','chromaggus','EU','en_GB','medium',NULL,0,0),('Coilfang','coilfang','US','en_US','medium',NULL,0,0),('Colinas Pardas','colinas-pardas','EU','es_ES','medium',NULL,0,0),('Confrérie du Thorium','confrerie-du-thorium','EU','fr_FR','medium',NULL,0,0),('Conseil des Ombres','conseil-des-ombres','EU','fr_FR','low',NULL,0,0),('Crushridge','crushridge','EU','en_GB','medium',NULL,0,0),('Culte de la Rive noire','culte-de-la-rive-noire','EU','fr_FR','medium',NULL,0,0),('Daggerspine','daggerspine','EU','en_GB','medium',NULL,0,0),('Dalaran','dalaran','EU','fr_FR','medium',NULL,0,0),('Dalvengyr','dalvengyr','EU','de_DE','low',NULL,0,0),('Dark Iron','dark-iron','US','en_US','medium',NULL,0,0),('Darkmoon Faire','darkmoon-faire','EU','en_GB','medium',NULL,0,0),('Darksorrow','darksorrow','EU','en_GB','medium',NULL,0,0),('Darkspear','darkspear','EU','en_GB','medium',NULL,0,0),('Darrowmere','darrowmere','US','en_US','medium',NULL,0,0),('Das Konsortium','das-konsortium','EU','de_DE','low',NULL,0,0),('Das Syndikat','das-syndikat','EU','de_DE','low',NULL,0,0),('Dath\'Remar','dathremar','US','en_US','low',NULL,0,0),('Dawnbringer','dawnbringer','US','en_US','low',NULL,0,0),('Deathguard','deathguard','EU','ru_RU','high',NULL,0,0),('Deathweaver','deathweaver','EU','ru_RU','medium',NULL,0,0),('Deathwing','deathwing','EU','en_GB','low',NULL,0,0),('Deepholm','deepholm','EU','ru_RU','high',NULL,0,0),('Defias Brotherhood','defias-brotherhood','EU','en_GB','high',NULL,0,0),('Demon Soul','demon-soul','US','en_US','medium',NULL,0,0),('Dentarg','dentarg','EU','en_GB','low',NULL,0,0),('Der abyssische Rat','der-abyssische-rat','EU','de_DE','low',NULL,0,0),('Der Mithrilorden','der-mithrilorden','EU','de_DE','medium',NULL,0,0),('Der Rat von Dalaran','der-rat-von-dalaran','EU','de_DE','medium',NULL,0,0),('Destromath','destromath','EU','de_DE','low',NULL,0,0),('Dethecus','dethecus','EU','de_DE','medium',NULL,0,0),('Detheroc','detheroc','US','en_US','medium',NULL,0,0),('Die Aldor','die-aldor','EU','de_DE','medium',NULL,0,0),('Die Arguswacht','die-arguswacht','EU','de_DE','low',NULL,0,0),('Die ewige Wacht','die-ewige-wacht','EU','de_DE','medium',NULL,0,0),('Die Nachtwache','die-nachtwache','EU','de_DE','medium',NULL,0,0),('Die Silberne Hand','die-silberne-hand','EU','de_DE','medium',NULL,0,0),('Die Todeskrallen','die-todeskrallen','EU','de_DE','low',NULL,0,0),('Doomhammer','doomhammer','EU','en_GB','medium',NULL,0,0),('Draenor','draenor','EU','en_GB','high',NULL,0,0),('Dragonblight','dragonblight','EU','en_GB','medium',NULL,0,0),('Dragonmaw','dragonmaw','EU','en_GB','low',NULL,0,0),('Drak\'Tharon','draktharon','US','en_US','medium',NULL,0,0),('Drak\'thul','drakthul','EU','en_GB','medium',NULL,0,0),('Draka','draka','US','en_US','medium',NULL,0,0),('Drakkari','drakkari','US','es_MX','medium',NULL,0,0),('Dreadmaul','dreadmaul','US','en_US','low',NULL,0,0),('Drek\'Thar','drekthar','EU','fr_FR','medium',NULL,0,0),('Drenden','drenden','US','en_US','medium',NULL,0,0),('Dun Modr','dun-modr','EU','es_ES','medium',NULL,0,0),('Dun Morogh','dun-morogh','EU','de_DE','medium',NULL,0,0),('Dunemaul','dunemaul','EU','en_GB','low',NULL,0,0),('Durotan','durotan','EU','de_DE','medium',NULL,0,0),('Duskwood','duskwood','US','en_US','low',NULL,0,0),('Earthen Ring','earthen-ring','EU','en_GB','medium',NULL,0,0),('Echo Isles','echo-isles','US','en_US','medium',NULL,0,0),('Echsenkessel','echsenkessel','EU','de_DE','low',NULL,0,0),('Eitrigg','eitrigg','EU','fr_FR','medium',NULL,0,0),('Eldre\'Thalas','eldrethalas','EU','fr_FR','medium',NULL,0,0),('Elune','elune','EU','fr_FR','medium',NULL,0,0),('Emerald Dream','emerald-dream','EU','en_GB','medium',NULL,0,0),('Emeriss','emeriss','EU','en_GB','medium',NULL,0,0),('Eonar','eonar','EU','en_GB','low',NULL,0,0),('Eredar','eredar','EU','de_DE','high',NULL,0,0),('Eversong','eversong','EU','ru_RU','high',NULL,0,0),('Executus','executus','EU','en_GB','medium',NULL,0,0),('Exodar','exodar','EU','es_ES','medium',NULL,0,0),('Farstriders','farstriders','US','en_US','low',NULL,0,0),('Feathermoon','feathermoon','US','en_US','medium',NULL,0,0),('Fenris','fenris','US','en_US','medium',NULL,0,0),('Festung der Stürme','festung-der-sturme','EU','de_DE','medium',NULL,0,0),('Firetree','firetree','US','en_US','medium',NULL,0,0),('Fizzcrank','fizzcrank','US','en_US','high',NULL,0,0),('Fordragon','fordragon','EU','ru_RU','high',NULL,0,0),('Forscherliga','forscherliga','EU','de_DE','medium',NULL,0,0),('Frostmane','frostmane','EU','en_GB','high',NULL,0,0),('Frostmourne','frostmourne','EU','de_DE','low',NULL,0,0),('Frostwhisper','frostwhisper','EU','en_GB','medium',NULL,0,0),('Frostwolf','frostwolf','EU','de_DE','high',NULL,0,0),('Galakrond','galakrond','EU','ru_RU','high',NULL,0,0),('Gallywix','gallywix','US','pt_BR','high',NULL,0,0),('Garithos','garithos','US','en_US','medium',NULL,0,0),('Garona','garona','EU','fr_FR','medium',NULL,0,0),('Garrosh','garrosh','EU','de_DE','medium',NULL,0,0),('Genjuros','genjuros','EU','en_GB','low',NULL,0,0),('Ghostlands','ghostlands','EU','en_GB','medium',NULL,0,0),('Gilneas','gilneas','EU','de_DE','medium',NULL,0,0),('Gnomeregan','gnomeregan','US','en_US','medium',NULL,0,0),('Goldrinn','goldrinn','EU','ru_RU','high',NULL,0,0),('Gordunni','gordunni','EU','ru_RU','high',NULL,0,0),('Gorefiend','gorefiend','US','en_US','low',NULL,0,0),('Gorgonnash','gorgonnash','EU','de_DE','low',NULL,0,0),('Greymane','greymane','EU','ru_RU','medium',NULL,0,0),('Grim Batol','grim-batol','EU','en_GB','high',NULL,0,0),('Grizzly Hills','grizzly-hills','US','en_US','low',NULL,0,0),('Grom','grom','EU','ru_RU','medium',NULL,0,0),('Gul\'dan','guldan','EU','de_DE','medium',NULL,0,0),('Gundrak','gundrak','US','en_US','low',NULL,0,0),('Gurubashi','gurubashi','US','en_US','medium',NULL,0,0),('Hakkar','hakkar','EU','en_GB','medium',NULL,0,0),('Haomarush','haomarush','EU','en_GB','low',NULL,0,0),('Hellfire','hellfire','EU','en_GB','low',NULL,0,0),('Hellscream','hellscream','EU','en_GB','medium',NULL,0,0),('Howling Fjord','howling-fjord','EU','ru_RU','high',NULL,0,0),('Hydraxis','hydraxis','US','en_US','medium',NULL,0,0),('Hyjal','hyjal','EU','fr_FR','high',NULL,0,0),('Icecrown','icecrown','US','en_US','medium',NULL,0,0),('Illidan','illidan','EU','fr_FR','medium',NULL,0,0),('Jaedenar','jaedenar','EU','en_GB','low',NULL,0,0),('Jubei\'Thos','jubeithos','US','en_US','low',NULL,0,0),('Kael\'thas','kaelthas','EU','fr_FR','medium',NULL,0,0),('Kalecgos','kalecgos','US','en_US','low',NULL,0,0),('Karazhan','karazhan','EU','en_GB','low',NULL,0,0),('Kargath','kargath','EU','de_DE','medium',NULL,0,0),('Kazzak','kazzak','EU','en_GB','high',NULL,0,0),('Kel\'Thuzad','kelthuzad','EU','de_DE','low',NULL,0,0),('Khadgar','khadgar','EU','en_GB','medium',NULL,0,0),('Khaz Modan','khaz-modan','EU','fr_FR','medium',NULL,0,0),('Khaz\'goroth','khazgoroth','EU','de_DE','medium',NULL,0,0),('Kil\'jaeden','kiljaeden','EU','de_DE','low',NULL,0,0),('Kilrogg','kilrogg','EU','en_GB','medium',NULL,0,0),('Kirin Tor','kirin-tor','EU','fr_FR','medium',NULL,0,0),('Kor\'gall','korgall','EU','en_GB','medium',NULL,0,0),('Korgath','korgath','US','en_US','high',NULL,0,0),('Korialstrasz','korialstrasz','US','en_US','low',NULL,0,0),('Krag\'jin','kragjin','EU','de_DE','low',NULL,0,0),('Krasus','krasus','EU','fr_FR','medium',NULL,0,0),('Kul Tiras','kul-tiras','EU','en_GB','medium',NULL,0,0),('Kult der Verdammten','kult-der-verdammten','EU','de_DE','medium',NULL,0,0),('La Croisade écarlate','la-croisade-ecarlate','EU','fr_FR','medium',NULL,0,0),('Laughing Skull','laughing-skull','EU','en_GB','low',NULL,0,0),('Les Clairvoyants','les-clairvoyants','EU','fr_FR','medium',NULL,0,0),('Les Sentinelles','les-sentinelles','EU','fr_FR','medium',NULL,0,0),('Lethon','lethon','US','en_US','medium',NULL,0,0),('Lich King','lich-king','EU','ru_RU','medium',NULL,0,0),('Lightbringer','lightbringer','EU','en_GB','medium',NULL,0,0),('Lightning\'s Blade','lightnings-blade','EU','en_GB','low',NULL,0,0),('Lightninghoof','lightninghoof','US','en_US','low',NULL,0,0),('Llane','llane','US','en_US','medium',NULL,0,0),('Lordaeron','lordaeron','EU','de_DE','medium',NULL,0,0),('Los Errantes','los-errantes','EU','es_ES','low',NULL,0,0),('Lothar','lothar','EU','de_DE','medium',NULL,0,0),('Madmortem','madmortem','EU','de_DE','medium',NULL,0,0),('Madoran','madoran','US','en_US','low',NULL,0,0),('Maelstrom','maelstrom','US','en_US','low',NULL,0,0),('Magtheridon','magtheridon','EU','en_GB','high',NULL,0,0),('Maiev','maiev','US','en_US','high',NULL,0,0),('Mal\'Ganis','malganis','EU','de_DE','medium',NULL,0,0),('Malfurion','malfurion','EU','de_DE','medium',NULL,0,0),('Malorne','malorne','EU','de_DE','low',NULL,0,0),('Malygos','malygos','EU','de_DE','medium',NULL,0,0),('Mannoroth','mannoroth','EU','de_DE','low',NULL,0,0),('Marécage de Zangar','marecage-de-zangar','EU','fr_FR','medium',NULL,0,0),('Mazrigos','mazrigos','EU','en_GB','medium',NULL,0,0),('Medivh','medivh','EU','fr_FR','medium',NULL,0,0),('Minahonda','minahonda','EU','es_ES','medium',NULL,0,0),('Misha','misha','US','en_US','medium',NULL,0,0),('Mok\'Nathal','moknathal','US','en_US','medium',NULL,0,0),('Moon Guard','moon-guard','US','en_US','high',NULL,0,0),('Moonglade','moonglade','EU','en_GB','medium',NULL,0,0),('Moonrunner','moonrunner','US','en_US','low',NULL,0,0),('Mug\'thol','mugthol','EU','de_DE','medium',NULL,0,0),('Muradin','muradin','US','en_US','medium',NULL,0,0),('Nagrand','nagrand','EU','en_GB','low',NULL,0,0),('Nathrezim','nathrezim','EU','de_DE','low',NULL,0,0),('Naxxramas','naxxramas','EU','fr_FR','medium',NULL,0,0),('Nazgrel','nazgrel','US','en_US','medium',NULL,0,0),('Nazjatar','nazjatar','EU','de_DE','low',NULL,0,0),('Nefarian','nefarian','EU','de_DE','low',NULL,0,0),('Nemesis','nemesis','EU','it_IT','medium',NULL,0,0),('Neptulon','neptulon','EU','en_GB','medium',NULL,0,0),('Ner\'zhul','nerzhul','EU','fr_FR','medium',NULL,0,0),('Nera\'thor','nerathor','EU','de_DE','low',NULL,0,0),('Nesingwary','nesingwary','US','en_US','medium',NULL,0,0),('Nethersturm','nethersturm','EU','de_DE','medium',NULL,0,0),('Nordrassil','nordrassil','EU','en_GB','medium',NULL,0,0),('Norgannon','norgannon','EU','de_DE','medium',NULL,0,0),('Nozdormu','nozdormu','EU','de_DE','medium',NULL,0,0),('Onyxia','onyxia','EU','de_DE','medium',NULL,0,0),('Outland','outland','EU','en_GB','high',NULL,0,0),('Perenolde','perenolde','EU','de_DE','medium',NULL,0,0),('Pozzo dell\'Eternità','pozzo-delleternita','EU','it_IT','medium',NULL,0,0),('Proudmoore','proudmoore','EU','de_DE','medium',NULL,0,0),('Quel\'dorei','queldorei','US','en_US','high',NULL,0,0),('Quel\'Thalas','quelthalas','EU','en_GB','medium',NULL,0,0),('Ragnaros','ragnaros','EU','en_GB','high',NULL,0,0),('Rajaxx','rajaxx','EU','de_DE','medium',NULL,0,0),('Rashgarroth','rashgarroth','EU','fr_FR','medium',NULL,0,0),('Ravencrest','ravencrest','EU','en_GB','high',NULL,0,0),('Ravenholdt','ravenholdt','EU','en_GB','low',NULL,0,0),('Razuvious','razuvious','EU','ru_RU','high',NULL,0,0),('Rexxar','rexxar','EU','de_DE','medium',NULL,0,0),('Rivendare','rivendare','US','en_US','medium',NULL,0,0),('Runetotem','runetotem','EU','en_GB','medium',NULL,0,0),('Sanguino','sanguino','EU','es_ES','medium',NULL,0,0),('Sargeras','sargeras','EU','fr_FR','medium',NULL,0,0),('Saurfang','saurfang','EU','en_GB','low',NULL,0,0),('Scarlet Crusade','scarlet-crusade','US','en_US','low',NULL,0,0),('Scarshield Legion','scarshield-legion','EU','en_GB','low',NULL,0,0),('Scilla','scilla','US','en_US','low',NULL,0,0),('Sen\'jin','senjin','EU','de_DE','medium',NULL,0,0),('Sentinels','sentinels','US','en_US','low',NULL,0,0),('Shadow Council','shadow-council','US','en_US','low',NULL,0,0),('Shadowmoon','shadowmoon','US','en_US','low',NULL,0,0),('Shadowsong','shadowsong','EU','en_GB','medium',NULL,0,0),('Shandris','shandris','US','en_US','medium',NULL,0,0),('Shattered Halls','shattered-halls','EU','en_GB','medium',NULL,0,0),('Shattered Hand','shattered-hand','EU','en_GB','medium',NULL,0,0),('Shattrath','shattrath','EU','de_DE','medium',NULL,0,0),('Shen\'dralar','shendralar','EU','es_ES','medium',NULL,0,0),('Shu\'halo','shuhalo','US','en_US','high',NULL,0,0),('Silver Hand','silver-hand','US','en_US','low',NULL,0,0),('Silvermoon','silvermoon','EU','en_GB','high',NULL,0,0),('Sinstralis','sinstralis','EU','fr_FR','medium',NULL,0,0),('Sisters of Elune','sisters-of-elune','US','en_US','low',NULL,0,0),('Skullcrusher','skullcrusher','EU','en_GB','low',NULL,0,0),('Skywall','skywall','US','en_US','medium',NULL,0,0),('Smolderthorn','smolderthorn','US','en_US','medium',NULL,0,0),('Soulflayer','soulflayer','EU','ru_RU','high',NULL,0,0),('Spinebreaker','spinebreaker','EU','en_GB','low',NULL,0,0),('Spirestone','spirestone','US','en_US','medium',NULL,0,0),('Sporeggar','sporeggar','EU','en_GB','low',NULL,0,0),('Staghelm','staghelm','US','en_US','low',NULL,0,0),('Steamwheedle Cartel','steamwheedle-cartel','EU','en_GB','low',NULL,0,0),('Stonemaul','stonemaul','US','en_US','high',NULL,0,0),('Stormrage','stormrage','EU','en_GB','medium',NULL,0,0),('Stormreaver','stormreaver','EU','en_GB','medium',NULL,0,0),('Stormscale','stormscale','EU','en_GB','high',NULL,0,0),('Sunstrider','sunstrider','EU','en_GB','medium',NULL,0,0),('Suramar','suramar','EU','fr_FR','medium',NULL,0,0),('Sylvanas','sylvanas','EU','en_GB','high',NULL,0,0),('Taerar','taerar','EU','de_DE','low',NULL,0,0),('Talnivarr','talnivarr','EU','en_GB','medium',NULL,0,0),('Tanaris','tanaris','US','en_US','low',NULL,0,0),('Tarren Mill','tarren-mill','EU','en_GB','high',NULL,0,0),('Teldrassil','teldrassil','EU','de_DE','medium',NULL,0,0),('Temple noir','temple-noir','EU','fr_FR','medium',NULL,0,0),('Terenas','terenas','EU','en_GB','medium',NULL,0,0),('Terokkar','terokkar','EU','en_GB','medium',NULL,0,0),('Terrordar','terrordar','EU','de_DE','medium',NULL,0,0),('Thaurissan','thaurissan','US','en_US','low',NULL,0,0),('The Forgotten Coast','the-forgotten-coast','US','en_US','medium',NULL,0,0),('The Maelstrom','the-maelstrom','EU','en_GB','high',NULL,0,0),('The Scryers','the-scryers','US','en_US','low',NULL,0,0),('The Sha\'tar','the-shatar','EU','en_GB','low',NULL,0,0),('The Underbog','the-underbog','US','en_US','medium',NULL,0,0),('The Venture Co','the-venture-co','EU','en_GB','low',NULL,0,0),('Theradras','theradras','EU','de_DE','medium',NULL,0,0),('Thermaplugg','thermaplugg','EU','ru_RU','medium',NULL,0,0),('Thorium Brotherhood','thorium-brotherhood','US','en_US','low',NULL,0,0),('Thrall','thrall','EU','de_DE','high',NULL,0,0),('Throk\'Feroth','throkferoth','EU','fr_FR','medium',NULL,0,0),('Thunderhorn','thunderhorn','EU','en_GB','medium',NULL,0,0),('Thunderlord','thunderlord','US','en_US','low',NULL,0,0),('Tichondrius','tichondrius','EU','de_DE','medium',NULL,0,0),('Tirion','tirion','EU','de_DE','medium',NULL,0,0),('Todeswache','todeswache','EU','de_DE','medium',NULL,0,0),('Tol Barad','tol-barad','US','pt_BR','medium',NULL,0,0),('Tortheldrin','tortheldrin','US','en_US','medium',NULL,0,0),('Trollbane','trollbane','EU','en_GB','medium',NULL,0,0),('Turalyon','turalyon','EU','en_GB','medium',NULL,0,0),('Twilight\'s Hammer','twilights-hammer','EU','en_GB','medium',NULL,0,0),('Twisting Nether','twisting-nether','EU','en_GB','high',NULL,0,0),('Tyrande','tyrande','EU','es_ES','medium',NULL,0,0),('Uldaman','uldaman','EU','fr_FR','medium',NULL,0,0),('Ulduar','ulduar','EU','de_DE','medium',NULL,0,0),('Uldum','uldum','EU','es_ES','medium',NULL,0,0),('Un\'Goro','ungoro','EU','de_DE','medium',NULL,0,0),('Undermine','undermine','US','en_US','medium',NULL,0,0),('Ursin','ursin','US','en_US','low',NULL,0,0),('Uther','uther','US','en_US','low',NULL,0,0),('Varimathras','varimathras','EU','fr_FR','medium',NULL,0,0),('Vashj','vashj','EU','en_GB','low',NULL,0,0),('Vek\'lor','veklor','EU','de_DE','medium',NULL,0,0),('Vek\'nilash','veknilash','EU','en_GB','medium',NULL,0,0),('Velen','velen','US','en_US','medium',NULL,0,0),('Vol\'jin','voljin','EU','fr_FR','medium',NULL,0,0),('Warsong','warsong','US','en_US','medium',NULL,0,0),('Whisperwind','whisperwind','US','en_US','high',NULL,0,0),('Wildhammer','wildhammer','EU','en_GB','medium',NULL,0,0),('Windrunner','windrunner','US','en_US','medium',NULL,0,0),('Winterhoof','winterhoof','US','en_US','medium',NULL,0,1397573945),('Wrathbringer','wrathbringer','EU','de_DE','low',NULL,0,0),('Wyrmrest Accord','wyrmrest-accord','US','en_US','high',NULL,0,1397573838),('Xavius','xavius','EU','en_GB','low',NULL,0,0),('Ysera','ysera','EU','de_DE','medium',NULL,0,0),('Ysondre','ysondre','EU','fr_FR','high',NULL,0,0),('Zangarmarsh','zangarmarsh','US','en_US','medium',NULL,0,1397573835),('Zenedar','zenedar','EU','en_GB','medium',NULL,0,0),('Zirkel des Cenarius','zirkel-des-cenarius','EU','de_DE','medium',NULL,0,0),('Zul\'jin','zuljin','EU','es_ES','medium',NULL,0,0),('Zuluhed','zuluhed','EU','de_DE','low',NULL,0,0);
/*!40000 ALTER TABLE `realmStatus` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-16  7:08:58
