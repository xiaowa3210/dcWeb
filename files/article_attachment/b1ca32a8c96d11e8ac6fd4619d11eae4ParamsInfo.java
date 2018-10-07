package com.example.demo.util;

import java.util.Map;

public class ParamsInfo {
    public static ThreadLocal<Map<String,String>> PARAMS = new InheritableThreadLocal<>();
}

