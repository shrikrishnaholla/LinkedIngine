
Databasengine
=============

This is an in-memory database engine  
It should support CRD (Create, Retrieve, Delete operations)  
Update has been omitted as this shouldn't update their profile details. This application's purpose is just analytical  

Query
-----

  
To allow for more powerful querying, we have developed a SQL-like syntax for passing queries to the database.  
Please follow the rules to get the optimum output.  
  
####The syntax goes something like this:  
return <returnvals> from <number> profiles whose [query parameters]  
  
Example: "return email,locality,experience from 10 profiles whose [(email=gmail;or;email=yahoo);and;(locality=bangalore;or;locality=delhi);and;(experience<5;or;experience>10)]"  
  
#####The available attributes are:  
fname                => First Name  
lname                => Last Name  
email                => e-mail id   
locality             => Location   
industry             => field of work   
current              => current job description  
past                 => Past jobs  
experience           => Job experience (integer)  
education            => Academic details  
skills               => skillsets  
project-descriptions => Description of listed projects  
  
####Available operators:  
=,<>                [equals, doesn't equal] for string and integer values  
<=,>=,<,>           [less than or equals, greater than or equals, less than, greater than] for integer values  
  
####Special numbers  
'*'   => Returns all fields. Ex: "return * from 5 profiles whose [past=adobe]"  
'all' => Returns all profiles that satisfy the condition. Ex: "return skills from all profiles whose [experience>15]"  
  
Note: '=' operator is liberal; ie, you can search for a valid value with an invalid key and QuerySQL will try to return the best possible results  
Ex: "return skills from 10 profiles whose [knowledge=python]"  
return email,locality,experience from 10 profiles whose [(email=gmail;or;email=yahoo);and;(locality=bangalore;or;locality=delhi);and;(experience<5;or;experience>10)]  

###querystring###

Takes a QuerySQL statement and a dictionary database of profiles as an input and returns a list of profiles as output  

###process###

Process the QuerySQL statement. A statement enters this method as left part, a boolean operator and a right part.  
    Based on whether the individual left and right parts are atomic or compound, either the substatements might be evaluated  
    or they can be sent back to parse() for further processing of compound statements  

Scraper
-------

This is a module used to scrape the public profiles of linkedIn users for meaningful profile data  
Usage: Suppose the profile of the person XYZ whose data is required has a linkedIn profile whose public url goes by  
www.linkedin.com/pub/xyz/123/456/789, on prompted, input 'xyz/123/456/789' into the console  

###collect###

Easy method to collect fields  

###collectmultiple###

Easy method to collect fields with multiple attributes  

Datacollector
-------------

This module is used by the testing console to provide different methods to collect profile data  

###collect###

Method to collect profile data  

Generator
---------

This module is used to generate structured profiles by picking out random elements from predefined lists and stitching   
together values for various fields in a typical LinkedIn profile  

###generate###

Generate profile data for creating test database  

Deserializer
------------

###deserialize###

Read deserialized data from file  
