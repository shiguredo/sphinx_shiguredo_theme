(function () {
    function setCurrentRightSideNaviReference() {
        const sections = document.querySelectorAll("section");
        if (sections.length === 0) {
            return;
        }
        // 現在のスクロール上部にある section を探す
        const target = Array.from(sections).reduce((prevSection, currentSection, _i, arr) => {
            const currentSectionRect = currentSection.getBoundingClientRect();
            if (1 < currentSectionRect.y) {
                arr.splice(1);
                return prevSection;
            }
            return currentSection;
        });
        if (!target) {
            return;
        }
        // 右コンテンツナビの対象リンクに current class を設定する
        const rightSidenavi = document.querySelector(".right-sidenavi-contents");
        if (rightSidenavi === null) {
            return;
        }
        const currentContent = rightSidenavi.querySelector("a.current");
        if (currentContent) {
            currentContent.classList.remove("current");
        }
        const nextContent = rightSidenavi.querySelector(`a[href="#${target.id}"]`);
        if (!nextContent) {
            return;
        }
        if (nextContent.classList.contains("current")) {
            return;
        }
        nextContent.classList.add("current");
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
