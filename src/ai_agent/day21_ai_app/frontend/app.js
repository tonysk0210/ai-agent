// const button = document.getElementById("researchButton");
// const topicInput = document.getElementById("topic");
// const status = document.getElementById("status");
// const result = document.getElementById("result");
//
// button.addEventListener("click", async (e) => {
//     e.preventDefault(); // 阻止表單提交
//
//     const topic = topicInput.value.trim(); // 移除主題前後的空白字元
//
//     // 檢查主題是否為空
//     if (!topic) {
//         status.textContent = "請輸入研究主題。";
//         return;
//     }
//
//     status.textContent = "準備開始研究...";
//     result.textContent = "";
//
//     try {
//         // 1. 與伺服器通訊以取得研究結果
//         const response = await fetch(
//             "/chat",
//             {
//                 method: "POST",
//                 headers: {"Content-Type": "application/json"},
//                 body: JSON.stringify({message: topic}) // {"message":"什麼是 AI agents"}
//             });
//
//         if (!response.ok) {
//             throw new Error("請求失敗");
//         }
//
//         // 2. 解析伺服器回應
//         const data = await response.json();
//
//         status.textContent = "研究完成!✨";
//         result.textContent = data.response;
//
//     } catch (error) {
//         status.textContent = "發生錯誤。";
//         result.textContent = "無法完成請求。";
//     }
// });

const button = document.getElementById("researchButton");
const topicInput = document.getElementById("topic");
const status = document.getElementById("status");
const result = document.getElementById("result");
const progressSection = document.getElementById("progressSection");
const resultSection = document.getElementById("resultSection");
const errorBox = document.getElementById("error");
const characterCount = document.getElementById("characterCount");

topicInput.addEventListener("input", () => {
    const length = topicInput.value.length;
    characterCount.textContent = `${length} 個字元`;
});

button.addEventListener("click", async () => {
    const topic = topicInput.value.trim();

    if (!topic) {
        errorBox.textContent = "請輸入研究主題。";
        errorBox.classList.remove("hidden");
        return;
    }

    errorBox.classList.add("hidden");
    resultSection.classList.add("hidden");
    progressSection.classList.remove("hidden");

    button.disabled = true;
    button.textContent = "研究進行中...";
    status.textContent = "研究代理正在處理您的研究...";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json",},
            body: JSON.stringify({message: topic,}),
        });

        if (!response.ok) {
            throw new Error("研究請求失敗，請稍後再試。");
        }

        const data = await response.json();

        progressSection.classList.add("hidden");
        resultSection.classList.remove("hidden");
        result.textContent = data.response;
    } catch (error) {
        progressSection.classList.add("hidden");
        errorBox.textContent = error.message || "無法完成研究。";
        errorBox.classList.remove("hidden");
    } finally {
        button.disabled = false;
        button.innerHTML = "<span>✦</span> 開始研究";
    }
});
