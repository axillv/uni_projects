# Disaster Relief Management System

This project is a disaster relief management system designed to streamline the process of managing resources and requests during a disaster. It includes a MySQL database schema, stored procedures, triggers, and test data to support a PHP-based web application.

## Database Schema

The database schema is defined in `db_schema.sql` and includes the following tables:

- `Administrator`: Stores information about system administrators.
- `user`: Stores information about all users (administrators, rescuers, and citizens).
- `Rescuer`: Stores information about rescuers who handle requests.
- `Citizen`: Stores information about citizens who can make requests and offers.
- `Items`: Stores information about items available for requests and offers.
- `Warehouse`: Manages item quantities in the warehouse.
- `Requests`: Manages requests made by citizens for specific items.
- `RequestItems`: Manages the items and quantities associated with each request.
- `Offers`: Manages offers made by citizens to provide specific items.
- `OfferItems`: Manages the items and quantities associated with each offer.
- `Vehicles`: Manages vehicles assigned to rescuers for delivering items.
- `VehicleItems`: Manages the items and quantities associated with each vehicle.
- `Announcements`: Stores announcements made by administrators.
- `AnnouncementItems`: Manages the items and quantities associated with each announcement.


## Stored Procedures and Triggers

The `Procedures_Trigers.sql` file contains stored procedures and triggers, including:

### Stored Procedures

1. **CreateNewRequest**
   - **Usage:** Create a new request using item names.
   - **Parameters:** 
     - `citizenID INT`: ID of the citizen making the request.
     - `items JSON`: JSON array of items and their quantities.
     - **Description:** Inserts a new request with status `PENDING` into the `Requests` table and associates items with the new request.

2. **CreateNewOffer**
   - **Usage:** Create a new offer using item names.
   - **Parameters:** 
     - `citizenID INT`: ID of the citizen making the offer.
     - `items JSON`: JSON array of items and their quantities.
     - **Description:** Inserts a new offer with status `PENDING` into the `Offers` table and associates items with the new offer.

3. **CreateNewRescuer**
   - **Usage:** Create a new rescuer and associate a vehicle with the rescuer.
   - **Parameters:** 
     - `username VARCHAR(50)`: Username of the rescuer.
     - `password VARCHAR(255)`: Password of the rescuer.
     - `latitude DECIMAL(10, 8)`: Latitude where the vehicle is located.
     - `longitude DECIMAL(11, 8)`: Longitude where the vehicle is located.
     - **Description:** Inserts a new rescuer into the `Rescuer` table and associates a vehicle with the new rescuer, including the vehicle's latitude and longitude.

4. **CreateNewCitizen**
   - **Usage:** Create a new citizen.
   - **Parameters:**
     - `username VARCHAR(50)`: Username of the citizen.
     - `password VARCHAR(255)`: Password of the citizen.
     - `name VARCHAR(100)`: Name of the citizen.
     - `phone VARCHAR(15)`: Phone number of the citizen.
     - `latitude DECIMAL(10, 8)`: Latitude of the citizen's location.
     - `longitude DECIMAL(11, 8)`: Longitude of the citizen's location.
     - **Description:** Inserts a new citizen into the `Citizen` table and associates the citizen with a user account.

5. **AssignRequest**
   - **Usage:** Assign a rescuer to a request.
   - **Parameters:** 
     - `requestID INT`: ID of the request.
     - `rescuerID INT`: ID of the rescuer.
   - **Description:** Assigns a rescuer to the specified request and updates the request status to `INPROGRESS`.

6. **CreateNewAdmin**
   - **Usage:** Create a new administrator.
   - **Parameters:** 
     - `username VARCHAR(255)`: Username of the new admin.
     - `password VARCHAR(255)`: Password for the new admin.
     - **Description:** Inserts a new admin into the `Admin` table and associates the admin with a user account.

7. **AssignOffer**
   - **Usage:** Assign a rescuer to an offer.
   - **Parameters:** 
     - `offerID INT`: ID of the offer.
     - `rescuerID INT`: ID of the rescuer.
   - **Description:** Assigns a rescuer to the specified offer and updates the offer status to `INPROGRESS`.


8. **CancelRequest**
   - **Usage:** Cancel a request.
   - **Parameters:** 
     - `requestID INT`: ID of the request.
   - **Description:** Cancels the specified request and updates the request status to `CANCELLED`.


