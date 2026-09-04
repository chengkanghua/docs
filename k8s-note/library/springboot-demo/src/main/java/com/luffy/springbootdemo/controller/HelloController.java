package com.luffy.springbootdemo.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

@RestController
public class HelloController {

    @RequestMapping(value = "/hello", method = RequestMethod.GET)
    public String hello(String name) {
        return "Hello, " + name;
    }

    @RequestMapping("/")
    public ModelAndView index(ModelAndView mv) {
        mv.setViewName("index");
        mv.addObject("requestname", "This is index");
        return mv;
    }

    @RequestMapping("/rightaway")
    public ModelAndView returnRightAway(ModelAndView mv) {
        mv.setViewName("index");
        mv.addObject("requestname","This request is RightawayApi");
        return mv;
    }

    @RequestMapping("/sleep")
    public ModelAndView returnSleep(ModelAndView mv) throws InterruptedException {
        Thread.sleep(2*1000);
        mv.setViewName("index");
        mv.addObject("requestname","This request is SleepApi"+",it will sleep 2s !");
        return mv;
    }
}