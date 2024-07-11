package com.TodoSpringboot2.Todo2.Model;

public class Todo {
    private  int id;
    private String item;
    public Todo(){

    }
    public Todo(int id, String item) {
        this.id=id;
        this.item=item;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getItem() {
        return item;
    }

    public void setItem(String item) {
        this.item = item;
    }
}
