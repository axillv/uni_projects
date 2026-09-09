USE kata_strofh;

-- Procedure to create a new request 
DELIMITER //
CREATE PROCEDURE CreateNewRequest(
    IN citizen_id INT,
    IN NumberofPeople INT,
    IN item_names VARCHAR(1000),  -- Comma-separated item names
    IN quantities VARCHAR(1000)   -- Comma-separated quantities
)
BEGIN
    DECLARE item_name VARCHAR(255);
    DECLARE quantity INT;
    DECLARE total_items INT;
    DECLARE request_id INT;
    DECLARE i INT DEFAULT 1;
    DECLARE found_item_id INT;
    DECLARE item_count INT;
    

    -- Calculate the total number of items from the comma-separated string
    SET total_items = LENGTH(item_names) - LENGTH(REPLACE(item_names, ',', '')) + 1;

    -- Initialize item count
    SET item_count = 0;

    -- Loop through the delimited item names and quantities to validate existence
    WHILE i <= total_items DO
        -- Extract the current item name
        SET item_name = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(item_names, ',', i), ',', -1));

        -- Extract the current quantity and convert it to an integer
        SET quantity = CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(quantities, ',', i), ',', -1)) AS UNSIGNED);

        -- Validate the existence of the item and get its ID
        SELECT COUNT(*) INTO found_item_id
        FROM Items
        WHERE Name = item_name
        LIMIT 1;

        -- Ensure the item exists and the quantity is valid
        IF found_item_id > 0 AND quantity > 0 THEN
            -- Increment the item count for each valid item
            SET item_count = item_count + 1;
        END IF;

        SET i = i + 1;
    END WHILE;

    -- Check if the number of valid items matches the total number of items
    IF item_count <> total_items THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'One or more items do not exist in the database or invalid quantities provided', MYSQL_ERRNO = 4001;
    END IF;

    -- Insert a new request with the current date
    INSERT INTO Requests (CitizenID,NumberofPeople,Status,DateCreated)
    VALUES (citizen_id,NumberofPeople,'PENDING',NOW());

    -- Retrieve the new request ID
    SET request_id = LAST_INSERT_ID();

    -- Reset the loop counter
    SET i = 1;

    -- Loop again to insert each item into RequestItems
    WHILE i <= total_items DO
        -- Extract the current item name
        SET item_name = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(item_names, ',', i), ',', -1));

        -- Extract the current quantity and convert it to an integer
        SET quantity = CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(quantities, ',', i), ',', -1)) AS UNSIGNED);

        -- Get the ItemID for the current item name
        SELECT ItemID INTO found_item_id
        FROM Items
        WHERE Name = item_name
        LIMIT 1;

        -- Insert the item into RequestItems
        IF found_item_id > 0 AND quantity > 0 THEN
            INSERT INTO RequestItems (RequestID, ItemID, Quantity)
            VALUES (request_id, found_item_id, quantity)
            ON DUPLICATE KEY UPDATE Quantity = Quantity + VALUES(Quantity);
        END IF;

        SET i = i + 1;
    END WHILE;
END//

DELIMITER ;


