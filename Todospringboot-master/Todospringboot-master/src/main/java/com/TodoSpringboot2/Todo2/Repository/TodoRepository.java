package com.TodoSpringboot2.Todo2.Repository;

import com.TodoSpringboot2.Todo2.Model.Todo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class TodoRepository{
    @Autowired
    private JdbcTemplate jdbcTemplate;




    public List<Todo> findall() {
        return jdbcTemplate.query("SELECT * FROM todo", new BeanPropertyRowMapper<>(Todo.class));
    }


    public List<Todo> insert(Todo todo) {
        jdbcTemplate.update("INSERT INTO todo(item) VALUES(?);",
                new Object[]{ todo.getItem()});
        return findall();
    }


    public List<Todo> update(Todo todo) {
        jdbcTemplate.update("UPDATE todo SET item=?,WHERE id=?:", new Object[]{todo.getId(),todo.getItem()});
        return findall();
    }
    public List<Todo> deleteById(int id){
        jdbcTemplate.update("DELETE FROM todo WHERE id=?",new Object[]{id});
        return findall();
    }
}
