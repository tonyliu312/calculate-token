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
    console.log('页面加载完成，开始初始化...');
    
    // 检查必要的DOM元素是否存在
    if (!modelList) {
        console.error('modelList元素不存在，请检查HTML结构');
        return;
    }
    
    // 延迟一点加载，确保DOM完全准备好
    setTimeout(() => {
        loadModels();
        setupEventListeners();
    }, 100);
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
        
        if (!response.ok) {
            throw new Error(`HTTP错误: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            availableModels = data.models.filter(m => m.available);
            selectedModels = availableModels.map(m => m.key); // 默认全选可用模型
            updateModelList();
        } else {
            console.error('加载模型列表失败:', data.error || '未知错误');
            showError('加载模型列表失败: ' + (data.error || '未知错误'));
            modelList.innerHTML = '<div class="loading" style="color: var(--error-color);">加载失败: ' + (data.error || '未知错误') + '</div>';
        }
    } catch (error) {
        console.error('加载模型列表时出错:', error);
        showError(`加载模型列表时出错: ${error.message}`);
        modelList.innerHTML = '<div class="loading" style="color: var(--error-color);">加载失败: ' + error.message + '</div>';
    }
}

// 更新模型列表显示
function updateModelList() {
    if (!modelList) {
        console.error('modelList元素不存在');
        return;
    }
    
    if (availableModels.length === 0) {
        modelList.innerHTML = '<div class="loading">暂无可用模型</div>';
        return;
    }

    try {
        modelList.innerHTML = availableModels.map(model => {
            const isChecked = selectedModels.includes(model.key);
            // 转义HTML特殊字符，防止XSS
            const modelKey = model.key
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
            return `
                <div class="model-item ${!model.available ? 'unavailable' : ''}">
                    <input 
                        type="checkbox" 
                        id="model-${modelKey}" 
                        ${isChecked ? 'checked' : ''}
                        ${!model.available ? 'disabled' : ''}
                        onchange="toggleModel('${modelKey}')"
                    >
                    <label for="model-${modelKey}">${modelKey}</label>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('更新模型列表时出错:', error);
        modelList.innerHTML = '<div class="loading" style="color: var(--error-color);">更新列表失败: ' + error.message + '</div>';
    }
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

// 所有成对符号配置
// 分为两类：开闭不同的符号，开闭相同的符号
const PAIR_SYMBOLS = {
    // 开闭不同的符号：直接映射
    openToClose: {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
        '（': '）',
        '【': '】',
        '［': '］',
        '｛': '｝',
        '「': '」',
        '『': '』',
        '〈': '〉',
        '《': '》',
        '\u201C': '\u201D',   // 中文左双引号 " -> 中文右双引号 "
        '\u2018': '\u2019',   // 中文左单引号 ' -> 中文右单引号 '
    },
    // 开闭相同的符号：需要配对匹配
    sameChar: ['"', "'", '`', '```'],
};

// 创建反向映射（闭括号 -> 开括号）
const closeToOpen = {};
for (const [open, close] of Object.entries(PAIR_SYMBOLS.openToClose)) {
    closeToOpen[close] = open;
}

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
    const pairInfo = new Array(tokens.length).fill(null);
    let colorIndex = 0;
    const bracketStack = [];
    const quoteStack = [];
    
    // 统计字符出现次数
    function countChar(str, char) {
        let count = 0;
        for (const c of str) if (c === char) count++;
        return count;
    }
    
    // 第一遍：处理括号（优先级高）
    for (let i = 0; i < tokens.length; i++) {
        const token = tokens[i].trim();
        if (!token) continue;
        
        // 遍历所有括号类型
        for (const [openChar, closeChar] of Object.entries(PAIR_SYMBOLS.openToClose)) {
            // 统计开括号并入栈
            const openCount = countChar(token, openChar);
            for (let k = 0; k < openCount; k++) {
                bracketStack.push({ index: i, char: openChar, color: colorIndex++ });
            }
            
            // 统计闭括号并配对
            const closeCount = countChar(token, closeChar);
            for (let k = 0; k < closeCount; k++) {
                for (let j = bracketStack.length - 1; j >= 0; j--) {
                    if (bracketStack[j].char === openChar) {
                        const openInfo = bracketStack.splice(j, 1)[0];
                        if (pairInfo[openInfo.index] === null) {
                            pairInfo[openInfo.index] = { pairIndex: openInfo.color % 8 };
                        }
                        if (pairInfo[i] === null) {
                            pairInfo[i] = { pairIndex: openInfo.color % 8 };
                        }
                        break;
                    }
                }
            }
        }
    }
    
    // 第二遍：处理引号
    for (let i = 0; i < tokens.length; i++) {
        const token = tokens[i].trim();
        if (!token) continue;
        
        for (const quote of PAIR_SYMBOLS.sameChar) {
            const count = countChar(token, quote);
            for (let k = 0; k < count; k++) {
                let found = false;
                for (let j = quoteStack.length - 1; j >= 0; j--) {
                    if (quoteStack[j].char === quote) {
                        const openInfo = quoteStack.splice(j, 1)[0];
                        if (pairInfo[openInfo.index] === null) {
                            pairInfo[openInfo.index] = { pairIndex: openInfo.color % 8 };
                        }
                        if (pairInfo[i] === null) {
                            pairInfo[i] = { pairIndex: openInfo.color % 8 };
                        }
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    quoteStack.push({ index: i, char: quote, color: colorIndex++ });
                }
            }
            if (count > 0) break;
        }
    }
    
    // 处理起止符号配对（如 <s></s>, [CLS][SEP] 等）
    for (const marker of START_END_TOKENS) {
        const startIndices = [];
        const endIndices = [];
        
        for (let i = 0; i < tokens.length; i++) {
            const token = tokens[i].trim();
            if (token === marker.start) {
                startIndices.push(i);
            }
            if (token === marker.end) {
                endIndices.push(i);
            }
        }
        
        // 只配对相同数量的起止符号
        const minPairs = Math.min(startIndices.length, endIndices.length);
        if (minPairs > 0 && startIndices.length === endIndices.length) {
            for (let i = 0; i < minPairs; i++) {
                pairInfo[startIndices[i]] = { pairIndex: colorIndex % 8 };
                pairInfo[endIndices[i]] = { pairIndex: colorIndex % 8 };
                colorIndex++;
            }
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
