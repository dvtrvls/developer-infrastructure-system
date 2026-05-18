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
        const response = await fetch(`${API}/metrics/current`)
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

function pulseCardByIndex(index) {
    const card = cards[index];

    card.classList.add("updated");

    setTimeout(() => {
        card.classList.remove("updated");
    }, 600);
}
fetchMetrics()
setInterval(fetchMetrics, 3000)