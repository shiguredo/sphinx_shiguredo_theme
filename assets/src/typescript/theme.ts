(function () {
  function setCurrentRightSideNaviReference(): void {
    const sections = document.querySelectorAll("section");
    if (sections.length === 0) {
      return;
    }
    // 現在のスクロール上部にある section を探す
    const target = Array.from(sections).reduce(
      (prevSection, currentSection) => {
        const prevSectionRect = prevSection.getBoundingClientRect();
        const currentSectionRect = currentSection.getBoundingClientRect();
        if (
          0 < currentSectionRect.y ||
          currentSectionRect.y < prevSectionRect.y
        ) {
          return prevSection;
        }
        return currentSection;
      }
    );
    if (!target) {
      return;
    }
    // 右コンテンツナビの対象リンクに current class を設定する
    const rightSidenavi = document.querySelector(".right-sidenavi-contents");
    if (!rightSidenavi) {
      return;
    }
    const currentContent = rightSidenavi.querySelector("a.current");
    if (currentContent) {
      currentContent.classList.remove("current");
    }
    const prevContent = rightSidenavi.querySelector(`a[href="#${target.id}"]`);
    if (!prevContent) {
      return;
    }
    if (prevContent.classList.contains("current")) {
      return;
    }
    prevContent.classList.add("current");
  }

  document.addEventListener("DOMContentLoaded", () => {
    // left navi
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

    // right navi
    setCurrentRightSideNaviReference();
  });

  window.addEventListener("scroll", (_) => {
    setCurrentRightSideNaviReference();
  });
})();
