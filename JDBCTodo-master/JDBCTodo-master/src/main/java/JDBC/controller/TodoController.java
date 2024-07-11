package JDBC.controller;

import JDBC.dao.TodoDao;
import JDBC.dao.UserDao;
import JDBC.model.Todo;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.List;

public class TodoController extends HttpServlet {
    private TodoDao todoDao;
    private UserDao userDao;
    public TodoController() throws SQLException, ClassNotFoundException {

        todoDao=new TodoDao();
        userDao=new UserDao();

    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
          String id=req.getParameter("id");
          if (id!=null){
              todoDao.deleteTodo(Integer.parseInt(id));
          }doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        RequestDispatcher dispatcher= req.getRequestDispatcher("home.jsp");
        int userid=Integer.parseInt(req.getSession().getAttribute("id").toString());
        String item=req.getParameter("todo");
        if (item!=null &&!item.trim().isEmpty()){
            todoDao.addTodo(userid,item);
        }
        List<Todo>todos=todoDao.selectalltodos(userid);
        req.setAttribute("todos",todos);
        dispatcher.forward(req,resp);
    }
}
