import lseg.data as ld
import os
import asyncio
import sys
import datetime

# 禁用输出缓冲
os.environ["PYTHONUNBUFFERED"] = "1"

async def main():
    try:
        # 打开会话
        config_path = os.path.join(os.getcwd(), "lseg-data.config.json")
        print(f"[{datetime.datetime.now().isoformat()}] 打开会话...", flush=True)
        ld.open_session(config_name=config_path)

        # 创建 BTC 实时数据流，指定字段 BID, ASK, TIMACT
        pricing_stream = ld.content.pricing.Definition(
            universe=["BTC="],
            fields=["BID", "ASK", "TIMACT"]
        ).get_stream()

        # 定义回调函数
        def on_refresh(fields, instrument_name, stream):
            timestamp = datetime.datetime.now().isoformat()
            print(f"[{timestamp}] BTC= 刷新: BID={fields.get('BID')}, ASK={fields.get('ASK')}, TIMACT={fields.get('TIMACT')}", flush=True)
            with open("btc_updates.log", "a") as f:
                f.write(f"刷新 {instrument_name}: {fields}\n")

        def on_update(fields, instrument_name, stream):
            timestamp = datetime.datetime.now().isoformat()
            print(f"[{timestamp}] BTC= 更新: BID={fields.get('BID')}, ASK={fields.get('ASK')}, TIMACT={fields.get('TIMACT')}", flush=True)
            with open("btc_updates.log", "a") as f:
                f.write(f"更新 {instrument_name}: {fields}\n")

        # 绑定回调
        pricing_stream.on_refresh(on_refresh)
        pricing_stream.on_update(on_update)

        # 打开数据流
        print(f"[{datetime.datetime.now().isoformat()}] 打开数据流...", flush=True)
        pricing_stream.open()

        # 获取快照数据
        print(f"[{datetime.datetime.now().isoformat()}] 获取快照数据（每10秒一次，共5次）...", flush=True)
        for _ in range(5):
            snapshot = pricing_stream.get_snapshot()
            print(f"[{datetime.datetime.now().isoformat()}] BTC= 快照：\n{snapshot}", flush=True)
            with open("btc_snapshots.log", "a") as f:
                f.write(f"快照 {snapshot}\n")
            await asyncio.sleep(10)

        # 接收实时更新
        print(f"[{datetime.datetime.now().isoformat()}] 接收实时数据，持续 60 秒...", flush=True)
        await asyncio.sleep(60)

    except Exception as e:
        print(f"[{datetime.datetime.now().isoformat()}] 错误：{e}", flush=True)

    finally:
        print(f"[{datetime.datetime.now().isoformat()}] 关闭数据流和会话...", flush=True)
        pricing_stream.close()
        ld.close_session()
        print(f"[{datetime.datetime.now().isoformat()}] 会话已关闭。", flush=True)

if __name__ == "__main__":
    asyncio.run(main())