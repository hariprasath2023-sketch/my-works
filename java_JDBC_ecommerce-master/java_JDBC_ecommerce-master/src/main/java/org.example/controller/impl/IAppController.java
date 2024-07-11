package org.example.controller.impl;

import org.example.util.AppException;

public interface IAppController {
    void init() throws AppException;
    void printAuthMenu() throws AppException;
}
