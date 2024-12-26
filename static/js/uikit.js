/*! Minimized UIkit for Video Game Vault | Supports: uk-navbar */

(function (global) {
    "use strict";

    // Utility Functions
    function addClass(element, cls) {
        element.classList.add(cls);
    }

    function removeClass(element, cls) {
        element.classList.remove(cls);
    }

    function toggleClass(element, cls) {
        element.classList.toggle(cls);
    }

    function hasClass(element, cls) {
        return element.classList.contains(cls);
    }

    // Dropdown Handling
    function initDropdown(navbar) {
        const dropdowns = navbar.querySelectorAll('.uk-navbar-dropdown');
        dropdowns.forEach(dropdown => {
            const parent = dropdown.closest('li');
            if (!parent) return;

            parent.addEventListener('mouseenter', () => {
                addClass(dropdown, 'uk-open');
            });

            parent.addEventListener('mouseleave', () => {
                removeClass(dropdown, 'uk-open');
            });
        });
    }

    // Navbar Initialization
    function initNavbar() {
        const navbars = document.querySelectorAll('[uk-navbar]');
        navbars.forEach(navbar => {
            initDropdown(navbar);
        });
    }

    // Document Ready
    document.addEventListener('DOMContentLoaded', () => {
        initNavbar();
    });

})(window);
