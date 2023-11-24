import PyPDF2

def extraire_texte_pdf(chemin_fichier):
    with open(chemin_fichier, 'rb') as fichier:
        lecteur_pdf = PyPDF2.PdfReader(fichier)
        texte_total = ""
        
        for page in lecteur_pdf.pages:
            texte_page = page.extract_text()
            texte_total += texte_page + "\n"  # Ajouter une nouvelle ligne entre les pages

    return texte_total

def nettoyer_texte(texte):
    # Ici, vous pouvez ajouter des règles de nettoyage supplémentaires si nécessaire
    texte = texte.replace('\n', ' ')  # Remplacer les sauts de ligne par des espaces
    return texte