import streamlit as st
from PIL import Image
import base64
import io
import requests
import time

# ---------------- 页面配置 ----------------
st.set_page_config(
    page_title="Amazon AI Visual Studio",
    layout="wide"
)

st.title("🛒 Amazon AI Visual Studio")
st.markdown("上传产品图和参考图，生成 Amazon 风格图片（Demo）")

# ---------------- Sidebar 配置 ----------------
with st.sidebar:
    st.header("🧩 配置")
    category = st.selectbox(
        "图片类型",
        ["主图", "场景图", "白底图"]
    )
    size = st.selectbox(
        "尺寸",
        ["1800x1800", "2000x2000", "2000x1500"]
    )
    st.divider()
    ref_image = st.file_uploader(
        "📌 上传参考图（可选）",
        type=["png", "jpg", "jpeg"]
    )

# ---------------- Main ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 产品素材图")
    source_image = st.file_uploader(
        "上传产品图",
        type=["png", "jpg", "jpeg"]
    )
    if source_image:
        st.image(source_image, caption="已上传素材图", use_column_width=True)

with col2:
    st.subheader("✨ 生成结果")
    result_placeholder = st.empty()

st.divider()

prompt = st.text_input(
    "✏️ 提示词（可选）",
    placeholder="例如：白色背景，专业灯光，Amazon 主图风格"
)

# ---------------- API 配置 ----------------
GENERATION_API_URL = "https://api.vectorengine.ai"  # 图片生成 API
GENERATION_API_KEY = "sk-Jd4OVoJWxUQc6QjktZY3OaxqE8LgkhJMhRnLIEI9FpIZ5rR2"

ANALYSIS_API_URL = "https://api.vectorengine.ai"  # 图像分析 API
ANALYSIS_API_KEY = "sk-Jd4OVoJWxUQc6QjktZY3OaxqE8LgkhJMhRnLIEI9FpIZ5rR2"

# ---------------- 图像分析函数 ----------------
def analyze_image(image_file):
    """
    调用图像分析 API，返回特征或标签列表
    """
    files = {"image": ("image.png", image_file)}
    headers = {"Authorization": f"Bearer {sk-Jd4OVoJWxUQc6QjktZY3OaxqE8LgkhJMhRnLIEI9FpIZ5rR2}"}

    try:
        response = requests.post(https://api.vectorengine.ai, files=files, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("tags", [])
    except Exception as e:
        st.warning(f"图像分析失败: {e}")
        return []

# ---------------- 图片生成函数 ----------------
def generate_image():
    if not source_image:
        st.error("请先上传产品素材图")
        return

    with st.spinner("AI 正在生成中..."):
        progress_text = st.empty()
        progress_bar = st.progress(0)

        # 分析产品图和参考图
        product_tags = analyze_image(source_image.getvalue())
        ref_tags = analyze_image(ref_image.getvalue()) if ref_image else []

        # 构建增强 prompt
        enhanced_prompt = prompt
        if product_tags:
            enhanced_prompt += ", " + ", ".join(product_tags)
        if ref_tags:
            enhanced_prompt += ", 参考图标签: " + ", ".join(ref_tags)

        # 构建文件上传
        files = {"image": ("source.png", source_image.getvalue())}
        if ref_image:
            files["ref_image"] = ("ref.png", ref_image.getvalue())

        data = {
            "prompt": enhanced_prompt,
            "category": category,
            "size": size
        }

        headers = {
            "Authorization": f"Bearer {sk-Jd4OVoJWxUQc6QjktZY3OaxqE8LgkhJMhRnLIEI9FpIZ5rR2}"
        }

        try:
            response = requests.post(https://api.vectorengine.ai, files=files, data=data, headers=headers, timeout=60)
        except requests.RequestException as e:
            st.error(f"请求失败: {e}")
            return

        if response.status_code == 200:
            try:
                resp_json = response.json()
            except ValueError:
                st.error(f"生成失败: API 返回的不是合法 JSON\n内容: {response.text}")
                return

            result_base64 = resp_json.get("result_image")
            if result_base64:
                try:
                    # 模拟生成进度条
                    for i in range(1, 101, 10):
                        progress_text.text(f"生成进度: {i}%")
                        progress_bar.progress(i)
                        time.sleep(0.1)

                    result_bytes = base64.b64decode(result_base64)
                    image = Image.open(io.BytesIO(result_bytes))
                except Exception as e:
                    st.error(f"解析图片失败: {e}")
                    return

                result_placeholder.image(
                    image,
                    caption="生成结果",
                    use_column_width=True
                )
                st.success("生成完成")
            else:
                st.error(f"生成失败: API 返回结果为空\n内容: {resp_json}")
        else:
            st.error(f"生成失败: HTTP {response.status_code}\n内容: {response.text}")

# ---------------- 按钮触发 ----------------
if st.button("🚀 生成图片"):
    generate_image()
