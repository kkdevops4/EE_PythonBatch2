import os
import shutil
import subprocess
from pathlib import Path

try:
    from docx2pdf import convert as docx2pdf_convert
except ImportError:
    docx2pdf_convert = None


class DocxToPDFConverter:

    @staticmethod
    def _find_soffice(custom_path=None):

        possible_locations = [
            custom_path,
            shutil.which("soffice"),
            shutil.which("libreoffice"),
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]

        for path in possible_locations:
            if path and os.path.exists(path):
                return path

        return None

    @staticmethod
    def _open_pdf_in_vscode(pdf_file):

        try:
            subprocess.Popen(
                ["code", str(pdf_file)],
                shell=True
            )
            print("[INFO] PDF opened in VS Code")

        except Exception as e:
            print(
                f"[WARNING] Could not open PDF in VS Code: {e}"
            )

    @staticmethod
    def convert(
        docx_file,
        pdf_file,
        soffice_path=None,
        timeout_seconds=120,
    ):

        docx_file = Path(docx_file).resolve()
        pdf_file = Path(pdf_file).resolve()

        if not docx_file.exists():
            raise FileNotFoundError(
                f"DOCX file not found: {docx_file}"
            )

        pdf_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==========================================
        # METHOD 1 - LibreOffice
        # ==========================================

        soffice = DocxToPDFConverter._find_soffice(
            soffice_path
        )

        if soffice:

            try:

                print(
                    f"[INFO] Using LibreOffice: {soffice}"
                )

                subprocess.run(
                    [
                        soffice,
                        "--headless",
                        "--convert-to",
                        "pdf",
                        "--outdir",
                        str(pdf_file.parent),
                        str(docx_file),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds,
                    check=True,
                )

                generated_pdf = (
                    pdf_file.parent /
                    f"{docx_file.stem}.pdf"
                )

                if generated_pdf.exists():

                    if generated_pdf != pdf_file:

                        if pdf_file.exists():
                            pdf_file.unlink()

                        shutil.move(
                            str(generated_pdf),
                            str(pdf_file)
                        )

                    print(
                        f"[SUCCESS] PDF generated: {pdf_file}"
                    )

                    DocxToPDFConverter._open_pdf_in_vscode(
                        pdf_file
                    )

                    return str(pdf_file)

            except subprocess.TimeoutExpired:

                raise RuntimeError(
                    f"LibreOffice conversion timed out "
                    f"after {timeout_seconds} seconds."
                )

            except subprocess.CalledProcessError as e:

                raise RuntimeError(
                    f"LibreOffice conversion failed:\n"
                    f"{e.stderr}"
                )

        # ==========================================
        # METHOD 2 - docx2pdf
        # ==========================================

        if docx2pdf_convert:

            try:

                print(
                    "[INFO] Trying docx2pdf..."
                )

                docx2pdf_convert(
                    str(docx_file),
                    str(pdf_file)
                )

                if pdf_file.exists():

                    print(
                        f"[SUCCESS] PDF generated: {pdf_file}"
                    )

                    DocxToPDFConverter._open_pdf_in_vscode(
                        pdf_file
                    )

                    return str(pdf_file)

            except Exception as e:

                print(
                    f"[ERROR] docx2pdf failed: {e}"
                )

        # ==========================================
        # FAILURE
        # ==========================================

        raise RuntimeError(
            "\nDOCX to PDF conversion failed.\n\n"
            f"LibreOffice Found : {'YES' if soffice else 'NO'}\n"
            f"docx2pdf Installed : "
            f"{'YES' if docx2pdf_convert else 'NO'}\n\n"
            "Please install:\n"
            "1. LibreOffice\n"
            "OR\n"
            "2. Microsoft Word + docx2pdf\n"
        )