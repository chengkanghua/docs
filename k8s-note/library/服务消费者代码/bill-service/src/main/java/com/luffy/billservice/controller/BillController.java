package com.luffy.billservice.controller;

import com.luffy.billservice.entity.User;
import com.luffy.billservice.interfaces.UserServiceCli;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BillController {

    @Autowired
    private UserServiceCli userServiceCli;


    @GetMapping("/bill/user")
    public String getUserInfo(){
        return userServiceCli.getUserService();
    }

    @GetMapping("/bill/user/{id}")
    public User getUserInfo(@PathVariable("id") int id){
        return userServiceCli.getUserInfo(id);
        //return restTemplate.getForObject("http://USER-SERVICE/user/" + id, String.class);
    }
}