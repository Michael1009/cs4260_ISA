# Jersey Marketplace
Our project's goal is to provide a marketplace for Soccer fans to buy and sell used/new jerseys. This project was created for the course Internet Scale Applications at the University of Virginia in order to help us learn about and experience using technologies that are used to scale web applications. 

### Architecture
This project has a 4-tier architecture, with the levels being: HTML Front-End, Experience Service, Model, and the database. An example request from a user would be as follows: The user requests data from the front-end, the request is sent to the experience service, the experience service will query as many models as needed to get the relevant data, and the model layer will query the database for the relevant data. Once all the data is gathered, the various models that were queried would send the gathered data to the experience service. The experience service will package all of this data (into JSON) and send it to the front-end. 

The reason why we have the 4-tier architecture is to enforce strict isolation between the levels, which allows this app to be scalable across a large team. Additionally, the reason why we have the experience service is because it allows us to create a single service call from the front-end to load a page. Now, instead of a page having to send multiple requests to load its content, it can just send one. The Experience service will handle all of the business logic to load all of the relevant data. 

### Technologies

Some of the technologies used to build this project were: Docker, MySQL, Django, Travis CI, Selenium, Kafka, HAProxy, Apache Spark, and ElasticSearch. 

Docker containers were used to hold the various layers in our application. MySQL was the database and Django was used for the Experience, Model, and HTML front-end layers. Travis CI was for running automated tests and Selenium was the tool for writing the tests themselves. HAProxy was to handle load balancing. 

Kafka queue was used when new Jersey listings were created and these were indexed into ElasticSearch such that users could search for Jerseys. The reason why we had Kafka queue instead of indexing directly into ElasticSearch is in the case that the ElasticSearch service (container) was down. If the ElasticSearch service was down, the new listings would sit in the Kafka queue until the service went back up. 

Apache Spark was used to build a recommendation system. The system would allow users to see Jerseys they would potentially be interested in viewing. The recommendation system used the idea of "co-views" to decide what to recommend users. 

