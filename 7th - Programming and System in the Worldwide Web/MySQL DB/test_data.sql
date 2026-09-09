USE kata_strofh;

-- Test entry to create a new rescuer
CALL CreateNewRescuer('john_dwoe', 'securepassword123', 38.04816300, 23.79188600);
CALL CreateNewRescuer('Sjanec_doe', 'securepassworcd456',38.04616300, 23.79643000);
CALL CreateNewRescuer('ssmitDh', 'securepassword789', 38.04459300, 23.78110400);

CALL CreateNewRescuer('VasilisPapa', '3424r44', 38.04659300, 23.78110400);


-- Test entry to create a new citizen
CALL CreateNewCitizen('jane_doce', 'securepassword456', 'Jane', 'Doe', '123-456-7890', 38.04161800, 23.78762700);
CALL CreateNewCitizen('john_dose', 'securepassword123', 'John', 'Doe', '987-654-3210', 38.03932500, 23.79466300);
CALL CreateNewCitizen('alixce_smith', 'securepassword789', 'Alice', 'Smith', '555-555-5555', 38.04173700, 23.79206500);
CALL CreateNewCitizen('Marianamits', '3424r44', 'Mariana', 'Mitsena', '555-555-5555', 38.04273700, 23.79306500);

-- Test entry to create a new admin
CALL CreateNewAdmin('admin_user', 'adminpassword');
CALL CreateNewAdmin('admin_muser2', 'adminpassword2');
CALL CreateNewAdmin('admin_usegayr3', 'adminpassword3');

-- Insert test data into Category table
INSERT INTO Category (CategoryName) VALUES
('Food'),
('Medicine'),
('Clothing');

-- Insert test data into Items table
INSERT INTO Items (CategoryID, Name, DetailName, DetailValue) VALUES
(1, 'Rice', 'volume', '1kg bag of rice'),
(1, 'Bread', 'quantity', '1 loaf of bread'),
(2, 'Aspirin', 'Pack of', '4'),
(2, 'Band-Aid', 'Pack of', '10'),
(3, 'Shirt', 'Size', 'M'),
(3, 'Jacket', 'Size', 'L'),
(3, 'Blanket', 'Size', 'Queen');


-- Insert test data into Warehouse table
INSERT INTO Warehouse (ItemID, Quantity) VALUES
(1, 100), -- 100 units of Rice
(2, 50),  -- 50 units of Bread
(3, 70),  -- 70 units of Aspirin
(4, 33),  -- 33 units of Band-Aid
(5, 33),  -- 33 units of Shirt
(6, 696969), -- 696969 units of Jacket
(7, 696969); -- 696969 units of Jacket

-- Insert sample data into VehicleItems table
INSERT INTO VehicleItems (VehicleID, ItemID, Quantity) VALUES
(1, 1, 10), -- Vehicle 1 carrying 10 units of Item 1
(1, 2, 5),  -- Vehicle 1 carrying 5 units of Item 2
(2, 3, 7),  -- Vehicle 2 carrying 7 units of Item 3
(2, 1, 15), -- Vehicle 2 carrying 15 units of Item 1
(3, 2, 20), -- Vehicle 3 carrying 20 units of Item 2
(3, 3, 10), -- Vehicle 3 carrying 10 units of Item 3
(4, 1, 30), -- Vehicle 4 carrying 30 units of Item 1
(4, 2, 25), -- Vehicle 4 carrying 25 units of Item 2
(4, 3, 15); -- Vehicle 4 carrying 15 units of Item 3



-- Insert sample data into Requests table
INSERT INTO Requests (CitizenID,NumberofPeople,Status, DateCreated) VALUES 
(1,1, 'PENDING', NOW()), -- John Doe requesting Rice
(2,1, 'PENDING', NOW()),  -- Jane Doe requesting Aspirin
(3,1, 'PENDING', NOW()),  -- Alice Smith requesting Blanket
(1,1, 'PENDING', NOW()),  -- John Doe requesting Aspirin
(2,1, 'PENDING', NOW()),  -- Jane Doe requesting Blanket
(3,1, 'PENDING', NOW()),  -- Alice Smith requesting Rice
(4,1, 'PENDING', NOW());  -- Alice Smith requesting Rice



INSERT INTO RequestItems (RequestID, ItemID, Quantity) VALUES
(1, 1, 10), -- John Doe requesting 10 units of Rice
(2, 2, 5),  -- Jane Doe requesting 5 units of Aspirin
(3, 3, 3),  -- Alice Smith requesting 3 units of Blanket
(4, 2, 7),  -- John Doe requesting 7 units of Aspirin
(5, 3, 10), -- Jane Doe requesting 10 units of Blanket
(6, 1, 15), -- Alice Smith requesting 15 units of Rice
(7, 1, 15); -- Alice Smith requesting 15 units of Rice


-- Insert sample data into Offers table
INSERT INTO Offers (CitizenID, Status, DateCreated) VALUES 
(1, 'PENDING', NOW()), -- John Doe offering Rice
(2, 'PENDING', NOW()),  -- Jane Doe offering Aspirin
(3, 'PENDING', NOW()),  -- Alice Smith offering Blanket
(1, 'PENDING', NOW()), -- John Doe offering Blanket
(2, 'PENDING', NOW()),  -- Jane Doe offering Rice
(3, 'PENDING', NOW()),  -- Alice Smith offering Aspirin
(4, 'PENDING', NOW());  -- Alice Smith offering Aspirin

