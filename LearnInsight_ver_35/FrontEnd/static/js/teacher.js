document.addEventListener("DOMContentLoaded",function(){
    console.log("Teacher page loaded.");

    initializeRowHover();
    initializeApprovalButtons();
    calculateClassOverview();
    calculateSubmissionOverview();
    initializeSubmissionFilter();
    initializeCommentToggle();
    initializeChatSystem();
    initializeGradeSave();
});

/* -------------------------
   Row Hover
------------------------- */

function initializeRowHover(){

    const rows=document.querySelectorAll(".student-table tbody tr,.request-table tbody tr");

    rows.forEach(function(row){

        row.addEventListener("mouseenter",function(){
            row.classList.add("row-hover");
        });

        row.addEventListener("mouseleave",function(){
            row.classList.remove("row-hover");
        });

    });

}

/* -------------------------
   Approve Reject
------------------------- */

function initializeApprovalButtons(){

    const approveButtons=document.querySelectorAll(".approve-btn");
    const rejectButtons=document.querySelectorAll(".reject-btn");

    approveButtons.forEach(function(button){

        button.addEventListener("click",function(event){

            const confirmed=confirm("Approve this class request?");

            if(!confirmed){
                event.preventDefault();
            }

        });

    });

    rejectButtons.forEach(function(button){

        button.addEventListener("click",function(event){

            const confirmed=confirm("Reject this class request?");

            if(!confirmed){
                event.preventDefault();
            }

        });

    });

}

/* -------------------------
   Class Overview
------------------------- */

function calculateClassOverview(){

    const scores=document.querySelectorAll(".score");
    const studyTimes=document.querySelectorAll(".study-time");
    const students=document.querySelectorAll(".student-name");

    let totalScore=0;
    let totalTime=0;

    scores.forEach(function(scoreElement){
        totalScore+=parseFloat(scoreElement.innerText)||0;
    });

    studyTimes.forEach(function(timeElement){
        totalTime+=parseFloat(timeElement.innerText)||0;
    });

    const avgScore=scores.length?Math.round(totalScore/scores.length):0;

    const studentCountElement=document.getElementById("studentCount");
    const avgScoreElement=document.getElementById("averageScore");
    const totalTimeElement=document.getElementById("totalStudyTime");

    if(studentCountElement){
        studentCountElement.innerText=students.length;
    }

    if(avgScoreElement){
        avgScoreElement.innerText=avgScore;
    }

    if(totalTimeElement){
        totalTimeElement.innerText=totalTime;
    }

    createScoreChart();

}

/* -------------------------
   Score Chart
------------------------- */

let scoreChart=null;

function createScoreChart(){

    if(typeof Chart==="undefined"){
        return;
    }

    const rows=document.querySelectorAll(".student-table tbody tr");

    const labels=[];
    const data=[];

    rows.forEach(function(row){

        const nameElement=row.querySelector(".student-name");
        const scoreElement=row.querySelector(".score");

        if(!nameElement||!scoreElement){
            return;
        }

        const name=nameElement.innerText.trim();
        const score=parseFloat(scoreElement.innerText)||0;

        labels.push(name);
        data.push(score);

    });

    const canvas=document.getElementById("scoreChart");

    if(!canvas){
        return;
    }

    const ctx=canvas.getContext("2d");

    if(scoreChart){
        scoreChart.destroy();
    }

    scoreChart=new Chart(ctx,{
        type:"bar",
        data:{
            labels:labels,
            datasets:[
                {
                    label:"Student Score",
                    data:data,
                    backgroundColor:"#22c55e"
                }
            ]
        },
        options:{
            responsive:true,
            plugins:{
                legend:{
                    display:false
                }
            },
            scales:{
                y:{
                    beginAtZero:true
                }
            }
        }
    });

}

/* -------------------------
   Submission Overview
------------------------- */

function calculateSubmissionOverview(){

    const rows=document.querySelectorAll(".student-table tbody tr");

    if(!rows.length){
        return;
    }

    let submissionCount=0;
    let withFileCount=0;
    let noFileCount=0;

    rows.forEach(function(row){

        const fileCell=row.querySelector("td:nth-child(5)");

        submissionCount++;

        if(fileCell){

            const fileText=fileCell.innerText.trim().toLowerCase();

            if(fileText==="no file"){
                noFileCount++;
            }
            else{
                withFileCount++;
            }

        }

    });

    const submissionCountElement=document.getElementById("submissionCount");
    const withFileCountElement=document.getElementById("withFileCount");
    const noFileCountElement=document.getElementById("noFileCount");

    if(submissionCountElement){
        submissionCountElement.innerText=submissionCount;
    }

    if(withFileCountElement){
        withFileCountElement.innerText=withFileCount;
    }

    if(noFileCountElement){
        noFileCountElement.innerText=noFileCount;
    }

}

/* -------------------------
   Submission Filter
------------------------- */

