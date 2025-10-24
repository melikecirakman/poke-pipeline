FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir jupyter nbconvert matplotlib pandas sqlalchemy

COPY . .

CMD ["jupyter", "nbconvert", "--to", "html", "report.ipynb", "--execute", "--ExecutePreprocessor.kernel_name=python3", "--output", "report_output.html"]