INSERT INTO OfferItems (OfferID, ItemID, Quantity) VALUES
(1, 1, 20), -- John Doe offering 20 units of Rice
(2, 2, 10),  -- Jane Doe offering 10 units of Aspirin
(3, 3, 5),  -- Alice Smith offering 5 units of Blanket
(4, 3, 7),  -- John Doe offering 7 units of Blanket
(5, 1, 15), -- Jane Doe offering 15 units of Rice
(6, 2, 20), -- Alice Smith offering 20 units of Aspirin
(7, 2, 20); -- Alice Smith offering 20 units of Aspirin


-- Insert sample data into Announcements table
INSERT INTO Announcements (AdminID, DateCreated) VALUES 
(1, '2023-01-01 10:00:00'), -- Admin 1 created an announcement on January 1, 2023
(2, '2023-02-15 14:30:00'); -- Admin 2 created an announcement on February 15, 2023

-- Insert initial base location
INSERT INTO BaseLocation (BaseName, Latitude, Longitude)
VALUES ('Main Base', 38.04035147, 23.78224611);

-- Insert sample data into AnnouncementItems table
INSERT INTO AnnouncementItems (AnnouncementID, ItemID, Quantity) VALUES
(1, 1, 10), -- Announcement 1 includes 10 units of Item 1
(1, 2, 50), -- Announcement 1 includes 50 units of Item 2
(2, 3, 75), -- Announcement 2 includes 75 units of Item 3
(2, 1, 150); -- Announcement 2 includes 150 units of Item 1

-- Drop temporary tables
DROP TABLE IF EXISTS tempitems;

-- Test entry for CreateNewRequest procedure

CALL CreateNewRequest(
    2,      
    10,               -- Citizen ID
    'Rice,Blanket', -- Comma-separated item names
    '888,30'             -- Corresponding quantities
);

-- Test entry for CreateNewOffer procedure
CALL CreateNewOffer(
    2,                      -- Citizen ID
    'Rice,Blanket', -- Comma-separated item names
    '69,3000'           -- Corresponding quantities
);

-- Test entry for CreateAnnouncement procedure
CALL CreateNewAnnouncement(1, 
    'Rice,Aspirin,Blanket', -- Comma-separated item names
    '100,50,70'             -- Corresponding quantities
);




-- Example of requests being assigned to rescuers
CALL AssignRequest(1, 1); -- Assigning first request to rescuer1
CALL AssignRequest(2, 2); -- Assigning second request to rescuer1
CALL AssignRequest(3, 1); -- Assigning third request to rescuer1


-- Example of offers being assigned to rescuers
CALL AssignOffer(1, 1); -- Assigning first offer to rescuer1
CALL AssignOffer(2, 1); -- Assigning second offer to rescuer1
CALL AssignOffer(3, 2); -- Assigning third offer to rescuer1
CALL AssignOffer(7, 3); -- Assigning fourth offer to rescuer1


CALL CancelRequest(89);

CALL CancelOffer(77);

CALL FinishRequest(2);

CALL FinishOffer(3);


-- Example usage:
-- CALL UnloadVehicleItems(2);



DELIMITER //

CREATE PROCEDURE GenerateEntries(IN num_entries INT)
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE base_date DATE DEFAULT '2024-05-14';  -- Start date 4 months before max date (14/09/2024)
    DECLARE max_date DATE DEFAULT '2024-09-14';   -- Max date is 14/09/2024
    
    -- Loop through the number of entries specified
    WHILE i <= num_entries DO
        -- Exit the loop if base_date exceeds max_date
        IF base_date > max_date THEN
            SET i = num_entries + 1;  -- Exit the loop by setting i beyond num_entries
        ELSE
            -- Insert Request
            INSERT INTO Requests (CitizenID, NumberofPeople, Status, DateCreated, DateAssignedVehicle, DateFinished, RescuerID)
            VALUES (1,1,  'FINISHED', base_date, base_date + INTERVAL 1 DAY, base_date + INTERVAL 2 DAY, 1);
            
            -- Insert corresponding RequestItem
            INSERT INTO RequestItems (RequestID, ItemID, Quantity)
            VALUES (LAST_INSERT_ID(), 1, 1);
            
            -- Insert Offer
            INSERT INTO Offers (CitizenID, Status, DateCreated, DateAssignedVehicle, DateFinished, RescuerID)
            VALUES (1, 'FINISHED', base_date, base_date + INTERVAL 1 DAY, base_date + INTERVAL 2 DAY, 1);
            
            -- Insert corresponding OfferItem
            INSERT INTO OfferItems (OfferID, ItemID, Quantity)
            VALUES (LAST_INSERT_ID(), 1, 1);

            -- Increment the base date by 1 day
            SET base_date = base_date + INTERVAL 1 DAY;

            -- Increment the loop counter
            SET i = i + 1;
        END IF;
    END WHILE;
    
END //

DELIMITER ;

CALL GenerateEntries(50);

-- example usage
-- CALL LoadVehicleFromOffer(86, 4);

-- example usage
-- CALL UnloadVehicleOnRequestCompletion(4, 89);

-- CALL LoadFromWarehouseToVehicle(
--     4,                      -- RescuerID
--     'Rice,Blanket',          -- Comma-separated item names
--     '1,3'                   -- Corresponding quantities
-- );

-- CALL UnloadFromVehicleToWarehouse(
--     2,                      -- RescuerID
--     'Rice,Blanket',          -- Comma-separated item names
--     '69,3'                   -- Corresponding quantities
-- );
