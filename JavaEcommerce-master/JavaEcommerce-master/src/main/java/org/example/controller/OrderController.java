package org.example.controller;

import org.example.models.CartProduct;
import org.example.models.User;
import org.example.util.AppException;
import org.example.util.StringUtils;
import org.example.view.OrdersPage;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

import static org.example.util.AppInput.enterInt;
import static org.example.util.FileUtil.getFilePath;
import static org.example.util.UserUtil.getLoggedUser;
import static org.example.util.Utils.println;

public class OrderController {

    private final HomeController homeController;
    private final OrdersPage ordersPage;

    public OrderController(HomeController homeController) {
        this.homeController = homeController;
        ordersPage = new OrdersPage();
    }


    public void checkout() {
        User loggedInUser = getLoggedUser();

        try {
            FileWriter fileWriter = new FileWriter(getFilePath() + loggedInUser.getId() + "-" + System.currentTimeMillis() + ".txt");
            fileWriter.write("Your Order are:");
            fileWriter.write("\n");

            double total = 0;
            for (CartProduct cartProduct : loggedInUser.getUserCart().getCartProducts()) {
                total += cartProduct.getCount() * cartProduct.getProduct().getPrice();
                fileWriter.write(cartProduct.getProduct().getTitle() + " x " + cartProduct.getCount() + " = Rs. " + cartProduct.getProduct().getPrice() * cartProduct.getCount());
                fileWriter.write("\n");
            }
            fileWriter.write("Total - Rs. " + total);
            fileWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        getLoggedUser().setUserCart(null);
        ordersPage.printSuccess();
        homeController.printMenu();
    }

    public void printOrders() {
      println(StringUtils.ORDER_WELCOME);
        Map<String, String> files = listFilesForFolder(new File(getFilePath()));
        if (files.isEmpty()) {
            ordersPage.printNoOrders();
            homeController.printMenu();
        } else {
            ordersPage.printOrder(files);
            try {
                int orderId = enterInt(StringUtils.ENTER_CHOICE);
                if (orderId == 99) {
                    homeController.printMenu();
                } else {
                    if (orderId > files.size()) {
                        println(StringUtils.INVALID_CHOICE);
                        printOrders();
                    } else {
                        int id = 1;
                        String path = "";
                        for (final String key : files.keySet()) {
                            if (id == orderId) {
                                path = files.get(key);
                            }
                        }
                        BufferedReader r = new BufferedReader(new FileReader(getFilePath() + path));
                        String line;
                        ordersPage.printDesign();
                        while ((line = r.readLine()) != null) {
                            println(line);
                        }
                        printOrders();
                    }
                }

            } catch (AppException | IOException e) {
                throw new RuntimeException(e);
            }
        }

    }

    private Map<String, String> listFilesForFolder(final File folder) throws RuntimeException {
        Map<String, String> files = new HashMap<>();
        for (final File fileEntry : Objects.requireNonNull(folder.listFiles())) {
            Path path = new File(getFilePath() + fileEntry.getName()).toPath();
            BasicFileAttributes file_att;
            try {
                file_att = Files.readAttributes(
                        path, BasicFileAttributes.class);

                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
                SimpleDateFormat dateFormat = new SimpleDateFormat("MM/dd/yyyy - ");

                Date d = sdf.parse(file_att.creationTime().toString());

                if (fileEntry.getName().startsWith(String.valueOf(getLoggedUser().getId())))
                    files.put(dateFormat.format(d), fileEntry.getName());
            } catch (IOException | ParseException e) {
                throw new RuntimeException(e);
            }

        }
        return files;
    }
}
