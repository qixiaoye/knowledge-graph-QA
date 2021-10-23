package com.services.controller;

import com.services.bean.UserBean;
import com.services.bean.messageBean.*;
import com.services.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;

//@Controller注解，项目启动时，SpringBoot会自动扫描加载Controller
//Controller层，实现与web前端的交互

@RestController
public class UserController {

    private final UserService userService;

    @Autowired //将Service注入Web层
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // 注册
    @RequestMapping(value = "/data/user/register", method = RequestMethod.GET)
    public Message register(@RequestParam(value = "name") String name,
                            @RequestParam(value = "password") String password,
                            @RequestParam(value = "client_tag") int client_tag){
        Message message = new Message();
        if(name == null || password == null || "".equals(name) || "".equals(password)){
            message.setResult(false);
            message.setMessage("用户名和密码不能为空。");
            return message;
        }
        if(userService.selectUserByName(name) != null){
            message.setResult(false);
            message.setMessage("用户名已被使用。");
            return message;
        }
        UserBean user = new UserBean();
        user.setName(name);
        user.setPassword(password);
        user.setClient_tag(client_tag);
        if(userService.insertUser(user) != 0){
            message.setResult(true);
            return message;
        }
        message.setResult(false);
        return message;
    }

    // 登录
    @RequestMapping(value = "/data/user/login", method = RequestMethod.GET)
    public Message login(@RequestParam(value = "name") String name,
                         @RequestParam(value = "password") String password,
                         HttpSession session){
        Message message = new Message();
        if(name == null && password == null ||  "".equals(name) || "".equals(password)){
            message.setResult(false);
            message.setMessage("用户名和密码不能为空。");
            return message;
        }
        if(userService.selectUserByName(name) == null){
            message.setResult(false);
            message.setMessage("用户不存在。");
            return message;
        }
        UserBean user = userService.selectUserByName(name);
        if(user.getPassword().equals(password)){
            session.setAttribute("userId",user.getId());  //用session保存了登录的用户
            LoginMessage loginMessage = new LoginMessage();
            loginMessage.setResult(true);
            loginMessage.setUserId(user.getId());
            loginMessage.setName(user.getName());
            loginMessage.setClient_tag(user.getClient_tag());
            return loginMessage;
        }
        message.setResult(false);
        message.setMessage("用户名或密码错误。");
        return message;
    }

    // 登出
    @RequestMapping(value = "/data/user/logout", method = RequestMethod.GET)
    public Message logout(HttpSession session){
        Message message = new Message();
        if(session.getAttribute("userId") != null){
            session.removeAttribute("userId");
            message.setResult(true);
            return message;
        }
        message.setResult(false);
        message.setMessage("用户登出失败。");
        return message;
    }

}
