const API = "http://localhost:8000"

const cpuValue = document.getElementById("cpu-value");
const cpuBar = document.getElementById("cpu-bar");
const cpuStatus = document.getElementById("cpu-status");

const memoryValue = document.getElementById("memory-value");
const memoryBar = document.getElementById("memory-bar");
const memoryStatus = document.getElementById("memory-status");

const diskValue = document.getElementById("disk-value");
const diskBar = document.getElementById("disk-bar");
const diskStatus = document.getElementById("disk-status");
const cards = document.querySelectorAll(".metric-card");

function getLevel(percent)
{
    if (percent >= 90) return "critical"
    if(percent >= 75) return "warning"
    return "normal" 
}

function updateMetricCard(valueId, barId, statusId, percent, label, index)
{
    const level = getLevel(percent)

    const valueE1 = document.getElementById(valueId)
    const barE1 = document.getElementById(barId)
    const statusE1 = document.getElementById(statusId)
    valueE1.classList.remove("skeleton");
    valueE1.textContent = percent + "%"
    valueE1.className = "metric-value value-" + level

   
    pulseCardByIndex(index)
    animateValue(valueE1, 0, percent);

    barE1.style.width = percent + "%"
    barE1.className = "metric-bar-fill bar-" + level

    statusE1.textContent = level
}

function animateValue(el, start, end, duration = 500) {
    let startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        const progress = timestamp - startTime;
        const value = Math.min(
            start + (end - start) * (progress / duration),
            end
        );

        el.textContent = Math.floor(value) + "%";

        if (progress < duration) {
            requestAnimationFrame(step);
        }
    }

    requestAnimationFrame(step);
}
async function fetchMetrics()
{
    try{
        const response = await fetch(`${API}/metrics/current`,{
    credentials: 'include'
})
        const data = await response.json()
        
        updateMetricCard("cpu-value", "cpu-bar", "cpu-status", data.cpu, "CPU",0)
        updateMetricCard("memory-value", "memory-bar", "memory-status", data.memory, "Memory",1)
        updateMetricCard("disk-value", "disk-bar", "disk-status", data.disk, "Disk",2)
    } catch(error)
    {
        console.error("Failed to fetch metrics:", error);
        cpuStatus.textContent = "Error loading data";
        memoryStatus.textContent = "Error loading data";
        diskStatus.textContent = "Error loading data";
    }
}


function timeAgo(timestamp)
{
    let then = new Date(timestamp);
    let now = new Date()

    const diffMs = now - then;
    const diffMin = Math.floor(diffMs/ 60000)
    
    if (diffMin < 1) return "just now";
    if (diffMin < 60) return `${diffMin} min ago`
    const diffHr = Math.floor(diffMin /60)
    return `${diffHr} hr ago`
}


function buildAlertRow(alert)
{
    const sev =  alert.severity.toLowerCase()
    const row = document.createElement("div")
    row.className = "alert-row"

     row.innerHTML = `
        <span class="severity-badge badge-${sev}">${alert.severity}</span>
        <div class="alert-body">
            <div class="alert-rule">${alert.rule_name}</div>
            <div class="alert-meta">${alert.source} · ${timeAgo(alert.timestamp)}</div>
        </div>
    `
    return row
}
function pulseCardByIndex(index) {
    const card = cards[index];

    card.classList.add("updated");

    setTimeout(() => {
        card.classList.remove("updated");
    }, 600);
}

async function fetchAlerts()
{
    try
    {
        const response = await fetch(`${API}/alerts/recent?limit=6`,  {
    credentials: 'include'
})
        const data = await response.json()

        const list = document.getElementById("alert-list")
        const totalEl = document.getElementById("alert-total")

        list.innerHTML = ""
        totalEl.textContent = `${data.count} total`


        if (data.alerts.length === 0) {
            list.innerHTML = `<div class="loading-text">no alerts yet</div>`
            return
        }

        data.alerts.forEach(alert => {
            list.appendChild(buildAlertRow(alert))
        })

        const hasCritical = data.alerts.some(a => a.severity === "CRITICAL")
        const panel = document.getElementById("alert-list").closest(".panel")

        if (hasCritical) {
            panel.classList.remove("panel-critical")
            void panel.offsetWidth  // force reflow so animation restarts
            panel.classList.add("panel-critical")
                }

    }catch (error)
    {
        console.error("Failed to fetch alerts: ", error)
    }
}