-- Procedure to create a new offer
DELIMITER //
CREATE PROCEDURE CreateNewOffer(
    IN citizen_id INT,
    IN item_names VARCHAR(1000),  -- Comma-separated item names
    IN quantities VARCHAR(1000)   -- Comma-separated quantities
)
BEGIN
    DECLARE item_name VARCHAR(255);
    DECLARE quantity INT;
    DECLARE total_items INT;
    DECLARE offer_id INT;
    DECLARE i INT DEFAULT 1;
    DECLARE found_item_id INT;
    DECLARE item_count INT;

    -- Calculate the total number of items from the comma-separated string
    SET total_items = LENGTH(item_names) - LENGTH(REPLACE(item_names, ',', '')) + 1;

    -- Initialize item count
    SET item_count = 0;

    -- Loop through the delimited item names and quantities to validate existence
    WHILE i <= total_items DO
        -- Extract the current item name
        SET item_name = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(item_names, ',', i), ',', -1));

        -- Extract the current quantity and convert it to an integer
        SET quantity = CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(quantities, ',', i), ',', -1)) AS UNSIGNED);

        -- Validate the existence of the item and get its ID
        SELECT COUNT(*) INTO found_item_id
        FROM Items
        WHERE Name = item_name
        LIMIT 1;

        -- Ensure the item exists and the quantity is valid
        IF found_item_id > 0 AND quantity > 0 THEN
            -- Increment the item count for each valid item
            SET item_count = item_count + 1;
        END IF;

        SET i = i + 1;
    END WHILE;

    -- Check if the number of valid items matches the total number of items
    IF item_count <> total_items THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'One or more items do not exist in the database or invalid quantities provided', MYSQL_ERRNO = 4001;
    END IF;

    -- Insert a new offer with the current date
    INSERT INTO Offers (CitizenID,Status,DateCreated)
    VALUES (citizen_id,'PENDING',NOW());

    -- Retrieve the new offer ID
    SET offer_id = LAST_INSERT_ID();

    -- Reset the loop counter
    SET i = 1;

    -- Loop again to insert each item into OfferItems
    WHILE i <= total_items DO
        -- Extract the current item name
        SET item_name = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(item_names, ',', i), ',', -1));

        -- Extract the current quantity and convert it to an integer
        SET quantity = CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(quantities, ',', i), ',', -1)) AS UNSIGNED);

        -- Get the ItemID for the current item name
        SELECT ItemID INTO found_item_id
        FROM Items
        WHERE Name = item_name
        LIMIT 1;

        -- Insert the item into OfferItems
        IF found_item_id > 0 AND quantity > 0 THEN
            INSERT INTO OfferItems (OfferID, ItemID, Quantity)
            VALUES (offer_id, found_item_id, quantity)
            ON DUPLICATE KEY UPDATE Quantity = Quantity + VALUES(Quantity);
        END IF;

        SET i = i + 1;
    END WHILE;
END//
DELIMITER ;


-- Procedure to create a new announcement
-- Procedure to create a new announcement
DELIMITER //
CREATE PROCEDURE CreateNewAnnouncement(
    IN admin_id INT,
    IN item_names VARCHAR(1000),  -- Comma-separated item names
    IN quantities VARCHAR(1000)   -- Comma-separated quantities
)
BEGIN
    DECLARE item_name VARCHAR(255);
    DECLARE quantity INT;
    DECLARE total_items INT;
    DECLARE announcement_id INT;
    DECLARE i INT DEFAULT 1;
    DECLARE found_item_id INT;
    DECLARE item_count INT;

    -- Calculate the total number of items from the comma-separated string
    SET total_items = LENGTH(item_names) - LENGTH(REPLACE(item_names, ',', '')) + 1;

    -- Initialize item count
    SET item_count = 0;

    -- Loop through the delimited item names and quantities to validate existence
    WHILE i <= total_items DO
        -- Extract the current item name
        SET item_name = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(item_names, ',', i), ',', -1));

        -- Extract the current quantity and convert it to an integer
        SET quantity = CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(quantities, ',', i), ',', -1)) AS UNSIGNED);

        -- Validate the existence of the item and get its ID
        SELECT COUNT(*) INTO found_item_id
        FROM Items
        WHERE Name = item_name
        LIMIT 1;

        -- Ensure the item exists and the quantity is valid
        IF found_item_id > 0 AND quantity > 0 THEN
            -- Increment the item count for each valid item
            SET item_count = item_count + 1;
        END IF;

        SET i = i + 1;
    END WHILE;

    -- Check if the number of valid items matches the total number of items
    IF item_count <> total_items THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'One or more items do not exist in the database or invalid quantities provided', MYSQL_ERRNO = 4001;
    END IF;

    -- Insert a new announcement with the current date
    INSERT INTO Announcements (AdminID, DateCreated)
    VALUES (admin_id, NOW());

    -- Retrieve the new announcement ID
    SET announcement_id = LAST_INSERT_ID();

    -- Reset the loop counter
    SET i = 1;

    -- Loop again to insert each item into AnnouncementItems
    WHILE i <= total_items DO
        -- Extract the current item name
        SET item_name = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(item_names, ',', i), ',', -1));

        -- Extract the current quantity and convert it to an integer
        SET quantity = CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(quantities, ',', i), ',', -1)) AS UNSIGNED);

        -- Get the ItemID for the current item name
        SELECT ItemID INTO found_item_id
        FROM Items
        WHERE Name = item_name
        LIMIT 1;

        -- Insert the item into AnnouncementItems
        IF found_item_id > 0 AND quantity > 0 THEN
            INSERT INTO AnnouncementItems (AnnouncementID, ItemID, Quantity)
            VALUES (announcement_id, found_item_id, quantity);
        END IF;

        SET i = i + 1;
    END WHILE;
