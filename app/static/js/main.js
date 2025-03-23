/**
 * 停车场管理系统通用JavaScript函数
 */

// 文档加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    initializeTooltips();
    
    // 初始化自动隐藏通知
    initializeAlertDismiss();
    
    // 初始化表单验证
    initializeFormValidation();
    
    // 初始化确认对话框
    initializeConfirmDialogs();
});

/**
 * 初始化Bootstrap工具提示
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * 初始化警告信息自动隐藏
 */
function initializeAlertDismiss() {
    // 自动关闭警告信息
    window.setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            if (alert) {
                alert.classList.add('fade');
                setTimeout(function() {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 500);
            }
        });
    }, 5000);
}

/**
 * 初始化表单验证
 */
function initializeFormValidation() {
    // 获取所有需要验证的表单
    const forms = document.querySelectorAll('.needs-validation');
    
    // 遍历表单并设置验证
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * 初始化确认对话框
 */
function initializeConfirmDialogs() {
    // 获取所有需要确认的操作元素
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    
    // 遍历元素并设置确认事件
    Array.from(confirmButtons).forEach(button => {
        button.addEventListener('click', event => {
            if (!confirm(button.dataset.confirm)) {
                event.preventDefault();
                event.stopPropagation();
            }
        });
    });
}

/**
 * 格式化日期时间
 * @param {Date|string} dateTime - 日期时间对象或字符串
 * @param {string} format - 输出格式
 * @returns {string} 格式化后的日期时间字符串
 */
function formatDateTime(dateTime, format = 'YYYY-MM-DD HH:mm:ss') {
    if (!dateTime) return '';
    
    const date = typeof dateTime === 'string' ? new Date(dateTime) : dateTime;
    
    if (isNaN(date.getTime())) return '';
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    
    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

/**
 * 格式化金额
 * @param {number} amount - 金额
 * @param {number} decimals - 小数位数
 * @returns {string} 格式化后的金额字符串
 */
function formatCurrency(amount, decimals = 2) {
    if (isNaN(amount)) return '0.00';
    
    return '¥' + amount.toFixed(decimals);
}

/**
 * 验证车牌号
 * @param {string} plateNumber - 车牌号
 * @returns {boolean} 是否有效
 */
function validatePlateNumber(plateNumber) {
    // 中国车牌号正则表达式
    const pattern = /^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$/;
    
    return pattern.test(plateNumber);
}

/**
 * 验证手机号
 * @param {string} phoneNumber - 手机号
 * @returns {boolean} 是否有效
 */
function validatePhoneNumber(phoneNumber) {
    // 中国大陆手机号正则表达式
    const pattern = /^1[3-9]\d{9}$/;
    
    return pattern.test(phoneNumber);
}

/**
 * 计算停车时长
 * @param {Date|string} entryTime - 入场时间
 * @param {Date|string} exitTime - 出场时间，如果为空则使用当前时间
 * @returns {number} 停车时长（小时）
 */
function calculateParkingDuration(entryTime, exitTime = null) {
    const entry = typeof entryTime === 'string' ? new Date(entryTime) : entryTime;
    const exit = exitTime ? (typeof exitTime === 'string' ? new Date(exitTime) : exitTime) : new Date();
    
    // 计算时间差（毫秒）
    const diff = exit.getTime() - entry.getTime();
    
    // 转换为小时
    const hours = diff / (1000 * 60 * 60);
    
    // 向上取整到0.25小时（15分钟）
    return Math.ceil(hours * 4) / 4;
}

/**
 * 计算停车费用
 * @param {number} duration - 停车时长（小时）
 * @param {string} vehicleType - 车辆类型
 * @returns {number} 停车费用
 */
function calculateParkingFee(duration, vehicleType) {
    let rate;
    
    // 根据车辆类型设置费率
    switch (vehicleType) {
        case 'car':
            rate = 10.0;
            break;
        case 'motorcycle':
            rate = 5.0;
            break;
        case 'truck':
            rate = 15.0;
            break;
        default:
            rate = 10.0;
    }
    
    // 计算费用并保留两位小数
    return Math.round(duration * rate * 100) / 100;
}

/**
 * AJAX请求封装
 * @param {string} url - 请求URL
 * @param {string} method - 请求方法
 * @param {Object} data - 请求数据
 * @param {Function} callback - 回调函数
 */
function ajaxRequest(url, method = 'GET', data = null, callback = null) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            if (callback) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    callback(null, response);
                } catch (e) {
                    callback(null, xhr.responseText);
                }
            }
        } else {
            if (callback) {
                callback(new Error('请求失败: ' + xhr.status), null);
            }
        }
    };
    
    xhr.onerror = function() {
        if (callback) {
            callback(new Error('请求错误'), null);
        }
    };
    
    if (data) {
        xhr.send(JSON.stringify(data));
    } else {
        xhr.send();
    }
}

/**
 * 生成随机颜色
 * @returns {string} 十六进制颜色代码
 */
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    
    return color;
}

/**
 * 导出表格为CSV
 * @param {HTMLElement} table - 表格元素
 * @param {string} filename - 文件名
 */
function exportTableToCSV(table, filename) {
    const rows = table.querySelectorAll('tr');
    let csv = [];
    
    for (let i = 0; i < rows.length; i++) {
        const row = [], cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length; j++) {
            // 替换双引号并用双引号包围字段
            let data = cols[j].innerText.replace(/"/g, '""');
            row.push('"' + data + '"');
        }
        
        csv.push(row.join(','));
    }
    
    // 下载CSV文件
    downloadCSV(csv.join('\n'), filename);
}

/**
 * 下载CSV文件
 * @param {string} csv - CSV内容
 * @param {string} filename - 文件名
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], {type: 'text/csv'});
    const downloadLink = document.createElement('a');
    
    // 设置下载链接属性
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    
    // 添加到文档并触发点击
    document.body.appendChild(downloadLink);
    downloadLink.click();
    
    // 清理
    document.body.removeChild(downloadLink);
}
