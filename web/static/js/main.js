// 全局状态
let availableModels = [];
let selectedModels = [];

// DOM元素
const textInput = document.getElementById('text-input');
const fileInput = document.getElementById('file-input');
const fileName = document.getElementById('file-name');
const charCount = document.getElementById('char-count');
const calculateBtn = document.getElementById('calculate-btn');
const modelList = document.getElementById('model-list');
const resultsSection = document.getElementById('results-section');
const resultsTable = document.getElementById('results-table');
const resultsTbody = document.getElementById('results-tbody');
const resultsSummary = document.getElementById('results-summary');
const errorMessage = document.getElementById('error-message');
const selectAllBtn = document.getElementById('select-all');
const selectNoneBtn = document.getElementById('select-none');

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    loadModels();
    setupEventListeners();
});

// 设置事件监听器
function setupEventListeners() {
    // 文本输入字符计数
    textInput.addEventListener('input', () => {
        updateCharCount();
    });

    // 文件选择
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            fileName.textContent = `已选择: ${file.name}`;
            // 读取文件内容
            const reader = new FileReader();
            reader.onload = (event) => {
                textInput.value = event.target.result;
                updateCharCount();
            };
            reader.readAsText(file, 'UTF-8');
        }
    });

    // 拖拽上传
    const fileLabel = document.querySelector('.file-label');
    fileLabel.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileLabel.style.borderColor = 'var(--accent-color)';
    });

    fileLabel.addEventListener('dragleave', () => {
        fileLabel.style.borderColor = 'var(--border-color)';
    });

    fileLabel.addEventListener('drop', (e) => {
        e.preventDefault();
        fileLabel.style.borderColor = 'var(--border-color)';
        const file = e.dataTransfer.files[0];
        if (file) {
            fileInput.files = e.dataTransfer.files;
            fileName.textContent = `已选择: ${file.name}`;
            const reader = new FileReader();
            reader.onload = (event) => {
                textInput.value = event.target.result;
                updateCharCount();
            };
            reader.readAsText(file, 'UTF-8');
        }
    });

    // 计算按钮
    calculateBtn.addEventListener('click', handleCalculate);

    // 全选/全不选
    selectAllBtn.addEventListener('click', () => {
        selectedModels = availableModels.map(m => m.key);
        updateModelList();
    });

    selectNoneBtn.addEventListener('click', () => {
        selectedModels = [];
        updateModelList();
    });
}

// 更新字符计数
function updateCharCount() {
    const count = textInput.value.length;
    charCount.textContent = `${count.toLocaleString()} 字符`;
}

// 加载模型列表
async function loadModels() {
    try {
        const response = await fetch('/api/models');
        const data = await response.json();
        
        if (data.success) {
            availableModels = data.models.filter(m => m.available);
            selectedModels = availableModels.map(m => m.key); // 默认全选可用模型
            updateModelList();
        } else {
            showError('加载模型列表失败');
        }
    } catch (error) {
        showError(`加载模型列表时出错: ${error.message}`);
    }
}

// 更新模型列表显示
function updateModelList() {
    if (availableModels.length === 0) {
        modelList.innerHTML = '<div class="loading">暂无可用模型</div>';
        return;
    }

    modelList.innerHTML = availableModels.map(model => {
        const isChecked = selectedModels.includes(model.key);
        return `
            <div class="model-item ${!model.available ? 'unavailable' : ''}">
                <input 
                    type="checkbox" 
                    id="model-${model.key}" 
                    ${isChecked ? 'checked' : ''}
                    ${!model.available ? 'disabled' : ''}
                    onchange="toggleModel('${model.key}')"
                >
                <label for="model-${model.key}">${model.key}</label>
            </div>
        `;
    }).join('');
}

// 切换模型选择
function toggleModel(modelKey) {
    const index = selectedModels.indexOf(modelKey);
    if (index > -1) {
        selectedModels.splice(index, 1);
    } else {
        selectedModels.push(modelKey);
    }
    updateModelList();
}

// 处理计算
async function handleCalculate() {
    const text = textInput.value.trim();
    const file = fileInput.files[0];

    if (!text && !file) {
        showError('请输入文本或上传文件');
        return;
    }

    // 检查是否选择了模型
    if (selectedModels.length === 0) {
        showError('请至少选择一个模型');
        return;
    }

    // 禁用按钮
    calculateBtn.disabled = true;
    calculateBtn.querySelector('.btn-text').style.display = 'none';
    calculateBtn.querySelector('.btn-loading').style.display = 'inline';

    try {
        const formData = new FormData();
        if (file) {
            formData.append('file', file);
        } else {
            formData.append('text', text);
        }
        selectedModels.forEach(model => {
            formData.append('models', model);
        });

        const response = await fetch('/api/calculate', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || '计算失败');
        }
    } catch (error) {
        showError(`计算时出错: ${error.message}`);
    } finally {
        // 恢复按钮
        calculateBtn.disabled = false;
        calculateBtn.querySelector('.btn-text').style.display = 'inline';
        calculateBtn.querySelector('.btn-loading').style.display = 'none';
    }
}

// 括号配对配置
const BRACKET_PAIRS = [
    { open: '(', close: ')' },
    { open: '[', close: ']' },
    { open: '{', close: '}' },
    { open: '<', close: '>' },
    { open: '「', close: '」' },
    { open: '『', close: '』' },
    { open: '【', close: '】' },
    { open: '《', close: '》' },
    { open: '"', close: '"' },
    { open: '"', close: '"' },
    { open: ''', close: ''' },
    { open: ''', close: ''' },
    { open: '（', close: '）' },
    { open: '［', close: '］' },
    { open: '｛', close: '｝' },
    { open: '〈', close: '〉' },
];