END//

DELIMITER ;


-- Procedure to create a new rescuer
DELIMITER //
CREATE PROCEDURE CreateNewRescuer(
    IN username VARCHAR(255),
    IN password VARCHAR(255),
    IN latitude DOUBLE,
    IN longitude DOUBLE
)
BEGIN
    DECLARE user_id INT;
    DECLARE rescuer_id INT;

    -- Insert into user table
    INSERT INTO Users (username, password ,Role ) VALUES (username, password, 'Rescuer');

    -- Retrieve the new user ID
    SET user_id = LAST_INSERT_ID();

    -- Insert into Rescuer table
    INSERT INTO Rescuer (UserID) VALUES (user_id);

    -- Retrieve the new Rescuer ID
    SET rescuer_id = LAST_INSERT_ID();

    -- Insert into Vehicles table
    INSERT INTO Vehicles (RescuerID, Latitude, Longitude) VALUES (rescuer_id, latitude, longitude);

END//
DELIMITER ;


-- Procedure to create a new citizen
DELIMITER //
CREATE PROCEDURE CreateNewCitizen(
    IN username VARCHAR(255),
    IN password VARCHAR(255),
    IN first_name VARCHAR(255),
    IN last_name VARCHAR(255),
    IN phone_number VARCHAR(255),
    IN latitude DOUBLE,
    IN longitude DOUBLE
)
BEGIN
    DECLARE user_id INT;

    -- Insert into user table
    INSERT INTO Users (username, password ,Role) VALUES (username, password, 'Citizen');

    -- Retrieve the new user ID
    SET user_id = LAST_INSERT_ID();

    -- Insert into Citizen table
    INSERT INTO Citizen (UserID, Name, Surname, Phone, Latitude, Longitude)
    VALUES (user_id, first_name, last_name, phone_number, latitude, longitude);
END//
DELIMITER ;


-- Procedure to create a new admin
DELIMITER //
CREATE PROCEDURE CreateNewAdmin(
    IN username VARCHAR(255),
    IN password VARCHAR(255)
)
BEGIN
    DECLARE user_id INT;

    -- Insert into user table
    INSERT INTO Users (username, password) VALUES (username, password);

    -- Retrieve the new user ID
    SET user_id = LAST_INSERT_ID();

    -- Insert into Admin table
    INSERT INTO Administrator (UserID) VALUES (user_id);
END//
DELIMITER ;


-- Procedure to assign a request to a rescuer
DELIMITER //
CREATE PROCEDURE AssignRequest (
    IN p_RequestID INT,
    IN p_RescuerID INT
)
BEGIN
    UPDATE Requests SET RescuerID = p_RescuerID, Status = 'INPROGRESS', DateAssignedVehicle = NOW() 
    WHERE RequestID = p_RequestID;
