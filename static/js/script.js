const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("excelFile");

const toggle = document.getElementById("togglePreview");
const preview = document.getElementById("previewContainer");

toggle.addEventListener("click", () => {

    if (preview.style.display === "none" || preview.style.display === "") {

        preview.style.display = "block";

        toggle.textContent = "Hide Preview";

    }

    else {

        preview.style.display = "none";

        toggle.textContent = "Show Preview";

    }

});

uploadBtn.addEventListener("click", async () => {

    if (fileInput.files.length === 0) {

        alert("Please select an Excel file.");

        return;

    }

    const formData = new FormData();

    formData.append("file", fileInput.files[0]);

    const response = await fetch("/upload", {

        method: "POST",

        body: formData

    });

    const data = await response.json();

    if (!data.success) {

        alert(data.message);

        return;

    }

    buildPreview(data.preview);

    if (data.columns) {

        buildColumns(data.columns);

    }

});

function buildPreview(rows) {

    const tbody = document.querySelector("#previewTable tbody");

    tbody.innerHTML = "";

    rows.forEach(row => {

        const tr = document.createElement("tr");

        row.forEach(cell => {

            const td = document.createElement("td");

            td.textContent = cell;

            tr.appendChild(td);

        });

        tbody.appendChild(tr);

    });

}

function buildColumns(columns) {

    const beneficiary = document.getElementById("beneficiaryColumn");
    const rc = document.getElementById("rcColumn");

    if (!beneficiary || !rc) {

        return;

    }

    beneficiary.innerHTML = "";
    rc.innerHTML = "";

    columns.forEach(column => {

        beneficiary.innerHTML += `<option value="${column}">${column}</option>`;

        rc.innerHTML += `<option value="${column}">${column}</option>`;

    });

}