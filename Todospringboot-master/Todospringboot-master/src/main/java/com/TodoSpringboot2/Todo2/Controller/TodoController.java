package com.TodoSpringboot2.Todo2.Controller;

import com.TodoSpringboot2.Todo2.Model.Todo;
import com.TodoSpringboot2.Todo2.Repository.TodoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("/api")
public class TodoController {
    @Autowired
    private TodoRepository todoRepository;
    @GetMapping("/todo/all")
    public List<Todo> getalltodos(){
        return todoRepository.findall();
    }
    @PostMapping("/todo")
    public List<Todo> addtodo(@RequestBody Todo todo){
        return  todoRepository.insert(todo);
    }

    @PutMapping("/todo")
    public List<Todo>updatetodo(@RequestBody Todo todo){
        return  todoRepository.update(todo);
    }
    @DeleteMapping("/todo/{id}")
    public  List<Todo> deletetodo(@PathVariable int id){
        return todoRepository.deleteById(id);
    }



}