console.log('Welcome to freetuts.net');

obj_json ={
    "name": "nodejs-freetuts",
    "version": "1.0.0",
    "description": "NodeJS Free Course",
    "main": "index.js",
    "scripts": {
        "test": "echo \"Error: no test specified\" && exit 1"
    },
    "author": "ThehalfHeart",
    "license": "ISC",
    "dependencies": {
        "node-persist": "0.0.8"
    }
}
console.log(obj_json.name);
console.log(obj_json.version);
console.log(obj_json.description);

var student_string = '{"name" : "Nguyen Van Cuong", "age" : "26"}';
var student_obj = JSON.parse(student_string);
console.log("Name: " + student_obj.name);
console.log("Age: " + student_obj.age);
console.log("+++++++JSON to STRING+++++++")
console.log(JSON.stringify(student_obj))

if (1===0){
    console.log("1 == 0")
}
else{
    console.log("1 != 0")
}
sum = 0
for (var i=0; i < 10; i++){
    sum += i
}
console.log("Sum 0-9",sum)