function myFunction() {
   var toDoList = document.getElementById("todolist");
   var li = document.createElement("li");
   var textfield = document.getElementById("textfield");

   toDoList.appendChild(li);
   li.innerHTML=textfield.value;
}