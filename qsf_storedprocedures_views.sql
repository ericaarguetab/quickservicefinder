USE quickservicefinder;
CREATE VIEW `viewCustomerUser_customer` AS SELECT 
c.idcustomer, c.names, c.surnames, c.sex, c.phonenumber1, c.phonenumber2, 
uc.username, uc.email 
FROM customer as c
INNER JOIN user_customer as uc
on c.idcustomer = uc.idcustomer;