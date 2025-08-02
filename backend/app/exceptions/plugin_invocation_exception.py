# exceptions.py
from typing import Optional

class PluginInvocationError(Exception):
    """
    Raised when a kernel plugin invocation fails or returns no data.

    Attributes:
        plugin_name    -- name of the plugin that was called
        function_name  -- name of the function that was invoked
        original_error -- the underlying exception, if any
    """
    def __init__(self, plugin_name: str, function_name: str, 
                 message: Optional[str], original_error: Optional[Exception] = None):
        if message is None:
            message = f"Invocation of plugin '{plugin_name}.{function_name}' failed."
        super().__init__(message)
        self.plugin_name = plugin_name
        self.function_name = function_name
        self.original_error = original_error

    def __str__(self):
        base = super().__str__()
        if self.original_error:
            # include the original error’s message
            return f"{base} (caused by {self.original_error!r})"
        return base
