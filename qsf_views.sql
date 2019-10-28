USE quickservicefinder;

CREATE VIEW `viewCustomerUser_customer` AS SELECT 
c.idcustomer, c.names, c.surnames, c.sex, c.phonenumber1, c.phonenumber2, 
uc.username, uc.email 
FROM customer AS c
INNER JOIN user_customer AS uc
ON c.idcustomer = uc.idcustomer;

CREATE VIEW `viewOwnerserviceUser_ownerservice` AS SELECT
os.idownerservice, os.names, os.surnames, os.sex, os.phonenumber1, os.phonenumber2,
uos.username, uos.email
FROM ownerservice AS os
INNER JOIN user_ownerservice AS uos
ON os.idownerservice = uos.idownerservice;

CREATE VIEW `viewNotification` AS SELECT
n.idNotification, n.Message, n.isAccepted,
n.Date, n.ResponseMessage, n.idservice, s.name AS servicename, os.idownerservice, os.names AS ownernames, 
os.surnames AS ownersurnames, c.idcustomer AS idcustomer, c.names AS customernames, c.surnames AS customersurnames
FROM notification AS n
	INNER JOIN service as s
		ON s.idservice = n.idservice
	INNER JOIN user_ownerservice as uos
		ON s.idowner = uos.iduser_ownerservice
	INNER JOIN ownerservice as os
		ON uos.idownerservice = os.idownerservice
	INNER JOIN user_customer as uc
		ON n.iduser_customer = uc.iduser_customer
	INNER JOIN customer as c
		ON uc.idcustomer = c.idcustomer;

CREATE VIEW `viewValoration` AS SELECT
v.idvaloration, v.comment, v.rate, s.idservice AS idservice, s.name AS servicename, c.idcustomer AS idcustomer, c.names AS customernames, c.surnames AS customersurnames
FROM valoration AS v
	INNER JOIN service as s
		ON s.idservice = v.idservice
	INNER JOIN user_customer as uc
		ON v.iduser_customer = uc.iduser_customer
	INNER JOIN customer as c
		ON uc.idcostumer = c.idcustomer;

CREATE VIEW `viewService` AS SELECT
s.idservice, s.name, s.address, s.description, sns.idsocialnetworkservice AS idsns, sns.name AS socialnetworkname, 
sns.link AS socialnetworklink, ss.idsubsector AS subsector, ss.names AS subsectorname, ss.idsector, sec.name AS sectorname,
s.idowner AS idowner, os.names AS ownernames, os.surnames AS ownersurnames
FROM service AS s
	INNER JOIN ownerservice as os
		ON os.idownerservice = s.idowner
	INNER JOIN socialnetworkservice as sns
		ON sns.idservice = s.idservice
	INNER JOIN subsector as ss
		ON ss.idsubsector = s.idsubsector
	INNER JOIN sector as sec
		ON sec.idsector = ss.idsector;




	