// 起止符号配置（特殊token标记）
const START_END_TOKENS = [
    { start: '<|start|>', end: '<|end|>' },
    { start: '<s>', end: '</s>' },
    { start: '<bos>', end: '<eos>' },
    { start: '[CLS]', end: '[SEP]' },
    { start: '<|im_start|>', end: '<|im_end|>' },
    { start: '<|begin|>', end: '<|finish|>' },
];

// 高亮token中的括号和起止符号（只高亮成对出现的）
function highlightBracketsAndMarkers(tokens) {
    // 初始化配对信息
    const pairInfo = new Array(tokens.length).fill(null);
    let pairColorIndex = 0;
    
    // 处理括号配对
    for (const pair of BRACKET_PAIRS) {
        const stack = [];
        
        for (let i = 0; i < tokens.length; i++) {
            const token = tokens[i];
            
            // 检查是否是开括号（精确匹配或token等于开括号）
            const isOpenBracket = token === pair.open || 
                                 (token.length === 1 && token === pair.open);
            
            // 检查是否是闭括号（精确匹配或token等于闭括号）
            const isCloseBracket = token === pair.close || 
                                  (token.length === 1 && token === pair.close);
            
            if (isOpenBracket) {
                // 遇到开括号，入栈
                stack.push({ index: i, color: pairColorIndex });
            } else if (isCloseBracket) {
                // 遇到闭括号，尝试配对
                if (stack.length > 0) {
                    const openInfo = stack.pop();
                    // 只有成功配对才标记
                    pairInfo[openInfo.index] = { type: 'bracket', pairIndex: openInfo.color % 8, isOpen: true };
                    pairInfo[i] = { type: 'bracket', pairIndex: openInfo.color % 8, isOpen: false };
                }
            }
        }
        
        // 如果成功配对了括号，使用下一个颜色索引
        if (pairInfo.some((p, idx) => p && p.pairIndex === pairColorIndex % 8)) {
            pairColorIndex++;
        }
    }
    
    // 处理起止符号配对
    for (const marker of START_END_TOKENS) {
        const startIndices = [];
        const endIndices = [];
        
        for (let i = 0; i < tokens.length; i++) {
            const token = tokens[i];
            // 精确匹配起止符号
            if (token === marker.start || token.trim() === marker.start) {
                startIndices.push(i);
            }
            if (token === marker.end || token.trim() === marker.end) {
                endIndices.push(i);
            }
        }
        
        // 只配对相同数量的起止符号（成对出现）
        const minPairs = Math.min(startIndices.length, endIndices.length);
        if (minPairs > 0 && startIndices.length === endIndices.length) {
            // 只有起止符号数量相等时才高亮（确保完全配对）
            for (let i = 0; i < minPairs; i++) {
                const startIdx = startIndices[i];
                const endIdx = endIndices[i];
                pairInfo[startIdx] = { type: 'marker', pairIndex: pairColorIndex % 8, isOpen: true };
                pairInfo[endIdx] = { type: 'marker', pairIndex: pairColorIndex % 8, isOpen: false };
            }
            pairColorIndex++;
        }
    }
    
    return pairInfo;
}

// 显示结果
function displayResults(data) {
    // 显示结果区域
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // 更新摘要
    const avgTokens = data.results.length > 0
        ? Math.round(data.results.reduce((sum, r) => sum + r.token_count, 0) / data.results.length)
        : 0;

    resultsSummary.innerHTML = `
        <div class="summary-item">
            <div class="summary-label">文本长度</div>
            <div class="summary-value">${data.text_length.toLocaleString()} 字符</div>
        </div>
        <div class="summary-item">
            <div class="summary-label">计算模型数</div>
            <div class="summary-value">${data.results.length}</div>
        </div>
        <div class="summary-item">
            <div class="summary-label">平均Token数</div>
            <div class="summary-value">${avgTokens.toLocaleString()}</div>
        </div>
    `;

    // 更新表格
    resultsTbody.innerHTML = data.results.map(result => {
        const tokenPreview = result.token_preview || [];
        const totalTokens = result.token_count || 0;
        const previewCount = result.preview_count || tokenPreview.length;
        
        // 高亮括号和起止符号
        const pairInfo = highlightBracketsAndMarkers(tokenPreview);
        
        // 显示所有token（不再限制为100个）
        const previewHtml = tokenPreview.length > 0
            ? tokenPreview.map((token, index) => {
                // 转义HTML特殊字符
                const escapedToken = token
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#039;');
                
                // 获取配对信息
                const pair = pairInfo[index];
                let className = 'token-item';
                if (pair) {
                    className += ` bracket-pair-${pair.pairIndex % 8}`;
                }
                
                return `<span class="${className}" title="${escapedToken}">${escapedToken}</span>`;
            }).join('')
            : '<span class="text-tertiary">无预览</span>';

        // 如果后端只返回了部分token，显示提示信息
        const moreTokens = totalTokens > previewCount
            ? `<div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid var(--border-color); color: var(--text-secondary); font-size: 0.875rem;">
                 <strong>提示：</strong>后端仅返回了前 ${previewCount} 个token的预览，实际共有 ${totalTokens.toLocaleString()} 个token
               </div>`
            : '';

        return `
            <tr>
                <td class="model-name">${result.model}</td>
                <td class="token-count">${totalTokens.toLocaleString()}</td>
                <td>${result.char_per_token.toFixed(2)}</td>
                <td>
                    <div class="token-preview">
                        ${previewHtml}
                        ${moreTokens}
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// 显示错误消息
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

