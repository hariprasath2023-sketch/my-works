package org.example.controller;

import org.example.controller.impl.IAppController;

import org.example.util.AppException;
import org.example.util.LoadUtils;
import org.example.view.WelcomePage;

public class AppController implements IAppController {

    private final WelcomePage welcomePage;
    private final AuthController authController;

    public AppController(){

        this.welcomePage = new WelcomePage();
        this.authController = new AuthController();
    }

    @Override
    public void init() throws AppException {
        LoadUtils.load();
        welcomePage.welcome();
        authController.authMenu();
    }

    @Override
    public void printAuthMenu() throws AppException {
        welcomePage.printAuthMenu();
    }
}
