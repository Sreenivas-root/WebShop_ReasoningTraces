# Instructions to run dockerfile

build dockerfile
> docker build -t webshop-app .

Will take time 

run dockerfile
> docker run --name webshop -it -p 3000:3000 webshop-app /bin/bash

This will copy the folder contents while building so active changes won't be considered

run dockerfile with folder mounting
> docker run  --name webshop -it -p 3000:3000 -v /Users/aadi/UIUC/"ml for llms"/WebShop_ReasoningTraces:/app webshop-app /bin/bash

You will now enter a linux terminal
- Verify folder structure
- rerun setup.sh
> ./setup.sh -d all
- run run_dev.sh
> ./run_dev.sh

Potential Error Solutions

# 500 internal server error
This can happen if indexes were not built
Solution:
```bash
cd search_engine
mkdir -p resources resources_100 resources_1k resources_100k
python convert_product_file_format.py
mkdir -p indexes
./run_indexing.sh
cd .. 
```

# .sh file not found
This can happen if the .sh file is in CRLF and not LF
> dos2unix setup.sh

# Any library issue or infinite recursion
- Rerun dockerfile
- if still persists re-build

Note:
gdown (Google drive downloader) keeps failing sometimes due to calling restrictions from GDrive, so small dataset is already added in the project in webshop/web_agent_site/data

To perform other tasks on WebShop, refer the readme.md of WebShop  

