# day27 SQL强化和实践

![image-20210531085557128](assets/image-20210531085557128.png)

课程目标：练习常见的SQL语句和表结构的设计。

课程概要：

- SQL强化
- 表结构设计（博客系统）



## 1. SQL强化

![image-20210531123055185](assets/image-20210531123055185.png)

1. 根据上图创建  数据库 & 表结构 并 录入数据（可以自行创造数据）。

   ```sql
   create database blogs default charset utf8 collate utf8_general_ci;
   create table class( cid int auto_increment primary key, class varchar(16) not null )charset=utf8;
   create table student( sid int auto_increment primary key, sname char(18) not null, gender char(1) not null, class_id int not null )charset=utf8;
   create table teacher( tid int auto_increment primary key, tname char(18) not null )charset=utf8;
   create table course( cid int auto_increment primary key, cname char(18) not null, teacher_id int not null  )charset=utf8;
   create table score( sid int auto_increment primary key, student_id int not null, course_id int not null, num int not null ) charset=utf8;
   
   -- alter table student add foreign key fk_student_classid (class_id) references class(cid);
   -- alter table course add foreign key fk_course_teacherid (teacher_id) references teacher(tid);
   -- alter table score add foreign key fk_score_studentid (student_id) references student(sid);
   -- alter table score add foreign key fk_socre_courseid (course_id) references course(cid);
   
   alter table student add constraint fk_student_classid foreign key  student(class_id) references class(cid);
   alter table course add constraint fk_course_teacherid foreign key  course(teacher_id) references teacher(tid);
   alter table score add constraint fk_score_studentid foreign key score(student_id) references student(sid);
   alter table score add constraint fk_socre_courseid foreign key score(course_id) references course(cid);
   
   -- 插入数据
   insert into class(caption) values('三年二班');
   insert into class(caption) values('一年三班');
   insert into class(caption) values('三年一班');
   insert into student(sname,gender,class_id) values('钢蛋','女',1);
   insert into student(sname,gender,class_id) values('铁锤','女',1);
   insert into student(sname,gender,class_id) values('三炮','男',2);
   insert into student(sname,gender,class_id) values('张晓峰','男',3);
   insert into student(sname,gender,class_id) values('张飞','男',2);
   insert into student(sname,gender,class_id) values('张晓菲','女',2);
   insert into teacher(tname) values('苍空');
   insert into teacher(tname) values('波多');
   insert into teacher(tname) values('饭岛');
   insert into teacher(tname) values('李三');
   insert into teacher(tname) values('李四');
   insert into course(cname,teacher_id) values('生物',1);
   insert into course(cname,teacher_id) values('体育',2);
   insert into course(cname,teacher_id) values('物理',3);
   insert into score(student_id,course_id,num) values(1,1,60);
   insert into score(student_id,course_id,num) values(1,2,59);
   insert into score(student_id,course_id,num) values(1,3,80);
   insert into score(student_id,course_id,num) values(2,2,100);
   insert into score(student_id,course_id,num) values(2,1,65);
   insert into score(student_id,course_id,num) values(2,2,70);
   insert into score(student_id,course_id,num) values(3,1,50);
   insert into score(student_id,course_id,num) values(3,2,56);
   insert into score(student_id,course_id,num) values(3,2,99);
   insert into score(student_id,course_id,num) values(5,1,56);
   insert into score(student_id,course_id,num) values(5,2,100);
   insert into score(student_id,course_id,num) values(4,1,80);
   insert into score(student_id,course_id,num) values(4,3,75);
   insert into score(student_id,course_id,num) values(6,3,80);
   insert into score(student_id,course_id,num) values(6,3,60);
   
   insert into score(student_id,course_id,num) values(6,1,65);
   ```

   

2. 创建用户 luffy 并赋予此数据库的所有权限。

   ```
   create user 'luffy'@'%' identified by 'root123';
   grant all privileges on blogs.* to 'luffy'@'%';
   flush privileges;
   ```

   

3. 查询姓“李”的老师的个数。

   ```
   select count(tname) from teacher where tname like '李%';
   ```

   

