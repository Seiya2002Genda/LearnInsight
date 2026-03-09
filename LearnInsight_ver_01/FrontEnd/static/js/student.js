document.addEventListener("DOMContentLoaded",function(){
    console.log("Student page loaded.");

    const materials=document.querySelectorAll(".material-item");
    materials.forEach(item=>{
        item.addEventListener("mouseenter",()=>{
            item.style.background="#f1f5f9";
        });
        item.addEventListener("mouseleave",()=>{
            item.style.background="transparent";
        });
    });

    const tasks=document.querySelectorAll(".task-item");
    tasks.forEach(task=>{
        task.addEventListener("mouseenter",()=>{
            task.style.background="#f1f5f9";
        });
        task.addEventListener("mouseleave",()=>{
            task.style.background="transparent";
        });
    });
});