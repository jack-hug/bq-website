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
                const activeSlide = this.slides[this.realIndex];

                // 检查 activeSlide 是否存在且 ID 为 "about"
                if (activeSlide && activeSlide.id === 'about') {
                    // 查找所有的 .counter 元素并触发动画
                    const counters = activeSlide.querySelectorAll('.counter');
                    counters.forEach(counter => {
                        if (counter.textContent === '0') {
                            const target = parseInt(counter.getAttribute('data-bs-target'));
                            animateCount(counter, target, 1500);
                        }
                    });
                } else {
                    console.log('当前活动的 slide 不是 #about');
                }
            }
        }
    })
;

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

// 首页news效果
var swiper3 = new Swiper('.swiper-news', {
    slidesPerView: 3,
    freeMode: true,
    speed: 5000,
    loop: true,
    autoplay: {
        delay: 0,
        disableOnInteraction: false,
        pauseOnMouseEnter: true,
    },
})





