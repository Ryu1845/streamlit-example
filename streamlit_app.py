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
    length = str(
        datetime.fromtimestamp(int(data["ended_at"]) / 1000)
        - datetime.fromtimestamp(int(data["started_at"]) / 1000)
    )
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
        {space['state']} {'but available for replay!'
                          if space['available_for_replay']
                          else ''}
      </p>
      <div class="mt-4 sm:flex sm:items-center sm:gap-2">
        <div class="flex items-center text-gray-500">
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          <p class="ml-1 text-xs font-medium">{length[:10]}</p>
        </div>

        <span class="hidden text-gray-500 sm:block" aria-hidden="true">&middot;</span>

        <p class="mt-2 text-xs font-medium text-gray-500 sm:mt-0">
          Featuring <a class="underline hover:text-gray-700" href="https://twitter.com/{space['creator_screen_name']}">{space['creator_name']}</a>
        </p>
      </div>
  </div>
</article>
""",
        height=250,
    )

if st.button(
    "Start Download",
    disabled=not bool(space["available_for_replay"] or space["state"] != "Ended"),
    help="Only available if there's a replay or if it's live",
):
    download = TwspaceDL(space, format_str=None)
    with st.spinner("Downloading... This might take up to 5 minutes"):
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
