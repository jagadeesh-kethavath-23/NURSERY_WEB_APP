SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema nursery_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema nursery_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `nursery_db` ;
USE `nursery_db` ;


-- -----------------------------------------------------
-- Table `nursery_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nursery_db`.`users` (
  `name` VARCHAR(45) NOT NULL,
  `user_id` VARCHAR(20) NOT NULL,
  `gender` VARCHAR(10) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  `address` MEDIUMTEXT NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `mydb`.`account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nursery_db`.`account` (
  `balance` INT NOT NULL,
  `user_id` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  CONSTRAINT `u_s_e_r_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `nursery_db`.`users` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`transactions`
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `nursery_db`.`warehouse`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nursery_db`.`warehouse` (
  `product_id` VARCHAR(45) NOT NULL,
  `ware_house_address` VARCHAR(45) NOT NULL,
  `quantity` INT NOT NULL,
  `user_id` VARCHAR(20) NOT NULL,
  `date_added` DATE NOT NULL,
  PRIMARY KEY (`product_id`, `ware_house_address`, `date_added`,`quantity`),
  INDEX `user_id4_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `user_id4`
    FOREIGN KEY (`user_id`)
    REFERENCES `nursery_db`.`users` (`user_id`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `nursery_db`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nursery_db`.`products` (
  `product_id` VARCHAR(45) NOT NULL,
  `product_quantity` INT NOT NULL,
  `product_name` VARCHAR(45) NOT NULL,
  `product_type` VARCHAR(45) NOT NULL,
  `cost` INT NOT NULL,
  PRIMARY KEY (`product_id`),
  UNIQUE INDEX `plant_id_UNIQUE` (`product_id` ASC) VISIBLE,
  CONSTRAINT `product_id5`
    FOREIGN KEY (`product_id`)
    REFERENCES `nursery_db`.`warehouse` (`product_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `nursery_db`.`cart`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nursery_db`.`cart` (
  `user_id` VARCHAR(20) NOT NULL,
  `product_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`, `product_id`),
  INDEX `product_id2` (`product_id` ASC) VISIBLE,
  CONSTRAINT `product_id2`
    FOREIGN KEY (`product_id`)
    REFERENCES `nursery_db`.`products` (`product_id`),
  CONSTRAINT `user_id2`
    FOREIGN KEY (`user_id`)
    REFERENCES `nursery_db`.`users` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `nursery_db`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nursery_db`.`orders` (
  `user_id` VARCHAR(20) NOT NULL,
  `product_id` VARCHAR(45) NOT NULL,
  `status` VARCHAR(10) NOT NULL,
  `order_quantity` INT NOT NULL,
  `ordered_date` DATE NOT NULL,
  `amount` INT NOT NULL,
  `received_date` DATE NOT NULL,
  PRIMARY KEY (`user_id`, `product_id`, `ordered_date`, `order_quantity`),
  INDEX `product_id1_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `product_id1`
    FOREIGN KEY (`product_id`)
    REFERENCES `nursery_db`.`products` (`product_id`)
    ON UPDATE CASCADE,
  CONSTRAINT `user_id1`
    FOREIGN KEY (`user_id`)
    REFERENCES `nursery_db`.`users` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `nursery_db`.`cards`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nursery_db`.`cards` (
  `card_number` VARCHAR(12) NOT NULL,
  `cvv` INT NOT NULL,
  `user_id` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`card_number`),
  UNIQUE INDEX `card_number_UNIQUE` (`card_number` ASC) VISIBLE,
  INDEX `uer_i_d_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `uer_i_d`
    FOREIGN KEY (`user_id`)
    REFERENCES `nursery_db`.`users` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `nursery_db`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nursery_db`.`reviews` (
  `product_id` VARCHAR(45) NOT NULL,
  `user_id` VARCHAR(20) NOT NULL,
  `rating` INT NOT NULL,
  `discription` MEDIUMTEXT NOT NULL,
  PRIMARY KEY (`product_id`, `user_id`),
  INDEX `user_id3_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `product_id3`
    FOREIGN KEY (`product_id`)
    REFERENCES `nursery_db`.`products` (`product_id`),
  CONSTRAINT `user_id3`
    FOREIGN KEY (`user_id`)
    REFERENCES `nursery_db`.`users` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