async function fetchStats() {
    try {
        const response = await fetch(`${API}/alerts/stats`,  {
    credentials: 'include'
})
        const data = await response.json()

        const bySev = data.by_severity

        document.getElementById("count-critical").textContent = bySev["CRITICAL"] || 0
        document.getElementById("count-warning").textContent  = bySev["WARNING"]  || 0
        document.getElementById("count-error").textContent    = bySev["ERROR"]    || 0
        document.getElementById("count-info").textContent     = bySev["INFO"]     || 0
        document.getElementById("alert-total").textContent    = `${data.total} total`
        document.getElementById("alert-count").textContent = data.total
        document.getElementById("alert-critical").textContent = `${bySev["CRITICAL"] || 0} critical`
    } catch (error) {
        console.error("Failed to fetch stats:", error)
    }
}


function formatTime(timestamp)
{
    const d = new Date(timestamp)
    return d.toTimeString().slice(0, 8)
}


function buildLogEntry(alert)
{
    const sev = alert.severity.toLowerCase()

    const entry =document.createElement("div")
    entry.className = "log-entry log-entry-new"

    entry.innerHTML = `
        <span class="log-time">${formatTime(alert.timestamp)}</span>
        <span class="log-sev-${sev}">[${alert.severity}]</span>
        <span class="log-message">${alert.rule_name} · ${alert.source} · ${alert.message || ""}</span>
    `
    return entry
}


function clearLogs() {
    const feed = document.getElementById("log-feed")
    feed.innerHTML = `<div class="loading-text">cleared · waiting for new logs...</div>`
    lastAlertId = 0
}




async function fetchLogFeed()
{
    try
    {
        const filter = document.getElementById("log-filter").value
        let url =  `${API}/alerts/recent?limit=50`
        if (filter !== "all")
            {
                url = `${API}/alerts/severity/${filter}`
            }

        const response = await fetch(url,  {
    credentials: 'include'
})
        const data = await response.json()
        
        const feed = document.getElementById("log-feed")

        const newAlerts = data.alerts.filter(a => a.id > lastAlertId)

        if (data.alerts.length === 0) {
            feed.innerHTML = `
                <div style="text-align:center; padding: 2rem 0; color: #475569;">
                    <div style="font-size: 24px; margin-bottom: 8px;">✓</div>
                    <div style="font-size: 13px;">no alerts fired yet</div>
                    <div style="font-size: 11px; margin-top: 4px;">system is healthy</div>
                </div>
            `
            return
        }
        if (lastAlertId === 0)
            {
                feed.innerHTML = ""
            }

        newAlerts.reverse().forEach(alert => 
            {
                const entry = buildLogEntry(alert)
                feed.prepend(entry)
            })

        lastAlertId = Math.max(...data.alerts.map(a => a.id))
        while (feed.children.length > 100)
            {
                feed.removeChild(feed.lastChild)
            }


    } catch (error)
    {
          console.error("Failed to fetch log feed:", error)
    }
}


document.getElementById("log-filter").addEventListener("change", ()=>
    {
        lastAlertId = 0;
        document.getElementById("log-feed").innerHTML = ""
        fetchLogFeed()
    })


async function checkConnection() {
    const dot = document.querySelector(".status-dot")
    const badge = document.querySelector(".status-badge")

    try {
        await fetch(`${API}/health`,  {
    credentials: 'include'
})
        dot.style.background = "#4ade80"
        badge.style.color = "#4ade80"
        badge.style.borderColor = "#166534"
    } catch {
        dot.style.background = "#ef4444"
        badge.style.color = "#ef4444"
        badge.style.borderColor = "#7f1d1d"
        badge.textContent = ""
        badge.innerHTML = `<div class="status-dot" style="background:#ef4444"></div>disconnected`
    }
}

let lastAlertId = 0

fetchMetrics()
fetchAlerts()
fetchStats()
fetchLogFeed()
checkConnection()

setInterval(fetchMetrics, 3000)
setInterval(fetchAlerts, 5000)
setInterval(fetchStats, 5000)
setInterval(fetchLogFeed, 3000)
setInterval(checkConnection, 10000)