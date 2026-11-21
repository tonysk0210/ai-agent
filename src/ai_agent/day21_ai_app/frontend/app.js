document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("researchButton");
    const topicInput = document.getElementById("topic");
    const status = document.getElementById("status");
    const progressSection = document.getElementById("progressSection");
    const resultSection = document.getElementById("resultSection");
    const reportContent = document.getElementById("reportContent");
    const errorBox = document.getElementById("error");
    const characterCount = document.getElementById("characterCount");
    const activityContainer = document.getElementById("activity");

    // 輸入字元計數器
    topicInput.addEventListener("input", () => {
        const length = topicInput.value.length;
        characterCount.textContent = `${length} 個字元`;
    });

    // 開始按鈕的事件監聽器
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
            await startResearch(topic);
        } catch (error) {
            errorBox.textContent = error.message;
            errorBox.classList.remove("hidden");
        } finally {
            button.disabled = false;
            button.innerHTML = "<span>✦</span> 開始研究";
        }
    });

    // 1. 清空上次的進度和報告，顯示研究進度區域。
    // 2. 用 fetch 請求 /research?topic=...，把主題送到後端。
    // 3. 確認請求成功，然後讀取回傳的串流資料。
    // 4. 把串流切成一個個 SSE 事件，解析其中的 JSON。
    // 5. 將每個事件交給 handleResearchEvent(data) 更新頁面，例如顯示進度或研究報告。
    // 簡單說，它是前端研究流程的「啟動與接收器」：送出主題，再把後端陸續傳回的事件交給頁面處理。
    async function startResearch(topic) {
        activityContainer.innerHTML = "";
        reportContent.innerHTML = "";
        status.textContent = "正在開始研究...";

        // 這行會從前端向後端送出一個 HTTP GET 請求，網址裡帶著使用者輸入的研究主題。
        // topic = "AI agent & tools"
        // /research?topic=AI%20agent%20%26%20tools
        // # 收到請求後，topic 會是解碼後的原始文字
        // research(topic="AI agent & tools")
        const response = await fetch(`/research?topic=${encodeURIComponent(topic)}`);

        if (!response.ok) {
            throw new Error("無法啟動研究，請稍後再試。");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
            const {value, done} = await reader.read();

            if (done) break;

            buffer += decoder.decode(value, {stream: true});
            const events = buffer.split("\n\n");
            buffer = events.pop();

            for (const event of events) {
                if (!event.startsWith("data: ")) continue;

                try {
                    const json = event.substring(6);
                    const data = JSON.parse(json);
                    handleResearchEvent(data);
                } catch (e) {
                    console.error("解析事件資料失敗：", e);
                }
            }
        }
    }

    // startResearch 負責接收事件，handleResearchEvent 負責判斷事件種類並更新畫面。
    function handleResearchEvent(event) {
        if (event.type === "plan") {
            status.textContent = "研究計畫已建立。";
            addActivity("✓", "研究計畫已建立");
            return;
        }

        if (event.type === "step") {
            addActivity("●", `研究代理步驟 ${event.step}`);
            return;
        }

        if (event.type === "tool") {
            const message = `正在使用工具：${event.tool}`;
            addActivity("●", message);
            status.textContent = message;
            return;
        }

        if (event.type === "tool_complete") {
            addActivity("✓", `已完成工具：${event.tool}`);
            return;
        }

        if (event.type === "verification") {
            addActivity("✓", "正在驗證研究證據");
            return;
        }

        if (event.type === "complete") {
            progressSection.classList.add("hidden");
            resultSection.classList.remove("hidden");
            renderReport(event.report);
            status.textContent = "研究完成。";
            return;
        }

        if (event.type === "error") {
            errorBox.textContent = event.message;
            errorBox.classList.remove("hidden");
            progressSection.classList.add("hidden");
        }
    }

    // 1. 建立一個新的 <div>，並加上 CSS class activity-item。
    // 2. 在裡面放入圖示和訊息。
    // 3. 把這個 <div> 加到頁面 id="activity" 的元素底下。
    function addActivity(icon, message) {
        const item = document.createElement("div");
        item.className = "activity-item";
        item.innerHTML = `
            <span class="activity-icon">${icon}</span>
            <span>${escapeHtml(message)}</span>
        `;
        activityContainer.appendChild(item);
    }

    // 會把後端傳來的純文字報告轉成 HTML，放進頁面的報告區顯示。它辨認幾種簡單的 Markdown 格式
    function renderReport(report) {
        if (!report) return;

        const lines = report.split("\n");
        let html = "";

        for (const line of lines) {
            const text = line.trim();
            if (!text) continue;

            if (text.startsWith("# ")) {
                html += `<h1>${escapeHtml(text.substring(2))}</h1>`;
            } else if (text.startsWith("## ")) {
                html += `<h2>${escapeHtml(text.substring(3))}</h2>`;
            } else if (text.startsWith("### ")) {
                html += `<h3>${escapeHtml(text.substring(4))}</h3>`;
            } else if (text.startsWith("- ")) {
                html += `<div class="report-bullet"><span>•</span><span>${escapeHtml(text.substring(2))}</span></div>`;
            } else {
                html += `<p>${escapeHtml(text)}</p>`;
            }
        }

        reportContent.innerHTML = html;
    }

    // 把文字中有特殊意義的 HTML 字元轉成安全的文字表示，避免瀏覽器把報告內容誤當成 HTML 標籤來解析
    function escapeHtml(string) {
        return String(string)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});