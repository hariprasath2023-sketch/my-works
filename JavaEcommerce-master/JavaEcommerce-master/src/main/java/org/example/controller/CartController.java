package org.example.controller;

import org.example.controller.impl.ICartController;
import org.example.models.Cart;
import org.example.models.CartProduct;
import org.example.models.Product;
import org.example.models.User;
import org.example.util.AppException;
import org.example.util.StringUtils;
import org.example.view.CartPage;

import static org.example.util.AppInput.enterInt;
import static org.example.util.LoadUtils.getProducts;
import static org.example.util.UserUtil.getLoggedUser;
import static org.example.util.UserUtil.setLoggedUser;
import static org.example.util.Utils.println;

import java.util.ArrayList;

public class CartController implements ICartController {

    private final HomeController homeController;
    private final OrderController orderController;
    private final CartPage cartPage;

    public CartController(HomeController homeController) {
        this.homeController = homeController;
        orderController = new OrderController(homeController);
        cartPage = new CartPage();
    }

    public void addToCart(int productId) {
            User loggedInUser = getLoggedUser();
            ArrayList<Product> products = getProducts();

            Product userProduct = null;
            for (Product product : products) {
                if (product.getId() == productId) {
                    userProduct = product;
                    break;
                }
            }

            if (loggedInUser.getUserCart() != null) {
                Cart cart = loggedInUser.getUserCart();

                boolean isFound = false;
                for (CartProduct cartProduct : cart.getCartProducts()) {
                    if (cartProduct.getProduct().getId() == productId) {
                        cartProduct.setCount(cartProduct.getCount() + 1);
                        isFound = true;
                    }
                }

                if (!isFound) {
                    cart.getCartProducts().add(new CartProduct(userProduct, 1));
                }

                loggedInUser.setUserCart(cart);
            } else {
                Cart cart = new Cart();
                ArrayList<CartProduct> cartProducts = new ArrayList<>();
                cartProducts.add(new CartProduct(userProduct, 1));
                cart.setCartProducts(cartProducts);
                loggedInUser.setUserCart(cart);
            }
            setLoggedUser(loggedInUser);
        }
    public void printCart() {
      println(StringUtils.CART);
        User loggedInUser = getLoggedUser();
        if (loggedInUser.getUserCart() == null) {
            cartPage.printEmptyCart();
            homeController.printMenu();
        } else {
            ArrayList<CartProduct> cartProducts = loggedInUser.getUserCart().getCartProducts();
            cartPage.printCart(cartProducts);

            cartPage.printCheckout();
            cartPage.printBack();

            try {
                int choice = enterInt(StringUtils.ENTER_CHOICE);
                if (choice == 88) {
                    checkout();
                } else if (choice == 99) {
                    homeController.printMenu();
                } else {
                    invalidChoice(new AppException(StringUtils.INVALID_CHOICE));
                }
            } catch (AppException appException) {
                invalidChoice(appException);
            }

        }
    }
    private void invalidChoice(AppException appException) {
        println(appException.getMessage());
        printCart();
    }

    private void checkout() {
        orderController.checkout();
    }
}

