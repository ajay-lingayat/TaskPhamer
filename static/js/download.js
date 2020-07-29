function generatePDF() {
        
  const element = document.getElementById("template");

  html2pdf()
    .from(element)
    .save();
}