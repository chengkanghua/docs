package com.luffy.billservice.interfaces;

import com.luffy.billservice.entity.User;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name="user-service")
public interface UserServiceCli {

    @GetMapping("/user")
    public String getUserService();

    @GetMapping("/user/{id}")
    public User getUserInfo(@PathVariable("id") int id);
}