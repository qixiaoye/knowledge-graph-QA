package com.services.service;

import com.services.bean.UserBean;
import com.services.mapper.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

//Service层业务接口类编写

@Service
public class UserService{
    private final UserMapper userMapper;

    @Autowired
    public UserService(UserMapper userMapper) {
        this.userMapper = userMapper;
    }

    public UserBean selectUserById(int id) {
        return userMapper.selectUserById(id);
    }

    public UserBean selectUserByName(String name) {
        return userMapper.selectUserByName(name);
    }

    public int insertUser(UserBean user){
        return userMapper.insertUser(user);
    }

}