from app.utils.pdf import extract_text_from_pdf

text = extract_text_from_pdf("uploads/resumes/CHIRAGCVV (2).pdf")

print(text[:1000])
