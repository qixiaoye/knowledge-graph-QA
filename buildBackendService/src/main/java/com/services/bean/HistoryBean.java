package com.services.bean;

//Bean实体类，依据数据库表，生成set和get方法

public class HistoryBean {
    private int id;
    private String question;
    private String answer;
    // 0 可能答案；1 正确答案
    private int correct_tag;
    // 提问者
    private int asker_id;
    // 回答者
    private int responder_id;

    public int getAsker_id() {
        return asker_id;
    }

    public int getCorrect_tag() {
        return correct_tag;
    }

    public int getId() {
        return id;
    }

    public int getResponder_id() {
        return responder_id;
    }

    public String getAnswer() {
        return answer;
    }

    public String getQuestion() {
        return question;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
    }

    public void setAsker_id(int asker_id) {
        this.asker_id = asker_id;
    }

    public void setCorrect_tag(int correct_tag) {
        this.correct_tag = correct_tag;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public void setResponder_id(int responder_id) {
        this.responder_id = responder_id;
    }

}
