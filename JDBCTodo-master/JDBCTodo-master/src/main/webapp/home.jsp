<%@ page language="java" contentType="text/html; charset=UTF-8"
 pageEncoding="UTF-8"%>
 <%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<html>
<title>Todo</title>
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
</head>
<body>
<p class="fs-1 text-center">My Todo</p>
    <%
        if(session.getAttribute("id") == null){
             response.sendRedirect(request.getContextPath());
        }
    %>
    <form action="todo" method="post">
        <p class="text-center fs-0 table-dark">Enter Todo: <input class="input mb-0" type="text" name="todo" value="${todo.todo}"/>
        <input class="btn btn-outline-secondary mb-1" type="submit" value="Add" />
    </form>
    <c:if test="${todos.size() eq 0}">
        <p>No Items to display</p>
    </c:if>
    <c:if test="${todos.size() gt 0}">
        <table class="table table-hover container">
                <thead>
                    <tr>
                        <th>Id</th>
                        <th>Todo</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <c:forEach var="todo" items="${todos}">
                        <tr>
                            <td>
                                <c:out value="${todo.id}" />
                            </td>
                            <td>
                                <c:out value="${todo.todo}" />
                            </td>
                            <td><a class="btn btn-danger me-2" href="todo?id=<c:out value='${todo.id}'/>">Delete</a><a class="btn btn-primary " href="todo?id=<c:out value='${todo.id}'/>">Edit</a></td>
                        </tr>
                    </c:forEach>
                </tbody>
            </table>
    </c:if>
   <form action="logout.jsp" method="link" class="d-flex justify-content-end me-5">
        <input class="btn btn-danger" type="submit" value="logout"/>
    </form>
</body>
</html>