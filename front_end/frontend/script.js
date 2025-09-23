// file: frontend/script.js

document.addEventListener('DOMContentLoaded', () => {
    // DOM 元素获取
    const startButton = document.getElementById('start-button');
    const buyIntentionSelect = document.getElementById('buy-intention');
    const progressContainer = document.getElementById('progress-container');
    const resultsContainer = document.getElementById('results-container');
    const finalActions = document.getElementById('final-actions');
    const downloadFullReportButton = document.getElementById('download-full-report');
    const downloadZipButton = document.getElementById('download-zip-report');
    const downloadEnvButton = document.getElementById('download-env-config'); // 正确获取按钮

    // 时间线元素
    const timelineNodesList = document.getElementById('timeline-nodes');
    const timelineProgressBar = document.getElementById('timeline-progress-bar');
    const progressPercentage = document.getElementById('progress-percentage');
    
    // 弹窗元素
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const closeButton = document.querySelector('.close-button');

    // 折叠逻辑的全局变量
    let eventSource;
    let fullReportData = [];        
    let allTimelineNodes = [];      
    let intersectionObserver;     
    const FOLD_TOP_COUNT = 3;     
    const FOLD_CONTEXT = 2;     


    // --- 辅助函数 ---
    function downloadJSON(data, filename) {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", filename);
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    }
    
    function triggerBlobDownload(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    }

    // 设置滚动侦探 (IntersectionObserver)
    function setupIntersectionObserver() {
        if (intersectionObserver) {
            intersectionObserver.disconnect();
        }
        const options = { root: null, rootMargin: '-40% 0px -40% 0px', threshold: 0 };
        const callback = (entries) => {
            const visibleEntry = entries.find(e => e.isIntersecting);
            if (visibleEntry) {
                const nodeDataId = parseInt(visibleEntry.target.dataset.nodeId, 10);
                const activeIndex = allTimelineNodes.findIndex(n => n.id === nodeDataId);
                if (activeIndex > -1) {
                    renderTimeline(activeIndex);
                }
            }
        };
        intersectionObserver = new IntersectionObserver(callback, options);
    }

    // 侧边栏重绘核心
    function renderTimeline(activeIndex = -1) {
        timelineNodesList.innerHTML = '';
        const indicesToShow = new Set();
        const totalNodes = allTimelineNodes.length;
        for (let i = 0; i < FOLD_TOP_COUNT && i < totalNodes; i++) { indicesToShow.add(i); }
        if (totalNodes > 0) { indicesToShow.add(totalNodes - 1); }
        if (activeIndex > -1) {
            for (let i = -FOLD_CONTEXT; i <= FOLD_CONTEXT; i++) {
                const indexToShow = activeIndex + i;
                if (indexToShow >= 0 && indexToShow < totalNodes) { indicesToShow.add(indexToShow); }
            }
        }
        let lastShownIndex = -1;
        const sortedIndices = [...indicesToShow].sort((a, b) => a - b); 
        sortedIndices.forEach(index => {
            if (lastShownIndex !== -1 && index > lastShownIndex + 1) {
                const ellipsis = document.createElement('li');
                ellipsis.className = 'timeline-ellipsis';
                ellipsis.textContent = '...';
                ellipsis.onclick = renderTimelineFull; 
                timelineNodesList.appendChild(ellipsis);
            }
            const nodeData = allTimelineNodes[index];
            const timelineNode = document.createElement('li');
            timelineNode.id = `timeline-node-${nodeData.id}`;
            timelineNode.className = `timeline-node ${nodeData.status}`;
            if (index === activeIndex) { timelineNode.classList.add('active'); }
            timelineNode.textContent = nodeData.name;
            timelineNodesList.appendChild(timelineNode);
            lastShownIndex = index;
        });
    }

    // 用于 "..." 点击事件，显示完整无折叠列表
    function renderTimelineFull() {
        timelineNodesList.innerHTML = '';
        allTimelineNodes.forEach((nodeData, index) => {
            const timelineNode = document.createElement('li');
            timelineNode.id = `timeline-node-${nodeData.id}`;
            timelineNode.className = `timeline-node ${nodeData.status}`;
            timelineNode.textContent = nodeData.name;
            timelineNode.classList.remove('active');
            timelineNodesList.appendChild(timelineNode);
        });
    }

    // 开始模拟函数
    startButton.addEventListener('click', startSimulation);
    function startSimulation() {
        startButton.disabled = true;
        progressContainer.classList.remove('hidden'); 
        resultsContainer.innerHTML = '';
        finalActions.classList.add('hidden'); 
        fullReportData = [];
        allTimelineNodes = []; 
        renderTimeline();      
        timelineProgressBar.style.height = '0%';
        progressPercentage.textContent = '0%';
        setupIntersectionObserver();

        const buyIntention = buyIntentionSelect.value;
        eventSource = new EventSource(`/run-simulation/?buy_intention=${buyIntention}`);

        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.status === 'finished') {
                timelineProgressBar.style.height = '100%'; 
                progressPercentage.textContent = '100%';
                startButton.disabled = false;
                finalActions.classList.remove('hidden'); 
                eventSource.close();
                return;
            }
            if (data.status === 'error') {
                console.error('Simulation error:', data);
                const errorMsg = data.output || data.error || '一个未知的错误发生了。'; 
                const traceback = (data.log && data.log.traceback) ? data.log.traceback : (data.traceback || '没有可用的堆栈跟踪。');
                const errorNode = `
                    <div class="node">
                        <h4>错误 (节点: ${data.node_name || 'N/A'})</h4> 
                        <div class="node-output" style="color: red; white-space: pre-wrap; max-height: 200px; overflow-y: auto;">
                            <strong>${errorMsg}</strong>
                            <hr style="margin: 10px 0;">
                            ${traceback}
                        </div>
                    </div>`;
                resultsContainer.insertAdjacentHTML('beforeend', errorNode);
                startButton.disabled = false;
                eventSource.close();
                if (intersectionObserver) intersectionObserver.disconnect();
                return; 
            }

            let isNewNode = false;
            let nodeDataInList = allTimelineNodes.find(n => n.id === data.id);
            if (!nodeDataInList) {
                isNewNode = true;
                nodeDataInList = { id: data.id, name: data.node_name, status: 'running' };
                allTimelineNodes.push(nodeDataInList); 
            } else {
                nodeDataInList.status = data.status;
            }

            const existingFullIndex = fullReportData.findIndex(node => node.id === data.id);
            if (existingFullIndex > -1) { fullReportData[existingFullIndex] = data; } 
            else { fullReportData.push(data); }

            updateUI(data, isNewNode);
        };

        eventSource.onerror = function(err) {
            console.error('EventSource failed:', err);
            const errorNode = `
                <div class="node">
                    <h4>网络连接错误</h4> 
                    <div class="node-output" style="color: red;">与服务器的连接已断开。后端可能已崩溃或网络中断。</div>
                </div>`;
            resultsContainer.insertAdjacentHTML('beforeend', errorNode);
            startButton.disabled = false;
            if (eventSource) eventSource.close();
            if (intersectionObserver) intersectionObserver.disconnect();
        };
    }

    // updateUI 函数
    function updateUI(data, isNewNode) {
        timelineProgressBar.style.height = `${data.progress}%`;
        progressPercentage.textContent = `${Math.round(data.progress)}%`;
        const activeIndex = allTimelineNodes.length - 1;
        renderTimeline(activeIndex);
        if (data.node_name === 'UserDecisionReportCreate') {
            if (data.status === 'completed') {
                const renderedHtml = marked.parse(data.output);
                const reportElement = document.createElement('div');
                reportElement.className = 'node final-report';
                reportElement.id = `node-${data.id}`;
                reportElement.dataset.nodeId = data.id; 
                reportElement.innerHTML = renderedHtml;
                resultsContainer.appendChild(reportElement);
                intersectionObserver.observe(reportElement);
            }
        } else {
            let nodeElement = document.getElementById(`node-${data.id}`);
            if (isNewNode && !nodeElement) {
                const nodeHTML = `
                    <div class="node" id="node-${data.id}" data-node-id="${data.id}">
                        <div class="node-header">
                            <h4>${data.node_name}</h4>
                            <span id="status-${data.id}" class="node-status ${data.status}">${data.status}</span>
                        </div>
                        <div id="output-${data.id}" class="node-output">等待输出...</div>
                        <div id="links-${data.id}" class="node-links hidden"></div>
                    </div>
                `;
                resultsContainer.insertAdjacentHTML('beforeend', nodeHTML);
                nodeElement = document.getElementById(`node-${data.id}`); 
                intersectionObserver.observe(nodeElement);
            }
            const statusElement = document.getElementById(`status-${data.id}`);
            if (statusElement) statusElement.textContent = data.status;
            if (statusElement) statusElement.className = `node-status ${data.status}`;
            if (data.status === 'completed') {
                const outputElement = document.getElementById(`output-${data.id}`);
                const linksContainer = document.getElementById(`links-${data.id}`);
                if (outputElement) outputElement.textContent = data.output || '此节点无直接文本输出';
                if (linksContainer) linksContainer.classList.remove('hidden');
                if (linksContainer) linksContainer.innerHTML = ''; 
                if (data.log) {
                    const viewDetailsLink = document.createElement('span');
                    viewDetailsLink.className = 'node-link';
                    viewDetailsLink.textContent = '查看详情(Log)';
                    viewDetailsLink.onclick = () => showModal(data);
                    linksContainer.appendChild(viewDetailsLink);
                }
                const downloadNodeLink = document.createElement('span');
                downloadNodeLink.className = 'node-link';
                downloadNodeLink.textContent = '下载此节点JSON';
                downloadNodeLink.onclick = () => {
                    const latestNodeData = fullReportData.find(n => n.id === data.id);
                    downloadJSON(latestNodeData, `node_${data.id}_${data.node_name}.json`);
                };
                if (linksContainer) linksContainer.appendChild(downloadNodeLink);
            }
        }
    }

    // --- 弹窗和下载按钮逻辑 ---
    function showModal(data) {
        modalTitle.textContent = `节点日志: ${data.node_name}`;
        modalBody.textContent = JSON.stringify(data.log, null, 2);
        modal.style.display = 'block';
    }
    closeButton.onclick = () => modal.style.display = 'none';
    window.onclick = (event) => { if (event.target == modal) { modal.style.display = 'none'; } };
    
    downloadFullReportButton.addEventListener('click', () => {
        downloadJSON(fullReportData, 'simulation_full_report.json');
    });

    downloadZipButton.addEventListener('click', () => {
        const zip = new JSZip();
        fullReportData.forEach(nodeData => {
            if (nodeData.status === 'completed') {
                const nodeFilename = `node_${nodeData.id}_${nodeData.node_name}.json`;
                const nodeContent = JSON.stringify(nodeData, null, 2);
                zip.file(nodeFilename, nodeContent);
            }
        });
        zip.generateAsync({ type: "blob" }).then(function(blob) {
            triggerBlobDownload(blob, "all_nodes_report.zip");
        }).catch(err => { console.error("生成ZIP失败:", err); });
    });

    // vvvv 这是关键的修正 vvvv
    // 使用正确的变量名 'downloadEnvButton' 来附加事件监听器
    downloadEnvButton.addEventListener('click', () => {
        fetch('/get-env-config/')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`网络响应错误: ${response.statusText}`);
                }
                return response.json();
            })
            .then(config => {
                downloadJSON(config, 'env_config.json');
            })
            .catch(error => {
                console.error('获取环境配置失败:', error);
                alert('获取环境配置失败，请查看控制台获取更多信息。');
            });
    });
    // ^^^^ 修正结束 ^^^^
});