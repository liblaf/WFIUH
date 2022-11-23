import concurrent.futures
import glob
import signal
import sys
import threading
import typing

import pandas as pd
import rich.console
import rich.live
import rich.panel
import rich.progress
import scipy.optimize
import sklearn.metrics

from . import models

interrupt_event = threading.Event()


def handle_sigint(signal_num, frame):
    interrupt_event.set()


signal.signal(signal.SIGINT, handle_sigint)


def curve_fitting(
    filepath: str,
    f: typing.Callable,
) -> dict | None:
    if interrupt_event.is_set():
        return None
    try:
        df = pd.read_csv(filepath)
        x = df["flowTime"]
        y = df["frequency"]
        res = scipy.optimize.curve_fit(f=f, xdata=x, ydata=y)
    except RuntimeError as e:
        raise type(e)(f"{filepath}: {e}")
    else:
        popt, pcov = res
        r2_score = sklearn.metrics.r2_score(y_true=y, y_pred=f(x, *popt))
        return {"filepath": filepath, "popt": popt, "r2_score": r2_score}


def main(
    prefix: str = "2-sub-WFIUH_rescaled",
    model_names: list[str] = ["normal_gaussian", "inverse_gaussian", "polynomial"],
) -> int:
    files = glob.glob(pathname=f"{prefix}/*.csv")
    overall_progress = rich.progress.Progress(
        rich.progress.TextColumn(
            text_format="{task.description}", style="logging.level.info"
        ),
        rich.progress.BarColumn(),
        rich.progress.TaskProgressColumn(),
        rich.progress.MofNCompleteColumn(),
        rich.progress.TimeElapsedColumn(),
    )
    models_progress = rich.progress.Progress(
        rich.progress.TextColumn(
            text_format="{task.description}", style="logging.level.info"
        ),
        rich.progress.BarColumn(),
        rich.progress.TaskProgressColumn(),
        rich.progress.MofNCompleteColumn(),
        rich.progress.TimeElapsedColumn(),
        rich.progress.TimeRemainingColumn(),
    )
    progress_group = rich.console.Group(
        rich.panel.Panel(models_progress), rich.panel.Panel(overall_progress)
    )
    with rich.live.Live(progress_group) as live:
        overview_task_id = overall_progress.add_task(description="Overall Progress")
        for model_name in overall_progress.track(model_names, task_id=overview_task_id):
            model_task_id = models_progress.add_task(
                description=model_name, total=len(files)
            )
            rets: list[dict] = []
            try:
                f = getattr(models, model_name)
                with concurrent.futures.ProcessPoolExecutor() as pool:
                    futures: list[concurrent.futures.Future] = list(
                        map(
                            lambda filepath: pool.submit(
                                curve_fitting, filepath=filepath, f=f
                            ),
                            files,
                        )
                    )
                    for future in concurrent.futures.as_completed(futures):
                        if interrupt_event.is_set():
                            raise KeyboardInterrupt()
                        try:
                            ret = future.result()
                            if ret:
                                rets.append(ret)
                                models_progress.advance(task_id=model_task_id)
                        except KeyboardInterrupt as e:
                            raise e
                        except Exception as e:
                            live.console.log(
                                f"{model_name}:", e, style="logging.level.error"
                            )
            except KeyboardInterrupt as e:
                results = pd.DataFrame(rets)
                results.to_csv(f"{model_name}.csv")
                raise e
            except Exception as e:
                live.console.log(f"{model_name}:", e, style="logging.level.error")
            else:
                results = pd.DataFrame(rets)
                results.to_csv(f"{model_name}.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
