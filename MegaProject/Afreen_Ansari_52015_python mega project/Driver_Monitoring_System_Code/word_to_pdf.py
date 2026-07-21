import os

def convert_word_to_pdf(word_file):
    word_application = None
    word_document = None
    try:
        import win32com.client
        word_path = os.path.abspath(word_file)
        if not os.path.isfile(word_path):
            print("Word report not found:",word_path)
            return None
        
        pdf_path = os.path.splitext(word_path)[0] + ".pdf"
        word_application = (win32com.client.DispatchEx("Word.Application"))
        word_application.Visible = False
        word_application.DisplayAlerts = 0
        word_document = (word_application.Documents.Open(word_path,ReadOnly=True))
        word_document.ExportAsFixedFormat(OutputFileName=pdf_path,ExportFormat=17,OpenAfterExport=False)
        return pdf_path

    except ImportError:
        print("PDF conversion failed:pywin32 is not installed.")
        print("Install it using: python -m pip install pywin32")
        return None
    
    except Exception as error:
        print("PDF conversion failed:",error)
        return None
    
    finally:
        if word_document is not None:
            try:
                word_document.Close(SaveChanges=False)
            except Exception:
                pass
        if word_application is not None:
            try:
                word_application.Quit()
            except Exception:
                pass