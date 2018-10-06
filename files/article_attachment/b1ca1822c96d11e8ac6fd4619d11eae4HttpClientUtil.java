package com.example.demo.util;

import org.apache.commons.lang3.StringUtils;
import org.apache.http.NameValuePair;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.entity.UrlEncodedFormEntity;

import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public class HttpClientUtil {
    private static RequestConfig requestConfig;
    private final static String URL_PARAM_INDEX_TAG = "?";
    private static CloseableHttpClient httpClient;

    static  {
        requestConfig = RequestConfig.custom().setConnectTimeout(10000).setSocketTimeout(60000)
                .setConnectionRequestTimeout(2000).build();
        HttpClientBuilder httpClientBuilder = HttpClientBuilder.create();
        httpClientBuilder.setMaxConnTotal(200);
        httpClientBuilder.setMaxConnPerRoute(50);
        httpClient = httpClientBuilder.build();
    }


    public static String get(String url, Map<String, String> params, Map<String, String> headers) throws Exception {
        HttpGet get;
        url = url.replaceAll(" ", "%20");
        if (params != null && params.size() > 0) {
            List<NameValuePair> paramList = new ArrayList<>();
            for (Map.Entry<String, String> entry : params.entrySet()) {
                paramList.add(new BasicNameValuePair(entry.getKey(), entry.getValue()));
            }
            String queryStr = EntityUtils.toString(new UrlEncodedFormEntity(paramList, "utf-8"));
            if (StringUtils.contains(url, URL_PARAM_INDEX_TAG)) {
                get = httpGet(url + "&" + queryStr);
            } else {
                get = httpGet(url + URL_PARAM_INDEX_TAG + queryStr);
            }
        } else {
            get = httpGet(url);
        }
        if (headers != null && headers.size() > 0) {
            for (Map.Entry<String, String> entry : headers.entrySet()) {
                get.setHeader(entry.getKey(), entry.getValue());
            }
        }
        return executeAndGetResult(get);
    }

    public static String post(String url, Map<String, String> paramMap, Map<String, String> headers) throws Exception {
        HttpPost post = httpPost(url);
        if (paramMap != null && paramMap.size() > 0) {
            List<NameValuePair> params = new ArrayList<>();
            for (Map.Entry<String, String> entry : paramMap.entrySet()) {
                params.add(new BasicNameValuePair(entry.getKey(), entry.getValue()));
            }
            post.setEntity(new UrlEncodedFormEntity(params, "utf-8"));
        }
        if (headers != null && headers.size() > 0) {
            for (Map.Entry<String, String> entry : headers.entrySet()) {
                post.setHeader(entry.getKey(), entry.getValue());
            }
        }
        return executeAndGetResult(post);
    }

    public static String post(String url, String json, Map<String, String> headers) throws Exception {
        HttpPost post = httpPost(url);
        if (StringUtils.isNotEmpty(json)) {
            post.setEntity(new StringEntity(json));
        }
        if (headers != null && headers.size() > 0) {
            for (Map.Entry<String, String> entry : headers.entrySet()) {
                post.setHeader(entry.getKey(), entry.getValue());
            }
        }
        return executeAndGetResult(post);
    }

    public String post(String url, String json) throws Exception {
        HttpPost post = httpPost(url);
        if (StringUtils.isNotEmpty(json)) {
            post.setEntity(new StringEntity(json));
        }
        return executeAndGetResult(post);
    }

    private static String executeAndGetResult(HttpUriRequest request) throws IOException {


//        SessionContext sessionContext = SessionContext.get();
//        if (sessionContext != null && StringUtils.isNotEmpty(sessionContext.getToken())) {
//            request.setHeader(TOKEN, sessionContext.getToken());
//        }

        CloseableHttpResponse response = httpClient.execute(request);


        try {
            return EntityUtils.toString(response.getEntity(), "utf-8");
        } finally {
            response.close();
        }
    }


    private static HttpGet httpGet(String requestUrl) {
        HttpGet get = new HttpGet(requestUrl);
        get.setConfig(requestConfig);
        return get;
    }

    private static HttpPost httpPost(String requestUrl) {
        HttpPost post = new HttpPost(requestUrl);
        post.setConfig(requestConfig);
        return post;
    }


    public static String getCurlUrl(String url, Map<String, String> map) {
        String curlUrl = "curl -d";
        if (StringUtils.isNotBlank(url) && map != null && !map.isEmpty()) {
            List<String> keys = new ArrayList<>(map.keySet());
            Collections.sort(keys);
            List<String> keyValueList = new ArrayList<>();
            for (String key : keys) {
                Object value = map.get(key);
                if (value != null) {
                    keyValueList.add(key + "=" + value);
                }
            }
            String queryString = StringUtils.join(keyValueList, "&");
            curlUrl = curlUrl + " '" + queryString + "' " + url;
        }
        return curlUrl;
    }

}