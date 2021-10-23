package com.services.bean.messageBean;

public class LoginMessage extends Message {
    private int userId;
    private String name;
    private int client_tag;

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getClient_tag() {
        return client_tag;
    }

    public void setClient_tag(int client_tag) {
        this.client_tag = client_tag;
    }
}
