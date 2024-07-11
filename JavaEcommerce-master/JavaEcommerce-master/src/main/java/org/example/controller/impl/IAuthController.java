package org.example.controller.impl;

import org.example.util.AppException;

public interface IAuthController {

    void authMenu() throws AppException;
    void login() throws AppException;
    void register() throws AppException;
    void logout();
}