END//
DELIMITER ;

-- Procedure to assign an offer to a rescuer
DELIMITER //
CREATE PROCEDURE AssignOffer (
    IN p_OfferID INT,
    IN p_RescuerID INT
)
BEGIN
    UPDATE Offers SET RescuerID = p_RescuerID, Status = 'INPROGRESS', DateAssignedVehicle = NOW() 
    WHERE OfferID = p_OfferID;
END//
DELIMITER ;

-- Procedure to Cancel a Request
DELIMITER //
CREATE PROCEDURE CancelRequest (
    IN reqID INT
)
BEGIN
    UPDATE Requests
    SET Status = 'PENDING', DateAssignedVehicle = NULL, RescuerID = NULL
    WHERE RequestID = reqID;
END//

DELIMITER ;

-- Procedure to Cancel an Offer
DELIMITER //
CREATE PROCEDURE CancelOffer (
    IN p_offerID INT
)
BEGIN
    -- Diagnostic message
    SELECT 'CancelOffer called with OfferID =', p_offerID;
    -- Update statement
    UPDATE Offers
    SET Status = 'PENDING', DateAssignedVehicle = NULL, RescuerID = NULL
    WHERE OfferID = p_offerID;
END//
DELIMITER ;

-- Procedure to Mark a Request as Finished
DELIMITER //
CREATE PROCEDURE FinishRequest (
    IN reqID INT
)
BEGIN
    UPDATE Requests
    SET Status = 'FINISHED' , DateFinished = NOW()
    WHERE RequestID = reqID;
END//
DELIMITER ;

-- Procedure to Mark an Offer as Finished
DELIMITER //
CREATE PROCEDURE FinishOffer (
    IN p_offerID INT
)
BEGIN
    UPDATE Offers
    SET Status = 'FINISHED',  DateFinished = NOW()
    WHERE OfferID = p_offerID;
END//
DELIMITER ;

-- Trigger to prevent rescuer assignment if they have reached the task limit for requests
DELIMITER //
CREATE TRIGGER BeforeAssignRescuerToRequest
BEFORE UPDATE ON Requests
FOR EACH ROW
BEGIN
    DECLARE taskCount INT;

    IF NEW.RescuerID IS NOT NULL AND NEW.Status != 'FINISHED' THEN
        SELECT COUNT(*) INTO taskCount
        FROM (
            SELECT RescuerID FROM Requests WHERE RescuerID = NEW.RescuerID AND Status = 'INPROGRESS'
            UNION ALL
            SELECT RescuerID FROM Offers WHERE RescuerID = NEW.RescuerID AND Status = 'INPROGRESS'
        ) AS RescuerTasks;

        IF taskCount >= 4 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Rescuer has reached the maximum number of tasks.', MYSQL_ERRNO = 6002;
        END IF;
    END IF;
END//
DELIMITER ;

-- Trigger to prevent rescuer assignment if they have reached the task limit for offers
DELIMITER //

CREATE TRIGGER BeforeAssignRescuerToOffer
BEFORE UPDATE ON Offers
FOR EACH ROW
BEGIN
    DECLARE taskCount INT;

    IF NEW.RescuerID IS NOT NULL AND NEW.Status != 'FINISHED' THEN
        SELECT COUNT(*) INTO taskCount
        FROM (
            SELECT RescuerID FROM Requests WHERE RescuerID = NEW.RescuerID AND Status = 'INPROGRESS'
            UNION ALL
            SELECT RescuerID FROM Offers WHERE RescuerID = NEW.RescuerID AND Status = 'INPROGRESS'
        ) AS RescuerTasks;

        IF taskCount >= 4 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Rescuer has reached the maximum number of tasks.', MYSQL_ERRNO = 6002;
        END IF;
    END IF;
END//
DELIMITER ;

