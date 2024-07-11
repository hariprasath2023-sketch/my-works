package org.example.util;

import org.example.models.Category;
import org.example.models.Product;
import org.example.models.Role;
import org.example.models.User;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class LoadUtils {
    private static ArrayList<Category> categories = new ArrayList<>();
    private static ArrayList<Product> products = new ArrayList<>();
    public static void load(){
        try {
            Scanner scanner = new Scanner(FileUtil.getCategoriesFile());
            while (scanner.hasNext()) {
                String value = scanner.next().trim();
                if (!value.startsWith("id")) {
                    String[] catArray = value.split(",");
                    categories.add(new Category((Integer.parseInt(catArray[0])),catArray[1]));
                }
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        try {
            Scanner scanner = new Scanner(FileUtil.getProductFile());
            while (scanner.hasNext()) {
                String value = scanner.next().trim();
                if (!value.startsWith("id")) {
                    String[] prodArray = value.split(",");
                    Category cat = new Category(0,"dummy");
                    for(Category category:categories){
                        if (category.getCategoryName().equals(prodArray[3])){
                            cat = category;
                            break;
                        }
                    }
                    products.add(new Product(Integer.parseInt(prodArray[0]),prodArray[1],Integer.parseInt(prodArray[2]),cat));
                }
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

    }

    public static ArrayList<Category> getCategories() {
        return categories;
    }

    public static ArrayList<Product> getProducts() {
        return products;
    }
}
