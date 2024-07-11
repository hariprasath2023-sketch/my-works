# Todospringboot
Todo using SpringBoot
Developed SpringBoot application to create the rest API.
 
 
## Description
 
- Using Postman we can able to do CRUD operation which reflects in database.
 
 
## 🛠 Technology used
 
- Springboot - 2.7.17
- JDBC
- MySQL
 
## 🛠 Tools used
 
- IntelliJ
- MySQL Workbench
- Postman
 
## 🔲 Architecture
 
- Controller
 
        1. Todo Controller
 
- Model
 
        1. Todo
 
- Repository
 
        1. Todo Repository
 
 
## 🔃Working of project
 
- application.properties
 
        - Here we have wrote workbence connectivity details.
 
- Application
 
        - Here where the application starts running.
        - Once compiled we  will get the port number like(8080) where we can use it to do CRUD operations.
 
- Todo
 
        - I have created this for model which should be same as the column in the database.
 
- Todo Repository
 
        - Here i have written the code to play with the database.
 
- Todo Controller
 
        - Have where the business logic takes place.
        - We would have used annotations here which has been described below.
## Annotations used
 
        @SpringBootApplication
        @Override
        @Repository
        @Autowired
        @RestController
        @RequestMapping
        @GetMapping
        @PostMapping
        @PutMapping
        @DeleteMapping
 

1. Get all todo(Retrieve)
 

 
2. Post todo(Create)
 

 
3. Put todo(Update)
 
 
4. Delete todo(Delete)

 
