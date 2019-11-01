USE quickservicefinder;
DELIMITER $$
CREATE PROCEDURE customer_GetCustomer (IN idcustomer INT)
BEGIN
	SELECT c.idcustomer, c.names, c.surnames, c.sex, c.phonenumber1, c.phonenumber2,
	uc.username, uc.email
	FROM customer AS c
	INNER JOIN user_customer AS uc
	ON c.idcustomer = uc.idcustomer
	WHERE c.idcustomer = idcustomer;
END$$

DELIMITER $$
CREATE PROCEDURE customer_InsertCustomer(
username VARCHAR(20),
password TEXT,
email VARCHAR(45),
names VARCHAR(45),
surnames VARCHAR(45),
sex VARCHAR(10),
phonenumber1 VARCHAR(15),
phonenumber2 VARCHAR(15))
BEGIN
DECLARE id_customer INT;
INSERT INTO customer (names, surnames, sex, phonenumber1, phonenumber2)
VALUES (names, surnames, sex, phonenumber1, phonenumber2);
SET id_customer = LAST_INSERT_ID();
INSERT INTO user_customer (idcustomer, username, password, email)
VALUES (id_customer, username, password, email);
END$$

DELIMITER $$
CREATE PROCEDURE customer_validateCustomer (IN username VARCHAR(20))
BEGIN
	SELECT * FROM user_customer AS uc WHERE uc.username = username;
END$$

DELIMITER $$
CREATE PROCEDURE notification_GetAcceptedCustomerNotifications(IN iduser_customer INT)
BEGIN
	SELECT n.idNotification, s.name, c.names, n.Message, n.isAccepted, n.Date, n.ResponseMessage, n.iduser_customer, n.idservice
    FROM notification AS n
    INNER JOIN user_customer AS uc ON
    uc.iduser_customer = n.iduser_customer
    INNER JOIN customer AS c ON
    uc.idcustomer = c.idcustomer
    INNER JOIN service AS s ON
    n.idservice = s.idservice
    WHERE n.isAccepted = 1 AND n.iduser_customer = iduser_customer;
END$$

DELIMITER $$
CREATE PROCEDURE notification_GetAcceptedNotifications()
BEGIN
	SELECT n.idNotification, s.name, c.names, n.Message, n.isAccepted, n.Date, n.ResponseMessage, n.iduser_customer, n.idservice
    FROM notification AS n
    INNER JOIN user_customer AS uc ON
    uc.iduser_customer = n.iduser_customer
    INNER JOIN customer AS c ON
    uc.idcustomer = c.idcustomer
    INNER JOIN service AS s ON
    n.idservice = s.idservice
    WHERE n.isAccepted = 1;
END$$

DELIMITER $$
CREATE PROCEDURE notification_GetDeniedCustomerNotifications(IN iduser_customer INT)
BEGIN
	SELECT n.idNotification, s.name, c.names, n.Message, n.isAccepted, n.Date, n.ResponseMessage, n.iduser_customer, n.idservice
    FROM notification AS n
    INNER JOIN user_customer AS uc ON
    uc.iduser_customer = n.iduser_customer
    INNER JOIN customer AS c ON
    uc.idcustomer = c.idcustomer
    INNER JOIN service AS s ON
    n.idservice = s.idservice
    WHERE n.isAccepted = 0 AND n.iduser_customer = iduser_customer;
END$$

DELIMITER $$
CREATE PROCEDURE notification_GetDeniedNotifications()
BEGIN
	SELECT n.idNotification, s.name, c.names, n.Message, n.isAccepted, n.Date, n.ResponseMessage, n.iduser_customer, n.idservice
    FROM notification AS n
    INNER JOIN user_customer AS uc ON
    uc.iduser_customer = n.iduser_customer
    INNER JOIN customer AS c ON
    uc.idcustomer = c.idcustomer
    INNER JOIN service AS s ON
    n.idservice = s.idservice
    WHERE n.isAccepted = 0;
END$$

DELIMITER $$
CREATE PROCEDURE notification_GetPendingNotifications (IN idservice INT)
BEGIN
	SELECT n.idNotification, s.name, c.names, n.Message, n.isAccepted, n.Date, n.ResponseMessage, n.iduser_customer, n.idservice
    FROM notification AS n
    INNER JOIN user_customer AS uc ON
    uc.iduser_customer = n.iduser_customer
    INNER JOIN customer AS c ON
    uc.idcustomer = c.idcustomer
    INNER JOIN service AS s ON
    n.idservice = s.idservice
    WHERE n.isAccepted IS NULL  AND n.ResponseMessage IS NULL AND n.idservice = idservice;
END$$

