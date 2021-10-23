package com.services.mapper;

import com.services.bean.UserBean;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Component;

//DAO层访问数据库接口文件

@Component
public interface UserMapper {

    @Select("select * from user where id = #{id}")
    UserBean selectUserById(int id);

    @Select("select * from user where name = #{name}")
    UserBean selectUserByName(String name);

    @Insert("insert into user(name,password,client_tag) values (#{name},#{password},#{client_tag})")
    int insertUser(UserBean user);
}
