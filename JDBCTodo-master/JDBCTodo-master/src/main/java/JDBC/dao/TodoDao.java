package JDBC.dao;

import JDBC.db.Dbconnection;
import JDBC.model.Todo;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class TodoDao {
    private  final Connection connection;
    private final String SELECT_ALL = "SELECT id,userId,item FROM todo WHERE userId=?";
    private final String SELECT_TODO = "SELECT id, todo, userId FROM todo WHERE id=?";
    private final String INSERT_TODO = "INSERT INTO todo (userId, item) VALUES (?, ?);";
    private final String UPDATE_TODO = "UPDATE todo SET todo = ? WHERE id = ?;";
    private final String DELETE_TODO = "DELETE FROM todo WHERE id=?;";

    public TodoDao() throws SQLException, ClassNotFoundException {
        connection = Dbconnection.getConnection();
    }
    public List<Todo>selectalltodos(int userid){
        List<Todo> todos=new ArrayList<>();
        try {
            PreparedStatement ps=connection.prepareStatement(SELECT_ALL);
            ps.setInt(1,userid);
            ResultSet rs=ps.executeQuery();
            while (rs.next()){
                Todo todo=new Todo();
                todo.setId(Integer.parseInt(rs.getString("id")));
                todo.setTodo(rs.getString("item"));
                todo.setUserid(rs.getInt("userid"));
                todos.add(todo);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }return todos;
    }
    public void addTodo( int userId,String item) {
        try {
            PreparedStatement ps = connection.prepareStatement(INSERT_TODO);
            ps.setInt(1,userId);
            ps.setString(2,item);
            ps.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }

    }

    public void deleteTodo(int id) {
        try {
            PreparedStatement ps = connection.prepareStatement(DELETE_TODO);
            ps.setInt(1, id);
            ps.executeUpdate();

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
