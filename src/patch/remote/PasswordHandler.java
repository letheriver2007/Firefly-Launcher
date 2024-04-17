package emu.lunarcore.server.http.handlers;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import java.io.File;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class PasswordHandler {
    private static final Gson gson = new GsonBuilder().setPrettyPrinting().create();
    private static final String filePath = "./remote.json";
    private static final Type PASSWORD_DATA_LIST_TYPE = new TypeToken<ArrayList<PasswordData>>() {}.getType();

    private static List<PasswordData> readPasswords() {
        File file = new File(filePath);
        if (!file.exists()) {
            try {
                file.createNewFile();
                return new ArrayList<>();
            } catch (IOException e) {
                e.printStackTrace();
                return new ArrayList<>();
            }
        }
        try (FileReader reader = new FileReader(filePath)) {
            return gson.fromJson(reader, PASSWORD_DATA_LIST_TYPE);
        } catch (IOException e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }

    private static void writePasswords(List<PasswordData> passwordDataList) {
        try (FileWriter writer = new FileWriter(filePath)) {
            gson.toJson(passwordDataList, writer);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void saveOrUpdatePassword(Integer uid, String password) {
        List<PasswordData> passwords = readPasswords();
        PasswordData existingPasswordData = passwords.stream()
                .filter(p -> p.uid.equals(uid))
                .findFirst()
                .orElse(null);

        String encryptedPassword = hashWithMD5(password);

        if (existingPasswordData != null) {
            existingPasswordData.password = encryptedPassword;
        } else {
            passwords.add(new PasswordData(uid, encryptedPassword));
        }

        writePasswords(passwords);
    }

    public static String getPasswordByUid(Integer uid) {
        List<PasswordData> passwords = readPasswords();
        PasswordData passwordData = passwords.stream()
                .filter(p -> p.uid.equals(uid))
                .findFirst()
                .orElse(null);

        return passwordData != null ? passwordData.password : null;
    }

    private static class PasswordData {
        private Integer uid;
        private String password;

        public PasswordData(Integer uid, String password) {
            this.uid = uid;
            this.password = password;
        }
    }
    
    private static String bytesToHex(byte[] hash) {
        StringBuilder hexString = new StringBuilder(2 * hash.length);
        for (int i = 0; i < hash.length; i++) {
            String hex = Integer.toHexString(0xff & hash[i]);
            if (hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString().toUpperCase();
    }
    
    public static String hashWithMD5(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            md.update(password.getBytes());
            byte[] digest = md.digest();
            return bytesToHex(digest);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }
}
