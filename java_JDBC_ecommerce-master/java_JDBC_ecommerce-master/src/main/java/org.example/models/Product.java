package org.example.models;

public class Product {
    private int id;

    private String title;

    public Product(int id, String title, double price, Category category) {
        this.id = id;
        this.title = title;
        this.price = price;
        this.category = category;
    }

    public int getId() {
        return id;
    }


    public String getTitle() {
        return title;
    }





    public double getPrice() {
        return price;
    }


    public Category getCategory() {
        return category;
    }


    private double price;
    private Category category;
}
