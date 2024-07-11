package org.example.models;

import java.sql.Timestamp;
import java.util.ArrayList;

public class Cart {
    private Timestamp id;
    private User user;

    private ArrayList<CartProduct> cartProducts;

    public Timestamp getId() {
        return id;
    }

    public void setId(Timestamp id) {
        this.id = id;
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
