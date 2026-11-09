/**
 * chatbot.js - Modern Minimal Chatbot Controller.
 * Starts in an empty state (no welcome messages, no menus).
 * Coordinates conversation state with Python Flask backend.
 */

document.addEventListener("DOMContentLoaded", () => {
  const conversationContainer = document.getElementById("conversationContainer");
  const messagesList = document.getElementById("messagesList");
  const chatForm = document.getElementById("chatForm");
  const messageInput = document.getElementById("messageInput");
  const sendBtn = document.getElementById("sendBtn");
  const typingIndicator = document.getElementById("typingIndicator");
  const botStatus = document.getElementById("botStatus");
  const studentPill = document.getElementById("studentPill");
  const studentPillId = document.getElementById("studentPillId");
  const resetSessionBtn = document.getElementById("resetSessionBtn");
  const menuButtonsArea = document.getElementById("menuButtonsArea");
  const chatBottomAnchor = document.getElementById("chatBottomAnchor");

  // Keep track of client state
  let currentState = "START";
  let authenticatedStudentId = null;

  // Initial load: conversation area is strictly empty (Section: Expected behaviour)

  function formatTimestamp() {
    return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function scrollToBottom() {
    setTimeout(() => {
      chatBottomAnchor.scrollIntoView({ behavior: "smooth" });
    }, 40);
  }

  function escapeHtml(text) {
    if (!text) return "";
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function formatMessageText(text) {
    if (!text) return "";
    const escaped = escapeHtml(text);
    // Convert newlines to <br>
    return escaped.replace(/\n/g, "<br>");
  }

  function appendMessage(sender, text) {
    const isUser = sender === "user";

    const row = document.createElement("div");
    row.className = `message-row ${isUser ? "align-items-end" : "align-items-start"}`;

    // Sender indicator label
    const label = document.createElement("span");
    label.className = `message-sender-label ${isUser ? "text-end" : "text-start"}`;
    label.textContent = isUser ? "You" : "Assistant";
    row.appendChild(label);

    // Bubble
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${isUser ? "user-bubble" : "bot-bubble"}`;
    bubble.innerHTML = formatMessageText(text);

    // Timestamp
    const timeSpan = document.createElement("div");
    timeSpan.className = `chat-time ${isUser ? "text-end text-white-50" : "text-start text-muted"}`;
    timeSpan.textContent = formatTimestamp();
    bubble.appendChild(timeSpan);

    row.appendChild(bubble);
    messagesList.appendChild(row);
    scrollToBottom();
  }

  function resetChatToEmpty() {
    // Resets conversation to initial empty state as requested
    messagesList.innerHTML = "";
    menuButtonsArea.classList.add("d-none");
    studentPill.classList.add("d-none");
    resetSessionBtn.classList.add("d-none");
    botStatus.textContent = "Online";
    messageInput.placeholder = "Type a message (e.g., 'Hi' or 'Hello')...";
    currentState = "START";
    authenticatedStudentId = null;
  }

  async function sendMessage(text) {
    const trimmed = (text || "").trim();
    if (!trimmed) return;

    // Append user message with original text preserved
    appendMessage("user", trimmed);

    // UI busy state
    messageInput.value = "";
    messageInput.disabled = true;
    sendBtn.disabled = true;
    typingIndicator.classList.remove("d-none");
    scrollToBottom();

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });

      const data = await response.json();
      currentState = data.state || currentState;

      // Check if session was reset / logged out
      if (data.reset_chat) {
        resetChatToEmpty();
        return;
      }

      // Append chatbot response
      appendMessage("bot", data.response);

      // Handle verified state & menu visibility
      if (data.is_authenticated && data.state === "VERIFIED") {
        authenticatedStudentId = data.student_id;
        studentPillId.textContent = data.student_id;
        studentPill.classList.remove("d-none");
        resetSessionBtn.classList.remove("d-none");
        botStatus.textContent = `Online • ${data.student_id}`;
        menuButtonsArea.classList.remove("d-none");
        messageInput.placeholder = "Select an option from the menu or type your request...";
      } else if (data.state === "WAITING_FOR_STUDENT_ID") {
        menuButtonsArea.classList.add("d-none");
        messageInput.placeholder = "Enter your Student ID (e.g., S1000)...";
      } else {
        menuButtonsArea.classList.add("d-none");
        messageInput.placeholder = "Type a message (e.g., 'Hi' or 'Hello')...";
      }
    } catch (err) {
      console.error("Communication error:", err);
      appendMessage("bot", "Error: Unable to connect to the server. Please verify Flask is running.");
    } finally {
      typingIndicator.classList.add("d-none");
      messageInput.disabled = false;
      sendBtn.disabled = false;
      messageInput.focus();
      scrollToBottom();
    }
  }

  // Form submission
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendMessage(messageInput.value);
  });

  // Menu button clicks
  document.querySelectorAll(".menu-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const command = btn.getAttribute("data-command");
      sendMessage(command);
    });
  });

  // Reset / Logout button in header
  resetSessionBtn.addEventListener("click", async () => {
    try {
      await fetch("/logout", { method: "POST" });
    } catch (e) {
      console.error(e);
    }
    resetChatToEmpty();
  });
});
