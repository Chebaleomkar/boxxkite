# Does `sh -c "sleep 30"` leave a grandchild holding the pipe after SIGKILL,
# and does asyncio's wait() then block? Run under 3.11 and 3.12.
import asyncio, os, signal, sys, time

async def once():
    proc = await asyncio.create_subprocess_shell(
        "sleep 30", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
    os.kill(proc.pid, signal.SIGKILL)  # what _signal_process_group does in the shared-group case
    t = time.monotonic()
    try:
        await asyncio.wait_for(proc.wait(), timeout=2)
        return time.monotonic() - t
    except (asyncio.TimeoutError, TimeoutError):
        return None

async def main():
    hung = 0
    for _ in range(int(sys.argv[1])):
        if await once() is None:
            hung += 1
    print(f"python {sys.version.split()[0]}: {hung}/{sys.argv[1]} waits hung past 2s")
    os.system("pkill -f 'sleep 30' 2>/dev/null")

asyncio.run(main())