4. 查询姓“张”的学生名单。

   ```
   select sname,gender,class_id from student where sname like '张%';
   ```

   

5. 查询男生、女生的人数。

   ```
   select gender,count(1) from student group by gender;
   ```

   

6. 查询同名同姓学生名单，并统计同名人数。

   ```
   select sname,count(1) from student group by sname having count(1) > 1;
   ```

   

7. 查询 “三年二班” 的所有学生。

   ```
   select * from student where class_id = (select cid from class where caption='二班');
   ```

   

8. 查询 每个 班级的 班级名称、班级人数。

   ```sql
   select class.caption,count(1) from student left join class on student.class_id = class.cid group by class.caption;
   
   select class.caption,count(1) from class left join student on class.cid=student.class_id group by class.caption;
   ```

   

9. 查询成绩小于60分的同学的学号、姓名、成绩、课程名称。

   ```sql
   select student.sid,student.sname,score.num,course.cname from score left join student on score.student_id=student.sid left join course on score.course_id=course.cid where num < 60;
   ```

   

10. 查询选修了 “生物课” 的所有学生ID、学生姓名、成绩。

    ```sql
    select student.sid,student.sname,score.num from student left join score on student.sid=score.sid  where score.course_id=(select cid from course where cname='生物');
    ```

    

11. 查询选修了 “生物课” 且分数低于60的的所有学生ID、学生姓名、成绩。

    ```sql
    select student.sid,student.sname,score.num,score.course_id from student left join score on student.sid=score.sid  where num < 60 and course_id =(select cid from course where cname='生物');
    ```

    

12. 查询所有同学的学号、姓名、选课数、总成绩。

    ```sql
     select student_id,student.sname,count(1),sum(num) from score left join student on score.student_id=student.sid group by student_id;
     
     
    select score.student_id,student.sname,count(1),sum(score.num) from score left join student on student.sid=score.student_id  group by score.student_id;
    
    ```

    

13. 查询各科被选修的学生数。

    ```sql
    select course.cname,count(1) from score left join course on score.course_id=course.cid group by course_id;
    ```

    

14. 查询各科成绩的总分、最高分、最低分，显示：课程ID、课程名称、总分、最高分、最低分。

    ```sql
    select course.cid,course.cname,sum(num),max(num),min(num) from score left join course on score.course_id=course.cid group by course.cid;
    ```

    

15. 查询各科成绩的平均分，显示：课程ID、课程名称、平均分。

    ```sql
    select course.cid,course.cname,avg(num) from score left join course on score.course_id=course.cid group by course.cid;
    ```

    

16. 查询各科成绩的平均分，显示：课程ID、课程名称、平均分（按平均分从大到小排序）。

    ```sql
    select course.cid,course.cname,avg(num) from score left join course on score.course_id=course.cid group by course.cid desc;
    ```

    

17. 查询各科成绩的平均分和及格率，显示：课程ID、课程名称、平均分、及格率。

    ```sql
    select course_id,course.cname,avg(num),sum(case when score.num > 60 then 1 else 0 end)/count(1) *100 as percent from score left join course on score.course_id=course.cid group by course_id;
    ```

    

18. 查询平均成绩大于60的所有学生的学号、平均成绩；。

    ```sql
    select student_id,avg(num) from score group by student_id having avg(num) > 60;
    
    ```

    

19. 查询平均成绩大于85的所有学生的学号、平均成绩、姓名。

    ```sql
    select student_id,avg(num),student.sname from score left join student on score.student_id=student.sid group by student_id having avg(num) > 85;
    ```

    

20. 查询 “三年二班”  每个学生的 学号、姓名、总成绩、平均成绩。

    ```
    select student_id,student.sname,sum(num),avg(num) from score left join student on score.student_id=student.sid group by student_id;
    ```

    

