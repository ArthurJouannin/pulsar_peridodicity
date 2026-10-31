from pathlib import Path
import pandas as pd

def discover_window(root, start = None, end = None, *, include_neighbors = True):
  """select hourly files before the exclusive end and optional neighbors"""
  start = pd.Timestamp(start).tz_convert('UTC')
  end = pd.Timestamp(end).tz_convert('UTC')
  
  pattern = '[0-9]'*8+'/sol_[0-2][0-9].csv'
  paths = list(Path(root).glob(pattern))
  
  names = [f"{path.parent.name} {path.stem[-2:]}" for path in paths]
  stamps = pd.to_datetime(names, format = '%Y%m%d %H', utc = True)
  files = {stamp: path for stamp, path in zip(stamps, paths) if pd.notna(stamp)}

  hour = pd.Timedelta(hours = 1)
  first = start.floor('h') if start is not None else min(files)
  stop = end.ceil('h') if end is not None else max(files)+hour
  
  hours = pd.date_range(first, stop, freq = 'h', inclusive = 'left')
  selected = set(hours) & files.keys()
  if include_neighbors: selected |= {first-hour, stop} & files.keys()
  return [files[date] for date in sorted(selected)]
