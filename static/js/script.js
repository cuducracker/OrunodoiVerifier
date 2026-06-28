// ========================================
// Global Variables
// ========================================

let uploadedFilePath = "";

// ========================================
// HTML Elements
// ========================================

const uploadBtn = document.getElementById("uploadBtn");
const startBtn = document.getElementById("startBtn");

const fileInput = document.getElementById("excelFile");

const beneficiaryColumn = document.getElementById("beneficiaryColumn");
const rcColumn = document.getElementById("rcColumn");

const startRow = document.getElementById("startRow");
const endRow = document.getElementById("endRow");

const fileName = document.getElementById("fileName");
const totalRows = document.getElementById("totalRows");
const totalColumns = document.getElementById("totalColumns");
const uploadStatus = document.getElementById("uploadStatus");

const progressBar = document.getElementById("progressBar");
const progressText = document.getElementById("progressText");

const currentRC = document.getElementById("currentRC");
const currentName = document.getElementById("currentName");
const currentStatus = document.getElementById("currentStatus");

const previewContainer = document.getElementById("previewContainer");
const togglePreview = document.getElementById("togglePreview");

const previewHead = document.querySelector("#previewTable thead");
const previewBody = document.querySelector("#previewTable tbody");

const downloadBtn = document.getElementById("downloadBtn");

// ========================================
// Toggle Preview
// ========================================

togglePreview.addEventListener("click", () => {

    if (previewContainer.style.display === "none" ||
        previewContainer.style.display === "") {

        previewContainer.style.display = "block";

        togglePreview.innerText = "Hide Preview";

    }

    else {

        previewContainer.style.display = "none";

        togglePreview.innerText = "Show Preview";

    }

});

// ========================================
// Upload Excel
// ========================================

uploadBtn.addEventListener("click", async () => {

    if (fileInput.files.length === 0) {

        alert("Please select an Excel file.");

        return;

    }

    uploadBtn.disabled = true;

    uploadStatus.innerText = "Uploading...";

    const formData = new FormData();

    formData.append(

        "file",

        fileInput.files[0]

    );

    try {

        const response = await fetch(

            "/upload",

            {

                method: "POST",

                body: formData

            }

        );

        const data = await response.json();

        if (!response.ok || !data.success) {

            throw new Error(

                data.message || "Upload Failed."

            );

        }

        uploadedFilePath = data.file_path || "";

        fileName.innerText = data.filename || "-";

        totalRows.innerText = data.total_rows || data.rows || 0;

        totalColumns.innerText = data.total_columns || data.columns.length;

        uploadStatus.innerText = "Upload Successful";

        endRow.value = data.total_rows || data.rows || 0;

        buildColumns(

            data.columns || []

        );

        buildPreview(

            data.preview || [],

            data.columns || []

        );

        autoSelectColumns(

            data.detected || {}

        );

    }

    catch (error) {

        console.error(error);

        uploadStatus.innerText = "Upload Failed";

        alert(error.message);

    }

    finally {

        uploadBtn.disabled = false;

    }

});

// ========================================
// Build Preview
// ========================================

function buildPreview(rows, columns) {

    previewHead.innerHTML = "";

    previewBody.innerHTML = "";

    if (columns.length > 0) {

        const headerRow = document.createElement("tr");

        columns.forEach(column => {

            const th = document.createElement("th");

            th.innerText = column;

            headerRow.appendChild(th);

        });

        previewHead.appendChild(headerRow);

    }

    rows.forEach(row => {

        const tr = document.createElement("tr");

        row.forEach(cell => {

            const td = document.createElement("td");

            td.innerText = cell ?? "";

            tr.appendChild(td);

        });

        previewBody.appendChild(tr);

    });

}

// ========================================
// Build Dropdowns
// ========================================

function buildColumns(columns) {

    beneficiaryColumn.innerHTML = "";

    rcColumn.innerHTML = "";

    columns.forEach(column => {

        beneficiaryColumn.innerHTML +=

            `<option value="${column}">${column}</option>`;

        rcColumn.innerHTML +=

            `<option value="${column}">${column}</option>`;

    });

}

// ========================================
// Auto Detect Columns
// ========================================

function autoSelectColumns(detected) {

    if (detected.beneficiary) {

        beneficiaryColumn.value = detected.beneficiary;

    }

    if (detected.rc_number) {

        rcColumn.value = detected.rc_number;

    }

}

// ========================================
// Start Verification
// ========================================

startBtn.addEventListener("click", async () => {

    if (uploadedFilePath === "") {

        alert("Please upload Excel first.");

        return;

    }

    progressText.innerText = "Verification Started...";

    currentStatus.innerText = "Running";

    progressBar.style.width = "10%";

    try {

        const response = await fetch(

            "/verify",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    file_path: uploadedFilePath,

                    beneficiary_column:

                        beneficiaryColumn.value,

                    rc_column:

                        rcColumn.value,

                    start_row:

                        startRow.value,

                    end_row:

                        endRow.value

                })

            }

        );

        const result = await response.json();

        if (!result.success) {

            alert(result.message);

            progressText.innerText = "Verification Failed";

            currentStatus.innerText = "Error";

            progressBar.style.width = "0%";

            return;

        }

        progressBar.style.width = "100%";

        progressText.innerText = "Verification Completed";

        currentStatus.innerText = "Completed";

        alert(

            "Verification Completed Successfully."

        );
        const downloadBtn = document.getElementById("downloadBtn");
        downloadBtn.disabled = false;
        downloadBtn.onclick = function () {

    window.location.href = "/download";

};
    }
    
    catch (error) {

        console.error(error);

        progressText.innerText = "Verification Failed";

        currentStatus.innerText = "Error";

        progressBar.style.width = "0%";

        alert("Verification Failed.");

    }

});
