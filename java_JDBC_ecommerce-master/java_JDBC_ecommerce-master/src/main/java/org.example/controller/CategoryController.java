package org.example.controller;

import org.example.models.Category;
import org.example.util.AppException;
import org.example.util.AppInput;
import org.example.util.LoadUtils;
import org.example.util.StringUtils;
import org.example.view.CategoryPage;

import java.util.ArrayList;

import static org.example.util.Utils.println;

public class CategoryController {
    private final CategoryPage categoryPage;
    private final ProductController productController;
    private final HomeController homeController;

    public CategoryController(HomeController homeController) {

        this.categoryPage = new CategoryPage();
        this.homeController = homeController;
        this.productController = new ProductController(homeController);
    }

    public void printMenu() {
      println(StringUtils.CAT_WELCOME);

        ArrayList<Category> categories = LoadUtils.getCategories();
        categoryPage.printMenu(categories);
        try{
            int choice = AppInput.enterInt(StringUtils.ENTER_CHOICE);
            if (choice == 99){
              homeController.printMenu();
            } else {
                int validCategoryId = 0;
                for (Category category : categories) {
                    if (category.getId() == choice) {
                        validCategoryId = category.getId();
                        break;
                    }
                }
                if(validCategoryId!=0) {
                    productController.showProducts(validCategoryId);
                } else{
                    invalidChoice(new AppException(StringUtils.INVALID_CHOICE));
                }
            }
        }catch (AppException appException) {
            invalidChoice(appException);
        }
    }

    private void invalidChoice(AppException e) {
        System.out.println(e.getMessage());
        printMenu();
    }
}
