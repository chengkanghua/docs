# day01作业

1. 整理今日课程的思维导图并导出成图片。

2. Python3的默认解释器编码是什么。

3. 列举变量名的命名规范和建议。

4. 如下那个变量名是正确的。

   ```
   name = '武沛齐'
   _ = 'alex'
   _9 = "wupeiqi"
   9name = "日天"
   luffy(edu = 666
   ```

5. 目前你了解的哪些值转换成布尔值是False。

6. 看代码写结果

   ```python
   nickname = "一米八大高个"
   username = nickname
   nickname = "弟弟"
   
   print(nickname)
   print(username)
   ```

   ```python
   string_number = "20"
   num = int(string_number)
   
   data = string_number * 3
   print(data)
   
   value = num * 3
   print(value)
   ```

7. 看代码写结果

   ```python
   v1 = 8 or 3 and 4 or 2 and 0 or 9 and 7
   print(v1)
   
   v2 = 0 or 2 and 3 and 4 or 6 and 0 or 3
   print(v2)
   ```

8. 实现用户登录系统，并且要支持连续三次输错之后直接退出，并且在每次输错误时显示剩余错误次数（提示：使⽤字符串格式化）。

9. 猜年龄游戏 
   要求：允许用户最多尝试3次，3次都没猜对的话，就直接退出，如果猜对了，打印恭喜信息并退出。

10. 猜年龄游戏升级版
    要求：允许用户最多尝试3次，每尝试3次后，如果还没猜对，就问用户是否还想继续玩，如果回答Y，就继续让其猜3次，以此往复，如果回答N，就退出程序，如何猜对了，就直接退出。