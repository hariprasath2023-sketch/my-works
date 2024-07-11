package org.example.view;

import org.example.util.StringUtils;

import static org.example.util.Utils.println;

public class HomePage {
    public void printMenu() {

      try {
        Thread.sleep(1000);
        println(StringUtils.HOME_WELCOME);
      } catch (InterruptedException e) {
        throw new RuntimeException(e);
      }


        System.out.println(StringUtils.HOME_MENU);
    }
}
