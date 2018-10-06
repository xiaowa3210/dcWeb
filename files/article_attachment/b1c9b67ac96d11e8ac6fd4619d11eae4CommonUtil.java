package com.example.demo.util;

import com.alibaba.fastjson.JSONObject;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang3.StringUtils;

import java.io.IOException;
import java.io.InputStream;
import java.util.Map;

public class CommonUtil {
    /*
     * 将json文件转换为map
     * */
    public static Map<String,Object> parseJsonFile(String filePath) throws IOException {
        InputStream inputStream = CommonUtil.class.getResourceAsStream(filePath);
        String text = IOUtils.toString(inputStream);
        if (text == null || StringUtils.isEmpty(text)){
            throw new RuntimeException("file to string failed!");
        }
        return (Map) JSONObject.parse(text);
    }
}
