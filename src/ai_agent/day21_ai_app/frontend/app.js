const button = document.getElementById("researchButton");
const topicInput = document.getElementById("topic");
const status = document.getElementById("status");
const result = document.getElementById("result");

button.addEventListener("click", async (e) => {
    e.preventDefault(); // 阻止表單提交

    const topic = topicInput.value.trim(); // 移除主題前後的空白字元

    // 檢查主題是否為空
    if (!topic) {
        status.textContent = "請輸入研究主題。";
        return;
    }

    status.textContent = "準備開始研究...";
    result.textContent = "";

    try {
        // 1. 與伺服器通訊以取得研究結果
        const response = await fetch(
            "/chat",
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message: topic}) // {"message":"什麼是 AI agents"}
            });

        if (!response.ok) {
            throw new Error("請求失敗");
        }

        // 2. 解析伺服器回應
        const data = await response.json();

        status.textContent = "研究完成!✨";
        result.textContent = data.response;

    } catch (error) {
        status.textContent = "發生錯誤。";
        result.textContent = "無法完成請求。";
    }
});
