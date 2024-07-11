package org.example.util;

import java.io.File;

public class FileUtil {
    private static File credentialsFile;
    private static File catogoriesFile;
    private static  File productsFile;

    public static File getCredentialsFile() {
        if (credentialsFile == null)
            credentialsFile = new File("src/main/java/org/example/assets/credentials.csv");
        return credentialsFile;
    }

    public static File getCategoriesFile() {
        if (catogoriesFile == null)
            catogoriesFile= new File("src/main/java/org/example/assets/category.csv");
        return catogoriesFile;
    }

    public static File getProductFile() {
        if (productsFile == null)
            productsFile= new File("src/main/java/org/example/assets/products.csv");
        return productsFile;
    }
    public static String getFilePath() {
        return "src/main/java/org/example/assets/";
    }
}
