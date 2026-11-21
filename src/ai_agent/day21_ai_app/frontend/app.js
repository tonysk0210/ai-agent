const button = document.getElementById("researchButton");
const topicInput = document.getElementById("topic");
const status = document.getElementById("status");
const result = document.getElementById("result");

button.addEventListener("click", () => {
    const topic = topicInput.value.trim();

    // 檢查主題是否為空
    if (!topic) {
        status.textContent = "請輸入研究主題。";
        return;
    }

    status.textContent = "準備開始研究。";
    result.textContent = "";
});
