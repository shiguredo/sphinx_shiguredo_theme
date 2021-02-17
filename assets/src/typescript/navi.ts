// left navi
document.addEventListener("DOMContentLoaded", () => {
  const scrollTarget = document.querySelector(".left-sidenavi-contents");
  if (!scrollTarget) {
    return;
  }
  const current = scrollTarget.querySelector("a.current");
  if (!current) {
    return;
  }
  const scrollTargetTop = scrollTarget?.getBoundingClientRect().top;
  const currentTop = current.getBoundingClientRect().top;
  scrollTarget.scrollTo(0, currentTop - scrollTargetTop);
});

// right navi
function f() {

}

window.addEventListener("scroll", (_) =>{
  const sections = document.querySelectorAll(".section");
  // 現在のスクロール上部にある section を探す
  const target = Array.from(sections).reduce((prevSection, currentSection) => {
    const prevSectionRect = prevSection.getBoundingClientRect();
    const currentSectionRect = currentSection.getBoundingClientRect();
    if (0 < currentSectionRect.y || currentSectionRect.y < prevSectionRect.y) {
      return prevSection;
    }
    return currentSection;
  });
  if (!target) {
    return;
  }
  // 右コンテンツナビの対象リンクに current class を設定する
  const rightSidenavi = document.querySelector(".right-sidenavi-contents");
  if (!rightSidenavi) {
    return;
  }
  const prevContent = rightSidenavi.querySelector(`a[href="#${target.id}"]`);
  if (!prevContent) {
    return;
  }
  if (prevContent.classList.contains("current")) {
    return;
  }
  const currentContent = rightSidenavi.querySelector("a.current");
  if (currentContent) {
    currentContent.classList.remove("current");
  }
  prevContent.classList.add("current");
});
