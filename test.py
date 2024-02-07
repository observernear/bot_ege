import requests
from sdamgia import SdamGIA
import uuid
import os

sdamgia = SdamGIA()


def get_test(subject, problems):
    id = sdamgia.generate_test(subject, problems)
    url = sdamgia.generate_pdf(subject=subject, testid=id)
    url_sol = sdamgia.generate_pdf(subject=subject, testid=id, solution=True)
    save_path = f'files/{uuid.uuid4()}.pdf'
    download_pdf(url, save_path)
    save_path_sol = f'files/1{uuid.uuid4()}.pdf'
    download_pdf(url_sol, save_path_sol)
    return save_path, save_path_sol


def download_pdf(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
