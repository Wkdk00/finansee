from yadisk import YaDisk
import requests
import os
from io import BytesIO

class YandexDiskDownloader:
    def __init__(self, save_folder="downloaded_files", public_link="https://disk.yandex.ru/d/9yHNs_v8y4306Q"):
        self.TOKEN = "y0__xDCyJ7DBxjblgMgis2BzBNhBSUwqElf_3JzFwpHBag1HPI0Cg"
        self.PUBLIC_LINK = public_link
        self.URL = "https://httpbin.org/post"

        self.yadisk = YaDisk(token=self.TOKEN)

        try:
            self.public_info = self.yadisk.get_public_meta(self.PUBLIC_LINK)
            self.public_key = self.public_info.public_key
        except Exception as e:
            raise Exception(f"Ошибка доступа к папке: {str(e)}")

    def download_files(self, seller: str, call_type: str, limit: int = 5, step: int = 1):
        results = []
        try:
            folder_path = f"/{seller}/{call_type}"
            count = 0
            load = 0
            items = list(self.yadisk.public_listdir(self.public_key, path=folder_path))
        except Exception as e:
            return {"status": "error", "message": f"Ошибка при получении списка файлов: {str(e)}"}

        for item in items:
            if load >= limit:
                break
            count += 1
            if count % step != 0:
                continue
            load+=1

            if item.type == "file":
                try:
                    download_url = self.yadisk.get_public_download_link(
                        self.public_key,
                        path=item.path
                    )

                    response = requests.get(download_url, stream=True)
                    response.raise_for_status()

                    with BytesIO() as file_in_memory:
                        for chunk in response.iter_content(chunk_size=8192):
                            file_in_memory.write(chunk)
                        file_in_memory.seek(0)

                        post_result = self.post_file(file_in_memory, item.name)
                        results.append({
                            "filename": item.name,
                            "status": "success",
                            "post_status": post_result
                        })

                except Exception as e:
                    results.append({
                        "filename": item.name,
                        "status": "error",
                        "message": str(e)
                    })

        return {
            "status": "success",
            "results": results,
            "total_files": len(results)
        }

    def post_file(self, file: BytesIO, filename: str):
        metadata = {
            "callId": "1750744884.127275",
            "callDate": "2025/06/24",
            "agentId": "8244"
        }

        files = {
            "file": (filename, file.getvalue(), "audio/mpeg")
        }

        try:
            response = requests.post(
                self.URL,
                data=metadata,
                files=files,
            )
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }