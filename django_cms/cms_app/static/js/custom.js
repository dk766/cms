/**
 * Custom JavaScript for Django CMS
 */

(function() {
    'use strict';

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {

        // Smooth scrolling for anchor links
        initSmoothScrolling();

        // Scroll to top button
        initScrollToTop();

        // Lazy loading images
        initLazyLoading();

        // Initialize gallery lightbox
        initGalleryLightbox();

        // Navbar scroll effect
        initNavbarScroll();

        // Animate elements on scroll
        initScrollAnimations();
    });

    /**
     * Smooth scrolling for anchor links
     */
    function initSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;

                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    /**
     * Scroll to top button
     */
    function initScrollToTop() {
        // Create scroll to top button
        const scrollBtn = document.createElement('div');
        scrollBtn.className = 'scroll-to-top';
        scrollBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
        document.body.appendChild(scrollBtn);

        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollBtn.classList.add('show');
            } else {
                scrollBtn.classList.remove('show');
            }
        });

        // Scroll to top on click
        scrollBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    /**
     * Lazy loading for images
     */
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver(function(entries, observer) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.classList.add('loaded');
                            imageObserver.unobserve(img);
                        }
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(function(img) {
                imageObserver.observe(img);
            });
        }
    }

    /**
     * Gallery lightbox effect
     */
    function initGalleryLightbox() {
        const galleries = document.querySelectorAll('.content-block-gallery');

        galleries.forEach(function(gallery) {
            const images = gallery.querySelectorAll('img');

            images.forEach(function(img, index) {
                img.style.cursor = 'pointer';
                img.addEventListener('click', function() {
                    openLightbox(images, index);
                });
            });
        });
    }

    /**
     * Open lightbox for gallery images
     */
    function openLightbox(images, currentIndex) {
        // Create lightbox overlay
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
        `;

        // Create image container
        const imgContainer = document.createElement('div');
        imgContainer.style.cssText = `
            max-width: 90%;
            max-height: 90%;
            position: relative;
        `;

        // Create image
        const img = document.createElement('img');
        img.src = images[currentIndex].src;
        img.style.cssText = `
            max-width: 100%;
            max-height: 90vh;
            object-fit: contain;
        `;

        // Create close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            position: absolute;
            top: 20px;
            right: 20px;
            background: white;
            border: none;
            font-size: 2rem;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            z-index: 10000;
        `;

        // Create navigation buttons if multiple images
        if (images.length > 1) {
            const prevBtn = document.createElement('button');
            prevBtn.innerHTML = '&#8249;';
            prevBtn.style.cssText = `
                position: absolute;
                left: 20px;
                top: 50%;
                transform: translateY(-50%);
                background: white;
                border: none;
                font-size: 3rem;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                cursor: pointer;
            `;

            const nextBtn = document.createElement('button');
            nextBtn.innerHTML = '&#8250;';
            nextBtn.style.cssText = prevBtn.style.cssText;
            nextBtn.style.left = 'auto';
            nextBtn.style.right = '20px';

            prevBtn.addEventListener('click', function() {
                currentIndex = (currentIndex - 1 + images.length) % images.length;
                img.src = images[currentIndex].src;
            });

            nextBtn.addEventListener('click', function() {
                currentIndex = (currentIndex + 1) % images.length;
                img.src = images[currentIndex].src;
            });

            overlay.appendChild(prevBtn);
            overlay.appendChild(nextBtn);
        }

        // Close lightbox
        closeBtn.addEventListener('click', function() {
            document.body.removeChild(overlay);
        });

        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                document.body.removeChild(overlay);
            }
        });

        // Assemble lightbox
        imgContainer.appendChild(img);
        overlay.appendChild(closeBtn);
        overlay.appendChild(imgContainer);
        document.body.appendChild(overlay);
    }

    /**
     * Navbar scroll effect
     */
    function initNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 50) {
                navbar.classList.add('shadow');
            } else {
                navbar.classList.remove('shadow');
            }
        });
    }

    /**
     * Animate elements when they come into view
     */
    function initScrollAnimations() {
        if ('IntersectionObserver' in window) {
            const animateObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                        animateObserver.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1
            });

            // Animate content blocks
            document.querySelectorAll('.content-block-wrapper').forEach(function(element) {
                element.style.opacity = '0';
                element.style.transform = 'translateY(20px)';
                element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
                animateObserver.observe(element);
            });

            // Animate feature items
            document.querySelectorAll('.feature-item').forEach(function(element) {
                element.style.opacity = '0';
                element.style.transform = 'translateY(20px)';
                element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
                animateObserver.observe(element);
            });
        }
    }

    /**
     * Form validation helper
     */
    window.validateForm = function(formId) {
        const form = document.getElementById(formId);
        if (!form) return false;

        let isValid = true;
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');

        inputs.forEach(function(input) {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });

        return isValid;
    };

    /**
     * Show toast notification
     */
    window.showToast = function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed bottom-0 end-0 m-3`;
        toast.style.zIndex = '10000';
        toast.innerHTML = message;

        document.body.appendChild(toast);

        setTimeout(function() {
            toast.style.opacity = '0';
            setTimeout(function() {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    };

})();
