from pyalex import Works
from langchain.document_loaders import PyPDFLoader
import os
from typing import Literal, List


def extract_pdf_to_txt(
    url_or_pdf_name: str, filename: str, mode: Literal["local", "online"] = "online"
) -> bool:
    """extracts text from pdf and stores in a txt file

    Args:
        url_or_pdf_name (str): url or file name of pdf (depends on "mode")
        filename (str): the filename of output txt file
        mode (Literal[&quot;local&quot;, &quot;online&quot;], optional): whether pdf data is stored locally or online. Defaults to "online".
    """
    print(f"extracting pdf data from {filename}...")
    # read pdf data
    if mode == "online":
        loader = PyPDFLoader(url_or_pdf_name)
        pages = loader.load()
    elif mode == "local":
        pdf_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "pdf",
            url_or_pdf_name,
        )
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

    filename = filename if filename.endswith(".txt") else filename + ".txt"
    outpath = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "text",
        filename,
    )
    try:
        # write pdf data to file
        with open(outpath, "w") as doc:
            for page in pages:
                doc.write(page.page_content)
        print(f"pdf extraction complete. data saved to {filename}")
        return True
    except:
        print("Error. Could not extract pdf.")
        return False


# Sample doi: https://doi.org/10.48550/arXiv.2308.02510
def extract_doi_to_txt(doi: str, filename: str = "document") -> None:
    """extract pdf data to text and store in .txt file

    Args:
        doi (str): doi of target paper
        filename (str, optional): name of output file (.txt added automatically). Defaults to "document".
    """
    print("reading from doi...")

    # get pdf data from openalex
    paper_work_object = Works()[doi]
    url = paper_work_object["open_access"]["oa_url"]
    print("pdf url successfully retrieved")

    extract_pdf_to_txt(url, filename=filename)


def get_string_from_text_file(
    filename: str = "document", verbose: bool = False, full_path: bool = False
) -> str:
    """read a txt file and returns the string.

    Args:
        filename (str, optional): name of the file you want to open. Defaults to "document".

    Returns:
        str: string of the text file
    """
    filename = filename if filename.endswith(".txt") else filename + ".txt"
    log(verbose, f"reading data from {filename}...")

    try:
        filepath = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "text",
            filename,
        )
        if full_path:
            filepath = filename
        with open(filepath, "r") as file:
            res = file.read()
        log(verbose, "string successfully retrieved.\n")
        return res
    except:
        print("Error. Could not read file.")


def list_to_text_file(target_list: List[str], filename: str):
    str_data = "\n".join(target_list)
    with open(filename, "w") as file:
        file.write(str_data)


def log(verbose: bool, text: str):
    if verbose:
        print(text)
