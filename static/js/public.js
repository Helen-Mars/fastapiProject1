// 功能1：注册按钮跳转
function setupRegisterButton() {
    const registerButton = document.getElementById('register-button');
    if (registerButton) {
        registerButton.addEventListener('click', function() {
            console.log('Register button clicked');
            window.location.href = '/register';
        });
    }
}

// 功能2：显示页面浏览次数
function loadPageViewCount() {
    const origin = window.location.origin;

    fetch(`${origin}/page_view_count`)
      .then(response => response.json())
      .then(data => {
        const countSpan = document.getElementById('view-count');
        if (countSpan && data.total_views !== undefined) {
          countSpan.innerText = `${data.total_views} times clicked.`;
        }
      })
      .catch((e) => {
        console.error('get page_view_count error', e);
      });
}

// 页面加载完后统一执行
(function() {
    setupRegisterButton();
    loadPageViewCount();
})();

  