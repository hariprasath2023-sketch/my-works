package org.example.view;

import org.example.util.StringUtils;

import static org.example.util.Utils.println;

public class LoginPage {


    public void printInvalidCredentials(){

        try {


            System.out.println("#---------------------#");
            System.out.println(StringUtils.INVALID_CREDENTIALS);
            System.out.println("#---------------------#");
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

  public void loginSuccess() {
      try
      {
        Thread.sleep(1500);
        println(StringUtils.LOGIN_SUCCESS);
      } catch (Exception e) {
          throw new RuntimeException(e);
      }
  }
}