-- Trigger to prevent reassignment of in-progress requests
DELIMITER //
CREATE TRIGGER PreventReassignInProgressRequest
BEFORE UPDATE ON Requests
FOR EACH ROW
BEGIN
    IF OLD.Status = 'INPROGRESS' AND OLD.RescuerID IS NOT NULL AND OLD.RescuerID != NEW.RescuerID THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'In-progress requests cannot be reassigned.', MYSQL_ERRNO = 5003;
    END IF;
END//
DELIMITER ;

-- Trigger to prevent reassignment of in-progress offers
DELIMITER //
CREATE TRIGGER PreventReassignInProgressOffer
BEFORE UPDATE ON Offers
FOR EACH ROW
BEGIN
    IF OLD.Status = 'INPROGRESS' AND OLD.RescuerID IS NOT NULL AND OLD.RescuerID != NEW.RescuerID THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'In-progress offers cannot be reassigned.', MYSQL_ERRNO = 5004;
    END IF;
END//
DELIMITER ;

-- Trigger to prevent pending requests from being marked as finished
DELIMITER //
CREATE TRIGGER PreventPendingRequestFinished
BEFORE UPDATE ON Requests
FOR EACH ROW
BEGIN
    IF OLD.Status = 'PENDING' AND NEW.Status = 'FINISHED' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Pending requests cannot be marked as finished.', MYSQL_ERRNO = 5005;
    END IF;
END//
DELIMITER ;

-- Trigger to prevent pending offers from being marked as finished
DELIMITER //
CREATE TRIGGER PreventPendingOfferFinished
BEFORE UPDATE ON Offers
FOR EACH ROW
BEGIN
    IF OLD.Status = 'PENDING' AND NEW.Status = 'FINISHED' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Pending offers cannot be marked as finished.', MYSQL_ERRNO = 5006;
    END IF;
END//
DELIMITER ;


-- Trigger to prevent finished requests from being altered
DELIMITER //
CREATE TRIGGER PreventFinishedRequestAlteration
BEFORE UPDATE ON Requests
FOR EACH ROW
BEGIN
    IF OLD.Status = 'FINISHED' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Finished requests cannot be altered.', MYSQL_ERRNO = 5007;  
    END IF;
END//
DELIMITER ;

-- Trigger to prevent finished offers from being altered

DELIMITER //
CREATE TRIGGER PreventFinishedOfferAlteration
BEFORE UPDATE ON Offers
FOR EACH ROW
BEGIN
    IF OLD.Status = 'FINISHED' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Finished offers cannot be altered.', MYSQL_ERRNO = 5008;
    END IF;
END//
DELIMITER ;


--
DELIMITER //

