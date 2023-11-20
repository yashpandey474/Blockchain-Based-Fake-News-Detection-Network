import asyncio
import streamlit as st
import time
async def show_time(t):
    while True:
        curr_time = int(time.time())
        t.markdown("%s" % str(curr_time))
        await asyncio.sleep(1)

async def main():
    t = st.empty()
    
    if st.button("Press Button"):
        st.write("Hello There!")

    await show_time(t)

if __name__ == "__main__":
    asyncio.run(main())