
//     @@@@@  NAVBAR JS @@@@@
function updateMenu() {
  const nav = document.getElementById("nav-links");
  const moreContainer = document.getElementById("more-container");
  const moreMenu = document.getElementById("more-menu");

  if (!nav || !moreContainer || !moreMenu) return;

// reset  
  const items = Array.from(nav.children).filter(el => el.id !== "more-container");
  moreMenu.innerHTML = "";
  items.forEach(item => item.classList.remove("hidden"));
  moreContainer.classList.add("hidden");

  // overflow handling
  for (let i = items.length - 1; i >= 0; i--) {
    if (nav.scrollWidth > nav.clientWidth) {
      moreContainer.classList.remove("hidden");

    const item = items[i];
    item.classList.add("hidden");

    // Clone the item for the dropdown menu
    const clone = item.cloneNode(true);
    clone.classList.remove("hidden", "whitespace-nowrap", "text-blue-600");
    clone.classList.add("block", "w-full", "text-left", "px-4", "py-2", "text-sm", "text-gray-700", "hover:bg-purple-100", "hover:text-purple-600", "rounded-md", "transition-colors");

    // Highlight active page in dropdown
    if (window.location.pathname === item.getAttribute('hx-get')) {
    clone.classList.add('bg-purple-200', 'text-purple-600', 'font-bold');
}
    clone.addEventListener("click", () => {
      item.click();
      moreMenu.classList.add("hidden");
    });

    moreMenu.prepend(clone);
    } else {  
     break; 
  }
  }

  if(typeof htmx !== 'undefined') {
    htmx.process(moreMenu);
  }
}

// events
function initMenuEvents() {
  const moreBtn = document.getElementById("more-btn");
  const moreMenu = document.getElementById("more-menu");
  const moreContainer = document.getElementById("more-container");

  if (!moreBtn || !moreMenu || !moreContainer) return;

// Toggle dropdown on click
    moreBtn.onclick = (e) => {
      e.stopPropagation();
      moreMenu.classList.toggle("hidden");
    };

// Show dropdown on hover
    moreContainer.onmouseenter = () => {
      moreMenu.classList.remove("hidden");
    };

// Hide dropdown when mouse leaves
    moreContainer.onmouseleave = () => {
    moreMenu.classList.add("hidden");
  };

// Hide dropdown when clicking outside
    document.onclick = (e) => {
    if (!moreContainer.contains(e.target)) {
      moreMenu.classList.add("hidden");
      }
    };
  }

// Initialize on load and after HTMX updates 
  document.addEventListener("DOMContentLoaded", () => {
  updateMenu();
  initMenuEvents();
  highlightActivePage();
});

// Re-run after HTMX content updates
document.body.addEventListener("htmx:afterSettle", () => {
  updateMenu();
  initMenuEvents();
  highlightActivePage();
  closeSidebar(); // Close sidebar after navigation
});

window.addEventListener('popstate', highlightActivePage);

// Recalculate on window resize with debounce
let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(updateMenu, 150);
});


//     @@@@@  SIDEBAR JS @@@@@
// Function to open the sidebar
function openSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (!sidebar || !overlay) return;

    // Show the sidebar and overlay
    sidebar.classList.remove('-left-[280px]');
    sidebar.classList.add('left-0');

    // Show the overlay with fade-in effect
    overlay.classList.remove('hidden');
    setTimeout(() => {
        overlay.classList.add('opacity-100');
        overlay.classList.remove('opacity-0');
    }, 10);

    // Prevent body from scrolling when sidebar is open
    document.body.style.overflow = 'hidden';
}

// Function to close the sidebar
function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (!sidebar || !overlay) return;

    // Hide the sidebar and overlay
    sidebar.classList.remove('left-0');
    sidebar.classList.add('-left-[280px]');

    // Hide the overlay with fade-out effect
    overlay.classList.add('opacity-0');
    overlay.classList.remove('opacity-100');

    setTimeout(() => {
        overlay.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }, 300);
}

// Close sidebar when clicking outside of it
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.getElementById('menu-button');

    // Only close the sidebar if it's currently open and the click is outside of the sidebar and menu button
    if (sidebar && !sidebar.classList.contains('-left-[280px]')) {
        if (!sidebar.contains(event.target) && (menuBtn && !menuBtn.contains(event.target))) {
            closeSidebar();
        }
    }
});


// @@@@@ ACTIVE LINK HIGHLIGHT (header or sidebar navigation) JS @@@@@

function highlightActivePage() {
    const currentPath = window.location.pathname;
    const allLinks = document.querySelectorAll('#nav-links a, #sidebar nav a');

    allLinks.forEach(link => {
        const linkPath = link.getAttribute('hx-get');

        if (currentPath === linkPath) {
          // Highlight Header active link
          if (link.closest('header')) {
                link.classList.add('text-purple-600', 'font-bold');
                link.classList.remove('text-blue-600');
            } else {
                // Highlight Sidebar active link
                link.classList.remove('font-medium', 'font-normal'); 
                link.classList.add('bg-purple-200', 'text-purple-600', 'font-bold', 'border-l-4', 'border-purple-600');
                link.classList.remove('text-gray-700');
            }
        }
          else {
          // Differentiate header vs sidebar links
          if (link.closest('header')) {
                link.classList.remove('text-purple-600', 'font-bold');
                link.classList.add('text-blue-600');
            } else {
                link.classList.remove('bg-purple-200', 'text-purple-600', 'font-bold', 'border-l-4', 'border-purple-600');
                link.classList.add('text-gray-700');
            }
        }
    });
}



// @@@@@  PASSWORD TOGGLE JS Login and Signup Eye function @@@@@
function togglePass(id, btn) {
    const input = document.getElementById(id);
    const eyeClosed = btn.querySelector('#eye-closed');
    const eyeOpen = btn.querySelector('#eye-open');

    if (input.type === "password") {
        input.type = "text";
        eyeClosed.classList.add('hidden');
        eyeOpen.classList.remove('hidden');
        btn.classList.add('text-blue-600');
    } else {
        input.type = "password";
        eyeClosed.classList.remove('hidden');
        eyeOpen.classList.add('hidden'); 
        btn.classList.remove('text-blue-600');
    }
}
