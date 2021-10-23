package com.services.service;

import com.services.bean.HistoryBean;
import com.services.mapper.HistoryMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

//Service层业务接口类编写

@Service
public class HistoryService {
    private final HistoryMapper historyMapper;

    @Autowired
    public HistoryService(HistoryMapper historyMapper) {
        this.historyMapper = historyMapper;
    }

    public HistoryBean selectHistoryById(int historyId) {
        return historyMapper.selectHistoryById(historyId);
    }

    public HistoryBean[] selectMyQuestionHistories(int asker_id) {
        return historyMapper.selectMyQuestionHistories(asker_id);
    }

    public HistoryBean[] selectMyAnswerHistories(int responder_id) {
        return historyMapper.selectMyAnswerHistories(responder_id);
    }

    public HistoryBean[] selectTotalHistories() {
        return historyMapper.selectTotalHistories();
    }

    public HistoryBean[] selectSystemHistories() {
        return historyMapper.selectSystemHistories();
    }

    public int insertHistory(HistoryBean history){
        return historyMapper.insertHistory(history);
    }

    public int answerHistory(HistoryBean history){
        return historyMapper.answerHistory(history);
    }

    public int markHistory(HistoryBean history){
        return historyMapper.markHistory(history);
    }
}