21. 查询各个班级的班级名称、总成绩、平均成绩、及格率（按平均成绩从大到小排序）。

    ```sql
    select class.cid,class.caption,sum(score.num),avg(num) as avg,sum(case when score.num > 60 then 1 else 0 end)/count(1) *100 as percent from score
    left join student on score.student_id=student.sid left join class on class.cid=student.class_id group by class.cid order by avg desc;
    
    ```

    

22. 查询学过 “波多” 老师课的同学的学号、姓名。

    ```sql
    select student.sid,student.sname from score left join student on score.student_id=student.sid left join course on score.course_id=course.cid left join teacher on course.teacher_id=teacher.tid where teacher.tname='波多';
    
    ```

    

23. 查询没学过 “波多” 老师课的同学的学号、姓名。

    ```sql
    select * from student where sid not in( select student.sid from score left join student ON score.student_id=student.sid left join course on score.course_id=course.cid left join teacher on course.teacher_id=teacher.tid where teacher.tname='波多');
    
    ```

    

24. 查询选修 “苍空” 老师所授课程的学生中，成绩最高的学生姓名及其成绩（不考虑并列）。

    ```sql
    select student.sname,max(score.num)as grade  from score left join student on score.student_id=student.sid left join course ON score.course_id=course.cid left join teacher ON course.teacher_id=teacher.tid where teacher.tname='苍空' group by student.sname  desc limit 1;
    ```

    

25. 查询选修 “苍空” 老师所授课程的学生中，成绩最高的学生姓名及其成绩（考虑并列）。

    ```sql
    select student.sname,score.num from score left join student on score.student_id=student.sid left join course ON score.course_id=course.cid left join teacher ON course.teacher_id=teacher.tid where teacher.tname='苍空' and score.num=(select max(num) from score left join course ON score.course_id=course.cid left join teacher ON course.teacher_id=teacher.tid where teacher.tname='苍空');
    
    ```

    

26. 查询只选修了一门课程的全部学生的学号、姓名。

    ```sql
    select student.sid,student.sname from score left join student ON score.student_id=student.sid group by score.student_id having count(1) =1;
    
    ```

    

27. 查询至少选修两门课程的学生学号、学生姓名、选修课程数量。

    ```sql
    select student.sid,student.sname,count(1) as course_num from score left join student ON score.student_id=student.sid group by score.student_id hav
    ing count(1) >=2;
    ```

    

28. 查询两门及以上不及格的同学的学号、学生姓名、选修课程数量。

    ```sQl
    select score.student_id,student.sname,sum(case when score.num < 60 then 1 else 0 end) as bjg_num from score left join student ON score.student_id=student.sid group by score.student_id having bjg_num >=2;
    
    ```

    

29. 查询选修了所有课程的学生的学号、姓名。

    ```sql
    select score.student_id,student.sname,count(1) from score left join student ON score.student_id=student.sid group by score.student_id having count(1)=(select count(1) from course);
    -- 这个结果的前提是每个学生不能重复报同一门课。
    
    ```

    

30. 查询未选修所有课程的学生的学号、姓名。

    ```sql
    select score.student_id,student.sname,count(1) from score left join student ON score.student_id=student.sid group by score.student_id having count(1) != (select count(1) from course);
    -- 这个结果的前提是每个学生不能重复报同一门课。
    ```

    

31. 查询所有学生都选修了的课程的课程号、课程名。

    ```sql
    
    select score.course_id,course.cname from score left join course ON score.course_id=course.cid group by course_id having count(1) = (select count(1) from student);
    ```

    

32. 查询选修 “生物” 和 “物理” 课程的所有学生学号、姓名。

    ```sql
    select student.sid,student.sname from score left join course ON score.student_id=course.cid left join student ON score.student_id=student.sid where course.cname in ('生物','物理') group by student_id having count(1) >=2;
    
    ```

    

33. 查询至少有一门课与学号为“1”的学生所选的课程相同的其他学生学号 和 姓名 。

    ```sql
    select student.sid,student.sname from score left join course ON score.course_id=course.cid left join student ON score.student_id=student.sid where score.course_id in (select course_id from score where student_id=1) and score.student_id !=1 group by student_id having count(1) >=1;
    
    ```

    

