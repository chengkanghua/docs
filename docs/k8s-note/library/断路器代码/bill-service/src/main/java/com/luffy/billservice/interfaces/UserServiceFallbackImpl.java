package com.luffy.billservice.interfaces;

import com.luffy.billservice.entity.User;
import org.springframework.stereotype.Component;

@Component("fallback")
public class UserServiceFallbackImpl implements UserServiceCli{

    @Override
    public String getUserService() {
        return "fallback user service";
    }

    @Override
    public User getUserInfo(int id) {
        User user = new User();
        user.setId(1);
        user.setName("feign-fallback");
        return user;
    }
}