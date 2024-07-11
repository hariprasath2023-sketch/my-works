package org.example.util;
import org.example.util.StringUtils;

import java.util.InputMismatchException;

import static org.example.util.AppScanner.getScanner;
import static org.example.util.Utils.print;
public class AppInput {
    public static String enterString(String msg) {
        print(msg);
        return getScanner().nextLine();
    }

    public static int enterInt(String msg) throws AppException {
        print(msg);
        int input;
        try {
            input = Integer.parseInt(getScanner().nextLine());
        } catch (Exception ex) {
            throw new AppException(StringUtils.INVALID_CHOICE);
        }
        return input;
    }
}
