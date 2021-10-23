package com.services.bean.messageBean;

import com.services.bean.HistoryBean;

public class HistoryMessage extends Message{
    private HistoryBean[] histories;

    public void setHistories(HistoryBean[] histories) {
        this.histories = histories;
    }

    public HistoryBean[] getHistories() {
        return histories;
    }
}
