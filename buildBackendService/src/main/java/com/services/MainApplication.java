package com.services;

import com.services.bean.messageBean.CommonMessage;
import com.services.bean.messageBean.Message;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
@ComponentScan(basePackages = {"com.services.service","com.services.controller","com.services.aspect","com.services.listener"})
@MapperScan("com.services.mapper")
@RestController
public class MainApplication {

    public static void main(String[] args) {
        SpringApplication.run(MainApplication.class, args);
    }

    @GetMapping("/data/hello")
    public Message hello(@RequestParam(value = "name", defaultValue = "World") String name) {
        CommonMessage commonMessage = new CommonMessage();
        commonMessage.setResult(true);
        commonMessage.setMessage("");
        commonMessage.setData(String.format("Hello %s!", name));
        return commonMessage;
    }

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

}
