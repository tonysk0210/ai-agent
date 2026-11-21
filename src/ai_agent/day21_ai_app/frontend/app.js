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
    document.getElementById("activity").innerHTML = "";
    progressSection.classList.remove("hidden");
    resultSection.classList.add("hidden");
    result.textContent = "";
    status.textContent = "正在開始研究...";

    // 這行會從前端向後端送出一個 HTTP GET 請求，網址裡帶著使用者輸入的研究主題。
    // topic = "AI agent & tools"
    // /research?topic=AI%20agent%20%26%20tools
    // # 收到請求後，topic 會是解碼後的原始文字
    // research(topic="AI agent & tools")
    const response = await fetch(`/research?topic=${encodeURIComponent(topic)}`);

    if (!response.ok) {
        throw new Error("無法開始研究，請稍後再試。");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
        const {value, done} = await reader.read();

        if (done) {
            break;
        }

        buffer += decoder.decode(value, {stream: true});

        const events = buffer.split("\n\n");
        buffer = events.pop();

        for (const event of events) {
            if (!event.startsWith("data: ")) {
                continue;
            }

            const json = event.substring(6);
            const data = JSON.parse(json);
            handleResearchEvent(data);
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
        addActivity("●", event.message);
        return;
    }

    if (event.type === "tool") {
        addActivity("●", event.message);
        status.textContent = event.message;
        return;
    }

    if (event.type === "tool_complete") {
        addActivity("✓", event.message);
        return;
    }

    if (event.type === "verification") {
        addActivity("✓", event.message);
        return;
    }

    if (event.type === "complete") {
        progressSection.classList.add("hidden");
        resultSection.classList.remove("hidden");
        result.textContent = event.report;
        status.textContent = "研究完成。";
    }
}

// 1. 建立一個新的 <div>，並加上 CSS class activity-item。
// 2. 在裡面放入圖示和訊息。
// 3. 把這個 <div> 加到頁面 id="activity" 的元素底下。
function addActivity(icon, message) {
    const item = document.createElement("div");
    item.className = "activity-item";
    item.innerHTML = `
        <span class="activity-icon">
            ${icon}
        </span>
        <span>
            ${message}
        </span>
    `;

    document.getElementById("activity").appendChild(item);
}
