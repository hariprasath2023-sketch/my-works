package org.example.controller;

import org.example.util.AppException;
import org.example.util.AppInput;
import org.example.util.StringUtils;
import org.example.view.HomePage;

import static org.example.util.UserUtil.setLoggedUser;
import static org.example.util.Utils.println;

public class HomeController {
    private final HomePage homePage;
    private final AuthController authController;
    private final CategoryController categoryController;
    private  final ProductController productController;
    private  final CartController cartController;
    private final OrderController orderController;


    public HomeController(AuthController authController) {
        this.homePage = new HomePage();
        this.authController = authController;
        this.categoryController = new CategoryController(this);
        this.productController=new ProductController(this);
        this.cartController=new CartController(this);
        orderController = new OrderController(this);
    }

    public void printMenu() {

        homePage.printMenu();
        try {
            int choice = AppInput.enterInt(StringUtils.ENTER_CHOICE);
            if (choice == 1) {
                categoryController.printMenu();
            } else if (choice == 2) {
                productController.showProducts(0);
            } else if (choice == 3) {
                cartController.printCart();
            } else if (choice == 4) {
                orderController.printOrders();
                printMenu();
            } else if (choice == 5) {
              println(StringUtils.LOGOUT_MESS);
                setLoggedUser(null);
                authController.authMenu();
            } else {
                invalidChoice(new AppException(StringUtils.INVALID_CHOICE));
            }

        } catch (AppException e) {
            invalidChoice(e);
        }
    }

    private void invalidChoice(AppException appException) {
        System.out.println(appException.getMessage());
        printMenu();
    }
}
