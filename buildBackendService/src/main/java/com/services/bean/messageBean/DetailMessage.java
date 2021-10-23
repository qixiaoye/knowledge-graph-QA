package com.services.bean.messageBean;

import com.services.bean.HistoryBean;
import com.services.bean.UserBean;

public class DetailMessage extends Message {
    private HistoryBean historyBean;
    private UserBean asker;
    private UserBean responder;

    public HistoryBean getHistoryBean() {
        return historyBean;
    }

    public UserBean getAsker() {
        return asker;
    }

    public UserBean getResponder() {
        return responder;
    }

    public void setHistoryBean(HistoryBean historyBean) {
        this.historyBean = historyBean;
    }

    public void setAsker(UserBean asker) {
        this.asker = asker;
    }

    public void setResponder(UserBean responder) {
        this.responder = responder;
    }
}
