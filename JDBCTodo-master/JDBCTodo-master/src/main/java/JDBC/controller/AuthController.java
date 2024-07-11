package JDBC.controller;

import JDBC.dao.UserDao;
import JDBC.db.Dbconnection;
import JDBC.model.User;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.sql.SQLException;

public class AuthController extends HttpServlet {
    private final UserDao userdao;

    public AuthController() {
        userdao = new UserDao();;
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException,IOException {
        String username = req.getParameter("username");
        String password = req.getParameter("password");
        User loginUser = userdao.loginuser(username, password);
        if (loginUser != null) {
            HttpSession httpSession = req.getSession();
            httpSession.setAttribute("id", loginUser.getId());
            RequestDispatcher request = req.getRequestDispatcher("todo");
            request.forward(req, resp);
        } else {
            req.setAttribute("error", true);
            RequestDispatcher dispatcher = req.getRequestDispatcher("index.jsp");
            dispatcher.forward(req, resp);
        }

    }

}