CREATE PROCEDURE UnloadFromVehicleToWarehouse(
    IN p_RescuerID INT,
    IN p_ItemIDs VARCHAR(1000),  -- Comma-separated item IDs
    IN p_Quantities VARCHAR(1000)  -- Comma-separated quantities
)
BEGIN
    DECLARE v_VehicleID INT;
    DECLARE v_ItemID INT;
    DECLARE v_Quantity INT;
    DECLARE v_VehicleQuantity INT;
    DECLARE total_items INT;
    DECLARE i INT DEFAULT 1;
    DECLARE v_ErrorMessage VARCHAR(255);  -- Variable to hold the error message
    
    -- Calculate total number of items from the comma-separated string
    SET total_items = LENGTH(p_ItemIDs) - LENGTH(REPLACE(p_ItemIDs, ',', '')) + 1;

    -- Get the VehicleID associated with the rescuer
    SELECT VehicleID INTO v_VehicleID
    FROM Vehicles
    WHERE RescuerID = p_RescuerID;

    IF v_VehicleID IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No vehicle assigned to the rescuer.';
    END IF;

    -- Start the transaction to ensure atomicity
    START TRANSACTION;

    -- Loop through the comma-separated item names and quantities
    WHILE i <= total_items DO
        -- Extract the current item ID
        SET v_ItemID = CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemIDs, ',', i), ',', -1)) AS UNSIGNED);

        -- Extract the current quantity and convert to an integer
        SET v_Quantity = CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p_Quantities, ',', i), ',', -1)) AS UNSIGNED);

        -- Check if the item exists in the vehicle and the quantity is sufficient
        SELECT Quantity INTO v_VehicleQuantity
        FROM VehicleItems
        WHERE VehicleID = v_VehicleID AND ItemID = v_ItemID;

        IF v_VehicleQuantity IS NULL THEN
            SET v_ErrorMessage = CONCAT('Item "', v_ItemID, '" is not available in the vehicle.');
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = v_ErrorMessage;
        ELSEIF v_VehicleQuantity < v_Quantity THEN
            SET v_ErrorMessage = CONCAT('Insufficient quantity of item "', v_ItemID, '" in the vehicle.');
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = v_ErrorMessage;
        END IF;

        -- If the item exists in the warehouse, update the quantity
        -- This will correctly sum the quantities in the Warehouse table
        INSERT INTO Warehouse (ItemID, Quantity)
        VALUES (v_ItemID, v_Quantity)
        ON DUPLICATE KEY UPDATE Quantity = Warehouse.Quantity + v_Quantity;

        -- Subtract the quantity from the vehicle
        UPDATE VehicleItems
        SET Quantity = Quantity - v_Quantity
        WHERE VehicleID = v_VehicleID AND ItemID = v_ItemID;

        -- If the remaining quantity in the vehicle is zero, delete the item from VehicleItems
        IF (v_VehicleQuantity - v_Quantity) <= 0 THEN
            DELETE FROM VehicleItems WHERE VehicleID = v_VehicleID AND ItemID = v_ItemID;
        END IF;

        SET i = i + 1;
    END WHILE;

    -- Commit the transaction to apply all changes
    COMMIT;

END //

DELIMITER ;



DELIMITER //

CREATE PROCEDURE UnloadVehicleOnRequestCompletion(
    IN p_RescuerID INT,
    IN p_RequestID INT
)
BEGIN
    DECLARE v_VehicleID INT;
    DECLARE v_ItemID INT;
    DECLARE v_RequestedQuantity INT;
    DECLARE v_VehicleQuantity INT;
    DECLARE v_ItemName VARCHAR(255);  -- To hold the item name
    DECLARE done INT DEFAULT 0;
    DECLARE v_ErrorMessage VARCHAR(255);  -- Variable to hold the error message
    
    -- Declare a cursor to go through each item in the request, fetching ItemID, Quantity, and ItemName
    DECLARE request_items_cursor CURSOR FOR 
    SELECT ri.ItemID, ri.Quantity, i.Name
    FROM RequestItems ri
    JOIN Items i ON ri.ItemID = i.ItemID
    WHERE RequestID = p_RequestID;

    -- Declare a handler for when the cursor finishes
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Step 1: Validate that the rescuer is assigned to the request
    IF NOT EXISTS (SELECT 1 FROM Requests WHERE RequestID = p_RequestID AND RescuerID = p_RescuerID) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Rescuer is not assigned to this request.';
    END IF;

    -- Step 2: Get the VehicleID associated with the rescuer
    SELECT VehicleID INTO v_VehicleID FROM Vehicles WHERE RescuerID = p_RescuerID;

    IF v_VehicleID IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No vehicle assigned to the rescuer.';
    END IF;

    -- Step 3: Start a transaction to ensure atomicity
    START TRANSACTION;

    -- Step 4: Open the cursor to iterate through request items
    OPEN request_items_cursor;

    -- Step 5: Loop through each item in the request
    items_loop: LOOP
        -- Fetch the current request item, including the item name
        FETCH request_items_cursor INTO v_ItemID, v_RequestedQuantity, v_ItemName;

        -- Exit the loop if done
        IF done = 1 THEN
            LEAVE items_loop;
        END IF;

        -- Step 6: Check if the item exists in the vehicle
        SELECT Quantity INTO v_VehicleQuantity 
        FROM VehicleItems 
        WHERE VehicleID = v_VehicleID AND ItemID = v_ItemID;

        -- If the item doesn't exist, raise an error
        IF v_VehicleQuantity IS NULL THEN
            SET v_ErrorMessage = CONCAT('Error: Item "', v_ItemName, '" (ID ', v_ItemID, ') does not exist in the vehicle.');
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = v_ErrorMessage;
        ELSE
            -- Check if the quantity in the vehicle is sufficient
            IF v_VehicleQuantity < v_RequestedQuantity THEN
                SET v_ErrorMessage = CONCAT('Error: Insufficient quantity of item "', v_ItemName, '" (ID ', v_ItemID, ') in the vehicle.');
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = v_ErrorMessage;
            ELSE
                -- Subtract the requested quantity from the vehicle
                UPDATE VehicleItems
                SET Quantity = Quantity - v_RequestedQuantity
                WHERE VehicleID = v_VehicleID AND ItemID = v_ItemID;

                -- Remove the item completely if the remaining quantity is zero
                IF (v_VehicleQuantity - v_RequestedQuantity) <= 0 THEN
                    DELETE FROM VehicleItems WHERE VehicleID = v_VehicleID AND ItemID = v_ItemID;
                END IF;
            END IF;
        END IF;
    END LOOP;

    -- Step 9: Close the cursor
    CLOSE request_items_cursor;

    -- Step 10: Commit the transaction to confirm the changes
    COMMIT;

