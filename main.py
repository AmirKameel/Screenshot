from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
import fitz  # PyMuPDF

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# Function to extract TOC and scan for sections not in TOC
def extract_toc_and_sections(pdf_path, expand_pages=7):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()  # Extract the Table of Contents (TOC)
    sections = {}

    for toc_entry in toc:
        level, title, page = toc_entry
        section_text = ""
        try:
            for i in range(page - 1, min(page - 1 + expand_pages + 1, len(doc))):
                section_text += doc.load_page(i).get_text("text") or "No text found\n"

            if title in sections:
                sections[title].append({
                    "level": level,
                    "page": page,
                    "text": section_text.strip()
                })
            else:
                sections[title] = [{
                    "level": level,
                    "page": page,
                    "text": section_text.strip()
                }]
        except Exception as e:
            sections[title] = [{"error": str(e)}]

    return {"toc": toc, "sections": sections}

class ParsePDF(Resource):
    def post(self):
        if 'pdf' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        pdf_file = request.files['pdf']
        expand_pages = int(request.form.get('expand_pages', 7))

        pdf_path = f"./temp_{pdf_file.filename}"
        pdf_file.save(pdf_path)

        try:
            result = extract_toc_and_sections(pdf_path, expand_pages)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            import os
            os.remove(pdf_path)

        return jsonify(result)

api.add_resource(ParsePDF, "/parse-pdf")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
