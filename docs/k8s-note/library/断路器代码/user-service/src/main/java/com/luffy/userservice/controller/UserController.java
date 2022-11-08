package com.luffy.userservice.controller;


import com.luffy.userservice.entity.User;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.Random;

@RestController
public class UserController {

    @GetMapping("/user")
    public String getUserService(){
        return "this is user-service";
    }

    @GetMapping("/user-nums")
    public Integer getUserNums(){
        return new Random().nextInt(100);
    }

    //{"id": 123, "name": "张三", "age": 20, "sex": "male"}
    @GetMapping("/user/{id}")
    public User getUserInfo(@PathVariable("id") int id){
        User user = new User();
        user.setId(id);
        user.setAge(20);
        user.setName("zhangsan");
        user.setSex("male");
        return user;
    }
}