END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE LoadVehicleFromOffer(
    IN p_OfferID INT,
    IN p_RescuerID INT
)
BEGIN
    DECLARE v_VehicleID INT;
    DECLARE v_ItemID INT;
    DECLARE v_OfferQuantity INT;
    DECLARE v_VehicleQuantity INT;
    DECLARE done INT DEFAULT 0;

    -- Declare a cursor to go through each item in the offer
    DECLARE offer_items_cursor CURSOR FOR 
    SELECT ItemID, Quantity FROM OfferItems WHERE OfferID = p_OfferID;

    -- Declare a handler for when the cursor finishes
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Step 1: Validate that the offer exists
    IF NOT EXISTS (SELECT 1 FROM Offers WHERE OfferID = p_OfferID) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Offer does not exist.';
    END IF;

    -- Step 2: Validate that the rescuer is assigned to the offer
    IF NOT EXISTS (SELECT 1 FROM Offers WHERE OfferID = p_OfferID AND RescuerID = p_RescuerID) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Rescuer is not assigned to this offer.';
    END IF;

    -- Step 3: Get the VehicleID associated with the rescuer
    SELECT VehicleID INTO v_VehicleID FROM Vehicles WHERE RescuerID = p_RescuerID;

    IF v_VehicleID IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No vehicle assigned to the rescuer.';
    END IF;

    -- Step 4: Start a transaction to ensure atomicity
    START TRANSACTION;

    -- Step 5: Open the cursor to iterate through offer items
    OPEN offer_items_cursor;

    -- Step 6: Loop through each item in the offer
    items_loop: LOOP
        -- Fetch the current offer item
        FETCH offer_items_cursor INTO v_ItemID, v_OfferQuantity;

        -- Exit the loop if done
        IF done = 1 THEN
            LEAVE items_loop;
        END IF;

        -- Step 7: Check if the item already exists in the vehicle
        IF EXISTS (SELECT 1 FROM VehicleItems WHERE VehicleID = v_VehicleID AND ItemID = v_ItemID) THEN
            -- Get the current vehicle quantity for the item
            SELECT Quantity INTO v_VehicleQuantity
            FROM VehicleItems 
            WHERE VehicleID = v_VehicleID AND ItemID = v_ItemID;

            -- Update the quantity in the vehicle
            UPDATE VehicleItems
            SET Quantity = v_VehicleQuantity + v_OfferQuantity
            WHERE VehicleID = v_VehicleID AND ItemID = v_ItemID;
        ELSE
            -- Insert the item into VehicleItems if it doesn't exist
            INSERT INTO VehicleItems (VehicleID, ItemID, Quantity)
            VALUES (v_VehicleID, v_ItemID, v_OfferQuantity);
        END IF;
    END LOOP;

    -- Step 8: Close the cursor
    CLOSE offer_items_cursor;

    -- Step 9: Commit the transaction to confirm the changes
    COMMIT;

