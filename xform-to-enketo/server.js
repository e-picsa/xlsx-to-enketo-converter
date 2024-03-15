const express = require("express");
const multer = require("multer");
const fs = require("fs").promises;
const { transform } = require("enketo-transformer"); 
const cors = require('cors');

const app = express();
app.use(cors());
const upload =  multer({ dest: "uploads/" });

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.json({ message: "Welcome to the xlsx convertor", status: "OK" });
});


app.get("/api/health", (req, res) => {
  res.json({ status: "OK" });
});

app.post("/api/xlsform-to-enketo", upload.array("files"), async (req, res) => {
  try {
    const files = req.files;
    const convertedFiles = [];

    // Assuming that each uploaded file is an XML file
    for (const file of files) {
      const xform = await fs.readFile(file.path, "utf-8");
      const convertedForm = await convertForm(xform);
      const outputName = file.originalname.replace(".xml", ".json");
      //await fs.writeFile(`./forms/${outputName}`, JSON.stringify(convertedForm, null, 2), "utf-8");

      convertedFiles.push({
        filename: outputName,
        content: convertedForm,
      });
    }

    res.json({ message: "Successfully uploaded and converted files", convertedFiles });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

async function convertForm(xform) {
  return transform({
    xform: xform,
    theme: "grid",
    markdown: false,
    preprocess: (doc) => doc,
  });
}

const PORT = process.env.PORT || 5261;

app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}`);
});
