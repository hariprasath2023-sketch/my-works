package org.example.Database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Dbconnection {
    private final static String connectionString = "jdbc:mysql://localhost:3306/sqlecommerce";
    private final static String username = "root";
    private final static String password = "root";


    public static Connection getConnection()
    {
        Connection connection;

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            connection = DriverManager.getConnection(connectionString,username,password);
//            System.out.println("connection:"+!connection.isClosed());
        } catch (ClassNotFoundException | SQLException e) {
            throw new RuntimeException(e);
        }
        return connection;
    }
}
