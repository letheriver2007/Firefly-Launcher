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

public class CodeHandler {
    private static final Gson gson = new GsonBuilder().setPrettyPrinting().create();
    private static final String filePath = "./remote.json";
    private static final Type CODE_DATA_LIST_TYPE = new TypeToken<ArrayList<CodeData>>() {}.getType();

    private static List<CodeData> readCodes() {
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
            return gson.fromJson(reader, CODE_DATA_LIST_TYPE);
        } catch (IOException e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }

    private static void writeCodes(List<CodeData> codeDataList) {
        try (FileWriter writer = new FileWriter(filePath)) {
            gson.toJson(codeDataList, writer);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void saveOrUpdateCode(Integer uid, String code) {
        List<CodeData> codes = readCodes();
        CodeData existingCodeData = codes.stream()
                .filter(p -> p.uid.equals(uid))
                .findFirst()
                .orElse(null);

        if (existingCodeData != null) {
            existingCodeData.code = code;
        } else {
            codes.add(new CodeData(uid, code));
        }

        writeCodes(codes);
    }

    public static String getCodeByUid(Integer uid) {
        List<CodeData> codes = readCodes();
        CodeData codeData = codes.stream()
                .filter(p -> p.uid.equals(uid))
                .findFirst()
                .orElse(null);

        return codeData != null ? codeData.code : null;
    }

    private static class CodeData {
        private Integer uid;
        private String code;

        public CodeData(Integer uid, String code) {
            this.uid = uid;
            this.code = code;
        }
    }
}
