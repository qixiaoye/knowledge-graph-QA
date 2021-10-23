package com.services.controller;

import com.services.bean.HistoryBean;
import com.services.bean.UserBean;
import com.services.bean.messageBean.DetailMessage;
import com.services.bean.messageBean.HistoryMessage;
import com.services.bean.messageBean.Message;
import com.services.bean.messageBean.AnswerMessage;
import com.services.service.HistoryService;
import com.services.service.UserService;
import org.json.JSONException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import javax.annotation.Resource;
import javax.servlet.http.HttpSession;

//@Controller注解，项目启动时，SpringBoot会自动扫描加载Controller
//Controller层，实现与web前端的交互

@RestController
public class HistoryController {
    private final HistoryService historyService;
    private final UserService userService;

    @Resource
    private RestTemplate restTemplate;

    @Autowired //将Service注入Web层
    public HistoryController(HistoryService historyService, UserService userService) {
        this.historyService = historyService;
        this.userService = userService;
    }

    // 提出问题（得到答案并插入问题库，返回答案）
    @RequestMapping(value = "/data/history/question", method = RequestMethod.GET)
    public Message question(@RequestParam(value = "question") String question,
                            HttpSession session) throws JSONException {
        Message message =  new Message();
        if (question == null || "".equals(question)){
            message.setResult(false);
            message.setMessage("问题为空，无法解决。");
        }
        if(session.getAttribute("userId") == null){
            message.setResult(false);
            message.setMessage("用户未登录，无法提问。");
            return message;
        }
        HistoryBean history = new HistoryBean();
        history.setQuestion(question);
        // 与问答模块进行连通
        String url = "http://1.117.28.192:8088/chat_robot?question={q}";
        String answer = restTemplate.getForObject(url, String.class, question);
        history.setAnswer(answer);
        history.setAsker_id((Integer) session.getAttribute("userId"));
        history.setCorrect_tag(0);
        System.out.println(history.getQuestion());
        if (historyService.insertHistory(history) != 0) {
            AnswerMessage answerMessage = new AnswerMessage();
            answerMessage.setResult(true);
            answerMessage.setAnswer(history.getAnswer());
            return answerMessage;
        }
        message.setResult(false);
        return message;
    }

    // 回答问题（更新问题库，标记为正确答案）
    @RequestMapping(value = "/data/history/answer", method = RequestMethod.GET)
    public Message answer(@RequestParam(value = "history_id") int history_id,
                          @RequestParam(value = "answer") String answer,
                            HttpSession session) {
        Message message =  new Message();
        if (answer == null || "".equals(answer)){
            message.setResult(false);
            message.setMessage("答案不能为空。");
        }
        if(session.getAttribute("userId") == null){
            message.setResult(false);
            message.setMessage("用户未登录，无法回答。");
            return message;
        }
        if (historyService.selectHistoryById(history_id) == null) {
            message.setResult(false);
            message.setMessage("问题不存在，无法回答。");
            return message;
        }
        HistoryBean history = historyService.selectHistoryById(history_id);
        history.setAnswer(answer);
        history.setResponder_id((Integer) session.getAttribute("userId"));
        history.setCorrect_tag(2);
        if (historyService.answerHistory(history) != 0) {
            message.setResult(true);
            return message;
        }
        message.setResult(false);
        return message;
    }

    // 查看需要回答的问题
    @RequestMapping(value = "/data/history/system", method = RequestMethod.GET)
    public Message system(){
        Message message =  new Message();
        if (historyService.selectTotalHistories() == null) {
            message.setResult(false);
            message.setMessage("暂时没有系统问题。");
            return message;
        }
        HistoryBean[] historyBeans = historyService.selectSystemHistories();
        HistoryMessage historyMessage = new HistoryMessage();
        historyMessage.setResult(true);
        historyMessage.setHistories(historyBeans);
        return historyMessage;
    }

    // 标记答案为正确答案或可能答案（更新问题库）
    @RequestMapping(value = "/data/history/mark", method = RequestMethod.GET)
    public Message mark(@RequestParam(value = "history_id") int history_id,
                          HttpSession session) {
        Message message =  new Message();
        if(session.getAttribute("userId") == null){
            message.setResult(false);
            message.setMessage("用户未登录，无法标记。");
            return message;
        }
        if (historyService.selectHistoryById(history_id) == null) {
            message.setResult(false);
            message.setMessage("问题不存在，无法标记。");
            return message;
        }
        HistoryBean history = historyService.selectHistoryById(history_id);
        history.setCorrect_tag(1);
        history.setResponder_id((Integer) session.getAttribute("userId"));
        if (historyService.markHistory(history) != 0) {
            message.setResult(true);
            return message;
        }
        message.setResult(false);
        return message;
    }