34. 查询与学号为 “2” 的同学选修的课程完全相同的其他 学生学号 和 姓名 。

    ```sql
     #方法一
     SELECT 
     student.sid, student.sname,group_concat(score.course_id) 
     FROM score 
     LEFT JOIN student ON score.student_id = student.sid 
     WHERE (select sum(course_id) from score where student_id=student.sid) = ( select sum(course_id) from score where student_id=2) 
     and (select count(1) from score where student_id=student.sid) = (select count(1) from score where student_id=2) 
     and student_id !=2
     GROUP BY student_id;
     #方法二
    SELECT  student.sid,student.sname /*,group_concat(score.course_id) as lis,count(score.course_id) as coun,sum(score.course_id)as su */ FROM score LEFT JOIN student ON score.student_id = student.sid  group by student.sid having ( select sum(course_id) from score where student_id=2) =sum(score.course_id) and ( select count(course_id) from score where student_id=2) = count(score.course_id) and student.sid !=2;  
      
    --  有问题 待解决
    
    SELECT 
    student.sid, student.sname
    FROM score 
    LEFT JOIN student ON score.student_id = student.sid 
    WHERE score.course_id in ( select course_id from score where student_id=2)  
    and (select count(1) from score where student_id=student.sid) = (select count(1) from score where student_id=2) 
    and student.sid !=2
    GROUP BY student_id;
    
    
    score那块改成先按照student_id,course_id,排序,然后group by分组，接着grouo_concat拼接course_id，再having过滤就差不多了
    SELECT 
    student.sid, student.sname,
    case when score.course_id where exists (group_concat(score.course_id)) 0 else score.course_id end as stat ,
    count(score.course_id)as cou,sum(score.course_id)as su
    FROM score 
    LEFT JOIN student ON score.student_id = student.sid 
    group by student.sid 
    
    
    select course_id from score where exists (select course_id from score where student_id=2);
    
    
    ```

    

35. 查询“生物”课程比“物理”课程成绩高的所有学生的学号；

    ```sql
    SELECT student_id, max(case cname WHEN "生物" then num else -1 end) as sw, max(case cname WHEN "物理" then num else -1 end) as wl FROM score left
    join course ON score.course_id=course.cid where cname in ('生物','物理') group by student_id having sw > wl;
    -- 这个结果包括了没报其中一门的课的学生， 例如： 物理没报 -1 只报了生物课的也算进去了
    
    
    # 查询同时报了生物和物理课的学生，并且生物比物理课程成绩高的学生。
    select student.sid,student.sname,max(case cname when '生物' then num else 0 end) as sw,max(case cname when '物理' then num else 0 end) as wl from
    score left join student on score.student_id=student.sid left join course ON score.course_id=course.cid where course.cname in ('生物','物理') group by student_id having count(score.num) > 1 and sw > wl;
    
    
    ```

    

36. 查询每门课程成绩最好的前3名 (不考虑成绩并列情况) 。

    ```sql
    SELECT cid,cname, -- 添加分数列
    ( select student.sname from score left join student on student.sid = score.student_id where course_id = course.cid order by num desc limit 1 offset 0) as "第1名",
    ( select score.num from score left join student on student.sid = score.student_id where course_id = course.cid order by num desc limit 1 offset 0) as "num",
    ( select student.sname from score left join student on student.sid = score.student_id where course_id = course.cid order by num desc limit 1 offset 1) as "第2名",
    ( select score.num from score left join student on student.sid = score.student_id where course_id = course.cid order by num desc limit 1 offset 1) as "num",
    ( select student.sname from score left join student on student.sid = score.student_id where course_id = course.cid order by num desc limit 1 offset 2) as "第3名",
    ( select score.num from score left join student on student.sid = score.student_id where course_id = course.cid order by num desc limit 1 offset 2) as "num"
    FROM course;
    
    +-----+--------+-----------+------+-----------+------+-----------+------+
    | cid | cname  | 第1名     | num  | 第2名     | num  | 第3名     | num  |
    +-----+--------+-----------+------+-----------+------+-----------+------+
    |   1 | 生物   | 张晓峰    |   80 | 铁锤      |   65 | 铁锤      |   65 |
    |   2 | 体育   | 铁锤      |  100 | 张飞      |  100 | 三炮      |   99 |
    |   3 | 物理   | 钢蛋      |   80 | 张晓菲    |   80 | 张晓峰    |   75 |
    +-----+--------+-----------+------+-----------+------+-----------+------+
    3 rows in set (0.00 sec)
    ```

    