function initializeSubmissionFilter(){

    const filter=document.getElementById("assignmentFilter");
    const rows=document.querySelectorAll(".student-table tbody tr");

    if(!filter||!rows.length){
        return;
    }

    filter.addEventListener("change",function(){

        const selectedValue=filter.value.trim().toLowerCase();

        rows.forEach(function(row){

            const assignmentCell=row.querySelector("td:nth-child(3)");

            if(!assignmentCell){
                row.style.display="";
                return;
            }

            const assignmentTitle=assignmentCell.innerText.trim().toLowerCase();

            if(selectedValue===""||selectedValue==="all"){
                row.style.display="";
            }
            else if(assignmentTitle===selectedValue){
                row.style.display="";
            }
            else{
                row.style.display="none";
            }

        });

    });

}

/* -------------------------
   Comment Toggle
------------------------- */

function initializeCommentToggle(){

    const buttons=document.querySelectorAll(".toggle-comment-btn");

    buttons.forEach(function(button){

        button.addEventListener("click",function(){

            const targetId=button.getAttribute("data-target");
            const commentBox=document.getElementById(targetId);

            if(!commentBox){
                return;
            }

            if(commentBox.style.display==="none"||commentBox.style.display===""){
                commentBox.style.display="block";
                button.innerText="Hide Comment";
            }
            else{
                commentBox.style.display="none";
                button.innerText="Show Comment";
            }

        });

    });

}

/* -------------------------
   Chat System (Discussion UI)
------------------------- */

function initializeChatSystem(){

    const chatForm=document.getElementById("chatForm");
    const chatInput=document.querySelector(".chat-input");
    const chatWindow=document.querySelector(".chat-window");

    if(!chatForm||!chatInput||!chatWindow){
        return;
    }

    scrollChatToBottom();

    chatForm.addEventListener("submit",function(){

        const message=chatInput.value.trim();

        if(message===""){
            return;
        }

        addTeacherMessage(message);
        scrollChatToBottom();

    });

}

/* Chat Messages */

function addTeacherMessage(text){

    const chatWindow=document.querySelector(".chat-window");

    if(!chatWindow){
        return;
    }

    const row=document.createElement("div");
    row.classList.add("chat-row","teacher");

    const wrapper=document.createElement("div");

    const sender=document.createElement("div");
    sender.classList.add("chat-sender");
    sender.innerText="Teacher";

    const bubble=document.createElement("div");
    bubble.classList.add("chat-message-box","teacher-bubble");
    bubble.innerText=text;

    wrapper.appendChild(sender);
    wrapper.appendChild(bubble);

    row.appendChild(wrapper);
    chatWindow.appendChild(row);

}

function addStudentMessage(text){

    const chatWindow=document.querySelector(".chat-window");

    if(!chatWindow){
        return;
    }

    const row=document.createElement("div");
    row.classList.add("chat-row","student");

    const wrapper=document.createElement("div");

    const sender=document.createElement("div");
    sender.classList.add("chat-sender");
    sender.innerText="Student";

    const bubble=document.createElement("div");
    bubble.classList.add("chat-message-box","student-bubble");
    bubble.innerText=text;

    wrapper.appendChild(sender);
    wrapper.appendChild(bubble);

    row.appendChild(wrapper);
    chatWindow.appendChild(row);

}

/* Scroll Chat */

function scrollChatToBottom(){

    const chatWindow=document.querySelector(".chat-window");

    if(!chatWindow){
        return;
    }

    chatWindow.scrollTop=chatWindow.scrollHeight;

}

/* -------------------------
   Grade Save UI
------------------------- */

function initializeGradeSave(){

    const forms=document.querySelectorAll(".student-table form");

    forms.forEach(function(form){

        form.addEventListener("submit",function(){

            const input=form.querySelector("input[name='grade']");
            const row=form.closest("tr");
            const gradeCell=row.querySelector("td:nth-child(7)");

            if(!input||!gradeCell){
                return;
            }

            const value=input.value;

            if(value!==""){
                gradeCell.innerHTML=`<span class="grade-score">${value}</span>`;
            }

        });

    });

}

document.addEventListener("DOMContentLoaded", function() {

    fetch("/teacher/class-overview-data")
        .then(response => response.json())
        .then(data => {
            document.getElementById("studentCount").innerText = data.student_count
            document.getElementById("averageScore").innerText = data.class_average_score
            document.getElementById("totalStudyTime").innerText = data.class_average_study_time
            const studentNames = data.students.map(s => s.username)
            const studentScores = data.students.map(s => s.avg_grade)
            const studentStudyTime = data.students.map(s => s.total_study_time)
            const scoreCtx = document.getElementById("scoreChart").getContext("2d")
            new Chart(scoreCtx,{
                type:"bar",
                data:{
                    labels:studentNames,
                    datasets:[{
                        label:"Average Grade per Student",
                        data:studentScores,
                        backgroundColor:"#3b82f6"
                    }]
                },
                options:{
                    responsive:true,
                    scales:{
                        y:{beginAtZero:true}
                    }
                }
            })
            const timeCtx = document.getElementById("studyTimeChart").getContext("2d")
            new Chart(timeCtx,{
                type:"bar",
                data:{
                    labels:studentNames,
                    datasets:[{
                        label:"Study Time per Student",
                        data:studentStudyTime,
                        backgroundColor:"#22c55e"
                    }]
                },
                options:{
                    responsive:true,
                    scales:{
                        y:{beginAtZero:true}
                    }
                }
            })
        })
})