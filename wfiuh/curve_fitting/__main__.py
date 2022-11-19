import concurrent.futures
import glob
import signal
import sys
import threading

import pandas as pd
import rich.progress
import scipy.optimize
import scipy.stats

from . import models


interrupt_event = threading.Event()


def handle_sigint(signal_num, frame):
    interrupt_event.set()


signal.signal(signal.SIGINT, handle_sigint)


def curve_fitting(
    filepath: str,
    f,
    progress: rich.progress.Progress = rich.progress.Progress(),
    task_id: rich.progress.TaskID = rich.progress.TaskID(0),
) -> dict | None:
    if interrupt_event.is_set():
        return None
    try:
        df = pd.read_csv(filepath)
        x = df["flowTime"]
        y = df["frequency"]
        res = scipy.optimize.curve_fit(f=f, xdata=x, ydata=y)
        popt, perr = res
        progress.advance(task_id=task_id)
        progress.console.log(f"{filepath} : popt = {popt}", style="bold bright_green")
        return {"filepath": filepath, "popt": popt}
    except:
        progress.console.log(f"{filepath} Failed!", style="bold bright_red")
        return None


def main(prefix: str = "2-sub-WFIUH_rescaled") -> int:
    files = glob.glob(pathname=f"{prefix}/*.csv")
    progress = rich.progress.Progress(
        rich.progress.TextColumn(text_format="{task.description}", style="bold blue"),
        rich.progress.BarColumn(),
        rich.progress.MofNCompleteColumn(),
        rich.progress.TimeElapsedColumn(),
        rich.progress.TimeRemainingColumn(),
    )
    with progress:
        task_id = progress.add_task(description="Progress", total=len(files))
        with concurrent.futures.ThreadPoolExecutor() as pool:
            futures: list[concurrent.futures.Future] = [
                pool.submit(
                    curve_fitting,
                    filepath=filepath,
                    f=models.f,
                    progress=progress,
                    task_id=task_id,
                )
                for filepath in files
            ]
            rets: list[dict] = []
            for future in futures:
                if interrupt_event.is_set():
                    break
                try:
                    ret = future.result()
                    if ret:
                        rets.append(ret)
                except:
                    pass
    results = pd.DataFrame(rets)
    results.to_csv("results.csv")
    if interrupt_event.is_set():
        raise KeyboardInterrupt()
    return 0


if __name__ == "__main__":
    sys.exit(main())
