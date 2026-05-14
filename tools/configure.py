from pathlib import Path

import shutil

assets_dir = Path(__file__).parent.parent.resolve() / "assets"


def configure_ocr_model():
    assets_ocr_dir = assets_dir / "MaaCommonAssets" / "OCR"
    if not assets_ocr_dir.exists():
        print(f"OCR assets directory not found at {assets_ocr_dir}")
        print("Attempting to download OCR model...")
        
        try:
            assets_ocr_dir.mkdir(parents=True, exist_ok=True)
            
            url = "https://download.maafw.xyz/MaaCommonAssets/OCR/ppocr_v5/ppocr_v5-zh_cn.zip"
            zip_path = assets_ocr_dir / "ppocr_v5-zh_cn.zip"
            
            print(f"Downloading OCR model from {url}...")
            urllib.request.urlretrieve(url, zip_path)
            
            print("Extracting OCR model...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(assets_ocr_dir / "ppocr_v5" / "zh_cn")
            
            os.remove(zip_path)
            print("OCR model downloaded successfully.")
        except Exception as e:
            print(f"Failed to download OCR model: {e}")
            print("Proceeding without OCR support...")
            return

    shutil.copytree(
        assets_dir / "MaaCommonAssets" / "OCR" / "ppocr_v5" / "zh_cn",
        ocr_dir,
        dirs_exist_ok=True,
    )
    print("OCR model configured.")


if __name__ == "__main__":
    configure_ocr_model()

    print("OCR model configured.")