package org.example.controller;

import org.example.controller.impl.IProductController;
import org.example.models.Product;
import org.example.util.AppException;
import org.example.util.LoadUtils;
import org.example.util.StringUtils;
import org.example.view.ProductsPage;

import java.util.ArrayList;

import static org.example.util.AppInput.enterInt;
import static org.example.util.LoadUtils.getProducts;
import static org.example.util.Utils.println;

public class ProductController implements IProductController {
    private int catId = 0;
    private final HomeController homeController;
    private final ProductsPage productsPage;
    private final CartController cartController;

    public ProductController(HomeController homeController) {
        this.homeController = homeController;
        this.productsPage = new ProductsPage();
        this.cartController =new CartController(homeController);
    }

    @Override
    public void showProducts(int catId) {
      println(StringUtils.PRODUCT_WELCOME);
        this.catId = catId;
        ArrayList<Product> products = getProducts();
        if (catId != 0) {
            ArrayList<Product> categoryProducts = new ArrayList<>();
            println(StringUtils.STYLE);
            println(StringUtils.PRODUCT_MENU);
            println(StringUtils.STYLE);
            for (Product product : products) {
                if (product.getCategory().getId() == catId) {
                    categoryProducts.add(product);
                }
            }
            products = categoryProducts;
        }

        productsPage.printProducts(products);

        try {
            int choice = enterInt(StringUtils.ENTER_CHOICE);
            int validProductId = 0;

            if (choice == 99) {
                homeController.printMenu();
            } else {
                for (Product product : products) {
                    if (product.getId() == choice) {
                        validProductId = product.getId();
                        break;
                    }
                }

                if (validProductId != 0) {
                    cartController.addToCart(validProductId);
                    productsPage.printSuccess();
                    showProducts(catId);
                } else {
                    invalidChoice(new AppException(StringUtils.INVALID_CHOICE));
                }
            }
        } catch (AppException appException) {
            invalidChoice(appException);
        }
    }

    private void invalidChoice(AppException appException) {
        println(appException.getMessage());
        showProducts(catId);
    }
}
