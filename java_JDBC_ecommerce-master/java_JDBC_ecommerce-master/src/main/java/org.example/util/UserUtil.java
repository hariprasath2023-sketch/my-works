package org.example.util;

import org.example.models.User;

public class UserUtil {
    private static User loggedUser;

    public static User getLoggedUser() {
        return loggedUser;
    }

    public static void setLoggedUser(User loggedUser) {
        UserUtil.loggedUser = loggedUser;
    }
}
