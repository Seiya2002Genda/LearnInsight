document.addEventListener("DOMContentLoaded", () => {
    console.log("Student page loaded.");

    initializeHoverEffects();
    initializeDeleteButtons();
    initializeCompleteButtons();
    initializeChatSystem();
    initializeTeacherFilter();
    initializeLLMChatSystem();
    loadAssignments();
});

/* -------------------------
   Hover Effects
------------------------- */

function initializeHoverEffects() {
    addHoverEffect(".material-item");
    addHoverEffect(".task-item");
    addHoverEffect(".class-item");
    addHoverEffect(".assignment");
    addHoverEffect(".student-table tbody tr");
}

function addHoverEffect(selector) {
    const elements = document.querySelectorAll(selector);

    elements.forEach(element => {
        element.addEventListener("mouseenter", () => {
            element.style.background = "#f1f5f9";
        });

        element.addEventListener("mouseleave", () => {
            element.style.background = "transparent";
        });
    });
}

/* -------------------------
   Delete Confirm
------------------------- */

function initializeDeleteButtons() {
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function (e) {
            const text = this.innerText.trim();

            let message = "Are you sure?";

            if (text.includes("Leave")) {
                message = "Are you sure you want to leave this class?";
            } else if (text.includes("Cancel")) {
                message = "Cancel this class request?";
            } else {
                message = "Are you sure you want to delete this item?";
            }

            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

/* -------------------------
   Complete Confirm
------------------------- */

function initializeCompleteButtons() {
    const completeButtons = document.querySelectorAll(".complete-btn");

    completeButtons.forEach(button => {
        button.addEventListener("click", function (e) {
            if (!confirm("Mark this task as completed?")) {
                e.preventDefault();
            }
        });
    });
}

/* -------------------------
   Chat System (Teacher / Discussion UI)
------------------------- */

function initializeChatSystem() {
    const chatForm = document.getElementById("chatForm");
    const chatInput = document.getElementById("chatInput");
    const chatWindow = document.querySelector(".chat-window");

    if (!chatForm || !chatInput || !chatWindow) {
        return;
    }

    scrollChatToBottom();

    chatForm.addEventListener("submit", () => {
        const message = chatInput.value.trim();

        if (message === "") {
            return;
        }

        addStudentMessage(message);
        scrollChatToBottom();
    });
}

function addStudentMessage(text) {
    const chatWindow = document.querySelector(".chat-window");

    if (!chatWindow) {
        return;
    }

    const row = document.createElement("div");
    row.classList.add("chat-row", "student");

    const wrapper = document.createElement("div");

    const sender = document.createElement("div");
    sender.classList.add("chat-sender");
    sender.innerText = "You";

    const bubble = document.createElement("div");
    bubble.classList.add("chat-message-box", "student-bubble");
    bubble.innerText = text;

    wrapper.appendChild(sender);
    wrapper.appendChild(bubble);

    row.appendChild(wrapper);
    chatWindow.appendChild(row);
}

function addTeacherMessage(text) {
    const chatWindow = document.querySelector(".chat-window");

    if (!chatWindow) {
        return;
    }

    const row = document.createElement("div");
    row.classList.add("chat-row", "teacher");

    const wrapper = document.createElement("div");

    const sender = document.createElement("div");
    sender.classList.add("chat-sender");
    sender.innerText = "Teacher";

    const bubble = document.createElement("div");
    bubble.classList.add("chat-message-box", "teacher-bubble");
    bubble.innerText = text;

    wrapper.appendChild(sender);
    wrapper.appendChild(bubble);

    row.appendChild(wrapper);
    chatWindow.appendChild(row);
}

function scrollChatToBottom() {
    const chatWindow = document.querySelector(".chat-window");

    if (!chatWindow) {
        return;
    }

    chatWindow.scrollTop = chatWindow.scrollHeight;
}

/* -------------------------
   Teacher Filter
------------------------- */

function initializeTeacherFilter() {
    const teacherSelect = document.getElementById("teacherSelect");
    const selectedTeacherInput = document.getElementById("selectedTeacher");

    if (!teacherSelect) {
        return;
    }

    teacherSelect.addEventListener("change", function () {
        const teacher = this.value;

        if (selectedTeacherInput) {
            selectedTeacherInput.value = teacher;
        }
    });
}

/* -------------------------
   Assignment System
------------------------- */

async function loadAssignments() {
    const container = document.getElementById("assignmentList");

    if (!container) {
        return;
    }

    try {
        const response = await fetch("/student/get_assignments");
        const data = await response.json();

        container.innerHTML = "";

        if (!data.data || data.data.length === 0) {
            container.innerHTML = `<p class="no-assignments">No assignments available.</p>`;
            return;
        }

        data.data.forEach(assignment => {
            const assignmentElement = createAssignmentElement(assignment);
            container.appendChild(assignmentElement);
        });

        initializeDynamicAssignmentForms();
        initializeHoverEffects();
    } catch (error) {
        console.error("Assignment load error:", error);
        container.innerHTML = `<p class="error-text">Failed to load assignments.</p>`;
    }
}

function createAssignmentElement(assignment) {
    const div = document.createElement("div");
    div.className = "assignment";

    const status = getAssignmentStatus(assignment);

    const urlHtml = assignment.url
        ? `<a href="${escapeAttribute(assignment.url)}" target="_blank">Open Assignment</a>`
        : "";

    const fileHtml = assignment.file_path
        ? `<a href="/${escapeAttribute(assignment.file_path)}" target="_blank">Download File</a>`
        : "";

    let statusHtml = "";
    let formHtml = "";

    if (status === "complete" || status === "submitted") {
        statusHtml = `<p class="complete-status">Submitted</p>`;
    } else {
        formHtml = `
            <form class="assignment-submit-form" action="/student/submit_assignment/${assignment.id}" method="POST" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <textarea name="comment" placeholder="Add comment"></textarea>
                <button type="submit" class="submit-assignment-btn">Submit Assignment</button>
            </form>
        `;
    }

    div.innerHTML = `
        <h3>${escapeHtml(assignment.title || "")}</h3>
        <p><strong>Class:</strong> ${escapeHtml(assignment.class_name || "")}</p>
        <p>${escapeHtml(assignment.description || "")}</p>
        <p class="teacher">Teacher : ${escapeHtml(assignment.teacher_name || "")}</p>
        <p class="due">Due : ${escapeHtml(assignment.due_date || "")}</p>
        ${urlHtml}
        ${fileHtml}
        ${statusHtml}
        ${formHtml}
    `;

    return div;
}

function getAssignmentStatus(assignment) {
    if (assignment.submitted === 1 || assignment.submitted === true) {
        return "submitted";
    }

    if (assignment.status) {
        return String(assignment.status).toLowerCase();
    }

    return "pending";
}

function initializeDynamicAssignmentForms() {
    const forms = document.querySelectorAll(".assignment-submit-form");

    forms.forEach(form => {
        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            const confirmed = confirm("Submit this assignment?");
            if (!confirmed) {
                return;
            }

            const formData = new FormData(form);

            const fileInput = form.querySelector('input[name="file"]');
            const submitButton = form.querySelector(".submit-assignment-btn");

            if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
                alert("Please select a file.");
                return;
            }

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerText = "Submitting...";
            }

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    body: formData
                });

                if (response.redirected || response.ok) {
                    await loadAssignments();
                    await refreshLearningSummary();
                    window.location.reload();
                    return;
                }

                alert("Failed to submit assignment.");
            } catch (error) {
                console.error("Assignment submit error:", error);
                alert("An error occurred while submitting.");
            } finally {
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.innerText = "Submit Assignment";
                }
            }
        });
    });
}

