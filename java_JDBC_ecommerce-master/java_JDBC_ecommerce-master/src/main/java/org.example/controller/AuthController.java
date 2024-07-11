package org.example.controller;

import org.example.controller.impl.IAuthController;
import org.example.models.Role;
import org.example.models.User;
import org.example.util.*;
import org.example.view.AuthPage;
import org.example.view.LoginPage;
import org.example.view.RegisterPage;

import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

import static org.example.util.AppInput.enterInt;
import static org.example.util.Utils.println;

public class AuthController implements IAuthController {
    private final HomeController homeController;
    private final LoginPage loginPage;
    private final RegisterPage registerPage;

    private final AuthPage authPage;
    public AuthController() {
        this.loginPage = new LoginPage();
        this.registerPage = new RegisterPage();
        this.homeController = new HomeController(this);
        this.authPage = new AuthPage();
    }

    public void authMenu() throws AppException {
        authPage.printAuthMenu();
        int choice;

        try {
            choice = enterInt(StringUtils.ENTER_CHOICE);
            if (choice ==1){
                login();
            } else if (choice == 2) {
                register();
            } else {
                invalidChoice(new AppException(StringUtils.INVALID_CHOICE));
            }
        } catch (AppException appException) {
            invalidChoice(appException);
        }
    }

    public void login() throws AppException {
      println(StringUtils.LOGIN_MESS);
        String email,password;
        email = AppInput.enterString(StringUtils.ENTER_EMAIL);
        password = AppInput.enterString(StringUtils.ENTER_PASSWORD);
        User user = validateUser(email,password);
        if (user != null){
            UserUtil.setLoggedUser(user);
            homeController.printMenu();
        } else {
            loginPage.printInvalidCredentials();
            authMenu();
        }
    }

    private User validateUser(String email, String password) {
        try {
            Scanner scanner = new Scanner(FileUtil.getCredentialsFile());
            while (scanner.hasNext()) {
                String value = scanner.next().trim();
                if (!value.startsWith("id")) {
                    String[] userArray = value.split(",");
                    if (userArray[2].equals(email) && userArray[3].equals(password)) {
                        User user = new User();
                        user.setId(Integer.parseInt(userArray[0]));
                        user.setName(userArray[1]);
                        user.setEmail(userArray[2]);
                        user.setPassword(userArray[3]);
                      loginPage.loginSuccess();
                        if (user.getEmail().equals("admin@admin.com"))
                            user.setRole(Role.ADMIN);
                        else
                            user.setRole(Role.USER);
                        return user;

                    }

                }

            }

            scanner.close();

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        return null;
    }

    public void register() throws AppException {
      println(StringUtils.REG_MESS);
        String email,password,name,c_password;
        name = AppInput.enterString(StringUtils.ENTER_NAME);
        email =  AppInput.enterString(StringUtils.ENTER_EMAIL);
        password =  AppInput.enterString(StringUtils.ENTER_PASSWORD);
        c_password =  AppInput.enterString(StringUtils.ENTER_PASSWORD_AGAIN);

        if(password.equals(c_password)){
            try {
                FileWriter csv = new FileWriter(FileUtil.getCredentialsFile(),true);
                int id = (int) (Math.random()*100);
                csv.append("\n");
                csv.append(id + "," + name + "," + email + "," + password);
                csv.flush();
                csv.close();
                RegisterPage.printRegistrationSuccessful();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

        }else {
            RegisterPage.passwordMissMatch();
        }
        authMenu();
    }

    @Override
    public void logout() {


    }

    public void invalidChoice(AppException e) throws AppException {
        System.out.println(e.getMessage());
        authMenu();
    }
}
