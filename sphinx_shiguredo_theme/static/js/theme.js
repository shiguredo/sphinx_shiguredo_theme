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
        const scrollTarget = document.querySelector(".left-sidenavi-body");
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

// mermaid のレンダリングが非同期で行われ、アンカー位置が当初とずれてしまう問題への対応
(function(){
    const locationHash = window.location.hash;
    if (locationHash === "") {
        return;
    }

    // アンカーが実在することを確認しておく
    const anchor = document.getElementById(locationHash.slice(1));  // 先頭の # を除去
    if (anchor === null) {
        return;
    }

    const mermaidNodes = [...document.querySelectorAll("div.mermaid")];
    if (mermaidNodes.length === 0) {
        return;
    }

    // すべての mermaid 要素のレンダリングが完了したら、ずれを補正するため
    // もう一度 anchor 位置に移動する。
    const mutationCallback = (mutationList, observer) => {
        for (const mutation of mutationList) {
            if (mutation.type === "attributes" && mutation.attributeName === "data-processed") {
                if (mermaidNodes.every((node) => node.getAttribute("data-processed") === "true")) {
                    observer.disconnect();
                    // data-processed = true になっても、実際のレンダリングが完了していないことがある。
                    // そのため location.replace() の実行は少し遅らせる。
                    setTimeout(() => {
                        location.replace(locationHash);
                    }, 50);
                }
            }
        }
    }
    const mutationObserver = new MutationObserver(mutationCallback);
    mermaidNodes.forEach((node) => {
        mutationObserver.observe(node, {
            attributes: true,
            attributeFilter: ["data-processed"],
        });
    });
    // 一定期間が経過してもレンダリングが完了しない場合は監視を打ち切る
    document.addEventListener("DOMContentLoaded", () => {
        setTimeout(() => {
            mutationObserver.disconnect();
        }, 10000);
    });
})();