37. 查询每门课程成绩最好的前3名 (考虑成绩并列情况) 。

    ```sql
    select *   -- 课件sql 学生姓名没显示 学生分数没做排序。
    from score 
    left join (
    SELECT cid,cname,
    ( select num from score  where course_id = course.cid GROUP BY num order by num desc limit 1 offset 0) as "最高分",
    ( select num from score  where course_id = course.cid GROUP BY num order by num desc limit 1 offset 1) as "第二高分",
    ( select num from score  where course_id = course.cid GROUP BY num order by num desc limit 1 offset 2) as third
    FROM course ) as C on score.course_id = C.cid 
    WHERE score.num >= C.third; 
    
    
    select score.sid,student.sname,score.num,C.cname,C.first,C.second,C.third  -- 优化sql
    from score  
    left join 
    ( SELECT cid,cname, ( select num from score  where course_id = course.cid GROUP BY num order by num desc limit 1 offset 0) as first, 
    ( select num from score  where course_id = course.cid GROUP BY num order by num desc limit 1 offset 1) as second, 
    ( select num from score  where course_id = course.cid GROUP BY num order by num desc limit 1 offset 2) as third 
    FROM course ) as C 
    on score.course_id = C.cid 
    left join student ON score.student_id=student.sid  
    WHERE score.num >= C.third order by cid asc,num desc;
    +-----+-----------+-----+--------+-------+--------+-------+
    | sid | sname     | num | cname  | first | second | third |
    +-----+-----------+-----+--------+-------+--------+-------+
    |   6 | 张晓峰    |  80 | 生物   |    80 |     65 |    56 |
    |  13 | 铁锤      |  65 | 生物   |    80 |     65 |    56 |
    |  15 | 张晓菲    |  65 | 生物   |    80 |     65 |    56 |
    |   5 | 张飞      |  56 | 生物   |    80 |     65 |    56 |
    |   3 | 铁锤      | 100 | 体育   |   100 |     99 |    59 |
    |   7 | 张飞      | 100 | 体育   |   100 |     99 |    59 |
    |  16 | 三炮      |  99 | 体育   |   100 |     99 |    59 |
    |   2 | 钢蛋      |  59 | 体育   |   100 |     99 |    59 |
    |  19 | 张晓菲    |  80 | 物理   |    80 |     75 |    60 |
    |  11 | 钢蛋      |  80 | 物理   |    80 |     75 |    60 |
    |  18 | 张晓峰    |  75 | 物理   |    80 |     75 |    60 |
    |  17 | 张晓峰    |  75 | 物理   |    80 |     75 |    60 |
    |  20 | 张晓菲    |  60 | 物理   |    80 |     75 |    60 |
    +-----+-----------+-----+--------+-------+--------+-------+
    13 rows in set (0.00 sec)
    
    ```

    

38. 创建一个表 `sc`，然后将 score 表中所有数据插入到 sc 表中。

    ```sql
    CREATE TABLE `sc` (
      `sid` int(11) NOT NULL AUTO_INCREMENT,
      `student_id` int(11) NOT NULL,
      `course_id` int(11) NOT NULL,
      `num` int(11) NOT NULL,
      PRIMARY KEY (`sid`),
      CONSTRAINT `fk_sc_studentid` FOREIGN KEY (`student_id`) REFERENCES `student` (`sid`),
      CONSTRAINT `fk_sc_courseid` FOREIGN KEY (`course_id`) REFERENCES `course` (`cid`)
    )DEFAULT CHARSET=utf8;
    
    insert into from select * from score;
    
    ```

    

