document.addEventListener("DOMContentLoaded", function () {
    let homeMenuList = document.querySelectorAll(".navigation li");  
    let homeToggle = document.querySelector(".toggle");  
    let homeNavigation = document.querySelector(".navigation");  
    let homeMain = document.querySelector(".main");  

    function updateTimeAndDate() {
        const now = new Date();
        
        const timeString = now.toLocaleTimeString('fr-FR', { 
            hour: '2-digit', 
            minute: '2-digit',
        });
        
        const dateString = now.toLocaleDateString('fr-FR', { 
            day: '2-digit', 
            month: '2-digit', 
            year: 'numeric'
        });
        
        const timeElement = document.getElementById('current-time');
        const dateElement = document.getElementById('current-date');
        
        if (timeElement) timeElement.textContent = timeString;
        if (dateElement) dateElement.textContent = dateString;
    }
  
    updateTimeAndDate();
    setInterval(updateTimeAndDate, 1000);

    function setHomeActiveMenu() {  
        let homeActiveMenu = localStorage.getItem("homeActiveMenu") || "home"; 
        homeMenuList.forEach(el => {
            if (el.dataset.menu === homeActiveMenu) {
                el.classList.add("dash-active");
            } else {
                el.classList.remove("dash-active");
            }
        });
    }
  
    function handleHomeActiveClassClick() {  
        homeMenuList.forEach(el => el.classList.remove("dash-active"));
        this.classList.add("dash-active");
        localStorage.setItem("homeActiveMenu", this.dataset.menu); 
    }
  
    function handleHomeHoverEffect() {  
        if (!this.classList.contains("dash-active")) {
            this.classList.add("hover-active");
        }
    }
  
    function removeHomeHoverEffect() { 
        this.classList.remove("hover-active");
    }
  
    homeMenuList.forEach((item) => {
        item.addEventListener("mouseover", handleHomeHoverEffect);
        item.addEventListener("mouseout", removeHomeHoverEffect);
        item.addEventListener("click", handleHomeActiveClassClick);
    });
  
    setHomeActiveMenu();
  
    homeToggle.onclick = function () {
        homeNavigation.classList.toggle("active");
        homeMain.classList.toggle("active");
    };

    /*=============== SEARCH BAR JS ===============*/
    const toggleSearch = (search, button) =>{
        const searchBar = document.getElementById(search),
              searchButton = document.getElementById(button)
    
        searchButton.addEventListener('click', () =>{
            searchBar.classList.toggle('show-search')
        })
     }

     toggleSearch('search-bar', 'search-button')
  });