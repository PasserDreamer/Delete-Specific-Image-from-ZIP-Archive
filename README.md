# 如何使用 / How To Use
## 注意：這是 Windows 腳本 / Note: This is a Windows script.
這基於 MD5 對照，將相同 MD5 的圖片從 ZIP 檔案中移除，當錯誤發生時不會中止，在執行的最後會整理發生過的錯誤。

This is based on MD5 checksums, removing images with the same MD5 from a ZIP file. 

It won't stop if errors occur, and it will compile a list of the errors that happened at the end of the execution.



中:
```
python remove_image_from_zip.py {參照圖片路徑} {目標 ZIP 或資料夾路徑}
```
En:
```
python remove_image_from_zip.py {reference image path} {target zip path or target folder path}
```
