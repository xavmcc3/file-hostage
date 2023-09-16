import pandas as pd
import random
import sys

from pathlib import Path
import asyncio
import psutil
import csv
import os

#region constants
IGNORE_PATHS = [
    "C:\Program Files (x86)",
    "C:\Program Files",
    "C:\OneDriveTemp",
    "C:\ProgramData",
    sys.executable,
    "C:\Python311",
    str(__file__),
    "C:\\tools",
    "C:\msys64",
    "C:\MinGW"
    ]
#endregion

#region csv storage
def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

class CSVList:
    def __init__(self, listname):
        self.filename = str(listname) + ".csv"
        self.listname = listname
        self.linecount = 0
            
    def empty(self):
        open(self.filename, 'w').close()
        self.linecount = 0
        self.list = []
        
    def add(self, item):
        with open(self.filename, 'a', newline='') as dbfile:
            writer = csv.writer(dbfile)
            writer.writerow([item])
        
        self.linecount += 1
        print(item)
    
    def set_line_count(self):
        with open(self.filename, "r", encoding="utf-8", errors='ignore') as f:
            self.linecount = sum(bl.count("\n") for bl in blocks(f))
            
    
    def read(self, chunksize = 100000):
        for chunk in pd.read_csv(self.filename, sep=",", header=None, encoding='ISO-8859-1', usecols=[0], names=['list'], dtype={'list': str}, chunksize=chunksize):
            print(chunk)
            
    async def random(self, chunksize = 100000):
        if self.linecount == 0:
            self.set_line_count()
            
        max_row = 0
        target_item = random.randrange(self.linecount)
        for chunk in pd.read_csv(self.filename, sep=",", header=None, encoding='ISO-8859-1', usecols=[0], names=['list'], dtype={'list': str}, chunksize=chunksize):
            max_row += len(chunk.index)
            if max_row >= target_item:
                return chunk.iloc[[max_row - target_item]]['list'].values[0]
            
#endregion

#region get files
def validate_path(path, abspath):
    if str(path).startswith("$"):
        return False
    if str(abspath) in IGNORE_PATHS:
        return False
    if str(path).startswith("~"):
        return False
    if str(path).endswith("~"):
        return False
    return True

async def get_files_recursive(directory, file_list):
    try:
        for path in os.listdir(directory):
            abspath = os.path.join(directory, path)
            if not validate_path(path, abspath):
                continue
            if os.path.isdir(abspath):
                await get_files_recursive(abspath, file_list)
                continue
            file_list.add(abspath)
    except Exception:
        pass

async def get_files_from_all_disks(file_list):
    file_list.empty()
    
    for disk in psutil.disk_partitions(all=True):
        await get_files_recursive(disk.device, file_list)
    return file_list
#endregion

#region main
async def main():
    file_list = CSVList('file_index')
    
    IGNORE_PATHS.append(os.path.abspath(str(file_list.listname) + ".csv"))
    if not os.path.exists(str(file_list.listname) + ".csv"):
        print("Getting files on disks... (This can take a really long time.)")
        await get_files_from_all_disks(file_list)
    for _ in range(10):
        path = await file_list.random()
        print(path)
    
asyncio.run(main())
#endregion