// click a screenshot to zoom it, click again (or press Esc) to close
document.querySelectorAll("figure img").forEach((img) => {
    img.addEventListener("click", () => img.classList.toggle("zoomed"));
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        document.querySelector("img.zoomed")?.classList.remove("zoomed");
    }
});