/* -------------------------
   LLM Chat System
------------------------- */

function initializeLLMChatSystem() {
    const form = document.getElementById("llm-form");
    const input = document.getElementById("llm-input");
    const chatBox = document.getElementById("llm-chat-box");

    if (!form || !input || !chatBox) {
        return;
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const message = input.value.trim();

        if (message === "") {
            return;
        }

        addLLMUserMessage("You", message);
        input.value = "";

        try {
            const response = await fetch("/student/llm-chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message
                })
            });

            const data = await response.json();

            addLLMAIMessage("LLM", data.reply || "No response");

            await refreshLearningSummary();
        } catch (error) {
            console.error("LLM chat error:", error);
            addLLMAIMessage("LLM", "An error occurred while contacting the LLM.");
        }
    });
}

function addLLMUserMessage(user, text) {
    const chatBox = document.getElementById("llm-chat-box");

    if (!chatBox) {
        return;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "message-wrapper user-wrapper";

    const name = document.createElement("div");
    name.className = "message-name";
    name.innerText = user;

    const bubble = document.createElement("div");
    bubble.className = "llm-message user-message";
    bubble.innerText = text;

    wrapper.appendChild(name);
    wrapper.appendChild(bubble);

    chatBox.appendChild(wrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addLLMAIMessage(user, text) {
    const chatBox = document.getElementById("llm-chat-box");

    if (!chatBox) {
        return;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "message-wrapper ai-wrapper";

    const name = document.createElement("div");
    name.className = "message-name";
    name.innerText = user;

    const bubble = document.createElement("div");
    bubble.className = "llm-message ai-message";
    bubble.innerText = text;

    wrapper.appendChild(name);
    wrapper.appendChild(bubble);

    chatBox.appendChild(wrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* -------------------------
   Learning Summary Refresh
------------------------- */

async function refreshLearningSummary() {
    try {
        const response = await fetch("/student/api/learning-summary");
        const data = await response.json();

        const scoreElement = document.getElementById("summary-score");
        const recordsElement = document.getElementById("summary-records");
        const studyElement = document.getElementById("summary-study");
        const trendElement = document.getElementById("summary-trend");

        if (scoreElement && data.average_score !== undefined) {
            scoreElement.innerText = data.average_score;
        }

        if (recordsElement && data.total_records !== undefined) {
            recordsElement.innerText = data.total_records;
        }

        if (studyElement && data.total_study_time !== undefined) {
            studyElement.innerText = data.total_study_time;
        }

        if (trendElement) {
            const avgScore = Number(data.average_score || 0);

            if (avgScore >= 85) {
                trendElement.innerText = "Excellent";
            } else if (avgScore >= 70) {
                trendElement.innerText = "Good Progress";
            } else if (avgScore > 0) {
                trendElement.innerText = "Needs Improvement";
            } else {
                trendElement.innerText = "No Data";
            }
        }
    } catch (error) {
        console.error("Summary update error:", error);
    }
}

/* -------------------------
   Utility
------------------------- */

function escapeHtml(value) {
    const div = document.createElement("div");
    div.innerText = value;
    return div.innerHTML;
}

function escapeAttribute(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

console.log("Student Assignment Submit System Loaded");