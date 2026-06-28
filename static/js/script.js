const uploadBtn = document.getElementById("uploadBtn");

const fileInput = document.getElementById("excelFile");

uploadBtn.addEventListener(

    "click",

    async () => {

        if (fileInput.files.length === 0) {

            alert("Please select an Excel file.");

            return;

        }

        const formData = new FormData();

        formData.append(

            "file",

            fileInput.files[0]

        );

        const response = await fetch(

            "/upload",

            {

                method: "POST",

                body: formData

            }

        );

        const data = await response.json();

        if (!data.success) {

            alert(data.message);

            return;

        }

        buildPreview(

            data.preview

        );

        buildColumns(

            data.columns

        );

    }

);


function buildPreview(rows) {

    const tbody = document.querySelector(

        "#previewTable tbody"

    );

    tbody.innerHTML = "";

    rows.forEach(row => {

        let tr = document.createElement("tr");

        row.forEach(cell => {

            let td = document.createElement("td");

            td.innerText = cell;

            tr.appendChild(td);

        });

        tbody.appendChild(tr);

    });

}


function buildColumns(columns) {

    const beneficiary = document.getElementById(

        "beneficiaryColumn"

    );

    const rc = document.getElementById(

        "rcColumn"

    );

    beneficiary.innerHTML = "";

    rc.innerHTML = "";

    columns.forEach(column => {

        beneficiary.innerHTML +=

        `<option>${column}</option>`;

        rc.innerHTML +=

        `<option>${column}</option>`;

    });

}