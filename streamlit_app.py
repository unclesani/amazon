import streamlit as st
from PIL import Image
import base64
import io

st.set_page_config(
    page_title="Amazon AI Visual Studio",
    layout="wide"
)

st.title("🛒 Amazon AI Visual Studio")

st.markdown("上传产品图和参考图，生成 Amazon 风格图片（Demo）")

# ---------------- Sidebar ----------------
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

with col2:
    st.subheader("✨ 生成结果")
    result_placeholder = st.empty()

st.divider()

prompt = st.text_input(
    "✏️ 提示词（可选）",
    placeholder="例如：白色背景，专业灯光，Amazon 主图风格"
)

import requests

API_URL = "https://api.vectorengine.ai"  # 你的 API 地址
API_KEY = "sk-Jd4OVoJWxUQc6QjktZY3OaxqE8LgkhJMhRnLIEI9FpIZ5rR2"  # 如果需要认证

if st.button("🚀 生成图片"):
    if not source_image:
        st.error("请先上传产品素材图")
    else:
        with st.spinner("AI 正在生成中..."):
            # 构建文件上传
            files = {"image": ("source.png", source_image.getvalue())}
            if ref_image:
                files["ref_image"] = ("ref.png", ref_image.getvalue())

            data = {
                "prompt": prompt,
                "category": category,
                "size": size
            }

            headers = {
                "Authorization": f"Bearer {API_KEY}"
            }

            response = requests.post(API_URL, files=files, data=data, headers=headers)

            if response.status_code == 200:
                # 假设 API 返回 base64 图片
                result_base64 = response.json().get("result_image")
                if result_base64:
                    result_bytes = base64.b64decode(result_base64)
                    image = Image.open(io.BytesIO(result_bytes))

                    result_placeholder.image(
                        image,
                        caption="生成结果",
                        use_column_width=True
                    )
                    st.success("生成完成")
                else:
                    st.error("生成失败: API 返回结果为空")
            else:
                st.error(f"生成失败: {response.text}")
