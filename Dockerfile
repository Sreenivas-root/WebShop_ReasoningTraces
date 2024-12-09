# Use an official Python runtime as a parent image
FROM python:3.8.13
# Set the working directory in the container
WORKDIR /app

# Install Java
RUN apt-get update && \
    apt-get install -y git curl wget dos2unix && \
    apt-get install -y default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Anaconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Add conda to PATH
ENV PATH="/opt/conda/bin:${PATH}"

# Clone the WebShop repository
# RUN git clone https://github.com/princeton-nlp/webshop.git /app/webshop
COPY . .

# Set working directory to the cloned repo
WORKDIR /app/webshop

# Install requirements
RUN dos2unix setup.sh
RUN chmod +x setup.sh
RUN ./setup.sh -d all

RUN rm -rf /root/.cache/pip && pip install --no-cache-dir -r requirements.txt

RUN dos2unix run_dev.sh
RUN chmod +x run_dev.sh

RUN dos2unix run_prod.sh
RUN chmod +x run_prod.sh

RUN dos2unix search_engine/run_indexing.sh
RUN chmod +x search_engine/run_indexing.sh

RUN dos2unix run_web_agent_site_env.sh
RUN chmod +x run_web_agent_site_env.sh

RUN dos2unix run_web_agent_text_env.sh
RUN chmod +x run_web_agent_text_env.sh
# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["./run_dev.sh"]