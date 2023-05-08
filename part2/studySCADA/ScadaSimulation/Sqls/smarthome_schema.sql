CREATE TABLE `miniproject`.`smarthomesensor` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Home_Id` VARCHAR(20) NOT NULL,
  `Room_Name` VARCHAR(20) NOT NULL,
  `Sensing_Datetime` DATETIME NOT NULL,
  `Temp` FLOAT NULL,
  `Humid` FLOAT NULL,
  PRIMARY KEY (`id`));
