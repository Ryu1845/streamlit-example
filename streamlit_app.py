from datetime import datetime
import os
import shutil

import streamlit as st
from twspace_dl import Twspace, TwspaceDL
import streamlit.components.v1 as components

os.environ["PATH"] = f"{os.environ['PATH']}:{os.path.dirname(__file__)}"

st.set_page_config(
    page_title="twspace-dl online",
    page_icon="🐦",
    layout="wide",
    menu_items={
        "About": "This was made using [twspace-dl](https://github.com/HoloArchivists/twspace-dl/). You can find the source [here](https://github.com/Ryu1845/streamlit-example)"
    },
)
"""
# Welcome to twspace-dl online!
"""

params = st.experimental_get_query_params()
url = st.text_input(
    label="Space URL",
    value=params["url"][0]
    if params.get("url")
    else "https://twitter.com/i/spaces/1RDxlgvQwAdJL",
)
if not url:
    st.warning("Please enter a space url to continue!")
    st.stop()
st.experimental_set_query_params(url=url)

space = Twspace.from_space_url(url)
data = space.source["data"]["audioSpace"].get("metadata")
creator_data = data["creator_results"]["result"]["legacy"]

with st.container():
    res = """
  <script src="https://cdn.tailwindcss.com"></script>
"""
    sound_icon = """
<div
  class="
    hidden
    sm:grid
    sm:h-20
    sm:w-20
    sm:shrink-0
    sm:place-content-center
    sm:rounded-full
    sm:border-2
    sm:border-indigo-500"
  aria-hidden="true"
>
  <div class="flex items-center gap-1">
    <span class="h-8 w-0.5 rounded-full bg-indigo-500"></span>
    <span class="h-6 w-0.5 rounded-full bg-indigo-500"></span>
    <span class="h-4 w-0.5 rounded-full bg-indigo-500"></span>
    <span class="h-6 w-0.5 rounded-full bg-indigo-500"></span>
    <span class="h-8 w-0.5 rounded-full bg-indigo-500"></span>
  </div>
</div>"""
    components.html(
        f"""
{res}
<article class="p-6 bg-gray-900 sm:p-8 shadow-xl rounded-xl border border-gray-800 block">
  <div class="flex items-start">
    {sound_icon}
    <div class="sm:ml-8">
      <strong
        class="rounded border border-indigo-500 bg-indigo-500 px-3 py-1.5 text-[10px] font-medium text-white"
      >{datetime.fromtimestamp(
                    int(data["ended_at"]) / 1000
                ).strftime("%A, %B %d, %Y")}
      </strong>

      <h2 class="mt-4 text-lg text-white font-medium sm:text-xl">
        <a href="{space['url']}" class="hover:underline"> {space['title']} </a>
      </h2>

      <p class="mt-1 text-sm text-gray-300">
        {space['state']}
      </p>
      <div>
        <dl class="flex mt-6">
          <div class="flex flex-col">
            <dt class="text-sm font-medium text-gray-400">Started at</dt>
            <dd class="text-xs text-gray-300">{datetime.fromtimestamp(
                    int(data["started_at"]) / 1000
                ).strftime("%H:%M %p UTC")}</dd>
          </div>

          <div class="flex flex-col ml-3 sm:ml-6">
            <dt class="text-sm font-medium text-gray-400">Ended at</dt>
            <dd class="text-xs text-gray-300">{datetime.fromtimestamp(
                    int(data["ended_at"]) / 1000
                ).strftime("%H:%M %p UTC")}</dd>
          </div>

          <div class="flex flex-col ml-3 sm:ml-6">
            <dt class="text-sm font-medium text-gray-400">Featuring</dt>
            <dd class="text-xs text-gray-300 underline"><a href="https://twitter.com/{space['creator_screen_name']}">{space['creator_name']}</a></dd>
          </div>
        </dl>
      </div>
    </div>
  </div>
</article>
""",
        height=250,
    )

if st.button("Start Download"):
    download = TwspaceDL(space, format_str=None)
    with st.spinner("Downloading... This might take a while"):
        download.download()
    with open(download.filename + ".m4a", "rb") as file:
        st.download_button(
            "Download File",
            data=file,
            file_name=download.filename + ".m4a",
            mime="audio/mp4",
        )
    st.balloons()

with st.expander("Source"):
    st.write(data)
