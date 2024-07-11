package JDBC.dao;

import JDBC.db.Dbconnection;
import JDBC.model.User;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import static JDBC.db.Dbconnection.password;

public class UserDao {
    private final Connection connection;
    private  String sql="Select id,username,password from auth where username=? and password=?";
    private  String registersql="INSERT INTO auth(username,password)VALUES(?,?)";

    public UserDao(){
        try {
            connection=Dbconnection.getConnection();
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public User loginuser(String username, String password) {
        User user=null;
        PreparedStatement preparedStatement= null;
        try {
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1,username);
            preparedStatement.setString(2,password);
            ResultSet resultSet=preparedStatement.executeQuery();
            if(resultSet.next()){
                user = new User();
                user.setId(Integer.parseInt(resultSet.getString("id")));
                user.setName(resultSet.getString("username"));
                user.setPassword(resultSet.getString("password"));

            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }

        return user;
    }
    public  void  register(String username,String password){
        try {
            PreparedStatement preparedStatement =connection.prepareStatement(registersql);
            preparedStatement.setString(1,username);
            preparedStatement.setString(2,password);
            preparedStatement.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }


}