    // 标记答案为可疑答案
    @RequestMapping(value = "/data/history/doubt", method = RequestMethod.GET)
    public Message doubt(@RequestParam(value = "history_id") int history_id,
                          HttpSession session) {
        Message message =  new Message();
        if(session.getAttribute("userId") == null){
            message.setResult(false);
            message.setMessage("用户未登录，无法标记。");
            return message;
        }
        if (historyService.selectHistoryById(history_id) == null) {
            message.setResult(false);
            message.setMessage("问题不存在，无法标记。");
            return message;
        }
        HistoryBean history = historyService.selectHistoryById(history_id);
        history.setCorrect_tag(3);
        history.setResponder_id((Integer) session.getAttribute("userId"));
        if (historyService.markHistory(history) != 0) {
            message.setResult(true);
            return message;
        }
        message.setResult(false);
        return message;
    }

    // 查看所有问题
    @RequestMapping(value = "/data/history/total", method = RequestMethod.GET)
    public Message total(){
        Message message =  new Message();
        if (historyService.selectTotalHistories() == null) {
            message.setResult(false);
            message.setMessage("暂时没有问题。");
            return message;
        }
        HistoryBean[] historyBeans = historyService.selectTotalHistories();
        HistoryMessage historyMessage = new HistoryMessage();
        historyMessage.setResult(true);
        historyMessage.setHistories(historyBeans);
        return historyMessage;
    }

    // 查看我提出的问题
    @RequestMapping(value = "/data/history/my_question", method = RequestMethod.GET)
    public Message myQuestion(HttpSession session){
        Message message =  new Message();
        if(session.getAttribute("userId") == null){
            message.setResult(false);
            message.setMessage("用户未登录，无法查看自己提出的问题。");
            return message;
        }
        if (historyService.selectMyQuestionHistories((Integer) session.getAttribute("userId")) == null) {
            message.setResult(false);
            message.setMessage("没有提出问题。");
            return message;
        }
        HistoryBean[] historyBeans = historyService.selectMyQuestionHistories((Integer) session.getAttribute("userId"));
        HistoryMessage historyMessage = new HistoryMessage();
        historyMessage.setResult(true);
        historyMessage.setHistories(historyBeans);
        return historyMessage;
    }

    // 查看我回答的问题
    @RequestMapping(value = "/data/history/my_answer", method = RequestMethod.GET)
    public Message myAnswer(HttpSession session){
        Message message =  new Message();
        if(session.getAttribute("userId") == null){
            message.setResult(false);
            message.setMessage("用户未登录，无法查看自己回答的问题。");
            return message;
        }
        if (historyService.selectMyAnswerHistories((Integer) session.getAttribute("userId")) == null) {
            message.setResult(false);
            message.setMessage("没有回答问题。");
            return message;
        }
        HistoryBean[] historyBeans = historyService.selectMyAnswerHistories((Integer) session.getAttribute("userId"));
        HistoryMessage historyMessage = new HistoryMessage();
        historyMessage.setResult(true);
        historyMessage.setHistories(historyBeans);
        return historyMessage;
    }

    // 查看问题详情
    @RequestMapping(value = "data/history/detail", method = RequestMethod.GET)
    public Message myAnswer(@RequestParam(value = "history_id") int history_id){
        Message message =  new Message();
        if (historyService.selectHistoryById(history_id) == null) {
            message.setResult(false);
            message.setMessage("问题不存在。");
            return message;
        }
        DetailMessage detailMessage = new DetailMessage();
        HistoryBean historyBean = historyService.selectHistoryById(history_id);
        detailMessage.setHistoryBean(historyBean);
        if (historyBean.getAsker_id() != 0) {
            UserBean userBean = userService.selectUserById(historyBean.getAsker_id());
            detailMessage.setAsker(userBean);
        }
        if (historyBean.getResponder_id() != 0) {
            UserBean userBean = userService.selectUserById(historyBean.getResponder_id());
            detailMessage.setResponder(userBean);
        }
        detailMessage.setResult(true);
        return detailMessage;
    }
}
