function trackPageView(options = {}) {
    const pageUrl = window.location.pathname + window.location.search;
    const origin = window.location.origin;

    const lastTracked = localStorage.getItem('last-page-view-time');
    const now = Date.now();

    // 默认配置
    const config = {
        retryTimes: 3, // 失败重试次数
        interval: 60000, // 上报间隔（默认60秒）
        endpoint: '/track_page', // 上报接口
        ...options
    };

    if (!lastTracked || now - parseInt(lastTracked) > config.interval) {
        let attempts = 0;

        const sendTrack = () => {
            fetch(`${origin}${config.endpoint}?url=${encodeURIComponent(pageUrl)}`, {
                method: 'GET'
            })
            .then(response => {
                if (!response.ok) throw new Error('Server responded with error');
                // 成功后，更新最后上报时间
                localStorage.setItem('last-page-view-time', now.toString());
            })
            .catch((e) => {
                console.error(`Track page view attempt ${attempts + 1} failed`, e);
                if (attempts < config.retryTimes) {
                    attempts++;
                    setTimeout(sendTrack, 1000 * attempts); // 指数级延迟重试（1s, 2s, 3s）
                }
            });
        };

        sendTrack();
    }
}

function showAlert(message, type) {
    const alertContainer = document.getElementById('liveAlertPlaceholder');
    const alertBox = document.createElement('div');
    alertBox.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show');
    alertBox.setAttribute('role', 'alert');
    alertBox.innerHTML = message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
    alertContainer.appendChild(alertBox);
    setTimeout(() => {
        if (document.body.contains(alertBox)) {  // 判断 alertBox 还在不在页面上
            var bsAlert = new bootstrap.Alert(alertBox);
            bsAlert.close();
        }
    }, 3000);
    
}


document.getElementById('messageForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // 防止表单默认提交行为

    const formData = new FormData(this);  // 获取表单数据

    // 构建请求的 payload 数据（把 FormData 转为 JSON）
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    try {
        const response = await fetch('/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // 设置请求头为 JSON
            },
            body: JSON.stringify(data),  // 把数据转换成 JSON 格式
        });

        if (response.ok) {
            showAlert("Message submitted successfully!", "success");
            this.reset();
        } else {
            showAlert("Failed to submit message, please check your input.", "danger");
        }
    } catch (error) {
        showAlert("Error: " + error, "danger");
    }
});


// 页面加载时调用
(function(){
    trackPageView();
})
