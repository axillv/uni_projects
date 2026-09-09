CREATE DATABASE IF NOT EXISTS kata_strofh DEFAULT CHARACTER SET = 'utf8mb4' DEFAULT COLLATE = 'utf8mb4_unicode_ci';
USE kata_strofh;
-- Users Table
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Role ENUM('Administrator', 'Rescuer', 'Citizen') NOT NULL,
    UNIQUE INDEX (Username)
) ENGINE = InnoDB;
-- Administrator Table
CREATE TABLE Administrator (
    UserID INT,
    AdminID INT AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
) ENGINE = InnoDB;
-- Rescuer Table
CREATE TABLE Rescuer (
    UserID INT,
    RescuerID INT AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
) ENGINE = InnoDB;
-- Citizen Table
CREATE TABLE Citizen (
    UserID INT,
    CitizenID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Surname VARCHAR(100) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Latitude DECIMAL(10, 8) NOT NULL,
    Longitude DECIMAL(11, 8) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
) ENGINE = InnoDB;
-- Category Table
CREATE TABLE Category (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(50) NOT NULL
) ENGINE = InnoDB;
-- Items Table
CREATE TABLE Items (
    ItemID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryID INT NOT NULL,
    Name VARCHAR(100) NOT NULL,
    DetailName VARCHAR(100),
    DetailValue VARCHAR(100),
    UNIQUE INDEX (Name),
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID) ON DELETE CASCADE
) ENGINE = InnoDB;
-- Warehouse Table
CREATE TABLE Warehouse (
    ItemID INT,
    Quantity INT NOT NULL CHECK (Quantity >= 0),
    UNIQUE (ItemID), 
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID) ON DELETE CASCADE
) ENGINE = InnoDB;

ALTER TABLE Warehouse ADD UNIQUE KEY uq_warehouse_item (ItemID);

-- Requests Table
CREATE TABLE Requests (
    RequestID INT AUTO_INCREMENT PRIMARY KEY,
    CitizenID INT,
    Status ENUM('PENDING', 'INPROGRESS', 'FINISHED') NOT NULL DEFAULT 'PENDING',
    NumberofPeople INT NOT NULL,
    DateCreated DATETIME NOT NULL,
    DateAssignedVehicle DATETIME,
    DateFinished DATETIME,
    RescuerID INT,
    FOREIGN KEY (CitizenID) REFERENCES Citizen(CitizenID) ON DELETE CASCADE,
    FOREIGN KEY (RescuerID) REFERENCES Rescuer(RescuerID) ON DELETE CASCADE,
    INDEX (CitizenID),
    INDEX (RescuerID),
    INDEX (DateCreated),
    INDEX (DateAssignedVehicle)
) ENGINE = InnoDB;
-- RequestItems Table to handle multiple items per request
CREATE TABLE RequestItems (
    RequestItemID INT AUTO_INCREMENT PRIMARY KEY,
    RequestID INT,
    ItemID INT,
    Quantity INT NOT NULL CHECK (Quantity >= 0),
    FOREIGN KEY (RequestID) REFERENCES Requests(RequestID) ON DELETE CASCADE,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID) ON DELETE CASCADE,
    INDEX (RequestID),
    INDEX (ItemID),
    UNIQUE KEY uq_request_item (RequestID, ItemID)
) ENGINE = InnoDB;



-- Offers Table
CREATE TABLE Offers (
    OfferID INT AUTO_INCREMENT PRIMARY KEY,
    CitizenID INT,
    Status ENUM('PENDING', 'INPROGRESS', 'FINISHED') NOT NULL DEFAULT 'PENDING',
    DateCreated DATETIME NOT NULL,
    DateAssignedVehicle DATETIME,
    DateFinished DATETIME,
    RescuerID INT,
    FOREIGN KEY (CitizenID) REFERENCES Citizen(CitizenID) ON DELETE CASCADE,
    FOREIGN KEY (RescuerID) REFERENCES Rescuer(RescuerID) ON DELETE CASCADE,
    INDEX (CitizenID),
    INDEX (RescuerID),
    INDEX (DateCreated),
    INDEX (DateAssignedVehicle)
) ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS BaseLocation (
    BaseID INT AUTO_INCREMENT PRIMARY KEY,
    BaseName VARCHAR(100) NOT NULL,
    Latitude DECIMAL(10, 8) NOT NULL,
    Longitude DECIMAL(11, 8) NOT NULL
);
-- OfferItems Table to handle multiple items per offer
CREATE TABLE OfferItems (
    OfferItemID INT AUTO_INCREMENT PRIMARY KEY,
    OfferID INT,
    ItemID INT,
    Quantity INT NOT NULL CHECK (Quantity >= 0),
    FOREIGN KEY (OfferID) REFERENCES Offers(OfferID) ON DELETE CASCADE,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID) ON DELETE CASCADE,
    INDEX (OfferID),
    INDEX (ItemID),
    UNIQUE KEY uq_request_item (OfferID, ItemID)
) ENGINE = InnoDB;
-- Vehicles Table
CREATE TABLE Vehicles (
    VehicleID INT AUTO_INCREMENT PRIMARY KEY,
    RescuerID INT,
    Latitude DECIMAL(10, 8) NOT NULL,
    Longitude DECIMAL(11, 8) NOT NULL,
    FOREIGN KEY (RescuerID) REFERENCES Rescuer(RescuerID) ON DELETE CASCADE,
    INDEX (RescuerID)
) ENGINE = InnoDB;
-- VehicleItems Table to handle multiple items per vehicle
CREATE TABLE VehicleItems (
    VehicleItemID INT AUTO_INCREMENT PRIMARY KEY,
    VehicleID INT,
    ItemID INT,
    Quantity INT NOT NULL CHECK (Quantity >= 0),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID) ON DELETE CASCADE,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID) ON DELETE CASCADE,
    UNIQUE KEY uq_vehicle_item (VehicleID, ItemID),
    INDEX (VehicleID),
    INDEX (ItemID)
) ENGINE = InnoDB;
-- Announcements Table
CREATE TABLE Announcements (
    AnnouncementID INT AUTO_INCREMENT PRIMARY KEY,
    AdminID INT,
    DateCreated DATETIME NOT NULL,
    FOREIGN KEY (AdminID) REFERENCES Administrator(AdminID) ON DELETE CASCADE,
    INDEX (AdminID),
    INDEX (DateCreated)
) ENGINE = InnoDB;
-- AnnouncementItems Table to handle multiple items per announcement
CREATE TABLE AnnouncementItems (
    AnnouncementItemID INT AUTO_INCREMENT PRIMARY KEY,
    AnnouncementID INT,
    ItemID INT,
    Quantity INT NOT NULL CHECK (Quantity >= 0),
    FOREIGN KEY (AnnouncementID) REFERENCES Announcements(AnnouncementID) ON DELETE CASCADE,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID) ON DELETE CASCADE,
    INDEX (AnnouncementID),
    INDEX (ItemID),
    UNIQUE KEY uq_announcement_item (AnnouncementID, ItemID)
) ENGINE = InnoDB;
-- DROP DATABASE kata_strofh;