39. 向 sc 表中插入一些记录，这些记录要求符合以下条件：
    - 学生ID为：没上过课程ID为 “2” 课程的学生的 学号；
    - 课程ID为：2
    - 成绩为：80

    ```sql
    
    insert into sc(student_id,course_id,num) select sid,2,80 from student where sid not in (select student_id from score where course_id=2);
    ```

    

40. 向 sc 表中插入一些记录，这些记录要求符合以下条件：
    - 学生ID为：没上过课程ID为 “2” 课程的学生的 学号。
    - 课程ID为：2。
    - 成绩为：课程ID为3的最高分。

```sql
select sid,2,(select max(num) from score where course_id=3)as num from student where sid not in (select student_id f
rom score where course_id=2); -- 需要插入的数据

insert into sc(student_id,course_id,num) select sid,2,(select max(num) from score where course_id=3)as num from student where sid not in (select student_id from score where course_id=2);

```





## 2. 设计表结构

根据如下的业务需求设计相应的表结构，内部需涵盖如下功能。

- 注册
- 登录
- 发布博客
- 查看博客列表，显示博客标题、创建时间、阅读数量、评论数量、赞数量等。
- 博客详细，显示博文详细、评论 等。
  - 发表评论
  - 赞 or 踩
  - 阅读数量 + 1

参考如下图片请根据如下功能来设计相应的表结构。



注意：只需要设计表结构，不需要用python代码实现具体的功能（再学一点知识点后再更好的去实现）。



### 2.1 注册和登录

![image-20210520204812764](assets/image-20210520204812764.png)

### 2.2 文章列表

![image-20210520204735867](assets/image-20210520204735867.png)





### 2.3 文章详细

![image-20210520205148509](assets/image-20210520205148509.png)



### 2.4 评论 & 阅读 & 赞 & 踩

![image-20210520205332907](assets/image-20210520205332907.png)

注意：假设都是一级评论（不能回复评论）。

```sql

create database if not exists cnblogs default charset utf8 collate utf8_general_ci;
use cnblogs

create table user(  
  id int not null auto_increment primary key,
  username varchar(16) not null,
  nickname varchar(16) not null,
  password varchar(64) not null,
  cellphone char(11) not null,
  email varchar(64) not null,
  ctime datetime not null
)default charset=utf8;

create table article(   -- 文章
	id int not null auto_increment primary key,
  title varchar(255) not null,   -- 标题
  text text not null, -- 文章内容
  read_count int default 0,   -- 阅读数
  comment_count int default 0,   -- 评论数
  support_count int default null,     -- 赞 数量
  step_count   int default null,      -- 踩 数量
  user_id int not null,      -- 外键userid
  ctime datetime not null   -- 发布时间
)default charset=utf8;


create table comment(    -- 评论
  id int not null auto_increment primary key,
  content varchar(255) not null, -- 内容
  user_id int not null,        -- 外键用户id
  article_id int not null,      -- 外键 essay-id
  ctime datetime not null         -- 时间
)default charset=utf8;

create table up_down(
	id int not null auto_increment primary key,
  choice tinyint not null, -- 1 赞 0踩
  user_id int not null, -- 外键用户id
  article_id int not null, -- 外键文章id
  ctime datetime not null -- 创建时间
)default charset=utf8;


alter table article add constraint fk_article_user foreign key (user_id) references user(id); 
alter table comment add constraint fk_comment_user foreign key (user_id) references user(id);
alter table comment add constraint fk_comment_article foreign key (article_id) references article(id);
alter table up_down add constraint fk_up_down_user foreign key (user_id) references user(id);
alter table up_down add constraint fk_up_down_article foreign key (article_id) references article(id);



# 数据库导出  包含 数据和表结构
$ mysqldump -u root -p database_name table_name > dump.txt
# -d 表示指导出表结构
mysqldump -uroot -p -d databasename > createtab.sql，

# 导入进去,先创建好数据名称
mysql -u root -p database_name < dump.txt
```









