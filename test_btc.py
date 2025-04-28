import lseg.data as ld
import os
import sys
import asyncio

os.environ["PYTHONUNBUFFERED"] = "1"  # 禁用缓冲

async def main():
    print("测试输出到控制台", file=sys.stdout, flush=True)
    ld.open_session(config_name="/home/ian/rdp_jpy_project/lseg-data.config.json")
    print("会话打开成功！", flush=True)

    pricing_stream = ld.content.pricing.Definition(
        universe=["BTC="],
        fields=["DSPLY_NAME", "BID", "ASK"]
    ).get_stream()
    print(f"Stream object: {pricing_stream}", flush=True)

    def on_refresh(fields, instrument_name, stream):
        print(f"触发刷新回调 - {instrument_name}: {fields}", flush=True)
        with open("btc_updates.log", "a") as f:
            f.write(f"刷新 {instrument_name}: {fields}\n")

    def on_update(fields, instrument_name, stream):
        print(f"触发更新回调 - {instrument_name}: {fields}", flush=True)
        with open("btc_updates.log", "a") as f:
            f.write(f"更新 {instrument_name}: {fields}\n")

    pricing_stream.on_refresh(on_refresh)
    pricing_stream.on_update(on_update)
    print("Callbacks bound", flush=True)

    pricing_stream.open()
    print("数据流打开成功！", flush=True)

    await asyncio.sleep(30)
    pricing_stream.close()
    ld.close_session()
    print("会话已关闭", flush=True)

asyncio.run(main())