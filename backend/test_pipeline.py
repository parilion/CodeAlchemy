"""
全流程端到端测试脚本
用法：python test_pipeline.py <zip路径>
"""
import sys
import time
import subprocess
import urllib.request
import urllib.error
import json
import os


ZIP_PATH = sys.argv[1] if len(sys.argv) > 1 else r"G:\BaiduNetdiskDownload\校园外卖服务系统.zip"
BASE_URL = "http://localhost:8002"
MODULES = ["smart_search", "smart_classify", "rag_retrieval", "collaborative_filter"]


def wait_for_server(url, retries=15, delay=1):
    for i in range(retries):
        try:
            urllib.request.urlopen(f"{url}/health", timeout=2)
            return True
        except Exception:
            print(f"  等待后端启动... ({i+1}/{retries})")
            time.sleep(delay)
    return False


def upload_file(zip_path):
    import http.client, mimetypes
    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    filename = os.path.basename(zip_path)
    with open(zip_path, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: application/zip\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    conn = http.client.HTTPConnection("localhost", 8002)
    conn.request("POST", "/api/enhance/upload",
                 body=body,
                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    resp = conn.getresponse()
    return json.loads(resp.read())


def enhance_project(project_id, modules):
    data = json.dumps({"project_id": project_id, "modules": modules}).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/api/enhance/",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    resp = urllib.request.urlopen(req, timeout=60)
    return json.loads(resp.read())


def download_zip(download_url, out_path):
    urllib.request.urlretrieve(f"http://localhost:8002{download_url}", out_path)


if __name__ == "__main__":
    print("=" * 50)
    print("CodeAlchemy 全流程测试")
    print("=" * 50)

    # 1. 启动后端
    print("\n[1/4] 启动后端服务...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8002"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if not wait_for_server(BASE_URL):
        # 打印输出帮助调试
        out, _ = proc.communicate(timeout=2)
        print("后端启动失败:", out.decode(errors="ignore"))
        sys.exit(1)
    print("  ✓ 后端就绪 http://localhost:8002")

    try:
        # 2. 上传 ZIP
        print(f"\n[2/4] 上传项目: {os.path.basename(ZIP_PATH)}")
        upload_result = upload_file(ZIP_PATH)
        project_id = upload_result["project_id"]
        print(f"  ✓ 上传成功，project_id: {project_id[:8]}...")

        # 3. AI 增强
        print(f"\n[3/4] 执行AI增强，模块: {MODULES}")
        enhance_result = enhance_project(project_id, MODULES)
        print(f"  ✓ 增强成功")
        print(f"  - 识别框架: {enhance_result['analysis'].get('framework', '未知')}")
        print(f"  - 识别Controllers: {enhance_result['analysis'].get('controllers', [])}")
        print(f"  - 识别API端点: {enhance_result['analysis'].get('api_endpoints', [])[:3]}")
        print(f"  - 注入模块: {enhance_result['injected_modules']}")
        print(f"  - 下载地址: {enhance_result['download_url']}")

        # 4. 下载结果
        print(f"\n[4/4] 下载增强后的源码包...")
        out_zip = f"output_{project_id[:8]}_enhanced.zip"
        download_zip(enhance_result["download_url"], out_zip)
        size_kb = os.path.getsize(out_zip) // 1024
        print(f"  ✓ 下载完成: {out_zip} ({size_kb} KB)")

        print("\n" + "=" * 50)
        print("✅ 全流程测试通过！")
        print("=" * 50)

    finally:
        proc.terminate()
        print("\n后端已停止。")
