document.addEventListener("DOMContentLoaded", function () {
  let list = document.querySelectorAll(".navigation li");
  let toggle = document.querySelector(".toggle");
  let navigation = document.querySelector(".navigation");
  let main = document.querySelector(".main");

  function setActiveMenu() {
      let activeMenu = localStorage.getItem("activeMenu") || "dashboard";  
      list.forEach(el => {
          if (el.dataset.menu === activeMenu) {
              el.classList.add("dash-active");
          } else {
              el.classList.remove("dash-active");
          }
      });
  }

  function handleActiveClassClick() {
      list.forEach(el => el.classList.remove("dash-active"));
      this.classList.add("dash-active");

      localStorage.setItem("activeMenu", this.dataset.menu);
  }

  function handleHoverEffect() {
      if (!this.classList.contains("dash-active")) {
          this.classList.add("hover-active");
      }
  }

  function removeHoverEffect() {
      this.classList.remove("hover-active");
  }

  list.forEach((item) => {
      item.addEventListener("mouseover", handleHoverEffect);
      item.addEventListener("mouseout", removeHoverEffect);
      item.addEventListener("click", handleActiveClassClick);
  });

  setActiveMenu();

  toggle.onclick = function () {
      navigation.classList.toggle("active");
      main.classList.toggle("active");
  };
});