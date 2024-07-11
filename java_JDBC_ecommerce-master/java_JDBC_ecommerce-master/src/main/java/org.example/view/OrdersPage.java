package org.example.view;

import org.example.util.StringUtils;

import java.util.Map;

import static org.example.util.Utils.println;

public class OrdersPage {
    public void printSuccess() {
        try {
          Thread.sleep(1000);

            println(StringUtils.PLACE_ORDER);


        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
    public void printOrder(Map<String, String> files) {

        println(StringUtils.ORDERS);

        int id = 1;
        for (Map.Entry<String, String> entry : files.entrySet()) {
            println(id + ". Date = " + entry.getKey() + " OrderId = " + entry.getValue());
            id++;
        }
        println(StringUtils.BACK_OPTION);
    }

    public void printDesign() {
        println("#---------------------#");
    }

    public void printNoOrders() {
        try {
            println("#---------------------#");
            println(StringUtils.NO_ORDER);
            println("#---------------------#");
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
