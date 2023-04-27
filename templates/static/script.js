$(document).ready(function() {
    let history = [];
  
    function appendMessage(content, sender) {
      const message = $('<div class="message"></div>');
      message.addClass(sender);
      message.text(content);
      $("#chatbox").append(message);
    }
  
    function sendMessage() {
      const userInput = $("#user-input").val().trim();
  
      if (userInput.length === 0) {
        return;
      }
  
      history.push({ role: "user", content: userInput });
      appendMessage(userInput, "user");
      $("#user-input").val("");
  
      $("#submit-btn").prop("disabled", true);
      $("#user-input").prop("disabled", true);
      appendMessage("Typing...", "ai");
  
      const model = $("#model-selection").val();
  
      $.post("/message", { message: userInput, history: JSON.stringify(history), model: model }, function(response) {
        $(".ai").last().remove();
        history.push({ role: "ai", content: response.message });
        appendMessage(response.message, "ai");
  
        $("#submit-btn").prop("disabled", false);
        $("#user-input").prop("disabled", false);
      });
    }
  
    function resetChat() {
      history = [];
      $("#chatbox").empty();
    }
  
    $("#submit-btn").click(sendMessage);
  
    $("#user-input").keypress(function(e) {
      if (e.which === 13 && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
  
    $("#reset-btn").click(resetChat);
  });
  