9. **CancelOffer**
   - **Usage:** Cancel an offer.
   - **Parameters:** 
     - `offerID INT`: ID of the offer.
   - **Description:** Cancels the specified offer and updates the offer status to `CANCELLED`.


10. **FinishRequest**
   - **Usage:** Mark a request as finished.
   - **Parameters:** 
     - `requestID INT`: ID of the request.
   - **Description:** Marks the specified request as `FINISHED`.


11. **FinishOffer**
   - **Usage:** Mark an offer as finished.
   - **Parameters:** 
     - `offerID INT`: ID of the offer.
   - **Description:** Marks the specified offer as `FINISHED`

12. **CreateAnnouncement**
   - **Usage:** Create a new announcement.
   - **Parameters:**
     - `adminID INT`: ID of the administrator making the announcement.
     - `items JSON`: JSON array of items and their quantities.
   - **Description:** Inserts a new announcement into the `Announcements` table and its associated items into the `AnnouncementItems` table.
date are reset.

### Triggers

1. **BeforeAssignRescuerToRequest**
   - **Description:** Checks conditions before assigning a rescuer to a request. Ensures that the rescuer is not already assigned to more than a certain number of task (e.g., 4 tasks) and that the request is currently in a `PENDING` state.

2. **BeforeAssignRescuerToOffer**
   - **Description:** Checks conditions before assigning a rescuer to an offer. Ensures that the rescuer is not already assigned to more than a certain number of tasks (e.g., 4 tasks) and that the offer is currently in a `PENDING` state.

3. **PreventReassignInProgressRequest**
   - **Description:** Prevents reassigning an `INPROGRESS` request to another rescuer.

4. **PreventReassignInProgressOffer**
   - **Description:** Prevents reassigning an `INPROGRESS` offer to another rescuer.

5. **PreventPendingRequestFinished**
   - **Description:** Prevents changing the status of a `PENDING` request directly to `FINISHED`.

6. **PreventPendingOfferFinished**
   - **Description:** Prevents changing the status of a `PENDING` offer directly to `FINISHED`.

7. **PreventFinishedRequestAlteration**
   - **Description:** Prevents any alteration of a `FINISHED` request.

8. **PreventFinishedOfferAlteration**
   - **Description:** Prevents any alteration of a `FINISHED` offer

### Custom Error Codes

| Error Code | Description                                    |
|------------|------------------------------------------------|
| 4001       | One or more items do not exist in the dB       |
|------------|------------------------------------------------|
| 6002       |Rescuer has reached the maximum number of tasks.|
|------------|------------------------------------------------|
| 5003       | In-progress requests cannot be reassigned.     |
|------------|------------------------------------------------|
| 5004       | In-progress offers cannot be reassigned.       |
|------------|------------------------------------------------|
| 5005       | Pending requests cannot be marked as finished. |
|------------|------------------------------------------------|
| 5006       | Pending offers cannot be marked as finished.   |
|------------|------------------------------------------------|
| 5007       | Finished requests cannot be altered.           |
|------------|------------------------------------------------|
| 5008       | Finished offers cannot be altered.             |
|------------|------------------------------------------------|


## Test Data

The `test_data.sql` file provides sample data to populate the database for testing purposes. It includes sample administrators, rescuers, citizens, items, requests, and offers.

## How to Use

1. **Setup Database:**
   - Create a new MySQL database.
   - Run `db_schema.sql` to create the database schema.
   - Run `Procedures_Trigers.sql` to add the stored procedures and triggers.
   - Run `test_data.sql` to populate the database with sample data.

2. **Configure PHP Application:**
   - Update the database connection settings in your PHP application to connect to the MySQL database.
   - Use the provided database schema and procedures to handle requests, offers, and other operations in the application.

3. **API Integration:**
   - Create PHP scripts to interact with the database using the defined schema and procedures.
   - Implement API endpoints to manage disaster relief operations, such as creating requests, assigning rescuers, updating statuses, and more.

## Example API Endpoints

- `POST /api/requests`: Create a new request.
- `POST /api/offers`: Create a new offer.
- `GET /api/requests`: Retrieve a list of requests.
- `GET /api/offers`: Retrieve a list of offers.
- `PUT /api/requests/:id/assign`: Assign a request to a rescuer.
- `PUT /api/requests/:id/status`: Update the status of a request.
- `PUT /api/offers/:id/assign`: Assign an offer to a rescuer.
- `PUT /api/offers/:id/status`: Update the status of an offer.