END //

DELIMITER ;

DELIMITER //

DELIMITER //

DROP PROCEDURE IF EXISTS LoadFromWarehouseToVehicle;
CREATE PROCEDURE LoadFromWarehouseToVehicle(
    IN p_RescuerID INT,
    IN p_ItemIDs VARCHAR(1000),  
    IN p_Quantities VARCHAR(1000)  
)
BEGIN
    DECLARE v_VehicleID INT;
    DECLARE v_ItemID INT;
    DECLARE v_Quantity INT;
    DECLARE v_WarehouseQuantity INT;
    DECLARE total_items INT;
    DECLARE i INT DEFAULT 1;
    DECLARE v_ErrorMessage VARCHAR(255);  
    
    -- Calculate total number of items from the comma-separated string
    SET total_items = LENGTH(p_ItemIDs) - LENGTH(REPLACE(p_ItemIDs, ',', '')) + 1;

    -- Get the VehicleID associated with the rescuer
    SELECT VehicleID INTO v_VehicleID
    FROM Vehicles
    WHERE RescuerID = p_RescuerID;

    IF v_VehicleID IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No vehicle assigned to the rescuer.';
    END IF;

    -- Start the transaction to ensure atomicity
    START TRANSACTION;

    -- Loop through the comma-separated item IDs and quantities
    WHILE i <= total_items DO
        -- Extract the current item ID
        SET v_ItemID = CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p_ItemIDs, ',', i), ',', -1)) AS UNSIGNED);

        -- Extract the current quantity and convert to an integer
        SET v_Quantity = CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p_Quantities, ',', i), ',', -1)) AS UNSIGNED);

        -- Get the Warehouse quantity for the current item
        SELECT Quantity INTO v_WarehouseQuantity
        FROM Warehouse
        WHERE ItemID = v_ItemID;

        IF v_WarehouseQuantity IS NULL THEN
            SET v_ErrorMessage = CONCAT('Error: Item "', v_ItemID, '" is not available in the warehouse.');
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = v_ErrorMessage;
        ELSEIF v_WarehouseQuantity < v_Quantity THEN
            SET v_ErrorMessage = CONCAT('Error: Insufficient quantity of item "', v_ItemID, '" in the warehouse.');
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = v_ErrorMessage;
        END IF;

        -- Insert into VehicleItems, or update quantity if the item already exists
        INSERT INTO VehicleItems (VehicleID, ItemID, Quantity)
        VALUES (v_VehicleID, v_ItemID, v_Quantity)
        ON DUPLICATE KEY UPDATE Quantity = Quantity + v_Quantity;

        -- Subtract the quantity from the warehouse
        UPDATE Warehouse
        SET Quantity = Quantity - v_Quantity
        WHERE ItemID = v_ItemID;

        -- If the remaining warehouse quantity is zero, delete the item from Warehouse
        IF (v_WarehouseQuantity - v_Quantity) <= 0 THEN
            DELETE FROM Warehouse WHERE ItemID = v_ItemID;
        END IF;

        SET i = i + 1;
    END WHILE;

    -- Commit the transaction to apply all changes
    COMMIT;

END //

DELIMITER ;



