import logging
from typing import Any

import toga

import mp3Player.core as core
from mp3Player.core import safe_async_call

log = logging.getLogger(__name__)


class FileOpenOpenCV(core.AsyncService):
    def __init__(self) -> None:
        super().__init__()
        self.toTogaImage = None  # ToTogaImage()

    @safe_async_call(log)
    async def handle_event(self,
                           widget: Any,
                           app,
                           service_callback,
                           *args, **kwargs):

        fnames = await widget.app.dialog(
            toga.OpenFileDialog("Open file",
                                file_types=["mp3"],
                                multiple_select=True,))
        if service_callback is not None and fnames:
            service_callback(fnames)
        return
