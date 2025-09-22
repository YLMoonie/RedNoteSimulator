// file: frontend/script.js

document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-button');
    const buyIntentionSelect = document.getElementById('buy-intention');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const resultsContainer = document.getElementById('results-container');
    const finalActions = document.getElementById('final-actions');
    const downloadButton = document.getElementById('download-report');
    
    // 弹窗元素
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const closeButton = document.querySelector('.close-button');

    let eventSource;
    let fullReportData = [];

    startButton.addEventListener('click', startSimulation);

    function startSimulation() {
        // 重置状态
        startButton.disabled = true;
        progressContainer.classList.remove('hidden');
        finalActions.classList.remove('hidden');
        resultsContainer.innerHTML = '';
        progressBar.style.width = '0%';
        progressText.textContent = '0%';
        fullReportData = [];

        const buyIntention = buyIntentionSelect.value;
        eventSource = new EventSource(`/run-simulation/?buy_intention=${buyIntention}`);

        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);

            if (data.status === 'finished') {
                console.log('Simulation finished.');
                progressText.textContent = '100%';
                progressBar.style.width = '100%';
                startButton.disabled = false;
                finalActions.classList.remove('hidden');
                eventSource.close();
                return;
            }

            if (data.status === 'error') {
                console.error('Simulation error:', data.error);
                const errorNode = `
                    <div class="node">
                        <h4>错误</h4>
                        <div class="node-output" style="color: red;">${data.error}</div>
                    </div>`;
                resultsContainer.insertAdjacentHTML('beforeend', errorNode);
                startButton.disabled = false;
                eventSource.close();
                return;
            }

            updateUI(data);
            
            // 保存每个节点的完整数据
            const existingNodeIndex = fullReportData.findIndex(node => node.id === data.id);
            if (existingNodeIndex > -1) {
                fullReportData[existingNodeIndex] = data;
            } else {
                fullReportData.push(data);
            }
        };

        eventSource.onerror = function() {
            console.error('EventSource failed.');
            startButton.disabled = false;
            eventSource.close();
        };
    }

    function updateUI(data) {
        // 更新进度条
        progressBar.style.width = `${data.progress}%`;
        progressText.textContent = `${Math.round(data.progress)}%`;

        let nodeElement = document.getElementById(`node-${data.id}`);

        if (!nodeElement) {
            // 如果节点不存在，创建它
            const nodeHTML = `
                <div class="node" id="node-${data.id}">
                    <div class="node-header">
                        <h4>${data.node_name}</h4>
                        <span id="status-${data.id}" class="node-status ${data.status}">${data.status}</span>
                    </div>
                    <div id="output-${data.id}" class="node-output">等待输出...</div>
                    <span id="details-${data.id}" class="view-details hidden">查看详情</span>
                </div>
            `;
            resultsContainer.insertAdjacentHTML('beforeend', nodeHTML);
            nodeElement = document.getElementById(`node-${data.id}`);
        }
        
        // 更新节点内容
        const statusElement = document.getElementById(`status-${data.id}`);
        const outputElement = document.getElementById(`output-${data.id}`);
        const detailsLink = document.getElementById(`details-${data.id}`);

        statusElement.textContent = data.status;
        statusElement.className = `node-status ${data.status}`;
        
        if (data.status === 'completed') {
            outputElement.textContent = data.output || '此节点无直接文本输出';
            if (data.log) {
                detailsLink.classList.remove('hidden');
                detailsLink.onclick = () => showModal(data);
            }
        }
    }

    function showModal(data) {
        modalTitle.textContent = `节点详情: ${data.node_name}`;
        modalBody.textContent = JSON.stringify(data.log, null, 2);
        modal.style.display = 'block';
    }

    // 关闭弹窗
    closeButton.onclick = () => modal.style.display = 'none';
    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    // 下载报告
    downloadButton.addEventListener('click', () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(fullReportData, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "simulation_report.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    });
});