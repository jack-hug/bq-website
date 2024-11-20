// 数字跳动动画函数
function animateCount(element, target, duration) {
    const start = 0;
    const increment = target / (duration / 16.67);
    let current = start;
    const startTime = performance.now();

    function updateCount(timestamp) {
        const elapsed = timestamp - startTime;
        current = Math.min(start + increment * (elapsed / 16.67), target);
        element.textContent = Math.floor(current);

        if (current < target) {
            requestAnimationFrame(updateCount);
        }
    }

    requestAnimationFrame(updateCount);
}

// 首页效果
var swiper = new Swiper('.swiper', {
    direction: 'vertical',
    spaceBetween: 0,
    mousewheel: true,
    speed: 1000,
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    on: {
        slideChangeTransitionEnd: function () {
            // 获取当前活动的滑块
            const activeSlide = document.querySelector('.swiper-slide-active');

            // 查找所有的 .counter 元素并触发动画
            const counters = activeSlide.querySelectorAll('.counter');
            counters.forEach(counter => {
                if (counter.textContent === '0') {
                    const target = parseInt(counter.getAttribute('data-bs-target'));
                    animateCount(counter, target, 1500);
                }
            })
        }
    }
});

// 首页banner效果
var swiper2 = new Swiper('.swiper-banner', {
    speed: 1000,
    effect: 'fade',
    fadeEffect: {
        crossFade: false
    },
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
    loop: true,
});

// 监听页面滚动事件
let isBannerVisible = true;

function handleScroll() {
    const bannerSection = document.getElementById('home');
    const bannerRect = bannerSection.getBoundingClientRect();

    if (bannerRect.top < window.innerHeight && bannerRect.bottom >= 0) {
        // Banner section is in view
        if (!isBannerVisible) {
            swiper2.autoplay.start();
            isBannerVisible = true;
        }
    } else {
        // Banner section is out of view
        if (isBannerVisible) {
            swiper2.autoplay.stop();
            isBannerVisible = false;
        }
    }
}

window.addEventListener('scroll', handleScroll);


