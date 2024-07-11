package org.example.models;

import java.sql.Date;
import java.sql.Timestamp;
import java.util.ArrayList;

public class Order {
    private Timestamp id;
    private Date date;
    private User user;
    private ArrayList<CartProduct> cartProducts;

    public Timestamp getId() {
        return id;
    }

    public void setId(Timestamp id) {
        this.id = id;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public ArrayList<CartProduct> getCartProducts() {
        return cartProducts;
    }

    public void setCartProducts(ArrayList<CartProduct> cartProducts) {
        this.cartProducts = cartProducts;
    }
}
