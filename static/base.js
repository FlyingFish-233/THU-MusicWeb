
document.addEventListener('DOMContentLoaded', addSearchEvent);
document.addEventListener('DOMContentLoaded', addBackToBtnEvent);

// 搜索框功能
function addSearchEvent() {
    const searchTypeDropdown = document.getElementById('searchTypeDropdown'); // 搜索类型下拉框
    const searchTypeItems = document.querySelectorAll('.search-type-item'); // 下拉框中歌手、歌曲两个选项
    const searchForm = document.getElementById('searchForm'); // 搜索表单
    const searchInput = document.getElementById('searchInput'); // 搜索输入框
    
    let currentSearchType = 'song';

    searchTypeItems.forEach(item => {
        item.addEventListener('click', SearchTypeItemEvent)
    });

    searchForm.addEventListener('submit', SearchFormEvent);

    // 点击下拉框中选项的事件
    function SearchTypeItemEvent(e) {
        e.preventDefault();
        searchTypeItem = e.currentTarget;
        searchTypeDropdown.textContent = searchTypeItem.textContent;
        searchInput.placeholder = '搜索' + searchTypeItem.textContent + '...';
        currentSearchType = searchTypeItem.getAttribute('data-type')
    }

    // 点击搜索按钮的事件
    function SearchFormEvent(e) {
        e.preventDefault();
        const searchQuery = searchInput.value.trim();
        if (!searchQuery) {
            alert("搜索内容不能为空！");
            return;
        }
        if (searchQuery.length > 20) {
            alert("搜索内容不能超过20个字符！");
            return;
        }
        window.location.href = DJANGO_URLS[currentSearchType] + `?q=${encodeURIComponent(searchQuery)}`;
    }
}

// 返回顶端按钮
function addBackToBtnEvent()
{
    const btn = document.getElementById('backToTopBtn');

    btn.addEventListener('click', scrollToTopEvent);
    window.addEventListener('scroll', backToTopBtnDisplay);

    function scrollToTopEvent(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    function backToTopBtnDisplay() {
        if (window.pageYOffset > 300)
            btn.classList.add('show');
        else
            btn.classList.remove('show');
    }
}