DELIMITER $$
CREATE PROCEDURE notification_InsertNotification(
iduser_customer INT,
idservice INT,
Message VARCHAR(150),
isAccepted INT,
Date DATE, 
ResponseMessage VARCHAR(150))
BEGIN
INSERT INTO notification (iduser_customer, idservice, Message, isAccepted, Date, ResponseMessage)
VALUES (iduser_customer, idservice, Message, isAccepted, Date, ResponseMessage);
END$$

DELIMITER $$
CREATE PROCEDURE notification_UpdateRequest(
IN idnotification INT,
IN isAccepted INT,
IN ResponseMessage VARCHAR(150)
)
BEGIN
	UPDATE notification AS n
	SET n.isAccepted = isAccepted, n.ResponseMessage = ResponseMessage
	WHERE n.idNotification = idnotification;
END$$

DELIMITER $$
CREATE PROCEDURE ownerService_GetOwnerService (IN idownerservice INT)
BEGIN
	SELECT os.idownerservice, os.names, os.surnames, os.sex, os.phonenumber1, os.phonenumber2,
	uos.username, uos.email
	FROM ownerservice AS os
	INNER JOIN user_ownerservice as uos
	ON uos.idownerservice = os.idownerservice
	WHERE os.idownerservice = idownerservice;
END$$

DELIMITER $$
CREATE PROCEDURE ownerService_InsertOwnerService (
username VARCHAR(20),
password TEXT,
email VARCHAR(45),
names VARCHAR(45),
surnames VARCHAR(45),
sex VARCHAR(20),
phonenumber1 VARCHAR(10),
phonenumber2 VARCHAR(10))
BEGIN
DECLARE id_owner_service INT;
INSERT INTO ownerservice (names, surnames, sex, phonenumber1, phonenumber2)
VALUES (names, surnames, sex, phonenumber1, phonenumber2);
SET id_owner_service = LAST_INSERT_ID();
INSERT INTO user_ownerservice (idownerservice, username, password, email)
VALUES (id_owner_service, username, password, email);
END$$

DELIMITER $$
CREATE PROCEDURE ownerservice_validateOwnerService (IN username VARCHAR(20))
BEGIN
	SELECT * FROM user_ownerservice AS uos WHERE uos.username = username;
END$$

DELIMITER $$
CREATE PROCEDURE service_GetServiceByOwner (IN idownerservice INT)
BEGIN
	SELECT s.idservice, sub.names, s.name, s.address, s.description
	FROM service AS s
    INNER JOIN subsector AS sub
    ON s.idsubsector = sub.idsubsector
    WHERE s.idownerservice = idownerservice;
END$$

DELIMITER $$
CREATE PROCEDURE service_GetServiceBySubsector(IN idsubsector INT)
BEGIN
	SELECT * FROM service AS s
	WHERE s.idsubsector = idsubsector;
END$$

DELIMITER $$
CREATE PROCEDURE service_GetServiceDetail (IN idservice INT)
BEGIN
	SELECT s.idservice, s.name, s.address, s.description, sns.idsocialnetworkservice AS idsns, 
    sns.name AS socialnetworkname, sns.link AS socialnetworklink, ss.idsubsector AS subsector, 
    ss.names AS subsectorname, ss.idsector, sec.name AS sectorname, s.idowner AS idowner, 
    os.names AS ownerservicename, os.surnames AS ownersurnames
FROM service AS s
	INNER JOIN ownerservice as os
		ON os.idownerservice = s.idowner
	INNER JOIN socialnetworkservice as sns
		ON sns.idservice = s.idservice
	INNER JOIN subsector as ss
		ON ss.idsubsector = s.idsubsector
	INNER JOIN sector as sec
		ON sec.idsector = ss.idsector
	WHERE s.idservice = idservice;
END$$

DELIMITER $$
CREATE PROCEDURE service_InsertService (
idownerservice INT,
idsubsector INT,
name VARCHAR(45),
address VARCHAR(100),
description VARCHAR(100))
BEGIN
INSERT INTO service (idownerservice, idsubsector, name, address, description)
VALUES (idownerservice, idsubsector, name, address, description);
END$$

DELIMITER $$
CREATE PROCEDURE socialnetworkservice_InsertSNS(
idservice INT,
name VARCHAR(45),
link VARCHAR(45))
BEGIN
INSERT INTO socialnetworkservice (idservice, name, link)
VALUES (idservice, name, link);
END$$

DELIMITER $$
CREATE PROCEDURE subsector_GetSubsector()
BEGIN
	SELECT * 
	FROM subsector AS ss;
END$$

DELIMITER $$
CREATE PROCEDURE valoration_InsertValoration(
idservice INT,
iduser_customer INT,
comment NVARCHAR(100),
rate INT)
BEGIN
INSERT INTO valoration (idservice, iduser_customer, comment, rate)
VALUES (idservice, iduser_customer, comment, rate);
END$$




