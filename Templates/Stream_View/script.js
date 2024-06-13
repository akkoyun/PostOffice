// Tablo satırlarını ve JSON kartını seç
const tableRows = document.querySelectorAll(".data-table tbody tr");
const jsonCard = document.querySelector(".json-card pre");

// Her bir satıra tıklama olayı ekle
tableRows.forEach((row) => {
    row.addEventListener("click", function () {
        // Önceki seçilen satırdan 'selected' sınıfını kaldır
        document.querySelector(".data-table tbody tr.selected")?.classList.remove("selected");
        // Bu satıra 'selected' sınıfını ekle
        this.classList.add("selected");

        // Tıklanan satırın data-json özelliğindeki JSON verisini al
        const jsonData = this.getAttribute("data-json");

        // JSON verisini vurgulama fonksiyonu
        function syntaxHighlight(json) {
            json = JSON.stringify(json, undefined, 2);
            json = json.replace(/&/g, "&").replace(/</g, "<").replace(/>/g, ">");
            return json.replace(
                /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(:)?|\b(true|false|null)\b|\d+)/g,
                function (match) {
                    var cls = "number";
                    if (/^"/.test(match)) {
                        if (/:$/.test(match)) {
                            cls = "key";
                        } else {
                            cls = "string";
                        }
                    } else if (/true|false/.test(match)) {
                        cls = "boolean";
                    } else if (/null/.test(match)) {
                        cls = "null";
                    }
                    return '<span class="' + cls + '">' + match + "</span>";
                }
            );
        }

        // JSON verisini parse et ve vurgula
        try {
            const jsonParsed = JSON.parse(jsonData);
            jsonCard.innerHTML = syntaxHighlight(jsonParsed);
            jsonCard.classList.add("active");
        } catch (e) {
            console.error("JSON parse hatası: ", e);
            jsonCard.innerHTML = "JSON verisi okunamadı.";
        }
    });
});
