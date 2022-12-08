import logging
from subprocess import DEVNULL, PIPE, Popen

logger = logging.getLogger("run_cmd")


def run_cmd(code, sync: bool = True, shell=True) -> None:
    """
    通用的命令执行方法
    """
    p = Popen(
        code,
        shell=shell,
        **(
            {"stdout": PIPE, "stderr": PIPE}
            if sync
            else {
                "stdin": None,
                "stdout": DEVNULL,
                "stderr": DEVNULL,
                "close_fds": True,
            }
        ),
    )
    logger.info(f"[PID:{p.pid} Sync:{sync}]\t{code}")
    if not sync:
        return
    stdout, stderr = list(map(bytes.decode, p.communicate()))
    if stderr:
        logger.error(stderr)
    logger.info(stdout)
    return stdout
