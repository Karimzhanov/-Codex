function showPostDetails(post) {
    var postDetailsContainer = document.getElementById('postDetailsContainer');
    var postImagesContainer = document.getElementById('postImagesContainer');
    var postDescriptionContainer = document.getElementById('postDescriptionContainer');

    // Очищаем контейнеры перед добавлением нового контента
    postImagesContainer.innerHTML = '';
    postDescriptionContainer.innerHTML = '';

    // Получаем ссылки на изображения и видео
    var images = post.getAttribute('data-images').split(',');
    var videos = post.getAttribute('data-videos').split(',');
    var caption = post.getAttribute('data-caption');
    var comments = post.getAttribute('data-comments');

    console.log("Images:", images);
    console.log("Videos:", videos);

    // Добавляем изображения в контейнер
    images.forEach(function(image) {
        var swiperSlide = document.createElement('div');
        swiperSlide.className = 'swiper-slide';
        var img = document.createElement('img');
        img.src = image.trim();
        img.alt = 'Изображение поста';
        swiperSlide.appendChild(img);
        postImagesContainer.appendChild(swiperSlide);
    });

    // Добавляем видео в контейнер
    videos.forEach(function(videoUrl) {
        var video = document.createElement('video');
        video.controls = true;
        video.className = 'instagram-video';
        var source = document.createElement('source');
        source.src = videoUrl.trim();
        source.type = 'video/mp4';
        video.appendChild(source);
        // Добавляем видео в контейнер
        var videoContainer = document.createElement('div'); // Создаем дополнительный div для видео
        videoContainer.className = 'swiper-slide video-container'; // Добавляем класс video-container
        videoContainer.appendChild(video);
        postImagesContainer.appendChild(videoContainer); // Добавляем видео-контейнер в swiper-slide
    });

    // Создаем описание поста
    var postDescription = document.createElement('div');
    postDescription.innerHTML = '<p><strong>Описание:</strong> ' + (caption ? caption : 'Отсутствует') + '</p>' +
                                '<p><strong>Комментарии:</strong> ' + (comments ? comments : 'Отсутствуют') + '</p>';
    postDescriptionContainer.appendChild(postDescription);

    // Показываем контейнер с подробной информацией о посте
    postDetailsContainer.classList.add('active');

    // Инициализируем Swiper
    var postSwiper = new Swiper('.swiper-container', {
        loop: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });
}

function closePostDetails() {
    var postDetailsContainer = document.getElementById('postDetailsContainer');
    postDetailsContainer.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', function() {
    var sortSelect = document.getElementById('sort');
    sortSelect.addEventListener('change', function() {
        sortPosts();
    });
});

function sortPosts() {
    var sortSelect = document.getElementById('sort');
    var selectedSort = sortSelect.value;
    var postsContainer = document.querySelector('.posts');
    var posts = postsContainer.querySelectorAll('.post');
    var sortedPosts = Array.from(posts);

    switch (selectedSort) {
        case 'date_desc':
            sortedPosts.sort((a, b) => {
                var dateA = new Date(a.getAttribute('data-date'));
                var dateB = new Date(b.getAttribute('data-date'));
                return dateB - dateA;
            });
            break;
        case 'date_asc':
            sortedPosts.sort((a, b) => {
                var dateA = new Date(a.getAttribute('data-date'));
                var dateB = new Date(b.getAttribute('data-date'));
                return dateA - dateB;
            });
            break;
        case 'comments_desc':
            sortedPosts.sort((a, b) => {
                var commentsA = parseInt(a.getAttribute('data-comments'));
                var commentsB = parseInt(b.getAttribute('data-comments'));
                return commentsB - commentsA;
            });
            break;
        case 'comments_asc':
            sortedPosts.sort((a, b) => {
                var commentsA = parseInt(a.getAttribute('data-comments'));
                var commentsB = parseInt(b.getAttribute('data-comments'));
                return commentsA - commentsB;
            });
            break;
        case 'likes_desc':
            sortedPosts.sort((a, b) => {
                var likesA = parseInt(a.getAttribute('data-likes'));
                var likesB = parseInt(b.getAttribute('data-likes'));
                return likesB - likesA;
            });
            break;
        case 'likes_asc':
            sortedPosts.sort((a, b) => {
                var likesA = parseInt(a.getAttribute('data-likes'));
                var likesB = parseInt(b.getAttribute('data-likes'));
                return likesA - likesB;
            });
            break;
    }

    // Удаление существующих постов
    postsContainer.innerHTML = '';

    // Добавление отсортированных постов
    sortedPosts.forEach(post => {
        postsContainer.appendChild(post);
    });
}
