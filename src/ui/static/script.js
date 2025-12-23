const checkboxes = document.querySelectorAll(".delete-checkbox");
const counter = document.getElementById("selected-count");
const exportBtn = document.getElementById("export-btn");
const selectAllBtn = document.getElementById("select-all-btn");

function updateState() {
    const selected = [...checkboxes].filter(cb => cb.checked);
    counter.textContent = selected.length;
    exportBtn.disabled = selected.length === 0;
}

checkboxes.forEach(cb =>
    cb.addEventListener("change", updateState)
);

selectAllBtn.addEventListener("click", () => {
    checkboxes.forEach(cb => cb.checked = true);
    updateState();
});

exportBtn.addEventListener("click", () => {
    const selectedPaths = [...checkboxes]
        .filter(cb => cb.checked)
        .map(cb => cb.dataset.path);

    const payload = {
        generated_at: new Date().toISOString(),
        count: selectedPaths.length,
        files: selectedPaths
    };

    const blob = new Blob(
        [JSON.stringify(payload, null, 2)],
        { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "cleaner_guru_export.json";
    document.body.appendChild(a);
    a.click();

    URL.revokeObjectURL(url);
    a.remove();
});