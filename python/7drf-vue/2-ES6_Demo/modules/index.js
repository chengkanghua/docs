// es6模块功能主要有两个命令构成：export和import
// export用于规定模块的对外接口 import用于输入其它模块提供的功能
// 一个模块就是独立的文件

/* export const name = '张三';
export const age = 18;
export function sayName(){
    return 'my name is 小马哥';
} */
// export {sayName}

const name = '张三';
const age = 18;
function sayName() {
    return 'my name is 小马哥';
}
export {
    name,age,sayName
}
/* const obj = {
    foo:'foo'
} */
class Person{
    constructor(){

    }
    sayAge(){
        console.log('16');
        
    }
}

export default Person;
