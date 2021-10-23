package com.services.mapper;

import com.services.bean.HistoryBean;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.springframework.stereotype.Component;

//DAO层访问数据库接口文件

@Component
public interface HistoryMapper {
    @Select("select * from history where id=#{id}")
    HistoryBean selectHistoryById(int id);

    @Select("select * from history")
    HistoryBean[] selectTotalHistories();

    @Select("select * from history where correct_tag=0 or correct_tag=3")
    HistoryBean[] selectSystemHistories();

    @Select("select * from history where asker_id=#{asker_id}")
    HistoryBean[] selectMyQuestionHistories(int asker_id);

    @Select("select * from history where responder_id=#{responder_id}")
    HistoryBean[] selectMyAnswerHistories(int responder_id);

    @Insert("insert into history(question,answer,asker_id,correct_tag) values (#{question},#{answer},#{asker_id},#{correct_tag})")
    int insertHistory(HistoryBean history);

    @Update("update history set answer=#{answer}, correct_tag=#{correct_tag}, responder_id=#{responder_id} where id = #{id}")
    int answerHistory(HistoryBean history);

    @Update("update history set correct_tag=#{correct_tag}, responder_id=#{responder_id} where id = #{id}")
    int markHistory(HistoryBean history);
}
