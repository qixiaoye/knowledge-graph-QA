package com.services.bean;

//Bean实体类，依据数据库表，生成set和get方法

public class UserBean {
    private int id;
    private String name;
    private String password;
    // 身份识别：0学生，1老师
    private int client_tag;


    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public int getClient_tag() {
        return client_tag;
    }

    public void setClient_tag(int client_tag) {
        this.client_tag = client_tag;
    }

}