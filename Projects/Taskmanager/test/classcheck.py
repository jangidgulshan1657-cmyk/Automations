import urllib.request
import urllib.error


print(issubclass(TimeoutError, urllib.error.URLError))
print(issubclass(urllib.error.URLError, TimeoutError))